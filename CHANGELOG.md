# Changelog

All notable changes to `cdfi-superpowers`. Versioning is CalVer (`YYYY.M.MINOR`).

## 2026.8.0

**CalVer discontinuity, noted deliberately.** `2026.7.3` through `2026.7.6` all
shipped in **August** (Aug 1, 5, 7 and 9) while keeping the `7` minor, so the
month segment had drifted a full month out of true. This release resets it to the
actual month rather than continuing the drift: `2026.7.6` → **`2026.8.0`**. Nothing
pins a `2026.7.x` string outside this repo — the plugin is not listed in any
external directory (see below) — so the jump breaks no installed pin.

### Added
- **The three skills are now installable by any spec-conformant agent, not just
  Claude Code.** The skills moved from `skills/` to **`.agents/skills/`**, the
  agent-neutral path in the Agent Skills spec. GitHub Copilot discovers skills
  from `.agents/skills/` (project) and `~/.copilot/skills/` (personal) and never
  scanned a bare `skills/`, which is why a Copilot user could not install this
  repo at all. Moved with `git mv` so history follows; **no SKILL.md was copied** —
  there is exactly one on-disk copy of each, as before.
- **A `compatibility:` frontmatter field on all three skills** (spec-defined,
  ≤500 chars), naming the real runtime requirement per skill: Python, pip, PyPI,
  and the specific federal endpoints that skill actually calls, sourced from
  `references/data-source-map.md`. This is the only edit made to any skill body.
- **README: a runtime-requirement block above the platform list.** These skills
  `pip install` and execute Python against public federal endpoints; in a
  locked-down enterprise that is what decides whether they can work at all, and
  the README never said so.

### Changed
- **README install section rewritten with real per-platform paths.** Section (c)
  previously read "Point any assistant at the raw Markdown," which is the shrug
  that the Copilot user hit. Now: (a) Claude Code/Cowork marketplace, (b)
  claude.ai `.skill` upload, (c) **GitHub Copilot** — project scope, personal
  scope, and a verified `gh skill install` form, (d) Cursor and other
  spec-conformant agents via `.agents/skills/`, (e) `llms.txt` labelled honestly
  as a crawler index rather than an install method.
- **`scripts/make_skills.sh`, `llms.txt` and `plugin.json` re-pointed** to
  `.agents/skills/`. The `.skill` archives are unaffected in shape — each is still
  a zip with `SKILL.md` at its root, because the script `cd`s into the skill
  directory before zipping and the source path is never recorded in the archive.
- **`hmda-analyzer`'s Python floor corrected in README and
  `references/package-index.md`.** Both said the pin implied **Python >=3.11**.
  That was true of `0.6.0` alone; **`0.6.1` (2026-08-07) relaxed `requires_python`
  back to `>=3.9`** while keeping the refusal. Verified this session: `pip install
  "hmda-analyzer>=0.6.0"` resolves to `0.6.1`, whose `__all__` is still 33 and
  still exports `GeographyVintageError`, `UnreachableFlagError`,
  `EmptyUniverseError` and the three basis maps. **The `>=0.6.0` floor is
  therefore kept, not bumped** — `0.6.1` changed nothing the skill layer depends
  on, and the pin already resolves to it everywhere. The bare-install hazard the
  floor guards against is unchanged and still documented.
- **`llms.txt`: the PyPI user corrected from `Jaypatel1511` to
  `thejaypatel1511`.** `Jaypatel1511` is the **GitHub** handle; the PyPI account
  is `thejaypatel1511`, confirmed against the Maintainers panel of a published
  project page. The README was already correct. Both handles are now named
  explicitly so the two namespaces stop being conflated.

### Verified — the plugin loader reads the dot-prefixed path
Tested from the working tree before the other two skills were moved, then again
with all three moved (`claude plugin install` + `claude plugin details`):

- All three skills load from `.agents/skills/` and are invocable. **No mirror, no
  symlink, no `.github/skills` fallback was needed.**
