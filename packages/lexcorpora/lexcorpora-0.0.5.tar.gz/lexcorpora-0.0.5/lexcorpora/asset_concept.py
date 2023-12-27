from collections.abc import Iterator
from enum import Enum
from pathlib import Path

import spacy
import srsly  # type: ignore
from spacy.language import Language
from spacy.tokens import Doc

from .asset import Asset
from .pre import path_ok
from .tokenizer import customize_tokenizer


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


def convert_concept_path_to_asset(asset_dir: Path) -> Iterator[Asset]:
    """Based on the `q.txt` and `patterns.json` files found in the path, generate
    patterns in a list of dicts where each dict consists of the following keys:

    1. `id`: <root-path>/<child-path>
    2. `label`: "concept"
    3. `pattern`: either a string or a list of dicts, following the spacy Matcher pattern
    style.
    """
    q_paths = asset_dir.glob("concept/**/q.txt")
    q_topic = {f.parent for f in q_paths}
    pattern_paths = asset_dir.glob("concept/**/patterns.json")
    pattern_topic = {f.parent for f in pattern_paths}
    topic_paths = q_topic.union(pattern_topic)
    for path in topic_paths:
        basis = f"{path.parent.stem}/{path.stem}"
        asset = Asset(src="concept", basis=basis, label="concept")
        yield asset


def create_concept_collection(asset_dir: Path):
    """Makes it possible to query and parse concepts even if they are dynamically created, e.g.:

    ```py
    Concept = create_concept_collection(asset_dir)
    Concept._member_names_
    # 'ADJECTIVE_CITIZENSHIP',
    # 'ADJECTIVE_CLAUSES',
    # 'ADJECTIVE_FINDINGS'
    ```

    In the above results, the first word is always the initial folder within concepts/
    """
    assets = convert_concept_path_to_asset(asset_dir)
    data = {ast.basis.replace("/", "_").upper(): ast for ast in assets}
    members = sorted(data.items(), key=lambda item: item[0])
    collection = Enum("Concept", members)  # type: ignore
    return collection


def compile_concepts_nlp(asset_dir: str | Path, base_model: str = "en_core_web_sm") -> Language:
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
    src = path_ok(asset_dir)
    nlp = spacy.load(base_model, exclude="senter,ner")

    nlp.tokenizer = customize_tokenizer(nlp=nlp, token_rules=srsly.read_json(src / "tokens.json"))
    ruler = nlp.add_pipe(
        "span_ruler",
        config={
            "spans_key": "sc",
            "phrase_matcher_attr": "LOWER",
            "spans_filter": {"@misc": "spacy.first_longest_spans_filter.v1"},
            # "validate": True,
        },
        # validate=True,
    )
    patterns = []

    for concept in create_concept_collection(src):
        patterns.extend(concept.value.from_disk(src))
    if not patterns:
        raise ValueError("Need to include either concept and/or artifact patterns.")
    ruler.add_patterns(patterns)  # type: ignore

    options = list({concept["id"].split("/")[0] for concept in patterns})
    nlp.add_pipe("add_cats_from_spans", config={"options": options})
    return nlp
