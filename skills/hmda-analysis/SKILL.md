---
name: hmda-analysis
description: >-
  Pull and describe HMDA mortgage-lending data (LAR records) for a county,
  state, lender (LEI), or multiple years, and compute a CRA-PROXY borrower- and
  tract-income distribution. Use when the user says "pull HMDA data", "LAR
  records", "mortgage lending data for [county/state/lender]", or "multi-year
  HMDA". DESCRIPTIVE ONLY — this skill does not do disparity, disparate-impact,
  or fair-lending analysis. Backed by the audited PyPI package hmda-analyzer.
---

# HMDA Analysis (descriptive)

Pulls HMDA LAR data from the CFPB API and produces **descriptive** cuts —
lending by county/state/tract, top lenders, and a **CRA-proxy income
distribution** — via the published, audited **hmda-analyzer** package.

## FIREWALL — read before anything else (non-negotiable)

**This skill is DESCRIPTIVE ONLY.** It does not perform, and the AI must not
produce using it:

- disparate-impact or disparity-ratio analysis
- protected-class (race/ethnicity/sex) stratified denial or approval analysis
- any "fair lending" screening, inference, statistical significance, or
  disparity claim
- any interpretation of the CRA-proxy output as CRA performance, a CRA rating,
  or an assessment-area result

**If the user asks for inferential fair-lending analysis, decline and explain
the descriptive/inferential distinction:** this skill counts and distributes
what was lent (descriptive); disparity/disparate-impact analysis draws
inferential conclusions about *why* and *whether lending is discriminatory*,
which requires court-defensible methodology, protected-class stratification, and
significance testing that this skill deliberately does not do. Do **not** point
the user to any fair-lending tool as the "v1 alternative" — just hold the line
on the distinction.

The installed `hmda-analyzer` package *does* expose disparity functions
(`disparity_ratio`, `denial_rate_by_race`, `denial_reasons_by_race`,
`generate_disparity_report`, and `summary_table`, whose output is a
disparity-by-race table). **This skill does not wrap them.** Treat them as out
of scope; if the user wants them, that is the inferential territory above.

## When to use

- "Pull 2023 HMDA LAR records for Rhode Island."
- "Show mortgage lending by county for this state."
- "Multi-year HMDA for county 17031, 2020–2023."
- "What's the CRA-proxy borrower-income distribution for this pull?"

## When NOT to use

- Any request in the FIREWALL list above (disparity / fair lending / CRA
  performance).
- Pre-2018 HMDA / CIIS-era TLR — the loaders target the canonical **2018+**
  column schema.

## Install

```
pip install hmda-analyzer
```

Verified this session: **hmda-analyzer 0.5.0** (PyPI).

**Dual import aliases** — both resolve to the same package (verified this
session, both report v0.5.0):

```python
import hmda_analyzer as h     # underscore alias
import hmdaanalyzer as h      # no-underscore alias — equivalent
```

## Loading data

- `load_from_api(year=2023, state=None, lei=None, county=None, limit=10000)` —
  single-year pull from the CFPB API.
- `load_range(start_year, end_year, state=None, lei=None, county=None,
  limit=10000)` — inclusive multi-year pull; adds an `activity_year` provenance
  column.
- `load_sample(n=5000, seed=42)` — offline synthetic sample (note: the sample
  frame does **not** carry the FFIEC income columns, so `cra_proxy_distribution`
  cannot run on it — use a real pull for the proxy).

**`load_range` fail-loud contract (verbatim from the package docstring):**

> * **Fail-loud, no partial.** If ANY year's fetch raises, `load_range`
>   re-raises immediately with the failing year named and returns NO frame —
>   there is no catch-and-continue and no partial result.
> * **Schema guard.** Every fetched year is validated against the canonical
>   2018+ column set; a missing or unexpected column raises
>   `SchemaValidationError` (naming the year).
> * **Provenance.** The native `activity_year` field is used and asserted to
>   match the requested year; a wrong-year payload raises
>   `ActivityYearMismatchError`.
> * **Legitimate empty.** A valid year that simply matches zero rows is NOT an
>   error — its correctly-columned empty frame participates in the concat.

So: **never report a partial multi-year result.** If `load_range` raises, name
the failing year and report the error — do not present the years that happened
to succeed.

## Worked example — descriptive lending cut (executed)

```python
import hmda_analyzer as h
df = h.load_sample()                 # 5000 rows, offline
lc = h.lending_by_county(df)
print(lc.head(5).to_string(index=False))
```

Actual output this session:

```
county_code  applications  denials  originations  total_loan_volume  avg_loan_amount  denial_rate state_code
      26067             8        0             8            2976002    372000.250000          0.0         26
      42066             8        1             7            3317790    414723.750000        0.125         42
      37076             8        0             8            1497582    187197.750000          0.0         37
      12143             8        0             8            2715158    339394.750000          0.0         12
      06001             7        1             6            2661144    380163.428571     0.142857         06
```

Descriptive functions this skill wraps: `lending_by_county`, `lending_by_state`,
`lending_by_tract`, `top_lenders_by_volume`, `lender_summary`, `lender_vs_market`,
`lending_desert_score`, and `cra_proxy_distribution`. (`summary_table` is **not**
wrapped — its output is a disparity-by-race table, which is firewalled.)

## Worked example — CRA-proxy distribution (executed, LIVE data)

`cra_proxy_distribution(df, by="borrower"|"tract"|"both", include_purchased=False,
year_column="activity_year")` — a pure descriptive transform on a frame from
`load_from_api`/`load_range`. No fetch, no network.