- **The `skills` array in `plugin.json` is *not* the only thing binding skill
  locations.** With the array emptied entirely, the two skills still sitting in
  `skills/` continued to load, while the one in `.agents/skills/` did not. The
  loader globs the conventional `skills/` directory *in addition to* the explicit
  array; the array is what makes a **non-conventional** path load. Moving the
  directories is therefore necessary **and** sufficient only because the array was
  repointed with them — and leaving any copy behind in `skills/` would have
  double-loaded it. `skills/` is now removed outright.

### Known — noticed, not changed
- **`llms.txt` still pins `cdfi-benchmark 0.2.0`** against `>=0.2.1` everywhere
  else. Unchanged for the same reason as the last three releases: it belongs to
  the cdfi-peer-benchmark sync, and correcting it here would assert a verification
  that has not happened. (Recorded here for the **fourth** time.)
- **`gh skill install` requires `--allow-hidden-dirs` against this layout.**
  `gh skill` classifies `.agents/skills/` as a hidden directory and, without the
  flag, reports "no standard skills found, but 3 skill(s) exist in hidden
  directories" and installs nothing. This is a real cost of the move: the plain
  `gh skill install <repo> <skill>` form worked against the old `skills/` layout
  and now needs one extra flag. The README prints the flag. Not worked around,
  because the Copilot discovery paths are the point of the move.
- **Two `SKILL.md` files exceed the 500-line guideline** — `hmda-analysis` (730)
  and `nmtc-eligibility` (561). Both **pass** `agentskills validate`; the limit is
  a guideline the reference validator does not enforce. Left alone rather than
  cut, since trimming correct, executed content to hit a soft target is not a
  change this release is scoped to make.
- **`cdfi-superpowers` is not listed in `anthropics/claude-plugins-community`.**
  Checked this session against that repo's `marketplace.json` (2,281 plugins):
  zero occurrences of `cdfi`, `nmtc`, `hmda` or `Jaypatel1511`. The 2026-07-19
  submission never landed. No stale SHA pins the old layout — which is the only
  reason this release's path move carries no external breakage.

## 2026.7.6

### Changed
- **nmtc-eligibility synced to nmtc-mapper 0.4.2** (published to PyPI 2026-08-05). Verified against
  a clean-venv, cold-cache, isolated-`HOME` install of the published wheel; every executed block in
  the skill was re-run against it and **no figure moved**.
  - **Install floor raised `>=0.4.1` → `>=0.4.2`, and the floor paragraph gained its third
    reason.** A tract reaches LIC status by three routes; the CDFI Fund publishes the poverty and
    80%-AMI routes in the eligibility workbook's column C and the §45D(e)(5) high-migration-rural
    route in column N. Pre-0.4.2 read column C alone as the entire verdict while separately
    parsing, storing and surfacing column N as `is_high_migration_rural`. Re-derived from the live
    table this session: 1,422 tracts carry the high-migration-rural designation and **168 qualify
    on that route alone** — all non-metro, all in the (80%, 85%] MFI band. Those 168 were reported
    ineligible by a package simultaneously surfacing the evidence of their eligibility. This is the
    skill's own third-state rule — "a false 'ineligible' is exactly as damaging as a false
    'eligible'" — shipped as a defect in its own backing dependency, which is why the floor is
    load-bearing rather than version hygiene. 0.4.2 reads the verdict as **C or N**.
  - **Corrected the release history the sync was scoped from.** The CDFI Fund moved the C/N
    boundary in **July 2026**, folding the high-migration-rural route into column C and renaming
    that column's header. Against the workbook the loader downloads today the 168-tract divergence
    is therefore **no longer reproducible** (HMR-yes/column-C-no is now an empty set), and 0.4.1
    does not answer at all — its positional header validation raises `EligibilitySchemaError` and
    loads nothing (executed this session). The skill states both presentations rather than the
    unreachable one.
  - **Added an `is_high_migration_rural` diagnostic** at the field list, written to what is
    actually observable on a stale install: `EligibilitySchemaError` against the current workbook,
    or a self-contradicting `is_high_migration_rural=True` / `nmtc_eligible=False` against a cached
    pre-July-2026 one. Remedy named (upgrade) and checkable with tract `01013953500`, the first of
    the 168 — `nmtc_eligible=True`, `is_high_migration_rural=True`, `distress_level='lic'` on 0.4.2.
  - **The 1,408 OZ vintage-miss figure re-derived rather than carried forward.** Previously cited to
    the 0.4.1 Known Issues; independently recomputed this session as 1,408 of the 8,764 designated
    OZ tracts (16.1%) absent from the 85,395-row 2020-basis table. Figure holds on 0.4.2.
  - **`is_nmtc_native_area` re-verified** as `True`-count 0 across all 85,395 rows on 0.4.2;
    citation moved to the 0.4.2 Known Issues. Field retained — its removal is coordinated with
    nmtc-mapper 0.5.0.
  - **Geocoder failure-mode provenance corrected to 0.4.2**, with all four branches re-executed:
    agreement and no-match against the live Census endpoint, transport failure and ambiguous-address
    both induced. `0.4.0`/`0.3.4+` attributions elsewhere in the file are accurate history and were
    left as written.
