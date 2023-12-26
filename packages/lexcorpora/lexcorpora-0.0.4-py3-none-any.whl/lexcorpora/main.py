from functools import cached_property
from pathlib import Path
from sqlite3 import connect
from typing import Iterable

import spacy
import srsly  # type: ignore
from pydantic import BaseModel, Field
from spacy.language import Language
from spacy.tokens import Doc, DocBin
from wasabi import msg  # type: ignore

from .asset import Artifact, Asset, create_concept_collection
from .pre import path_ok
from .tokenizer import customize_tokenizer

SPANS_KEY = "sc"


@Language.factory(name="add_cats_from_spans")
class AddTextCatComponent:
    def __init__(self, nlp: Language, name: str, options: list[str]):
        self.nlp = nlp
        self.options = options

    def __call__(self, doc) -> Doc:
        doc.cats = {op: 0.0 for op in self.options}
        for span in doc.spans["sc"]:
            if span.id:  # some spans won't have an id
                value = self.nlp.vocab.strings[span.id]
                if "/" in value:  # e.g. political/bill_of_rights
                    main_topic = value.split("/")[0]  # just political
                    if main_topic in self.options:
                        if doc.cats[main_topic] == 0.0:
                            doc.cats[main_topic] = 1.0
        return doc


def create_trainer_nlp(
    base_model: str,
    output_path: str | Path,
    with_textcat_scorer: bool = True,
    params_file: str | Path = Path("params.json.gz"),
) -> Language:
    """This model compiles all _span ruler_ patterns under the spans key 'sc'
    so that this can be used in creating training data for spancat (and thus textcat), e.g annotation:

    ```json
    {
    "doc_annotation": {
        "cats": {
            "ethics": 0.0,
            "mercantile": 1.0,
            "tax": 0.0,
            "criminal": 0.0,
            "labor": 0.0,
            "civil": 0.0,
            "political": 0.0,
            "remedial": 0.0,
        },
        "spans": {"sc": [(165, 182, "concept", "")]},
        }
    }
    ```
    `tl;dr`: Because of `spans` found in `sc`, the `cats` can be calculated.

    This model does _not_ have spancat nor the textcat model.

    It only uses the _span ruler_ pipeline and places all the spans found under the 'sc' key. A
    custom pipeline, `add_cats_from_spans`, to generate a score for each possible textcat option.

    This allows us to parse documents to this model and create training data.

    Args:
        base_model (str): Must use at least an en_core_web_sm to take advantage of the
            tagger / lemmatizer that are used in pattern files.
        params_file (str | Path): Accepts a path to `params_file` which is the
            unpacked variant of `create_data_cfg()`.
        output_path (str | Path): Where to store the trainer model
        with_textcat_scorer (bool, optional): Whether the textcat scorer pipeline is included.
            Defaults to True.

    Returns:
        Language: Modified language model, saved to `output_path`
    """
    msg.info("Loading gzip settings for tokenizer/patterns.")
    cfg = srsly.read_gzip_json(path_ok(params_file))
    if not isinstance(cfg, dict):
        raise Exception(f"Must be dict unzipped {params_file}=")

    nlp = spacy.load(base_model, exclude="senter,ner")
    nlp.tokenizer = customize_tokenizer(nlp=nlp, token_rules=cfg["tokenizer_rules"])
    ruler = nlp.add_pipe(
        "span_ruler",
        config={
            "spans_key": "sc",
            "phrase_matcher_attr": "LOWER",
            "spans_filter": {"@misc": "spacy.first_longest_spans_filter.v1"},
            "validate": True,
        },
        validate=True,
    )
    ruler.add_patterns(cfg["span_ruler_patterns"])  # type: ignore

    if with_textcat_scorer:
        nlp.add_pipe("add_cats_from_spans", config={"options": cfg["textcat_options"]})

    nlp.to_disk(output_path)
    return nlp


