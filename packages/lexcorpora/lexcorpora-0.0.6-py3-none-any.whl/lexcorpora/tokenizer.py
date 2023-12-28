from pathlib import Path

import srsly  # type: ignore
from spacy.lang.char_classes import (
    ALPHA,
    ALPHA_LOWER,
    ALPHA_UPPER,
    CONCAT_QUOTES,
    LIST_ELLIPSES,
    LIST_ICONS,
)
from spacy.language import Language
from spacy.tokenizer import Tokenizer  # type: ignore
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex
from srsly._json_api import JSONOutput  # type: ignore

from .pre import (
    Abbv,
    PreUnit,
    admin_case,
    admin_matter,
    bar_matter,
    batas_pambansa,
    commonwealth_act,
    executive_order,
    general_register,
    make_uniform_lines,
    pres_decree,
    republic_act,
)

INFIXES_OVERRIDE = (
    LIST_ELLIPSES
    + LIST_ICONS
    + [
        r"(?<=[0-9])[+\\-\\*^](?=[0-9-])",
        r"(?<=[{al}{q}])\\.(?=[{au}{q}])".format(al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES),
        r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
        # ✅ Commented out regex that splits on hyphens between letters:
        # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
        r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
    ]
)
"""Remove hyphen '-' as infix, see [spacy docs](https://spacy.io/usage/linguistic-features#native-tokenizer-additions)"""

PAIRS = [("(", ")"), ("[", "]")]


def customize_prefix_list(pfx: list[str] = ["\\(", "\\["]):
    """Only use prefix `(` and `[` if _not_ followed by a single word `\\w+`
    with a closing `)` or `]`

    Note that modifications to a prefix should be done after the prefix removed, e.g.
    if the prefix is `(`, modify the `(`<add here> when appending a new rule.
    This is because of `compile_suffix_regex` which appends a `^` at the start of
    every prefix.

    The opening `open` will be considered a prefix only if not subsequently terminated
    by a closing `close`.

    example | status of `(`
    --:|:--
    `(`Juan de la Cruz v. Example) | is prefix
    Juan `(`de) la Cruz v. Example | is _not_ prefix

    How to use:

    ```
    from spacy.tokenizer import Tokenizer
    from spacy.util import compile_prefix_regex

    default_prefixes = list(nlp.Defaults.prefixes)
    p = compile_prefix_regex(customize_prefix_list(default_prefixes))
    Tokenizer(
        nlp.vocab,
        prefix_search=p.search,
    )
    ```
    """
    for opened, closed in PAIRS:
        pfx.remove(f"\\{opened}")
        pfx.append(f"\\{opened}(?![\\w\\.]+\\{closed})")
    return pfx


def customize_suffix_list(sfx: list[str] = ["\\)", "\\]"]):
    """Enable partner closing character, e.g. `)` or `]` to be excluded as a suffix
    if matched with an opening `(` or `[` within the range provided by `num`.

    Assuming a range of 20, this means 19 characters will be allowed:

    Let's exceed this range with 22, this results in a split of the
    terminal character `)`:

    ```py
    text = "twenty_two_char_string"
    len(text)  # 22
    nlp.tokenizer.explain("A (twenty_two_char_string)")
    # [('TOKEN', 'A'),
    # ('PREFIX', '('),
    # ('TOKEN', 'twenty_two_char_string'),
    # ('SUFFIX', ')')]
    ```

    This becomes the exception to the general rule that the closing suffix `)` should
    be removed from the custom tokenizer.

    However, if the number of characters within a closed / covered single world is 19
    and below:

    ```py
    text = "smol"
    len(text)  # 4
    nlp.tokenizer.explain("A (smol)")
    # [('TOKEN', 'A'),
    # ('TOKEN', '(smol)'),
    # ('TOKEN', 'word')]
    ```

    The suffix ")" is removed per the general rule.

    How to use:

    ```
    from spacy.tokenizer import Tokenizer
    from spacy.util import compile_suffix_regex

    default_suffixes = list(nlp.Defaults.suffixes)
    s = compile_suffix_regex(compile_suffix_regex(default_suffixes))
    Tokenizer(
        nlp.vocab,
        suffix_search=s.search,
    )
    ```
    """

    for opened, closed in PAIRS:
        sfx.remove(f"\\{closed}")
        _pre = "".join([f"(?<!\\{opened}\\w{{{i}}})" for i in range(1, 20)])
        sfx.append(f"{_pre}\\{closed}")
    return sfx


