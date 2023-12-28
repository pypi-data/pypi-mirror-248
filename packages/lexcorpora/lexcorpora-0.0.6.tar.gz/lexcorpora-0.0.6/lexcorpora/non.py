from pathlib import Path
from sqlite3 import Connection
from typing import Callable

import spacy
from spacy.tokens import DocBin


def extract_existing_segment_ids(corpus_path: Path, asset_type: str):
    docbin = DocBin(attrs=[])
    for file in corpus_path.glob(f"**/{asset_type}*.spacy"):
        docbin.merge(DocBin().from_disk(file))
    nlp = spacy.blank("en")
    for doc in docbin.get_docs(nlp.vocab):
        if doc.user_data.get("segment_id"):
            yield doc.user_data["segment_id"]


def create_non_span(
    conn: Connection,
    existing_doc_ids: set[str],
    target_path: Path,
    func: Callable,
    asset_dir: Path,
    spans_key: str = "sc",
    count: int = 500,
):
    """Detect text fragments in the database that are _not_ included in the
    `existing_doc_ids` and do not have any spans found within a doc.spans[`spans_key`]"""
    target_path.parent.mkdir(exist_ok=True, parents=True)
    nlp = func(asset_dir=asset_dir)
    _docbin = DocBin(attrs=[], store_user_data=True)
    while len(_docbin) < count:
        rows = conn.execute(
            """--sql
            select distinct(text), id
            from opinion_segments
            where char_count between 200 and 2000 and category = 'ruling' and id like '%gr%'
            ;"""
        )
        doc, id = next(nlp.pipe(rows, as_tuples=True))
        if id in existing_doc_ids:
            continue
        if doc.spans[spans_key]:
            continue
        doc.user_data["segment_id"] = id
        _docbin.add(doc)
    _docbin.to_disk(target_path)


def finalize_artifact_corpus(corpus_path: Path, data_type: str, asset_type: str):
    docbin = DocBin(attrs=[])
    files = corpus_path.glob(f"{data_type}/{asset_type}-*.spacy")
    for file in files:
        docbin.merge(DocBin().from_disk(file))
    if data_type == "train":
        docbin.merge(DocBin().from_disk(corpus_path / "non" / f"{asset_type}.spacy"))
    docbin.to_disk(corpus_path / f"{asset_type}-{data_type}.spacy")
