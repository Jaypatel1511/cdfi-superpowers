---
name: nmtc-eligibility
description: >-
  Check whether a U.S. address or census tract is New Markets Tax Credit (NMTC)
  eligible as a Low-Income Community, and screen a project's NMTC feasibility.
  Use when the user asks "is this address/tract NMTC eligible", about "distress
  criteria", "severe distress", "deep distress", "low-income community" / "LIC"
  status, or wants a first-pass NMTC deal feasibility score. Backed by the
  audited PyPI packages nmtc-mapper and nmtc-screener — never estimate
  eligibility from general knowledge.
---

# NMTC Eligibility

Grounds NMTC eligibility answers in two published, audited packages instead of
guessing. **nmtc-mapper** geocodes an address to a census tract and looks the
tract up in the CDFI Fund's NMTC Low-Income Community (LIC) eligibility table.
**nmtc-screener** runs a structured first-pass feasibility score on a project.

## When to use

- "Is 2400 Grand Concourse, Bronx NY NMTC eligible?"
- "Is census tract 36005023702 a low-income community?"
- "Does this tract qualify for severe distress / the 85% investment commitment?"
- "Screen this $8.5M grocery project for NMTC feasibility."

## When NOT to use

- Anything requiring the *official* CDFI Fund allocation decision — this is a
  screening/eligibility lookup, not an allocation award or legal determination.
- Historic Tax Credit, LIHTC, or Opportunity Zone *investment* structuring
  (OZ *flag* is reported by the mapper, but OZ deal mechanics are `oz-tracker`).
- NMTC transaction / credit / capital-stack modeling beyond the screener's
  first-pass estimate — that depth lives in `nmtc-calc`.

## Install

```
pip install nmtc-mapper nmtc-screener
```

Verified this session: **nmtc-mapper 0.3.3**, **nmtc-screener 0.1.0** (PyPI).

Import names (dist name ≠ import name):

| dist | import |
|---|---|
| nmtc-mapper | `nmtcmapper` |
| nmtc-screener | `nmtc_screener` |

## The hard failure rule (non-negotiable)

**If a tool errors, report the error verbatim and stop. NEVER estimate NMTC
eligibility from general knowledge, from the address alone, or from what a
neighborhood "seems like."** Eligibility is a specific tract-level lookup
against a specific CDFI Fund table; there is no valid way to infer it. A wrong
"eligible" answer can send a real deal down a dead end. A user asking for a
"best guess," "ballpark," or "rough" eligibility answer does not override this
rule; decline and report that the lookup failed.

## Worked example — address eligibility (executed)

```python
import nmtcmapper as nm

m = nm.NMTCMapper()
result = m.check_address("2400 Grand Concourse, Bronx, NY 10458")
result.summary()          # prints a formatted block; returns None
```

Actual output this session:

```
NMTC Eligibility Result
==================================================
  Address:          2400 Grand Concourse, Bronx, NY 10458
  Census Tract:     36005023702
  NMTC Eligible:    ✅ YES
  Distress Level:   SEVERE
  Description:      Severe Distress — qualifies for 85% investment commitment

  Poverty Rate:     32.1%
  AMI Ratio:        53.2%
  Unemployment:     10.7%
  Non-Metro:        No
  Opportunity Zone: No
  High Migration:   No
```

