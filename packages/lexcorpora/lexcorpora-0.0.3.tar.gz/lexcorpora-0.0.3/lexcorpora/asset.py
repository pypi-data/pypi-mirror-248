import random
import sqlite3
from collections.abc import Iterator
from enum import Enum
from pathlib import Path
from typing import Any

import srsly  # type: ignore
from pydantic import BaseModel, Field, StringConstraints
from spacy.language import Language
from spacy.tokens import Doc, DocBin
from typing_extensions import Annotated
from wasabi import msg  # type: ignore

from .pre import (
    collect_texts,
    make_uniform_lines,
    patterns_axiom,
    patterns_date,
    patterns_docket,
    patterns_juridical,
    patterns_numbered_generic,
    patterns_report,
    patterns_report_foreign,
    patterns_statute,
    patterns_unit,
    patterns_vs,
    randomize_fts_expr,
)


class Asset(BaseModel):
    """`patterns` associated with a single `label`. See generally:

    1. https://spacy.io/usage/rule-based-matching#entityruler-files
    2. https://spacy.io/usage/rule-based-matching#spanruler-files

    A `Asset` enables the creation of such pattern objects containing the same `Label`
    and custom `id`, if provided. Sample rule:

    ```py
    sample = Asset(
        src="artifact",
        basis="some-office",
        label="govt",
        matchers=[
            [
                {"LOWER": "the", "OP": "?"},
                {"LOWER": "ministry"},
                {"LOWER": "of"},
                {"LOWER": "labor"},
            ]
        ],
    )
    ```
    """

    src: str = Field(
        default="artifact",
        description="Folder source in corpus-assets; helps created a nested `@id`.",
    )
    basis: str = Field(
        default=...,
        description="Many 'basis' topics can be associated with single label; helps created nested `@id`.",
    )
    label: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^[A-Za-z]+$")] = Field(
        default=...,
        description="Applicable to spaCy SpanRuler and EntityRuler labels.",
    )
    matchers: list[list[dict[str, Any]]] | None = Field(
        default=None,
        description="Patterns from /preprocessor serializable to corpus-assets via `matchers_to_disk()`",
    )
    phrasers: set[str] = Field(
        default=None,
        description="Filenames from /assets/text serializable to corpus-assets via `phrases_to_disk()`",
    )
    fts_expr: list[str] | None = Field(
        default=None,
        description="If supplied, fills up full-text search sql statement in `query()` as parameter.",
    )
    chunk_limit: int | None = Field(
        default=3,
        description="If supplied, each q.txt or list of `fts_expr` is broken into chunks of this value.",
    )
    results_per_query: int | None = Field(
        default=50,
        description="The sql statement will be contain a default limit clause with this value.",
    )

    def __str__(self) -> str:
        return f"{self.src}-{self.basis}"

    def __repr__(self) -> str:
        return f"<Asset {self.src}/{self.basis}>"

    @property
    def id(self):
        return str(self)

    @property
    def matcher_path(self):
        return "/".join([self.src, self.basis, "patterns.json"])

    @property
    def phrase_path(self):
        return "/".join([self.src, self.basis, "q.txt"])

    def create_patterns(self, objs):
        return [{"label": self.label, "pattern": obj, "id": self.id} for obj in objs]

    def check_path(self, folder: Path, filename: str) -> Path:
        if not folder.exists():
            raise Exception(f"Missing {folder=}")
        return folder.joinpath(filename)

    def phrases_to_disk(self, folder: Path) -> Path:
        """The `phrasers` field, if it exists, is converted into a q.txt file. This
        overwrites conventional `q.txt` file in the proper folder."""
        if not self.phrasers:
            raise Exception("Phrase filenames not declared.")
        texts = collect_texts(src=folder.joinpath("text"), filter_filenames=self.phrasers)
        data = "\n".join(texts).strip()
        if not data:
            raise Exception("No lines detected.")
        file = self.check_path(folder, self.phrase_path)
        file.write_text(data=data)
        return file

    def matchers_to_disk(self, folder: Path) -> Path:
        """The `matchers` field, if it exists, is converted into a json file. This
        overwrites conventional `patterns.json` file in the proper folder."""
        if not self.matchers:
            raise Exception("Matcher patterns not declared.")
        file = self.check_path(folder, self.matcher_path)
        srsly.write_json(path=file, data=self.matchers)
        return file

    def to_disk(self, folder: Path):
        """Export patterns to the proper file and folder, populating / ovewriting
        `q.txt` and `patterns.json`."""
        try:
            self.phrases_to_disk(folder)
            msg.good(f"Phrases updated in assets: {self.id}")
        except Exception:
            msg.info(f"No need for phrase updates in assets: {self.id}")

        try:
            self.matchers_to_disk(folder)
            msg.good(f"Phrases updated in assets: {self.id}")
        except Exception:
            msg.info(f"No need for pattern updates in assets: {self.id}")

    def phrases_from_disk(self, folder: Path) -> list[str]:
        """Get rule's phrases from expected location."""
        file = self.check_path(folder, self.phrase_path)
        if not file.exists():
            return []
        return make_uniform_lines(file)

    def matchers_from_disk(self, folder: Path) -> list[list[dict[str, Any]]]:
        """Get rule's patterns from expected location."""
        file = self.check_path(folder, self.matcher_path)
        if not file.exists():
            return []

        data = srsly.read_json(path=file)
        if not isinstance(data, list):
            raise Exception(f"Improper {data=}")

        return data

    def convert_phrases_to_patterns(self, folder: Path) -> list[dict[str, Any]]:
        """Use `phrases_from_disk` to construct a list of patterns."""
        objs = self.phrases_from_disk(folder)
        patterns = self.create_patterns(objs)
        return patterns

    def convert_matchers_to_patterns(self, folder: Path) -> list[dict[str, Any]]:
        """Use `matchers_from_disk` to construct a list of patterns."""
        objs = self.matchers_from_disk(folder)
        patterns = self.create_patterns(objs)
        return patterns

    def from_disk(self, folder: Path):
        """Import patterns from the proper file and folder, sourcing from
        `q.txt` and `patterns.json`."""
        phrases = self.convert_phrases_to_patterns(folder)
        matchers = self.convert_matchers_to_patterns(folder)
        patterns = phrases + matchers
        return patterns

    def query(
        self,
        conn: sqlite3.Connection,
        terms: list[str] | None = None,
        chunk_limit: int | None = None,
        results_per_query: int | None = None,
    ) -> Iterator[tuple[str, str]]:
        """Extract annotatable segments associated with the asset from the `conn`, based
        on explicit `terms` provided.

        Args:
            conn (sqlite3.Connection): Means of searching segments associated with the asset
            terms (list[str] | None, optional): If no terms are included but `@fts_expr`  is supplied, use it.
                Note it's possible to use `.phrases_from_disk()` method to get the terms needed for searching
                but this requires another parameter `asset_dir`. Defaults to None.
            chunk_limit (int, optional): The text file / fts query may have too many strings, best to chunk it
                into sublists for variety;  otherwise may result in biased results. Defaults to 3.
            results_per_query (int, optional): sql's limit clause value. Defaults to 10.

        Yields:
            Iterator[tuple[str, str]]: The first part is raw text matching the query, the second part is the
            source id that may be useful as metadata.
        """
        if not (q := terms or self.fts_expr):
            raise ValueError("No query terms available.")

        num_per_chunk = chunk_limit or self.chunk_limit
        if not num_per_chunk or not isinstance(num_per_chunk, int):
            raise ValueError("No number of chunks specified.")

        num_segments = results_per_query or self.results_per_query
        if not num_per_chunk or not isinstance(num_segments, int):
            raise ValueError("No number of segments specified.")

        sql = """--sql
            select distinct(os.text), os.id -- must be a tuple for nlp.pipe in `parse()`
            from opinion_segments os join opinion_segments_fts on os.rowid = opinion_segments_fts.rowid
            where opinion_segments_fts match :fts_expr and os.char_count between 50 and 2000
            limit :num_segments -- prevent Republic v. CA and other common titles to bias results
        ;"""

        uniq_results: set[tuple[str, str]] = set()
        for fts_expr in randomize_fts_expr(q, num_per_chunk):
            params = {"fts_expr": fts_expr, "num_segments": num_segments}
            results = conn.execute(sql, params)
            uniq_results.update(results)

        yield from uniq_results

    def extract_span_ruler_terms(self, nlp: Language):
        ruler = nlp.get_pipe("span_ruler")
        phrases = []
        for obj in ruler.patterns:  # type: ignore
            if obj["id"] == self.id:
                if isinstance(obj["pattern"], str):
                    phrases.append(obj["pattern"])
        return phrases

    def parse(
        self,
        nlp: Language,
        conn: sqlite3.Connection,
        terms: list[str] | None = None,
        examples_per_asset: int = 50,
        spans_key: str = "sc",
        chunk_limit: int | None = None,
        results_per_query: int | None = None,
    ) -> Iterator[Doc]:
        """Create spaCy-based annotations of raw text from the database.

        Args:
            nlp (Language): What language to apply to the fetched segments from the database
            conn (sqlite3.Connection): Means of searching segments associated with the asset
            terms (list[str] | None, optional): If no terms are included but `@fts_expr`  is supplied, use it.
                Note it's possible to use `.phrases_from_disk()` method to get the terms needed for searching
                but this requires another parameter `asset_dir`; alternatively, can also use the language object
                to derive phrases based on `extract_phrasers_patterns(nlp)`. Defaults to None.
            examples_per_asset (int, optional): _description_. Defaults to 50.
            spans_key (str, optional): _description_. Defaults to "sc".
            chunk_limit (int, optional): The text file / fts query may have too many strings, best to chunk it
                into sublists for variety;  otherwise may result in biased results. Defaults to 3.
            results_per_query (int, optional): sql's limit clause value. Defaults to 10.

        Yields:
            Iterator[Doc]: Instances of candidates annotated by spaCy.
        """
        query_terms = terms or self.fts_expr or self.extract_span_ruler_terms(nlp)
        if not query_terms:
            msg.fail(f"No terms for {self.id=}; skip.")
            return

        texts = self.query(
            conn=conn,
            terms=query_terms,
            chunk_limit=chunk_limit,
            results_per_query=results_per_query,
        )

        counter = 0
        for doc, idx in nlp.pipe(texts, as_tuples=True):
            for span in doc.spans[spans_key]:
                if span.label_ == self.label:
                    counter += 1
                    doc.user_data["segment_id"] = idx
                    doc.user_data["asset_id"] = self.id
                    yield doc
                    break
            if counter == examples_per_asset:
                break

    def split(
        self,
        docs: Iterator[Doc],
        train_output_dir: Path,
        dev_output_dir: Path,
        ratio: float = 0.8,
    ):
        """Store DocBins based on the id"""
        file = f"{self.id.replace("/", "-")}.spacy"
        _docs = list(docs)
        if not _docs:
            msg.fail(f"No training data generated for {self.id}; skip.")
            return

        random.shuffle(_docs)
        split_idx = int(len(_docs) * ratio)
        train_docs, dev_docs = _docs[:split_idx], _docs[split_idx:]

        msg.info(f"{self.id=} no. of train Docs: {len(train_docs)}")
        msg.info(f"{self.id=} no. of dev Docs: {len(dev_docs)}")
        with msg.loading("Saving docs..."):
            DocBin(attrs=[], store_user_data=True, docs=train_docs).to_disk(train_output_dir / file)
            DocBin(attrs=[], store_user_data=True, docs=dev_docs).to_disk(dev_output_dir / file)
            msg.good("Done.")

    def bin(
        self,
        nlp: Language,
        conn: sqlite3.Connection,
        train_output_dir: Path,
        dev_output_dir: Path,
        terms: list[str] | None = None,
        examples_per_asset: int = 50,
        spans_key: str = "sc",
        chunk_limit: int = 3,
        results_per_query: int = 10,
        ratio: float = 0.8,
    ):
        """Combine `.split()` with `.parse()` to store DocBin annotations, thus querying database fragments of text
        processing it through this preprocess library, to generate `*.spacy` files stored in corpus-assets.

        Args:
            nlp (Language): The language object with a `SpanRuler`.
            conn (sqlite3.Connection): _description_
            train_output_dir (Path): Where to save the spacy train files
            dev_output_dir (Path): Where to save the spacy dev files
            terms (list[str] | None, optional): _description_. Defaults to None.
            examples_per_asset (int, optional): Each spacy file will contain Examples, this determines number.
                Defaults to 50.
            spans_key (str, optional): The key used to access the relevant SpanGroup. Defaults to "sc".
            chunk_limit (int, optional): Lists will be broken down to chunks of X number. Defaults to 3.
            results_per_query (int, optional): Each sql result set will be limited by this figure. Defaults to 10.
            ratio (float, optional): _description_. Defaults to 0.8.
        """
        msg.info(f"Starting {self.id}")
        if docs := self.parse(
            nlp=nlp,
            conn=conn,
            terms=terms,
            examples_per_asset=examples_per_asset,
            spans_key=spans_key,
            chunk_limit=chunk_limit,
            results_per_query=results_per_query,
        ):
            msg.info(f"Created docs for {self.id}")
            self.split(
                docs=docs,
                train_output_dir=train_output_dir,
                dev_output_dir=dev_output_dir,
                ratio=ratio,
            )