- **Stale `nmtc-mapper` pins corrected in three places** — `README.md`, `llms.txt` and
  `references/package-index.md` all read `>=0.4.1` against the skill's new `>=0.4.2` floor; now
  `>=0.4.2`. Manifests to 2026.7.6 and the README version line with them.

### Noticed, not changed
- **`llms.txt` pins `cdfi-benchmark 0.2.0`** against `>=0.2.1` everywhere else in the repo. Different
  package, and the cdfi-peer-benchmark skill has not been verified against an install; correcting the
  string without that verification would assert a sync that has not happened. Left for that skill's
  own release. (Recorded here for the third time.)

## 2026.7.5

### Fixed
- **hmda-analysis: corrected a false safe-list.** 2026.7.4 stated that
  "`lending_by_county` and `lending_by_state` are likewise unaffected — county and state FIPS did
  not change at this boundary." **County FIPS did change at exactly that boundary.** Alaska retired
  `02261` (Valdez-Cordova) into `02063` (Chugach) + `02066` (Copper River), landing in the LAR at
  2021→2022. Verified against live LAR this session, full-state Alaska pulls with
  `limit_truncated=False` in both years: `02261` carries 323 rows in 2021 and 0 in 2022; `02063`
  and `02066` carry 0 in 2021 and 158 and 40 in 2022. A pooled 2021+2022 `lending_by_county`
  fragments one county into three rows. This was worse than over-warning: a safe-list broader than
  the safety, telling an AI to confidently pool a cut the package now refuses. `lending_by_state`
  remains correct and is still listed as unaffected. Scope is stated narrowly — one county at one
  boundary — so the correction does not over-swing into "all county work is unsafe."

### Added
- **hmda-analysis: the 2023→2024 boundary, which the skill did not know existed.** Connecticut
  replaced its eight legacy counties (`09001`…`09015`) with nine planning regions
  (`09110`…`09190`) for federal statistical use (87 FR 34235, 2022-06-06; Census lists it as the
  sole county-equivalent change of the 2020s), landing in the LAR at 2023→2024 and moving every CT
  tract GEOID's first five digits. It is a different shape from 2021→2022: there GEOIDs are reused
  for different ground (silent collision), here the key sets are disjoint (a pooled frame doubles
  rows). Confined to one state; the refusal is national, and the package's message says so and
  prices the cost.

