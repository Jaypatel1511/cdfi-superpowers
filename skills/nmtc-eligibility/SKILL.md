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
pip install "nmtc-mapper>=0.4.0" nmtc-screener
```

Verified this session (PyPI): **nmtc-mapper 0.4.0**, **nmtc-screener 0.1.0**
(`nmtc-calc 0.2.1` is pulled in as a dependency). The `>=0.4.0` floor is not
cosmetic — 0.4.0 is where `nmtc_eligible` became tri-state (see below). A reader
on 0.3.x following this skill's third-state guidance would never see `None`,
because 0.3.x collapses "could not determine" into `False`.

Import names (dist name ≠ import name):

| dist | import |
|---|---|
| nmtc-mapper | `nmtcmapper` |
| nmtc-screener | `nmtc_screener` |

## The answer space is TRI-STATE (0.4.0 — read this before anything else)

`nmtc_eligible` is **`Optional[bool]`** — `True`, `False`, or **`None`**. There
are three outcomes, not two:

| `nmtc_eligible` | `distress_level` | meaning |
|---|---|---|
| `True`  | `deep` / `severe` / `lic` | **verified eligible** — the table says YES |
| `False` | `ineligible`              | **verified ineligible** — the table says NO |
| `None`  | `unknown`                 | **INDETERMINATE** — no verdict was reached |

**`None` / `"unknown"` means "could not be determined." It is NOT "not
eligible."** Never render `None` as "no," "ineligible," "not eligible," or a
falsy `False`. A `None` reached two ways: the address did not geocode, or the
tract is absent from the ~85k-tract universe (a bad/mistyped GEOID, or a
vintage mismatch). Neither is a NO — both are "we don't know."

`EligibilityResult.eligibility_status` (property, 0.4.0) collapses this into one
explicit four-way string so you never have to infer intent from a `None`:

```
verified-eligible  |  verified-ineligible  |  not-found  |  geocode-failed
```

`not-found` and `geocode-failed` are the two indeterminate cases. `summary()`
prints indeterminate results as `❓ UNKNOWN — … (indeterminate, NOT ineligible)`
on the eligibility line itself — that inline qualifier is defined in
`nmtcmapper/eligibility/checker.py::EligibilityResult.summary`, not a footer.

## The hard failure rule (non-negotiable)

**If a tool errors, report the error verbatim and stop. NEVER estimate NMTC
eligibility from general knowledge, from the address alone, or from what a
neighborhood "seems like."** Eligibility is a specific tract-level lookup
against a specific CDFI Fund table; there is no valid way to infer it. A wrong
"eligible" answer can send a real deal down a dead end. A user asking for a
"best guess," "ballpark," or "rough" eligibility answer does not override this
rule; decline and report that the lookup failed.

## The third-state rule (non-negotiable — the load-bearing addition)

The hard failure rule above governs a tool that *errors*. This rule governs a
lookup that *succeeds and returns UNKNOWN* (`nmtc_eligible is None`,
`distress_level == "unknown"`, `eligibility_status` in `{not-found,
geocode-failed}`). An unknown verdict is a **result, not an error** — and it
must be reported as its own answer:

- Report it as **"NMTC eligibility could not be determined for this tract"**,
  and **name the tract ID** (or state the address did not geocode). Say *why*:
  tract absent from the vintage's universe, or address failed to geocode.
- **Never** collapse it into "not eligible," "no," or "ineligible."
- **Never** soften it into "probably not eligible" or "likely ineligible."
- **Never** resolve it from a neighboring tract, the ZIP, the city, or the
  address's apparent neighborhood — the same anti-pressure posture as the
  best-guess rule above.

**Why, inline (a model reading this needs the reason, not just the rule):** a
`None` rendered as "not eligible" is a *fabricated negative*. It kills a deal
that may genuinely qualify — the tract simply was not checkable in this vintage,
and the correct next step is to re-check against the vintage in force at
application time, not to declare the deal dead. A false "ineligible" is exactly
as damaging as a false "eligible," in the opposite direction.

## Worked example — address eligibility (executed)

```python
import nmtcmapper as nm

