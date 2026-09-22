# Caveats and Limits

What this plugin, and the portfolio behind it, deliberately does **not** do. These
are design boundaries, not missing features — do not route around them.

## 1. No inferential fair-lending analysis from the descriptive skill — and no fair-lending *findings* from any skill

The hmda-analysis skill is **descriptive only**: counts, distributions, and the
CRA-**proxy** transform. It does **not** perform disparity ratios,
protected-class stratified denial/approval analysis, statistical significance
testing, or any "fair lending" inference.

`hmda-analyzer` the package *does* ship disparity functions
(`disparity_ratio`, `denial_rate_by_race`, `denial_reasons_by_race`,
`denial_rate_by_income_band`, `generate_disparity_report`, `summary_table` —
whose output is a disparity-by-race table — and `racial_composition_by_tract`).
Re-checked against 0.6.0's 33 exports; the list is complete. **hmda-analysis
does not wrap them**, by design, and never will: a disparity number narrated off
a descriptive table, with no controls and no significance test, is the harm the
firewall exists to prevent.

Since 2026.9.3 the plugin **does** offer inferential work — through the
separate `fair-lending-screening` skill, which wraps `fair-lending-screener`
(>=0.2.2). That skill is the other side of the firewall, and it carries its own
boundaries, which are the reason it can be offered at all:

- it produces a **screening signal** — an adjusted odds ratio with a 95% CI
  and p-value — and every result, in the package's own report text, states that
  it "does not constitute a finding of discrimination under ECOA or the Fair
  Housing Act";
- the package is **alpha-status**, its methodology not yet externally
  reviewed, and (as of 0.2.2) it describes itself as *informed by* the FFIEC
  risk-factor framework, **not** as examiner methodology and **not** as
  disparate-impact analysis;
- the adjusted odds ratio is an **upper bound** — public HMDA has no credit
  score or AUS result, and omitting them biases the coefficient upward;
- it compares **race groups only** (`derived_race`); ethnicity, sex and age are
  out of scope in 0.2.2;
- typed errors (`InsufficientDataError`, `ModelConvergenceError`, …) are
  surfaced verbatim, never smoothed into a partial result.

If a user asks hmda-analysis for inferential work, the AI routes to
fair-lending-screening and its guardrails. If a user asks fair-lending-screening
for a *finding* — proof of discrimination, a verdict on a named lender, a
dropped caveat — the AI declines: that is outside what public-data logistic
regression can show, and the package's own report withholds the lender name
whenever the result is non-significant, non-converged, or has pseudo-R² below
0.05.

Why: inferential disparity claims are court-adjacent. The 2026.9.3 design keeps
the descriptive layer descriptive and confines inference to a skill whose
package states its own limits on every page it renders.

## 2. No CRA performance ratings

The CRA-proxy distribution is a **proxy**, never a CRA rating, grade, metric, or
performance evaluation. Specifically it is:

- **not assessment-area-bound** (HMDA has no assessment-area concept; the proxy
  spans all HMDA lending in the requested geography — a different population than
  any CRA exam evaluates — the largest single gap);
- **mortgage-only** (CRA lending tests also cover small-business, small-farm, and
  community-development lending, invisible to HMDA);
- computed on a **reporter population ≠ CRA-covered institutions**;
- **without a comparator** — distribution only; not interpretable as CRA
  performance.

The official CRA exam ratings come from `cra-scraper` (which is residential-only,
see data-source-map.md), never derived from the proxy.

## 3. No credit-union / loan-fund benchmarking

cdfi-peer-benchmark covers **FDIC-insured bank CDFIs and MDIs only** (FDIC
BankFind). Credit unions / CDCUs (NCUA-regulated) and unregulated CDFI loan funds
have no call-report data in this source and are out of scope. Do not force them
through the benchmark.

## 4. No pre-2018 (CIIS-era) HMDA / TLR

The HMDA loaders target the canonical **2018+** LAR column schema. Pre-2018
HMDA and CIIS-era Transaction Level Report (TLR) data are out of scope for the
hmda-analysis skill. (Separately, `cdfidata` handles CDFI Fund TLR/CLR/Awards
ETL — a different dataset from HMDA LAR.)

## 5. Eligibility and benchmarks are lookups/estimates, not determinations

- NMTC eligibility is a **tract-level, vintage-specific lookup** against the CDFI
  Fund table (2016–2020 vintage in force this session) — not an allocation
  award or legal opinion.
- The NMTC feasibility screener produces a **first-pass heuristic score**, not
  underwriting.
- Peer benchmarks reflect **FDIC-reported** call-report data and heuristic peer
  groups, not an independent audit.

## 6. The fabrication firewall (portfolio-wide)

Across the wrapped packages, a missing/uncomputable value is **surfaced as
NaN/None/N-A and never imputed** into a plausible number. The AI must render N/A
where the package returns N/A, report the excluded-count/exclusion-reason tallies
so denominators reconcile, and report typed errors rather than smoothing them
over. Fabricating a tract eligibility, a capital ratio, or an income-band share
is the cardinal failure these tools are built to prevent.