### Changed
- **hmda-analysis synced to hmda-analyzer 0.6.0** (published to PyPI 2026-08-05). Verified against
  a clean-venv install of the published wheel; every figure below was re-read from it.
  - **The vintage section rewritten around the refusal.** In 0.5.0 the rule was an instruction an
    AI had to remember; in 0.6.0 the package enforces it. Six guarded geography-keyed aggregation
    sites across five public functions (`lending_by_tract`, `lending_by_county`,
    `lending_desert_score`, `racial_composition_by_tract`, and `lender_summary` — guarded twice,
    once per key) raise `GeographyVintageError`. `lending_by_state` is deliberately unguarded.
    Added a rule-zero prohibition on routing around it: no `try`/`except` that proceeds (every
    refusal subclasses `ValueError`, so a bare `except ValueError` catches it), no hand-rolled
    `groupby` to recover the declined number, no self-improvised crosswalk.
  - **The two refusals separated, because conflating them yields advice that does not work.**
    (1) *Unmapped year* — 2024 and 2025 have no cited tract basis, so pooling either with any other
    year refuses; excluding a state does not help, because the verdict is computed from the years
    the frame spans, never from the rows it contains. (2) *Two cited bases in one frame* — e.g. the
    county map across 2023→2024, where the refusal names the Connecticut cause. Both messages are
    quoted verbatim from the installed wheel. Also documents that which refusal fires is a function
    of the key, not the boundary: at 2023→2024 a tract-keyed call hits (1) while a county-keyed
    call hits (2), and only the county key surfaces the Connecticut text.
  - **"Filtering rows is never a way through" stated explicitly**, because it is the intuitive
    thing to try. Both refusals resolve the same two ways, both of which change the years rather
    than the rows: split at the boundary into two labelled panels (endorsed), or narrow with
    `vintage=` — which takes the *basis* year, not the data year.
  - **The bundled `tract_vintage_methodology.md` (242,085 bytes) named as authoritative.**
    `get_methodology_path` now takes a filename; the old no-argument call still returns
    `cra_proxy_methodology.md` (22,313 bytes) unchanged.
  - **`lender_vs_market` small-N suppression surfaced.** A silent 5-application threshold
    (`MIN_APPLICATIONS_FOR_RATE`) was dropping race groups entirely in 0.5.0 with nothing recording
    it; 0.6.0 discloses it in six columns, three per side, because the two frames are suppressed
    independently. The skill now requires surfacing them whenever the table is rendered, the same
    way it requires the CRA-proxy caveat — an absent group that is not named reads as a group with
    no lending. Verified on a 60-row frame: five protected classes suppressed market-side, 10
    applications, all named.
  - **`lending_desert_score` documented as it actually computes.** `is_lending_desert` is a
    conjunction (`app_percentile < 25` **and** `denial_rate > 0.15`), not a cut on `desert_score`;
    below `DESERT_TRACT_FLOOR` (5) tracts the flag is arithmetically unreachable and the call raises
    `UnreachableFlagError` rather than returning a fabricated `False`. No housing-unit figure is
    read anywhere — the "expected volume based on housing units" claim was removed from the package
    in 0.6.0 as unfounded, and the skill now forbids it in output. (It never appeared in this
    repo's prose; nothing had to be deleted.)
  - **`cra_proxy_distribution(include_purchased=True)` now raises `EmptyUniverseError`** on a frame
    with no action-6 rows — which is always, for API-loaded frames, since `API_ACTIONS_TAKEN` never
    fetches action 6. Purchased-loan analysis requires `load_from_file` with data obtained another
    way. The signature line also now shows the 0.6.0 keyword-only arguments.
  - **`limit=` documented as truncation, not sampling.** Every loaded frame carries
    `limit_truncated`, written even when `False`; under `load_range` it is per year and therefore
    not uniform across the frame. A truncated pull must never be described as a sample, and
    `limit_truncated=True` must be disclosed beside the number.
  - **Constants section added, with definition paths rather than re-export paths.** The three basis
    maps and `basis_year` are top-level exports; the thresholds are not.
    `MIN_APPLICATIONS_FOR_RATE`, `API_ACTIONS_TAKEN` and `TRUNCATED_COLUMN` are defined in
    `hmdaanalyzer.data.schema`; `DESERT_PERCENTILE_THRESHOLD`, `DESERT_DENIAL_RATE_FLOOR` and
    `DESERT_TRACT_FLOOR` in `hmdaanalyzer.geography_vintage`. The `analysis.disparity`,
    `analysis.geographic` and `data.loader` paths resolve to the same objects but are re-exports;
    citing them sends a reader to a file where the constant cannot be changed. `DESERT_TRACT_FLOOR`
    is *derived* from the percentile threshold at import, not configured.
  - **Python floor is now `>=3.11`** (0.5.0 was `>=3.9`), and the install section leads with it: on
    Python 3.10 or older a bare `pip install hmda-analyzer` does not fail — pip resolves backwards
    and silently installs 0.5.0, the version with none of the above. The skill now pins
    `"hmda-analyzer>=0.6.0"` and requires checking `h.__version__` before quoting any number.
  - All four new typed errors added to the "Data source & typed errors" and "Failure modes" lists.
- **hmda-analysis firewall: `denial_rate_by_income_band` added to the not-wrapped list.** Re-checked
  against 0.6.0's `__all__`, which grew 25 → 33. The eight additions are three basis maps, four
  exception classes and the `basis_year` helper — no new analysis function, so nothing *new* belongs
  behind the firewall. But `denial_rate_by_income_band` shipped in 0.5.0, was never named in the
  firewall paragraph, and was neither wrapped nor firewalled: it lives in
  `hmdaanalyzer.analysis.disparity` and its own docstring states its purpose as identifying
  "income-based disparities." Now firewalled, with the reasoning stated.
  `racial_composition_by_tract` was named in the prose but missing from the enumerated list; added.
  No firewalled function was wrapped; the descriptive/inferential firewall is unchanged.
- **README, `llms.txt`, `references/package-index.md`: stale package pins corrected.** All three
  pinned `nmtc-mapper 0.3.3` against the nmtc-eligibility skill's load-bearing `>=0.4.1` floor, and
  `hmda-analyzer 0.5.0`. Now `>=0.4.1` and `>=0.6.0` respectively, with the Python floor noted.
  Nothing in the nmtc-eligibility skill body was touched.
- **README now states the plugin version** (`2026.7.5`), which both manifests carried and it did
  not.

### Known — noticed, not changed
- `llms.txt` line 17 pins `cdfi-benchmark 0.2.0`, while the README, the cdfi-peer-benchmark skill,
  and the 2026.7.3 CHANGELOG entry all carry `>=0.2.1`. Same class of stale-index defect as the
  pins fixed above, but it belongs to the cdfi-peer-benchmark sync and was left for it rather than
  corrected here unverified.

## 2026.7.4

### Fixed
- **hmda-analysis: added the tract-vintage boundary rule.** HMDA LAR carries 2010 census tracts for
  data years 2018–2021 and 2020 census tracts from 2022 onward. The skill had no mention of vintage
  or tract boundaries, documented `lending_by_tract` without qualification, and its own "When to use"
  example (`2020–2023`) spanned the boundary — so an AI following it would produce a tract-level cut
  that silently merges two different geographies under identical GEOID strings. Confirmed empirically
  in King County WA, DC, and Fulton County GA (August 2026): 308 colliding GEOIDs in King County
  alone, ~71% of each year's rows on a colliding key, nothing raised. Added a non-negotiable
  tract-vintage section, corrected the example, annotated `lending_by_tract`, and added a caveat
  bullet. Also states explicitly what is *not* affected (`cra_proxy_distribution`, which classifies
  per-row; `lending_by_county` / `lending_by_state`, whose FIPS did not change) so the rule does not
  over-warn.
- No package version change. The underlying defect is tracked for `hmda-analyzer` 0.6.0, where
  `lending_by_tract` will fail loud on a vintage-spanning frame; this skill change is the interim
  guard for skill-mediated use.

## 2026.7.3

### Fixed
- **cdfi-peer-benchmark: added the missing annualization / period-basis disclosure.** The skill
  covered data quality, heuristic peer groups, and synthetic sample peers, but carried no reference
  to `cdfi-benchmark` 0.2.1's disclosed non-annualization of NIM, ROAA, and ROAE at interim report
  dates — the skill's core output. An AI following the prior text would compare an interim NIM
  against a peer median and state the level as fact, understated by up to ~4×. Added a
  non-negotiable period-basis rule (disclosure quoted verbatim from the package CHANGELOG), a
  caveat bullet, and a note marking the worked example's 12/31 `report_date` as the one basis at
  which the issue does not arise. No package version change; floor remains `cdfi-benchmark>=0.2.1`.

### Changed
- **Marketplace/plugin metadata, released here rather than under 2026.7.2.** Commits `542152c` and
  `ce37550` (July 18 2026) added `displayName`, `author`, `repository`, `category`, `keywords`, and
  `tags`, and expanded the plugin description — all after 2026.7.2 was cut, so they sat on `main`
  unversioned. No skill text, no analytical behavior, and no dependency floors changed. Recorded
  here so the version history reflects what actually shipped under each tag.

## 2026.7.2

- Synced `nmtc-eligibility` skill to nmtc-mapper 0.4.1. Install floor raised to
  `>=0.4.1`.
  - **Tri-state answer space (0.4.0):** `nmtc_eligible` is `Optional[bool]`.
    `None` / `"unknown"` means could-not-determine and is never "not eligible".
    New non-negotiable third-state rule; new `eligibility_status` four-way
    property; absent-tract worked example.
  - **Geocoder vintage bind (0.4.1):** the geocoder now resolves onto the
    eligibility table's 2020 tract basis (`schema.TRACT_VINTAGE`). Documented as
    data-source fragility context.
  - **OZ "No" is ambiguous:** a `Yes` may be reported as fact; a `No` cannot
    distinguish not-designated from a 2010/2020 tract-vintage miss (~16% of
    designations unreachable). Flagship example annotated accordingly.
  - **`is_nmtc_native_area` is always `False`** — no data source populates it; a
    `False` means "not determined", not "not a Native Area".
  - **FAQ citations re-pointed** to the current Feb 1 2024 version of the NMTC
    LIC ACS FAQ (was the superseded Sept 1 2023 version).
  - **Island Areas scope corrected:** not covered by the 2016-2020 ACS; the CDFI
    Fund publishes a separate territory file this package does not carry.
  - **Vintage-scope rule:** the three-window QLICI transition keyed to close
    date.

## 2026.7.1

- Synced `cdfi-peer-benchmark` skill to cdfi-benchmark 0.2.1 (leverage-ratio
  metric, real institution names, working name search, corrected efficiency
  ratio); examples re-executed against the published wheel.

## 2026.7.0 — Phase 1

Initial public skeleton — an AI skill layer over Jay Patel's published CDFI PyPI
portfolio. No new analytical code; skills install and call the existing packages.

### Added

- **Three skills**, each with executed worked examples and firm failure/caveat rules:
  - `nmtc-eligibility` — nmtc-mapper 0.3.3 + nmtc-screener 0.1.0.
  - `cdfi-peer-benchmark` — cdfi-benchmark 0.2.0 (bank CDFIs only; NaN-not-fabrication contract).
  - `hmda-analysis` — hmda-analyzer 0.5.0 (descriptive only; CRA-proxy with verbatim caveat; fair-lending firewall).
- **References**: `cdfi-industry-primer.md`, `data-source-map.md`,
  `package-index.md` (22 packages, PyPI-verified), `caveats-and-limits.md`.
- **Plugin packaging**: `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json` (single-plugin marketplace),
  `scripts/make_skills.sh` (builds `dist/*.skill` archives), `llms.txt`.

### Verified this session

- All cited PyPI versions checked against live PyPI JSON.
- Every skill code example executed in a fresh `/tmp` venv; real output pasted in.
- CRA-proxy caveat language copied verbatim from the package constant /
  bundled methodology, not paraphrased.

### Known gaps (flagged, not papered over)

- `nmtc-screener` PyPI metadata is bare; ownership inferred from its GitHub repo.
