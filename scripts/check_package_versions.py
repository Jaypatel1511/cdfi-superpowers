#!/usr/bin/env python3
"""Assert that every package version this repo STATES agrees with live PyPI.

Why this exists
---------------
``.github/workflows/refresh-versions.yml`` rewrites the version chips in
``docs/index.html`` from PyPI every morning. It rewrites nothing else. Versions
are stated on four surfaces:

  1. ``references/package-index.md``  -- hand-maintained; the machine-readable
     package reference an agent loading this plugin actually reads.
  2. ``llms.txt``                     -- hand-maintained "resolves to X" claims.
  3. ``docs/index.html``              -- auto-maintained by the refresh job.
  4. ``README.md``                    -- install floors, no resolution claims.

Because only surface 3 was automated, surface 3 stayed nearly right while
surface 1 -- the one an agent reads -- drifted to ten wrong rows out of
twenty-two, three of which pointed at releases that had been **yanked for
presenting fabricated data as federal data**. A stale chip is cosmetic. A row
directing an agent at such a release is not.

Why a gate and not a second rewriter
------------------------------------
The version cell in ``references/package-index.md`` is not a bare literal. It
carries install floors (``>=0.6.1``), resolution notes
(``>=0.6.0 (pin resolves 0.6.1, py>=3.9; ...)``) and yank warnings. A floor is a
deliberate, load-bearing judgment -- README.md argues at length that the
``cdfi-benchmark`` floor is *deliberately not* the latest release because the
latest changed no library code. An automatic rewriter would have to decide
whether a floor should move, which is a semantic call it cannot make, and
bumping floors mechanically would erase exactly that reasoning. So this file is
CHECKED, not rewritten, and a disagreement fails the run loudly.

Checks
------
For every distribution named in the package-index table:

  * an exact version cell (``0.3.2``) must equal the current non-yanked release;
  * a floor (``>=0.6.1``) must name a real, non-yanked release no newer than the
    current one -- floors are allowed to lag, they are not allowed to be fiction;
  * any ``resolves 0.6.1`` / ``resolves to 0.6.1`` claim, wherever it appears,
    must equal the current release -- a dated claim that is now false is still
    false, so these are machine-checked rather than trusted;
  * a distribution with ANY yanked release must say ``yanked`` in its row -- a
    reader who pins an old version deserves to know it was withdrawn;
  * no version token stated anywhere in a row may itself be yanked.

And for ``docs/index.html``: every ``pkg-ver`` chip must equal the current
release for its ``pypi.org/project/SLUG/`` link. Chips are auto-maintained, so a
red here means the refresh job has not run since that package last published.

``CHANGELOG.md`` is deliberately NOT checked. A version there narrates a past
release ("nmtc-mapper 0.5.0 introduced ..."); it is a true statement about the
past, not a claim about what is current, and rewriting it would falsify history.

A lookup failure is a hard failure. A gate that cannot reach PyPI must never
report success -- silently-half-covered automation is what produced this defect.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "references" / "package-index.md"
LLMS = ROOT / "llms.txt"
DOCS = ROOT / "docs" / "index.html"

UA = {"User-Agent": "cdfi-superpowers-version-claims-gate"}

# A version token: 0.1.0, 1.7.1, 2026.9.1 -- three dot-separated numeric parts.
VERSION = r"\d+\.\d+\.\d+"
# "resolves 0.6.1" / "resolves to 0.6.1" -- PRESENT tense only. Past tense
# ("resolved 0.6.1 at the time", "verified 2026-08-13 ... resolved to 0.6.1") is
# a true statement about the past and does not decay; only a present-tense claim
# about what the floor resolves to TODAY can go false while sitting still.
RESOLVES = re.compile(rf"resolves(?:\s+to)?\s+(?:the\s+)?({VERSION})", re.I)
# "Latest on PyPI 2026-09-07: cdfi-benchmark 0.3.1" / "LATEST: 0.3.1"
LATEST = re.compile(rf"latest\b[^\n]*?({VERSION})", re.I)
# A docs chip: <a ... href=".../project/SLUG/">NAME</a><span class="pkg-ver">VER</span>
CHIP = re.compile(
    r'href="https://pypi\.org/project/(?P<slug>[^/"]+)/"[^>]*>'
    r'[^<]+</a><span class="pkg-ver">(?P<ver>[^<]+)</span>'
)


def pypi(dist: str) -> tuple[str, dict[str, str]]:
    """Return (current non-yanked version, {yanked version: reason})."""
    url = f"https://pypi.org/pypi/{dist}/json"
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        data = json.load(r)

    yanked: dict[str, str] = {}
    live: list[str] = []
    for version, files in data["releases"].items():
        if not files:
            continue
        if any(f.get("yanked") for f in files):
            reasons = [f.get("yanked_reason") or "" for f in files if f.get("yanked")]
            yanked[version] = next((x for x in reasons if x), "(no reason given)")
        else:
            live.append(version)

    # info.version is PyPI's own answer for "latest". Do not take it on trust:
    # assert it is a release we independently see as present and NOT yanked.
    current = data["info"]["version"]
    if current in yanked:
        raise RuntimeError(
            f"{dist}: PyPI info.version is {current}, which this check sees as YANKED. "
            "The assumption that info.version excludes yanked releases does not hold here."
        )
    if current not in live:
        raise RuntimeError(f"{dist}: PyPI info.version is {current}, which has no live files.")
    return current, yanked


def index_rows() -> list[tuple[int, str, str, str]]:
    """(line number, dist, version cell, whole row) for each table row."""
    rows = []
    for n, line in enumerate(INDEX.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        dist = cells[0]
        if dist in ("dist (PyPI)", "") or set(dist) <= set("-: "):
            continue
        rows.append((n, dist, cells[3], line))
    return rows


def main() -> int:
    failures: list[str] = []
    lookups: dict[str, tuple[str, dict[str, str]]] = {}

    rows = index_rows()
    if not rows:
        print(f"REFUSING: parsed 0 package rows out of {INDEX}. The table shape and "
              "this script disagree; a check that silently examines nothing is worse "
              "than none.")
        return 1

    slugs = {dist for _, dist, _, _ in rows}
    slugs |= {m.group("slug") for m in CHIP.finditer(DOCS.read_text(encoding="utf-8"))}

    for slug in sorted(slugs):
        try:
            lookups[slug] = pypi(slug)
        except (urllib.error.URLError, OSError, KeyError, ValueError, RuntimeError) as exc:
            failures.append(f"PyPI lookup failed for {slug}: {exc}")

    if failures:  # never grade claims against a partial picture
        print("FAILED lookups (a gate that cannot reach PyPI must not report success):")
        for f in failures:
            print(f"  {f}")
        return 1

    # ---- references/package-index.md -------------------------------------
    for n, dist, cell, row in rows:
        current, yanked = lookups[dist]
        where = f"{INDEX.relative_to(ROOT)}:{n} [{dist}]"

        floor = re.fullmatch(rf">=({VERSION})", cell)
        exact = re.fullmatch(VERSION, cell)

        if exact:
            if cell != current:
                failures.append(f"{where}: states {cell}, PyPI current is {current}")
        elif floor:
            pinned = floor.group(1)
            if pinned in yanked:
                failures.append(f"{where}: floor >={pinned} names a YANKED release")
            elif pinned not in {current} | set(yanked) and pinned > current:
                failures.append(f"{where}: floor >={pinned} is newer than PyPI current {current}")
        elif not re.search(VERSION, cell):
            failures.append(f"{where}: version cell {cell!r} states no version at all")

        # A yank anywhere in the package's history must be disclosed in the row.
        if yanked and "yank" not in row.lower():
            listed = ", ".join(sorted(yanked))
            failures.append(
                f"{where}: PyPI has yanked release(s) {listed} but the row does not say 'yanked'"
            )

        # No token anywhere in the row may point at a yanked release, unless the
        # row is explicitly describing it as yanked.
        for token in re.findall(VERSION, row):
            if token in yanked and "yank" not in row.lower():
                failures.append(f"{where}: row states {token}, which is YANKED: {yanked[token]}")

    # ---- "resolves to X" / "latest is X" claims, wherever they live --------
    # These are the claims that DECAY. A dated claim that is now false is still
    # false, so they are machine-checked rather than trusted to a date stamp.
    for path in (INDEX, LLMS, ROOT / "README.md",
                 *sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md"))):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            # Which distribution is this line talking about?
            named = [d for d in lookups if d in line]
            if not named:
                continue
            dist = max(named, key=len)  # longest match wins (nmtc-mapper vs nmtc-calc)
            current, _ = lookups[dist]
            for kind, rx in (("the floor resolves to", RESOLVES),
                             ("the latest release is", LATEST)):
                claim = rx.search(line)
                if claim and claim.group(1) != current:
                    failures.append(
                        f"{path.relative_to(ROOT)}:{n} [{dist}]: claims {kind} "
                        f"{claim.group(1)}, PyPI current is {current}"
                    )

    # ---- docs/index.html chips -------------------------------------------
    html = DOCS.read_text(encoding="utf-8")
    chips = list(CHIP.finditer(html))
    declared = len(re.findall(r'<span class="pkg-ver">', html))
    if len(chips) != declared:
        failures.append(
            f"{DOCS.relative_to(ROOT)}: page has {declared} version chips but this "
            f"check's pattern matched {len(chips)}; markup and check disagree"
        )
    for m in chips:
        slug, stated = m.group("slug"), m.group("ver")
        current, _ = lookups[slug]
        if stated != current:
            line = html[: m.start()].count("\n") + 1
            failures.append(
                f"{DOCS.relative_to(ROOT)}:{line} [{slug}]: chip says {stated}, "
                f"PyPI current is {current} (the refresh job has not run since it published)"
            )

    if failures:
        print(f"{len(failures)} version claim(s) disagree with PyPI:\n")
        for f in failures:
            print(f"  FAIL {f}")
        print("\nFix the stated version, or -- for a floor -- say why it deliberately lags.")
        return 1

    print(
        f"OK: {len(rows)} package-index rows, {len(chips)} docs chips and every "
        "'resolves to' claim agree with live PyPI; every yanked release is disclosed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