The `EligibilityResult` fields (read these, don't re-derive): `address`,
`tract_id`, `nmtc_eligible` (bool), `distress_level` (`'severe'`, `'deep'`,
`'ineligible'`, …), `poverty_rate`, `ami_ratio`, `unemployment_rate`,
`is_non_metro`, `is_high_migration_rural`, `is_nmtc_native_area`,
`severe_distress`, `deep_distress`, `geocode_success`, `is_opportunity_zone`.
`distress_description` gives the plain-English line (e.g. *"Severe Distress —
qualifies for 85% investment commitment"*).

Note `.summary` is a **method** — call `result.summary()`. `result.summary`
alone returns the bound method object, not the text.

## Worked example — tract lookup + the NaN honesty rule (executed)

```python
import nmtcmapper as nm
m = nm.NMTCMapper()
r = m.check_tract("11001980000")   # a non-residential DC tract
print(r.nmtc_eligible, r.distress_level, r.poverty_rate, r.ami_ratio)
```

Actual output this session:

```
False ineligible nan nan
```

`poverty_rate` and `ami_ratio` came back **NaN** for this tract. Render that as
"not available" — do **not** invent a poverty rate. `nmtc_eligible=False` is the
answer; the NaN demographics are simply not populated for that tract.

## Worked example — project feasibility screen (executed)

```python
import nmtc_screener as ns

r = ns.run_screening(
    project_name="Maple Street Grocery",
    location="Bronx, NY (Tract 36005023702)",
    total_project_cost=8_500_000,
    project_type="commercial",
    annual_revenue=3_200_000,
    lic_status="yes",          # accepted: "yes" | "unknown" | (anything else = treated as not-LIC)
)
print(r.qualification_likelihood, r.qualification_score)
```

Actual output this session:

```
HIGH 95
```

`qualification_reasons` (actual):

```
- Project is in a confirmed Low Income Community census tract (+35 pts)
- Project type 'Other': Eligibility depends on specific business activities and community benefit. (+10 pts)
- Project cost ≥$5MM — meets minimum viable deal size (+5 pts)
- Revenue ($3,200,000/yr) covers estimated debt service at 1.25x DSCR (+5 pts)
```

Note: the screener does not currently map project_type='commercial' to a
specific category — it scores it as 'Other' (+10 pts), so this component of the
score is type-agnostic; treat the result as a first-pass heuristic, not
underwriting.

`run_screening` signature (positional or keyword): `run_screening(project_name,
location, total_project_cost, project_type, annual_revenue, lic_status)`. The
`ScreeningResult` also carries `estimated_allocation`, `transaction_result`,
`credit_result`, `subsidy_result`, and a `plain_english_summary`.

**`lic_status` is the user's assertion, not a lookup.** If the user has not
confirmed LIC status, either run `nmtcmapper` first and pass the real answer, or
pass `"unknown"` — do not pass `"yes"` on assumption. The screener's score is
only as honest as this input.

## Output-presentation rules

- Always report the **census tract ID** alongside any eligibility verdict — it
  is the unit the answer is actually about.
- State the **eligibility table vintage** (below) so the user knows what the
  answer is current as of.
- Render NaN/None demographic fields as "not available," never as a number.
- Distinguish the mapper's *tract-eligibility lookup* (authoritative table
  lookup) from the screener's *feasibility score* (a heuristic first pass).
- Report the OZ flag as a separate fact; NMTC eligibility and OZ status are
  independent.

## Data dependencies & fragility (must document)

- **Census geocoder** — `geocode_address()` / `check_address()` call
  `geocoding.geo.census.gov`. This host has **no cloud WAF**, so it works from
  cloud/datacenter IPs (unlike the CRA/Cloudflare-blocked hosts elsewhere in the
  portfolio). Verified working this session (returned tract `11001980000` for a
  DC address).
- **CDFI Fund eligibility table** — `load_eligibility_table()` downloads the
  NMTC LIC eligibility workbook from cdfifund.gov and caches it under
  `~/.nmtcmapper/cache/`. **CDFI Fund URLs move**: the Fund relocates these files
  periodically, so a download can fail even though the package is fine. If it
  fails, **say the lookup failed and why — never guess eligibility.**
- **Tract vintage in force (verified this session):** the cached table is
  `NMTC_LIC_Eligibility_2016_2020.xlsb`, **85,395 census tracts**, columns
  including `nmtc_eligible`, `distress_level`, `poverty_rate`, `ami_ratio`,
  `unemployment_rate`, `is_non_metro`, `is_high_migration_rural`,
  `is_nmtc_native_area`, `severe_distress`, `deep_distress`. This is a
  2016–2020 ACS-based vintage. Report the vintage with the answer; the CDFI Fund
  periodically re-bases eligibility, and a deal must be checked against the
  vintage in force at application time.

## Failure modes

- **Geocoder returns no tract** (bad/ambiguous address): `geocode_address`
  returns `None`. Report "address could not be geocoded" — do not fall back to a
  ZIP-code or city-level guess.
- **CDFI Fund file download fails / 404** (URL moved): report the error and that
  eligibility could not be determined. Do not answer from memory.
- **NaN demographic fields**: report "not available," never fabricate.
- **Screener `lic_status` misuse**: passing `"yes"` without confirming LIC
  status produces a falsely high score. Confirm first.

## Caveats

- This is an **eligibility and feasibility screening layer**, not an allocation
  award, legal opinion, or the CDFI Fund's determination.
- Eligibility is **tract-specific and vintage-specific**. An "eligible" answer is
  only valid for the table vintage named above.
- The screener's score and estimated allocation are **first-pass heuristics** to
  triage deals, not underwriting or a commitment.
