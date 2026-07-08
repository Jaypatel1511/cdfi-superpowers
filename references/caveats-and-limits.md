# Caveats and Limits

What this plugin, and the portfolio behind it, deliberately does **not** do. These
are design boundaries, not missing features — do not route around them.

## 1. No inferential fair-lending analysis (in this plugin)

The hmda-analysis skill is **descriptive only**: counts, distributions, and the
CRA-**proxy** transform. It does **not** perform disparate-impact analysis,
disparity ratios, protected-class stratified denial/approval analysis,
statistical significance testing, or any "fair lending" inference.

`hmda-analyzer` the package *does* ship disparity functions
(`disparity_ratio`, `denial_rate_by_race`, `denial_reasons_by_race`,
`generate_disparity_report`, and `summary_table` — whose output is a
disparity-by-race table). The `fair-lending-screener` package (v0.2.1) exists for
statistical disparate-impact analysis. **Neither is wrapped by any skill in this
plugin's v1**, by design. If a user wants inferential fair-lending work, the AI
declines and explains the descriptive/inferential distinction — it does not
present a fair-lending tool as the "alternative."

Why: inferential disparity claims are court-adjacent and require
court-defensible methodology, protected-class handling, and significance
testing. Getting that wrong — or letting an AI narrate a disparity conclusion off
a descriptive table — is a real harm. The firewall keeps the descriptive layer
descriptive.

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