# Concepts as Assets


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


# Artifacts as Assets


axiom = Asset(
    basis="axiom",
    label="axiom",
    matchers=patterns_axiom,
    chunk_limit=1,
    results_per_query=30,
)

decorator = Asset(
    basis="decorator",
    label="decorator",
    chunk_limit=1,
    results_per_query=30,
)

money = Asset(
    basis="money",
    label="money",
    fts_expr=["Php ", "Philippine currency", "peso ", "USD", "dollars"],
)

date_rule = Asset(
    basis="date",
    label="date",
    matchers=patterns_date,
)

vs_casename = Asset(
    basis="title_vs",
    label="title",
    matchers=patterns_vs,
    phrasers={
        "casenames.txt",
        "fn_casenames.txt",
        "eyecite_goodnames.txt",
        "goodnames_1.txt",
    },
)

statute_title = Asset(
    basis="title_statute",
    label="title",
    phrasers={"clean_statute_titles.txt", "rules.txt"},
    chunk_limit=1,
    results_per_query=30,
)

reference = Asset(
    basis="reference",
    label="ref",
    matchers=patterns_report + patterns_report_foreign,
    phrasers={"fn_reporter.txt", "us.txt", "us2.txt"},
)

serial_number = Asset(
    basis="serial_num",
    label="serial",
    matchers=patterns_statute + patterns_docket + patterns_numbered_generic,
    phrasers={"fn_statutes.txt", "fn_docketnums.txt"},
)

statutory_unit = Asset(
    basis="unit",
    label="unit",
    matchers=patterns_unit,  # type: ignore
    phrasers={"fn_provisions.txt"},
)

juridical_actor = Asset(
    basis="actor_juridical",
    label="actor",
    matchers=patterns_juridical,
    phrasers={"juridicals.txt"},
)


class Artifact(Enum):
    """An `Artifact` has pre-determined, constructable patterns;
    this is different from legal concepts: arbitrary, approximatable spans."""

    DECORATOR = decorator
    AXIOM = axiom
    MONEY = money
    DATE = date_rule
    UNIT = statutory_unit
    SERIAL = serial_number
    REF = reference
    STATUTE_TITLE = statute_title
    VS_TITLE = vs_casename
    JURIDICAL_ACTOR = juridical_actor

    @classmethod
    def compile(cls, artifact_folder: Path) -> Iterator[dict[str, Any]]:
        """Update `artifact_folder` before collecting patterns from the same."""
        for member in cls:
            member.value.to_disk(artifact_folder)
            yield from member.value.from_disk(artifact_folder)
