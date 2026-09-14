#!/usr/bin/env python3
"""Gate: every plugin document that describes nmtc-mapper's ``eligibility_status``
vocabulary must agree with the INSTALLED package, not with a list retyped here.

Why this exists. nmtc-mapper 0.4.0 introduced ``eligibility_status`` with four
values; 0.6.0 added a fifth (``not-covered-territory``). Three package releases
in a row silently falsified this plugin's prose, because the vocabulary was
copied into several documents and updated in some. 2026.9.1 found twelve such
failures by hand. This script is the check that round ran as a scratch file,
made permanent and run by CI (``.github/workflows/refresh-versions.yml``).

What it does — and the two things it refuses to do:

1. Imports ``ELIGIBILITY_STATUS_VALUES`` from the installed ``nmtcmapper``.
   The five strings are NEVER retyped here. A gate that hard-codes the list
   certifies that the docs agree with the gate, not with the package.
2. Derives the INDETERMINATE subset (the statuses on which ``nmtc_eligible is
   None``) BY EXECUTION: it drives ``NMTCMapper.from_sample()`` (no network)
   through ``check_tract``, ``check_address`` with the geocoder stubbed to a
   genuine no-match, and ``enrich``, then collects the statuses that carried
   ``None``. It is never a literal.
3. For every document that lists two or more statuses: it must list all of
   them. (Two, not four — a 4-of-5 threshold is blind to a 3-of-5 copy.)
4. The ``None`` contract, wherever it is stated as a membership set
   (``{not-found, geocode-failed}``) or as a sentence saying
   ``eligibility_status`` is/in two or more statuses and speaking of ``None``:
   it must name every indeterminate status. Rule 3 is document-level and cannot
   see a two-value test inside a document that lists all five elsewhere.
5. No stale count word beside the enumeration: an ``N-way`` on a line about
   ``eligibility_status`` where N is not the vocabulary's size, an ``N
   indeterminate`` where N is not the indeterminate set's size, or ``either
   indeterminate``.
6. A floor: at least ``MIN_VOCABULARY_DOCS`` vocabulary-bearing documents must
   be found, the nmtc-eligibility SKILL.md must be one of them, and a scan
   that matches nothing FAILS rather than passing vacuously.

Run by hand from the repo root::

    pip install "nmtc-mapper==<the version the workflow pins>"
    python3 scripts/check_status_vocabulary.py

Exit 0 = every document agrees with the installed package. Exit 1 = drift, each
failure printed with file and line. If the installed package's vocabulary has
changed (a new release), the failures ARE the notification: fix the documents,
then bump the pin in the workflow.
"""
from __future__ import annotations

import io
import contextlib
import pathlib
import re
import sys
from unittest import mock

import pandas as pd

import nmtcmapper
from nmtcmapper import ELIGIBILITY_STATUS_VALUES, NMTCMapper

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Documents that carry user-facing prose about the packages. CHANGELOG.md is
# deliberately excluded: a changelog quotes the stale wording it fixed.
DOC_GLOBS = (
    ".agents/skills/*/SKILL.md",
    "references/*.md",
    "llms.txt",
    "README.md",
    "docs/index.html",
)

# Number of vocabulary-bearing documents found when this gate was written
# (2026-09-13, on 2026.9.1): .agents/skills/nmtc-eligibility/SKILL.md and
# docs/index.html. Raise it when a new document starts carrying the list;
# never lower it to make the gate pass.
MIN_VOCABULARY_DOCS = 2
KEY_DOC = ".agents/skills/nmtc-eligibility/SKILL.md"

NUMBER_WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
    6: "six", 7: "seven", 8: "eight", 9: "nine",
}