def customize_tokenizer(nlp: Language, token_rules: dict[str, list] | JSONOutput) -> Tokenizer:
    """Create a custom tokenizer with `token_rules` added to `nlp.tokenizer.add_special_case`."""
    # Customize prefixes like ( [
    pfx_override = customize_prefix_list(list(nlp.Defaults.prefixes))  # type: ignore
    prefix_re = compile_prefix_regex(pfx_override)
    nlp.tokenizer.prefix_search = prefix_re.search  # type: ignore

    # Customize suffixes like ) ]
    sfx_override = customize_suffix_list(list(nlp.Defaults.suffixes))  # type: ignore
    suffix_re = compile_suffix_regex(sfx_override)
    nlp.tokenizer.suffix_search = suffix_re.search  # type: ignore

    # Remove hyphen '-' as infix, see https://spacy.io/usage/linguistic-features#native-tokenizer-additions
    infix_re = compile_infix_regex(INFIXES_OVERRIDE)  # type: ignore
    nlp.tokenizer.infix_finditer = infix_re.finditer  # type: ignore

    # Add all token rules to the tokenizer
    for k, v in token_rules.items():  # type: ignore
        nlp.tokenizer.add_special_case(k, v)  # type: ignore
    return nlp.tokenizer


members = (
    admin_case,
    admin_matter,
    bar_matter,
    general_register,
    batas_pambansa,
    commonwealth_act,
    executive_order,
    pres_decree,
    republic_act,
)
serialized_abbvs = {k: v for member in members if member.initials for k, v in member.initials.as_token.items()}
generic_abbreviations = {
    f"{bit}.": [{"ORTH": f"{bit}."}] for style in (None, "lower", "upper") for bit in Abbv.set_abbvs(cased=style)
}
preunit_abbreviations = {
    f"{bit}.": [{"ORTH": f"{bit}."}] for style in (None, "lower", "upper") for bit in PreUnit.set_abbvs(cased=style)
}


def make_special_dotted():
    """Add a period after every text item to consider each a single token.
    These patterns can be used as a special rule in creating a custom tokenizer."""
    text = "Rep Sen vs Vs v s et al etc no nos Ll p Pp PP P.P R.P H.E H.B S.B a.k.a A.O CA-G.R Exh Ed ed infra supra id ibid rollo Rollo Id Ibid"  # noqa: E501
    return {f"{t}.": [{"ORTH": f"{t}."}] for t in text.split() if not t.endswith(".")}


def set_single_tokens(asset_path: Path, target_file: str = "artifact/singleton/patterns.json"):
    """Results in a dict of various exceptional rules for use in spacy tokenizer, e.g.:

    ```pycon
    >>> treat_as_single_token()
    {'A.C.': [{'ORTH': 'A.C.'}],
    'A.M.': [{'ORTH': 'A.M.'}],
    'B.M.': [{'ORTH': 'B.M.'}],
    'G.R.': [{'ORTH': 'G.R.'}],
    'A.O.': [{'ORTH': 'A.O.'}],
    'B.P.': [{'ORTH': 'B.P.'}],
    'C.A.': [{'ORTH': 'C.A.'}],
    ...}
    ```

    How to use:

    ```
    from spacy.tokenizer import Tokenizer
    Tokenizer(
        nlp.vocab,
        rules=set_single_tokens(),
    )
    """
    pubs = {
        line: [{"ORTH": line}]
        for line in make_uniform_lines(asset_path.joinpath("text/report_publisher_variants.txt"), min_char=2)
    }
    tokens = serialized_abbvs | generic_abbreviations | preunit_abbreviations | make_special_dotted() | pubs
    exported_file = asset_path.joinpath(target_file)
    srsly.write_json(exported_file, tokens)
    return tokens
