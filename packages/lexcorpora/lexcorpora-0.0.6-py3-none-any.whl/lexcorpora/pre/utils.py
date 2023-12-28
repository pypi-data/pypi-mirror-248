import random
import re
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

from pydantic.functional_validators import AfterValidator
from rich.jupyter import print
from spacy.tokens import Doc
from typing_extensions import Annotated

camel_case_pattern = re.compile(r".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)")


def randomize_fts_expr(obj_list: list, num_per_chunk: int) -> Iterator[str]:
    """Randomize in place before querying so that first few items queried won't bias which
    annotations are selected. Divides `obj_list` based on a max `num_per_chunk`"""
    random.shuffle(obj_list)
    for index in range(0, len(obj_list), num_per_chunk):
        partial_list = obj_list[index : index + num_per_chunk]
        cleaned_terms = (re.sub(r"[^\w\s]+", " ", term) for term in partial_list)
        quoted_terms = (f'"{cleaned}"' for cleaned in cleaned_terms)
        yield " OR ".join(quoted_terms)


def uncamel(text: str) -> list[str]:
    """For text in camelCaseFormatting, convert into a list of strings."""
    return [m.group(0) for m in camel_case_pattern.finditer(text)]


def check_titlecased_word(v: str) -> str:
    assert all(bit.istitle for bit in v.split("-")), f"{v} is not titlecased."
    return v


TitledString = Annotated[str, AfterValidator(check_titlecased_word)]


def create_regex_options(texts: Iterable[str]):
    return "(" + "|".join(texts) + ")"


def spacy_re(v: str, anchored: bool = True, op: str | None = None) -> dict[str, Any]:
    """Helper function to add an anchored, i.e. `^`<insert value `v` here>`$`
    regex pattern, following `{"TEXT": {"REGEX": f"^{v}$"}}` spacy convention,
    unless modified by arguments.
    """
    if anchored:
        v = f"^{v}$"
    result = {"TEXT": {"REGEX": v}}
    return result | {"OP": op} if op else result


def spacy_in(v_list: list[str], default: str = "ORTH", op: str | None = None):
    """Helper function to add a specific list of options following
    `{"ORTH": {"IN": v_list}}` spacy convention, unless modified by arguments.
    """
    result = {default: {"IN": v_list}}
    return result | {"OP": op} if op else result


def set_optional_node():
    """Deal with nodes like (R.A.), [PD]"""
    _open = create_regex_options(texts=("\\(", "\\["))
    _close = create_regex_options(texts=("\\)", "\\]"))
    _in = "[\\w\\.]+"
    regex = "".join([_open, _in, _close])
    return spacy_re(v=regex, op="?")


def path_ok(candidate_path: str | Path) -> Path:
    if isinstance(candidate_path, str):
        candidate_path = Path(candidate_path)  # type: ignore
        if not candidate_path.exists():
            raise FileNotFoundError(candidate_path)
        return candidate_path
    elif isinstance(candidate_path, Path):
        return candidate_path
    raise Exception(f"Invalid {candidate_path}")


def see(doc: Doc) -> Doc:
    """Rich jupyter-based print spacy-entities and span groups from `doc`."""
    if doc.user_data:
        print(f"{doc.user_data=}")

    entity_data: dict[str, Any] = {}
    if doc.ents:
        for ent in doc.ents:
            if ent.label_ not in entity_data:
                entity_data[ent.label_] = []
            entity_data[ent.label_].append(ent.text)
        print(f"{entity_data=}")

    span_data: dict[str, Any] = {}
    if doc.spans:
        for key in doc.spans.keys():  # e.g. sc, ruler
            if span_group := doc.spans.get(key):
                for span in span_group:
                    if span.label_ not in span_data:
                        span_data[span.label_] = []
                    span_data[span.label_].append(span.text)
        print(f"{span_data=}")

    if doc.cats:
        cats_data = sorted(
            doc.cats.items(),
            key=lambda kv: (kv[1], kv[0]),
            reverse=True,
        )
        print(f"{cats_data=}")

    return doc


def make_uniform_lines(file: Path, min_char: int = 3) -> list[str]:
    """Updates file with sorted lines, filtering those not reaching `min_char` length."""
    raw_lines = file.read_text().splitlines()
    lines = sorted(
        set(bit.replace("’", "'").replace("`", "'") for bit in raw_lines if bit.strip() and len(bit) > min_char)
    )
    file.write_text("\n".join(lines))
    return lines


def extract_lines_from_txt_files(files: Iterable[Path]) -> Iterator[str]:
    """Accepts iterator of `*.txt` files, yields each line (after sorting, set content for uniqueness)."""
    for file in files:
        if file.suffix != ".txt":
            raise Exception(f"{file=} must be a .txt file separated by lines.")
        yield from make_uniform_lines(file)  # sort before split


def collect_texts(
    src: Path,
    filter_filenames: set[str],
    include_only_if_regex: str | None = None,
    exclude_always_if_regex: str | None = None,
) -> list[str]:
    uniqs = set()
    for file in src.glob("**/*.txt"):
        if file.name in filter_filenames:
            lines = make_uniform_lines(file)
            for line in lines:
                if include_only_if_regex:
                    if not re.search(include_only_if_regex, line):
                        continue
                if exclude_always_if_regex:
                    if re.search(exclude_always_if_regex, line):
                        continue
                uniqs.add(line)
    return sorted(uniqs)


def create_corpus_dirs(corpus_path: Path = Path("corpus")) -> tuple[Path, Path]:
    """Ensure initial directories exist

    Args:
        corpus_path (str): Where to store annotated DocBin .spacy files post-training with the model in the output path
    """
    corpus_path.mkdir(exist_ok=True)
    corpus_path.joinpath("train").mkdir(exist_ok=True)
    corpus_path.joinpath("dev").mkdir(exist_ok=True)
    return corpus_path / "train", corpus_path / "dev"
