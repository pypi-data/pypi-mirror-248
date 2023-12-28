import random
import sqlite3
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import spacy
import srsly  # type: ignore
from pydantic import BaseModel, Field, StringConstraints
from spacy.language import Language
from spacy.tokens import Doc, DocBin
from typing_extensions import Annotated
from wasabi import msg  # type: ignore

from .pre import collect_texts, make_uniform_lines, randomize_fts_expr
from .tokenizer import customize_tokenizer


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
    include_footnotes: bool | None = Field(
        default=False,
        description="`opinion_segments` is used; but if True, then will also use `opinion_footnotes` table.",
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
        q = terms or self.fts_expr
        if not q:
            raise ValueError("No query terms available.")

        num_per_chunk = chunk_limit or self.chunk_limit
        if not num_per_chunk or not isinstance(num_per_chunk, int):
            raise ValueError("No number of chunks specified.")

        search_queries = list(randomize_fts_expr(q, num_per_chunk))

        sql_segments = """--sql
            select distinct(os.text), os.id -- must be a tuple for nlp.pipe in `parse()`
            from opinion_segments os join opinion_segments_fts on os.rowid = opinion_segments_fts.rowid
            where opinion_segments_fts match :fts_expr and os.char_count between 50 and 2000
            limit :num_results -- prevent Republic v. CA and other common titles to bias results
        ;"""

        sql_footnotes = """--sql
            select distinct(os.value), os.id -- must be a tuple for nlp.pipe in `parse()`
            from opinion_footnotes os join opinion_footnotes_fts on os.rowid = opinion_footnotes_fts.rowid
            where opinion_footnotes_fts match :fts_expr
            limit :num_results -- prevent Republic v. CA and other common titles to bias results
        ;"""

        num_results = results_per_query or self.results_per_query
        if not num_per_chunk or not isinstance(num_results, int):
            raise ValueError("No number of segments specified.")

        uniq_results: set[tuple[str, str]] = set()
        for fts_expr in search_queries:
            uniq_results.update(conn.execute(sql_segments, {"fts_expr": fts_expr, "num_results": num_results}))

        if self.include_footnotes:
            for fts_expr in search_queries:
                uniq_results.update(conn.execute(sql_footnotes, {"fts_expr": fts_expr, "num_results": num_results}))

        yield from uniq_results

    def query_not_in_ids(self, conn: sqlite3.Connection, raw_ids: set[str]):
        bits = [f"'{_id}'" for _id in raw_ids]
        ids = ",".join(bits)
        yield from conn.execute(
            f"""--sql
            select distinct(os.text), os.id -- must be a tuple for nlp.pipe in `parse()`
            from opinion_segments os
            where os.char_count between 250 and 1000 and os.id not in ({ids})
            limit {int(len(bits) * 0.1)}-- 10% of ids
        ;"""
        )

    def extract_span_ruler_terms_from_nlp(self, nlp: Language):
        ruler = nlp.get_pipe("span_ruler")
        phrases = []
        for obj in ruler.patterns:  # type: ignore
            if obj["id"] == self.id:
                if isinstance(obj["pattern"], str):
                    phrases.append(obj["pattern"])
        return phrases

    def create_asset_nlp(self, asset_dir: Path, base_model: str = "en_core_web_sm") -> Language:
        """Create rules-based nlp object with limited number of spacy patterns
        based on the id of the asset."""
        nlp = spacy.load(base_model, exclude="senter,ner")
        nlp.tokenizer = customize_tokenizer(nlp=nlp, token_rules=srsly.read_json(asset_dir.joinpath("tokens.json")))
        ruler = nlp.add_pipe(
            factory_name="span_ruler",
            config={
                "spans_key": "sc",
                "phrase_matcher_attr": "LOWER",
                "spans_filter": {"@misc": "spacy.first_longest_spans_filter.v1"},
                "validate": True,
            },
            validate=True,
        )
        ruler.add_patterns(self.from_disk(folder=asset_dir))  # type: ignore
        return nlp

    def apply_ruler_nlp(
        self,
        nlp: Language,
        conn: sqlite3.Connection,
        terms: list[str] | None = None,
        spans_key: str = "sc",
        chunk_limit: int | None = None,
        results_per_query: int | None = None,
        examples_per_asset: int = 50,
    ) -> Iterator[Doc]:
        """Create spaCy-based annotations of raw text from the database. It's possible to use
        the nlp object created by `Corpora().nlp` and the more focused `self.create_asset_nlp()`.
        These have different patterns included in the SpanRuler pipeline.

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
        query_terms = terms or self.fts_expr or self.extract_span_ruler_terms_from_nlp(nlp)
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

    def split_train_data(
        self,
        docs: Iterator[Doc],
        ratio: float = 0.8,
        train_output_dir: Path = Path("corpus/train"),
        dev_output_dir: Path = Path("corpus/dev"),
    ):
        """Split the docs that have been converted by `apply_ruler_nlp()` into two categories: dev and train.
        Then store each docbin in separate folders."""
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

    def data_to_spacy(
        self,
        nlp: Language,
        conn: sqlite3.Connection,
        ratio: float = 0.8,
        train_output_dir: Path = Path("corpus/train"),
        dev_output_dir: Path = Path("corpus/dev"),
        terms: list[str] | None = None,
        spans_key: str = "sc",
        chunk_limit: int = 3,
        results_per_query: int = 10,
        examples_per_asset: int = 10000,
    ):
        """Methods employed:

        1. Query database text that match q.txt / terms: `query()`
        2. Convert each text to a spaCy Doc: `apply_ruler_nlp()`
        3. store each Doc in a DocBin, serialized to .spacy format: this step.

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
        if docs := self.apply_ruler_nlp(
            nlp=nlp,
            conn=conn,
            terms=terms,
            examples_per_asset=examples_per_asset,
            spans_key=spans_key,
            chunk_limit=chunk_limit,
            results_per_query=results_per_query,
        ):
            msg.info(f"Created docs for {self.id}")
            self.split_train_data(
                docs=docs,
                train_output_dir=train_output_dir,
                dev_output_dir=dev_output_dir,
                ratio=ratio,
            )