m = nm.NMTCMapper()
result = m.check_address("2400 Grand Concourse, Bronx, NY 10458")
result.summary()          # prints a formatted block; returns None
print(result.eligibility_status)   # -> 'verified-eligible'
```

Actual output this session (nmtc-mapper 0.4.0, clean-venv PyPI install):

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

`eligibility_status` is `verified-eligible`. Tract `36005023702` verified
**present** in the live 2016–2020 table this session.

The `EligibilityResult` fields (read these, don't re-derive): `address`,
`tract_id`, `nmtc_eligible` (**`Optional[bool]` — True / False / None**),
`distress_level` (str: `'deep'`, `'severe'`, `'lic'`, `'ineligible'`,
`'unknown'`), `poverty_rate`, `ami_ratio`, `unemployment_rate`, `is_non_metro`,
`is_high_migration_rural`, `is_nmtc_native_area`, `severe_distress`,
`deep_distress`, `geocode_success`, `is_opportunity_zone`, **`tract_found`**
(bool, 0.4.0 — `False` when the tract is absent from the table). Properties:
`distress_description` (plain-English line, e.g. *"Severe Distress — qualifies
for 85% investment commitment"*) and **`eligibility_status`** (the four-way
string above).

Note `.summary` is a **method** — call `result.summary()`. `result.summary`
alone returns the bound method object, not the text.

## Worked example — verified-ineligible tract + the NaN honesty rule (executed)

A tract that is **present in the table with an explicit NO flag** — distinct
from an absent tract (next example). Verified this session: `11001980000` **is**
one of the 85,395 rows, flagged not-eligible, with unpopulated demographics.
This is a real DC non-residential tract (the `9800xx` series is special
land-use — parks, water — with no resident population, hence NaN rates).

```python
import nmtcmapper as nm
m = nm.NMTCMapper()
r = m.check_tract("11001980000")   # present, explicit NO, null demographics
print(r.nmtc_eligible, r.distress_level, r.poverty_rate, r.ami_ratio)
print(r.eligibility_status, "| tract_found:", r.tract_found)
```

Actual output this session:

```
False ineligible nan nan
verified-ineligible | tract_found: True
```

`poverty_rate` and `ami_ratio` came back **NaN** because this tract has no
population to measure — render them "not available," never invent a number.
`nmtc_eligible=False` / `eligibility_status='verified-ineligible'` /
`tract_found=True` is a **real NO from the table** — the answer *is*
ineligible. This is NOT the third state; contrast the next example, where the
tract is absent and the honest answer is "unknown."

## Worked example — the third state: an ABSENT tract (executed)

The teaching case for `None`/`"unknown"`. A syntactically valid GEOID that is
**not in the 2016–2020 universe** (a mistyped tract, or one from a different
vintage). Verified absent this session: `36061980000` is **not** among the
85,395 rows.

```python
import nmtcmapper as nm
m = nm.NMTCMapper()
r = m.check_tract("36061980000")   # a tract ABSENT from the 2016-2020 universe
print(r.nmtc_eligible, r.distress_level, r.eligibility_status, r.tract_found)
r.summary()
```

Actual output this session:

```
None unknown not-found False
```

```
NMTC Eligibility Result
==================================================
  Address:          Census Tract 36061980000
  Census Tract:     36061980000
  NMTC Eligible:    ❓ UNKNOWN — tract not in eligibility table (indeterminate, NOT ineligible)
  Distress Level:   UNKNOWN
  Description:      Indeterminate — eligibility not verified (no match / tract absent)
  Non-Metro:        No
  Opportunity Zone: No
  High Migration:   No
```

Report this as: *"NMTC eligibility could not be determined for tract
36061980000 — it is absent from the 2016–2020 eligibility universe."* Do **not**
report it as "not eligible." The `Description` line —
*"Indeterminate — eligibility not verified (no match / tract absent)"* — is the
verbatim value of `DISTRESS_LEVELS["unknown"]` in
`nmtcmapper/data/schema.py`.

The same third state reaches you from `check_address` when an address does not
geocode: `nmtc_eligible=None`, `distress_level="unknown"`,
`eligibility_status="geocode-failed"`, and `summary()` prints *"❓ UNKNOWN —
address could not be geocoded (indeterminate, NOT ineligible)."* (executed this
session against a deliberately unresolvable address).

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

Actual output this session (nmtc-screener 0.1.0):

```
HIGH 95
```

`qualification_reasons` (actual):

```
Project is in a confirmed Low Income Community census tract (+35 pts)
Project type 'Other': Eligibility depends on specific business activities and community benefit. (+10 pts)
Project cost ≥$5MM — meets minimum viable deal size (+5 pts)
Revenue ($3,200,000/yr) covers estimated debt service at 1.25x DSCR (+5 pts)
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
pass `"unknown"` — do not pass `"yes"` on assumption. And if the mapper returned
the **third state** (`None`/`"unknown"`), pass `"unknown"` to the screener —
never `"yes"`, and never `"no"`, because you do not know. The screener's score
is only as honest as this input.

## Output-presentation rules

- Always report the **census tract ID** alongside any eligibility verdict — it
  is the unit the answer is actually about — and, for an indeterminate result,
  name the tract (or state the address did not geocode) as part of the "could
  not be determined" answer.
- State the **eligibility table vintage** (below) so the user knows what the
  answer is current as of.
- Render NaN/None demographic fields as "not available," never as a number.
- Report a `None`/`"unknown"` eligibility verdict as "could not be determined,"
  never as "not eligible." (See the third-state rule.)
- Distinguish the mapper's *tract-eligibility lookup* (authoritative table
  lookup) from the screener's *feasibility score* (a heuristic first pass).