class Corpora(BaseModel):
    db_file: Path = Field(
        default=...,
        description="Where to source annotatable documents",
    )
    asset_dir: Path = Field(
        default=...,
        description="Where to source / create `*.txt`, `*.jsonl` files; where to output the `*.spacy` files.",
    )
    base_model: str = Field(
        default=...,
        description="Pre-trained model to serve as the base, should have parser / tagger for pattern file matching.",
    )
    params_file: Path | None = Field(
        default=Path("params.json.gz"),
        description="Settings required to modify the base model to accomodate span ruler patterns / custom tokenizer.",
    )
    spans_key: str = Field(
        default="sc", description="Used as the `SpanGroup` key for `SpanRuler` since 'sc' is the default for `SpanCat`."
    )
    output_path: str | Path = Field(
        default=...,
        description="Where to store model with injected `params_file` so that it can be used to annotate documents.",
    )

    def create_data_cfg(self) -> Path:
        """Initialize patterns from `asset_folder` for training a _spancat x textcat_ model, including:

        1. Special tokenizer rules
        2. Aggregated SpanRuler patterns (under `spans_key`)
        3. Textcat options

        The file is saved in `*.json.gz` and can be consumed in `create_trainer_nlp()`.

        Args:
            asset_folder (str | Path): Where the assets are found
            target_file (str | Path, optional):  Where the settings are to be created. Defaults to "params.json.gz".
            spans_key (str, optional):  We'll be applying this `create_trainer_nlp()` model
                to raw text; so the training data can be annotated with
                `'spans': {'sc': [(165, 182, 'concept', '')]}`. This can be later used for training spancat models
                where [`sc` is the default spans_key](https://spacy.io/api/spancategorizer#assigned-attributes).
                Defaults to "sc".

        Returns:
            Path:  The `target_file` as a pathlib object that can be read with `srsly.read_gzip_json(`<target_file>`)`
        """
        settings = {}
        settings["tokenizer_rules"] = srsly.read_json(self.asset_dir.joinpath("artifact/singleton/patterns.json"))
        concept_patterns = []
        for concept in create_concept_collection(self.asset_dir):
            concept_patterns.extend(concept.value.from_disk(self.asset_dir))
        settings["span_ruler_patterns"] = list(Artifact.compile(artifact_folder=self.asset_dir)) + concept_patterns
        settings["textcat_options"] = list({concept["id"].split("/")[0] for concept in concept_patterns})
        path = self.params_file or self.asset_dir / "params.json.gz"
        srsly.write_gzip_json(path, settings)
        return path_ok(path)

    def model_post_init(self, __context) -> None:
        _dir = self.asset_dir.joinpath("corpus")
        _dir.mkdir(exist_ok=True)
        _dir.joinpath("train").mkdir(exist_ok=True)
        _dir.joinpath("dev").mkdir(exist_ok=True)
        self.create_data_cfg()

    @cached_property
    def nlp(self) -> Language:
        return create_trainer_nlp(
            base_model=self.base_model,
            params_file=self.params_file or self.asset_dir / "params.json.gz",
            output_path=self.output_path,
        )

    def annotate_artifacts(self, *args, **kwargs):
        for artifact in Artifact:  # generic enum
            artifact.value.bin(
                nlp=self.nlp,
                conn=connect(self.db_file),
                train_output_dir=self.asset_dir / "corpus" / "train",
                dev_output_dir=self.asset_dir / "corpus" / "dev",
                *args,
                **kwargs,
            )

    def annotate_concepts(self, *args, **kwargs):
        for concept in create_concept_collection(self.asset_dir):  # dynamic enum
            asset: Asset = concept.value  # type: ignore
            asset.bin(
                nlp=self.nlp,
                conn=connect(self.db_file),
                train_output_dir=self.asset_dir / "corpus" / "train",
                dev_output_dir=self.asset_dir / "corpus" / "dev",
                *args,
                **kwargs,
            )

    def merge_annotations(self, asset_type: str = "concept"):
        if asset_type in ("concept", "artifact"):
            for data_type in ("train", "dev"):
                compiled = DocBin(attrs=[])
                folder = self.asset_dir / "corpus" / data_type
                for file in folder.glob("*.spacy"):
                    if file.name.startswith(asset_type):
                        compiled.merge(DocBin().from_disk(file))
                compiled.to_disk(self.asset_dir / "corpus" / f"{asset_type}_{data_type}.spacy")