def derive_indeterminate_by_execution() -> tuple[set[str], set[str]]:
    """Return (indeterminate, determinate) status sets observed on real code paths.

    Uses the shipped 12-tract sample (no network). Every status in the
    installed vocabulary must be reached, or the derivation is incomplete and
    the gate fails — a vocabulary this script cannot exercise is one it cannot
    certify.
    """
    with contextlib.redirect_stdout(io.StringIO()):
        m = NMTCMapper.from_sample()
    table = m._table
    eligible = str(table[table["nmtc_eligible"] == True].index[0])   # noqa: E712
    ineligible = str(table[table["nmtc_eligible"] == False].index[0])  # noqa: E712
    probes = [
        eligible,
        ineligible,
        "36061980000",  # well-formed, absent from the sample
        "66010950100",  # Guam — a DECIA territory prefix
    ]
    observed: dict[str, list] = {}

    # Surface 1: EligibilityResult via check_tract
    for tid in probes:
        r = m.check_tract(tid)
        observed.setdefault(r.eligibility_status, []).append(r.nmtc_eligible)

    # Surface 1, geocode branch: check_address with a genuine no-match. The
    # Census geocoder returns None for zero matches; stub exactly that.
    with mock.patch.object(nmtcmapper.mapper, "geocode_address", return_value=None):
        r = m.check_address("99999 Nonexistent Street, Nowhereville, ZZ 00000")
    observed.setdefault(r.eligibility_status, []).append(r.nmtc_eligible)

    # Surface 2: enrich (enrich_dataframe) on the same probes plus a None id.
    df = pd.DataFrame({"tract_id": probes + [None]})
    with contextlib.redirect_stdout(io.StringIO()):
        out = m.enrich(df, tract_col="tract_id")
    for status, val in zip(out["eligibility_status"], out["nmtc_eligible"]):
        observed.setdefault(status, []).append(None if pd.isna(val) else bool(val))

    unreached = set(ELIGIBILITY_STATUS_VALUES) - set(observed)
    unknown = set(observed) - set(ELIGIBILITY_STATUS_VALUES)
    if unreached or unknown:
        sys.exit(
            f"FAIL derivation: statuses not exercised={sorted(unreached)}, "
            f"statuses observed but not in ELIGIBILITY_STATUS_VALUES={sorted(unknown)}"
        )
    indeterminate = {s for s, vals in observed.items() if all(v is None for v in vals)}
    determinate = {s for s, vals in observed.items() if all(v is not None for v in vals)}
    mixed = set(observed) - indeterminate - determinate
    if mixed:
        sys.exit(f"FAIL derivation: status carried both None and a bool: {sorted(mixed)}")
    return indeterminate, determinate


def status_pattern(value: str) -> re.Pattern:
    # A status token bounded by non-identifier characters, so "not-found" does
    # not match inside "not-found-in-this-vintage" and "eligible" alone never
    # matches "verified-eligible".
    return re.compile(rf"(?<![\w-]){re.escape(value)}(?![\w-])")