- Report the OZ flag as a separate fact; NMTC eligibility and OZ status are
  independent.

## Data dependencies & fragility (must document)

- **Census geocoder** — `geocode_address()` / `check_address()` call
  `geocoding.geo.census.gov`. This host has **no cloud WAF**, so it works from
  cloud/datacenter IPs (unlike the CRA/Cloudflare-blocked hosts elsewhere in the
  portfolio). Verified working this session (geocoded 2400 Grand Concourse to
  tract `36005023702`).
- **CDFI Fund eligibility table** — `load_eligibility_table()` downloads the
  NMTC LIC eligibility workbook from cdfifund.gov and caches it under
  `~/.nmtcmapper/cache/`. **CDFI Fund URLs move**: the Fund relocates these files
  periodically, so a download can fail even though the package is fine. On
  failure the loader now **raises** `EligibilityDownloadError` /
  `EligibilityParseError` (0.3.4+) rather than silently substituting demo data —
  **say the lookup failed and why; never guess eligibility.** (For offline
  demos only, `NMTCMapper.from_sample()` exists and stamps `data_source ==
  "sample"`; its 12 synthetic tracts are NEVER valid for a real answer.)
- **Tract vintage in force (verified this session):** the cached table is
  `NMTC_LIC_Eligibility_2016_2020.xlsb`, **85,395 census tracts**, sourced from
  the CDFI Fund's Aug-2025b Severe/Deep Distress release. Normalized columns
  include `nmtc_eligible`, `distress_level`, `poverty_rate`, `ami_ratio`,
  `unemployment_rate`, `is_non_metro`, `is_high_migration_rural`,
  `is_nmtc_native_area`, `severe_distress`, `deep_distress`. This is a
  2016–2020 ACS-based vintage (mandatory for QLICIs closed on/after Sept 1,
  2024). Report the vintage with the answer; the CDFI Fund periodically
  re-bases eligibility, and a deal must be checked against the vintage in force
  at application time. 0.4.0 validates this structure at load
  (`EligibilitySchemaError` / `EligibilityValueError`) before trusting any row,
  because the loader binds columns positionally.

## Failure modes

**Geocoder (0.4.0 splits the old single `None` return into four distinct
outcomes).** `geocode_address` / `check_address` now behave as follows
(all verified this session against the installed wheel):

- **Transport / HTTP-status / decode failure** (403, 5xx, timeout,
  connection/DNS, non-JSON body), after retries are exhausted → **raises
  `GeocoderTransportError`**. The message names the failure kind and the address.
  Report it verbatim and stop.
- **Address matches multiple tracts that disagree** → **raises
  `AmbiguousAddressError`**, naming the candidate tracts; it refuses to silently
  take the first match. Report it and stop — do not pick one.
- **Genuine no-match** (HTTP 200, zero address matches) → **returns `None`**.
  This is the *only* thing `None` means now. It is the third state, not a NO:
  report "address could not be geocoded" / `eligibility_status='geocode-failed'`
  — do not fall back to a ZIP-code or city-level guess.
- **Matches that all agree on the same tract** → proceeds normally, returning
  that tract.

  Both `GeocoderTransportError` and `AmbiguousAddressError` subclass
  `GeocoderError`, which subclasses `NMTCMapperError` (verified by reflection
  this session) — so `except NMTCMapperError` catches every error the package
  raises. Source: `nmtcmapper/exceptions.py`, `nmtcmapper/geocoder/census.py`.

**Tract absent from the table** (`check_tract` on a GEOID not in the ~85k
universe): **not a failure** — it is the third state. Returns
`nmtc_eligible=None`, `distress_level="unknown"`, `tract_found=False`,
`eligibility_status="not-found"`. Report "could not be determined," never
"ineligible." (See the third-state rule and its worked example.)

**CDFI Fund file download fails / 404** (URL moved): raises
`EligibilityDownloadError` / `EligibilityParseError`. Report the error and that
eligibility could not be determined. Do not answer from memory.

**NaN demographic fields** (a real tract with no measurable population, e.g.
`11001980000`): report "not available," never fabricate. This is orthogonal to
the tri-state verdict — the tract is genuinely `False`/verified-ineligible; only
its demographics are null.

**Screener `lic_status` misuse**: passing `"yes"` without confirming LIC status
produces a falsely high score. Confirm first; pass `"unknown"` when the mapper
returned the third state.

## Caveats

- This is an **eligibility and feasibility screening layer**, not an allocation
  award, legal opinion, or the CDFI Fund's determination.
- Eligibility is **tract-specific and vintage-specific**. An "eligible" answer is
  only valid for the table vintage named above.
- An **"unknown" answer is a real answer** — "could not be determined for this
  tract/address," never "not eligible."
- The screener's score and estimated allocation are **first-pass heuristics** to
  triage deals, not underwriting or a commitment.