Print the caveat (`r.caveat` — the `STANDARD_CRA_PROXY_CAVEAT` constant plus the
standing no-comparator line) **beneath each table**, so no single extracted
table is ever caveat-free:

```python
import hmda_analyzer as h
df = h.load_from_api(year=2023, state="RI", limit=2000)   # live CFPB pull
r = h.cra_proxy_distribution(df, by="both")
for t in r.tables:
    print(f"--- dimension={t.dimension} universe={t.universe} year={t.year} ---")
    print(t.distribution.to_string(index=False))
    print("classified_denominator:", t.classified_denominator, "  excluded:", t.excluded)
    print(r.caveat)          # STANDARD_CRA_PROXY_CAVEAT + no-comparator line — under EVERY table
    print()
```

Actual output this session (2,000 RI LAR records → 976 originations). The caveat
text under each table is copied verbatim from `r.caveat`:

```
--- dimension=borrower universe=originated year=None ---
category  count  cra_proxy_share
     Low     57         0.060897
Moderate    196         0.209402
  Middle    291         0.310897
   Upper    392         0.418803
classified_denominator: 936   excluded: {'na_income': 40}
CRA-proxy distribution estimate — NOT a CRA metric, rating, grade, or performance evaluation. Not assessment-area-bound: HMDA has no assessment-area concept, so this proxy spans all HMDA lending in the requested geography — a different population than any CRA exam evaluates. Mortgage-only: CRA lending tests also cover small-business, small-farm, and community-development lending, invisible to HMDA. Reporter population != CRA-covered institutions.
Distribution only; no comparator — not interpretable as CRA performance.

--- dimension=tract universe=originated year=None ---
category  count  cra_proxy_share
     Low     45         0.046680
Moderate    137         0.142116
  Middle    464         0.481328
   Upper    318         0.329876
classified_denominator: 964   excluded: {'unknown_tract': 12}
CRA-proxy distribution estimate — NOT a CRA metric, rating, grade, or performance evaluation. Not assessment-area-bound: HMDA has no assessment-area concept, so this proxy spans all HMDA lending in the requested geography — a different population than any CRA exam evaluates. Mortgage-only: CRA lending tests also cover small-business, small-farm, and community-development lending, invisible to HMDA. Reporter population != CRA-covered institutions.
Distribution only; no comparator — not interpretable as CRA performance.
```

## Rendering the CRA-proxy output — mandatory

1. **Attach `STANDARD_CRA_PROXY_CAVEAT` verbatim to every rendered table**, plus
   the **no-comparator line** — "*Distribution only; no comparator — not
   interpretable as CRA performance.*" — on every table. Both live in
   `r.caveat`; copy them, do not paraphrase.
2. Never present a CRA-proxy share as a CRA metric, rating, grade, or
   performance figure. The word "CRA" never appears in output without "proxy"
   adjacent.
3. **Reconcile the denominator every time.** Report the classified denominator
   and the excluded counts so totals reconcile:
   borrower `936 + 40 = 976`; tract `964 + 12 = 976`. If they don't reconcile,
   something is wrong — say so.
4. Warn against **differencing** the borrower-LMI% and tract-LMI% — they are
   computed on different populations.

### Exclusion-reason vocabulary (verified in source)

Every excluded row carries one of these reasons; surface them so the AI's
denominators reconcile the same way the package's do:

| reason | meaning |
|---|---|
| `na_income` | borrower `income` is NA/blank — excluded, never imputed |
| `missing_area_median` | `ffiec_msa_md_median_family_income` is 0/blank/NA — never divide |
| `out_of_range_income` | computed borrower MFI% out of accepted range |
| `unknown_tract` | tract income % is the Unknown sentinel (0/blank/NA) |
| `out_of_range_tract_pct` | tract income % negative, non-finite, or above ceiling |
| `unknown_year` | (multi-year) row has missing/NA `activity_year` |

A missing input is **excluded and surfaced**, never imputed into an income band
and never fabricated as a plausible default.

## Bundled methodology

`h.get_methodology_path()` returns the path to the bundled
`cra_proxy_methodology.md` (verified present this session). When any CRA-proxy
caveat wording is in question, quote that file — it travels with the installed
wheel and is the authoritative source for the firewall and limitations.

## Data source & typed errors

- Source: the **CFPB HMDA API** (`ffiec.cfpb.gov` / CFPB HMDA endpoints) — no
  cloud WAF; verified reachable this session (200 records, 101 columns, both
  FFIEC income fields present).
- Typed errors: `CFPBAPIError` (API failure), `SchemaValidationError`,
  `ActivityYearMismatchError`, `MissingColumnError` (a required column for the
  requested cut is absent — verified: `cra_proxy_distribution` on the FFIEC-less
  sample raises `MissingColumnError`). Report these; do not smooth them over.

## Failure modes

- **`load_range` partial failure** → the whole call raises with the failing year
  named; report the error, never the surviving years.
- **`cra_proxy_distribution` on a frame missing FFIEC columns** →
  `MissingColumnError`. Use a real `load_from_api`/`load_range` frame, not
  `load_sample`.
- **User asks for disparity / fair lending / CRA performance** → decline per the
  FIREWALL.
- **CFPB API down** → `CFPBAPIError`; report it.

## Caveats

- HMDA is **2018+** schema here; earlier data is out of scope.
- The CRA-proxy is a **proxy**, not a CRA metric: not assessment-area-bound,
  mortgage-only, reporter-population ≠ CRA-covered institutions, no comparator.
  See the verbatim `STANDARD_CRA_PROXY_CAVEAT` above.
- HMDA `income` is lender-relied-upon (often combined co-applicant) income — an
  imperfect, likely upward-biased proxy for borrower income (tends to understate
  LMI borrower share).