def check_document(path: pathlib.Path, vocab: tuple[str, ...], indeterminate: set[str]) -> tuple[list[str], bool]:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    failures: list[str] = []

    present = {v for v in vocab if status_pattern(v).search(text)}
    vocabulary_bearing = len(present) >= 2
    if vocabulary_bearing:
        missing = set(vocab) - present
        if missing:
            failures.append(f"{rel}: lists {sorted(present)} — missing {sorted(missing)}")

    # Rule 4: the None contract, in the two shapes 2026.9.1 found it stated in.
    #  (a) a brace set naming any status — `{not-found, geocode-failed}` was
    #      the membership test at SKILL.md:205 — must name every indeterminate
    #      status;
    #  (b) a sentence that says `eligibility_status` is/in two or more statuses
    #      and speaks of `None` / indeterminate — the tying rule at :167 — must
    #      name every indeterminate status.
    # Document-level rule 3 cannot see either: both sat inside a document that
    # listed the (then) full vocabulary elsewhere.
    contract_words = re.compile(r"\bindeterminate\b|`None`|\bis None\b|=None\b|\bNone\b")
    for m in re.finditer(r"\{[^{}]*\}", text):
        in_set = {v for v in vocab if status_pattern(v).search(m.group(0))}
        if in_set and not indeterminate <= in_set:
            line_no = text.count("\n", 0, m.start()) + 1
            failures.append(
                f"{rel}:{line_no}: membership set {m.group(0)!r} names "
                f"{sorted(in_set)} — missing {sorted(indeterminate - in_set)}"
            )
    # Prose rules run on a FLATTENED copy: markdown emphasis characters and
    # newlines become spaces, one-for-one, so offsets (and therefore line
    # numbers) are preserved but "**two**\nindeterminate cases" reads as
    # "two indeterminate cases". The first red proof of this gate passed a
    # bolded, line-wrapped reinstatement of exactly that phrase.
    # Underscore is NOT flattened: it lives inside every identifier this gate
    # keys on (``eligibility_status``), and no document here uses _emphasis_.
    flat = re.sub(r"[*`\n]", " ", text)
    for m in re.finditer(r"[^.!?]*[.!?]", flat):
        sent = m.group(0)
        if "eligibility_status" not in sent or not contract_words.search(sent):
            continue
        in_sent = {v for v in vocab if status_pattern(v).search(sent)}
        if len(in_sent) >= 2 and not indeterminate <= in_sent:
            line_no = text.count("\n", 0, m.start()) + 1
            failures.append(
                f"{rel}:~{line_no}: sentence states the None contract naming "
                f"{sorted(in_sent)} — missing {sorted(indeterminate - in_sent)}"
            )

    # Rule 5: stale count words.
    n_way_ok = NUMBER_WORDS[len(vocab)]
    n_indet_ok = NUMBER_WORDS[len(indeterminate)]
    is_count = lambda w: w in NUMBER_WORDS.values() or w.isdigit()
    # An ``N-way`` belongs to the nearest property named in the 240 characters
    # before it: ``eligibility_status``, or one of the OZ properties, which
    # legitimately have their own arity.
    owner = re.compile(r"eligibility_status|ELIGIBILITY_STATUS|opportunity_zone_status|oz2_nomination_status")
    for m in re.finditer(r"\b(\w+)-way\b", flat):
        word = m.group(1).lower()
        if not is_count(word):
            continue
        owners = list(owner.finditer(flat, max(0, m.start() - 240), m.start()))
        if not owners or not owners[-1].group(0).lower().startswith("eligibility_status"):
            continue
        if word != n_way_ok and word != str(len(vocab)):
            line_no = text.count("\n", 0, m.start()) + 1
            failures.append(f"{rel}:{line_no}: stale count word {m.group(0)!r} (vocabulary has {len(vocab)})")
    for m in re.finditer(r"\b(\w+)\s+indeterminate\s+(?:case|branch|status|value|outcome)", flat, re.IGNORECASE):
        word = m.group(1).lower()
        if is_count(word) and word != n_indet_ok and word != str(len(indeterminate)):
            line_no = text.count("\n", 0, m.start()) + 1
            failures.append(f"{rel}:{line_no}: stale count word {' '.join(m.group(0).split())!r} (indeterminate set has {len(indeterminate)})")
    for m in re.finditer(r"\beither\s+indeterminate\b", flat, re.IGNORECASE):
        line_no = text.count("\n", 0, m.start()) + 1
        failures.append(f"{rel}:{line_no}: stale count word 'either indeterminate' (indeterminate set has {len(indeterminate)})")

    return failures, vocabulary_bearing


def main() -> int:
    vocab = tuple(ELIGIBILITY_STATUS_VALUES)
    indeterminate, determinate = derive_indeterminate_by_execution()
    print(f"nmtc-mapper {nmtcmapper.__version__}")
    print(f"ELIGIBILITY_STATUS_VALUES ({len(vocab)}): {vocab}")
    print(f"indeterminate by execution ({len(indeterminate)}): {sorted(indeterminate)}")
    print(f"determinate by execution   ({len(determinate)}): {sorted(determinate)}")

    docs = sorted({p for g in DOC_GLOBS for p in ROOT.glob(g) if p.is_file()})
    if not docs:
        print("FAIL: no documents matched DOC_GLOBS — the scan cannot pass vacuously")
        return 1

    all_failures: list[str] = []
    bearing: list[str] = []
    for p in docs:
        failures, is_bearing = check_document(p, vocab, indeterminate)
        all_failures.extend(failures)
        if is_bearing:
            bearing.append(str(p.relative_to(ROOT)))

    print(f"\nscanned {len(docs)} documents; {len(bearing)} carry the vocabulary: {bearing}")
    if len(bearing) == 0:
        all_failures.append("no document lists the vocabulary at all — a scan that matches nothing must fail")
    elif len(bearing) < MIN_VOCABULARY_DOCS:
        all_failures.append(f"only {len(bearing)} vocabulary-bearing documents found; floor is {MIN_VOCABULARY_DOCS}")
    if KEY_DOC not in bearing:
        all_failures.append(f"{KEY_DOC} does not carry the vocabulary — it is the document this gate exists for")

    if all_failures:
        print()
        for f in all_failures:
            print("FAIL", f)
        print(f"\n{len(all_failures)} failure(s)")
        return 1
    print("OK: every document agrees with the installed package")
    return 0


if __name__ == "__main__":
    sys.exit(main())
