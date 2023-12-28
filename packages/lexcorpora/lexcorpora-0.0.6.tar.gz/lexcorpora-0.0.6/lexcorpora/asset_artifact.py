from collections.abc import Iterator
from enum import Enum
from pathlib import Path
from typing import Any

import spacy
import srsly  # type: ignore
from spacy.language import Language

from .asset import Asset
from .pre import (
    path_ok,
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
)
from .tokenizer import customize_tokenizer

axiom = Asset(
    basis="axiom",
    label="axiom",
    matchers=patterns_axiom,
)

decorator = Asset(
    basis="decorator",
    label="decorator",
)

juridical_actor = Asset(
    basis="actor_juridical",
    label="actor",
    matchers=patterns_juridical,
    phrasers={"juridicals.txt"},
)

money = Asset(
    basis="money",
    label="money",
    fts_expr=[
        "Php ",
        "Philippine currency",
        "peso ",
        "USD",
        "dollars",
    ],
)

date_rule = Asset(
    basis="date",
    label="date",
    matchers=patterns_date,
)

vs_casename = Asset(
    basis="title_vs",
    label="vs",
    matchers=patterns_vs,
    phrasers={
        "casenames.txt",
        "fn_casenames.txt",
        "eyecite_goodnames.txt",
        "goodnames_1.txt",
    },
    fts_expr=[
        " v. ",
        " vs. ",
    ],
    chunk_limit=1,
    results_per_query=100,
)

statute_title = Asset(
    basis="title_statute",
    label="title",
    phrasers={"short.txt", "rules.txt"},
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
    def compile(cls, asset_dir: Path) -> Iterator[dict[str, Any]]:
        """Update `artifact_folder` before collecting patterns from the same."""
        for member in cls:
            member.value.to_disk(asset_dir)
            yield from member.value.from_disk(asset_dir)

    @classmethod
    def create_nlp(cls, asset_dir: Path, base_model: str = "en_core_web_sm") -> Language:
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
        ruler.add_patterns(cls.compile(asset_dir))  # type: ignore
        return nlp
