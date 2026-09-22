# Package Index

Jay Patel's published portfolio on PyPI (user `thejaypatel1511`). Import names
were read from the installed wheel's `top_level.txt` **in the session that first
wrote this table** and have not been re-read since — treat an import name as a
hypothesis and check it against the installed wheel.

**Every version in this table is machine-checked against live PyPI** by
`scripts/check_package_versions.py`, which CI runs on every push, on every pull
request, and again each morning; a row that disagrees fails the run. The gate
exists because this table was, before it, wrong on **ten of twenty-two rows** —
and three of those pointed at releases that had been **yanked for presenting
fabricated or sample data as federal data**, presented here as current. An agent
reading this file would have installed them.

**A version below is the current non-yanked release** unless the cell shows a
`>=` floor, which is a deliberate install floor and is allowed to lag (the skills
say why; see `README.md`). Where a package has a withdrawn release the row says
so — **do not pin a yanked version**: `pip` installs one without complaint if you
name it exactly.

**Naming is not uniform — dist (PyPI) ≠ repo (GitHub) ≠ import (Python).** The
one mismatch between dist and repo is `cdfidata` (repo `cdfi-data`); the frequent
mismatch is dist vs. import (hyphen/underscore collapse). Do not assume.

| dist (PyPI) | repo (GitHub) | import | version | purpose |
|---|---|---|---|---|
| nmtc-mapper | nmtc-mapper | `nmtcmapper` | >=0.6.1 | Automated NMTC eligibility checker — geocode addresses and check Low-Income Community status using CDFI Fund + Census data. **(wrapped: nmtc-eligibility)** |
| nmtc-screener | nmtc-screener | `nmtc_screener` | 0.1.0 | CLI tool for NMTC feasibility screening. **(wrapped: nmtc-eligibility)** |
| cdfi-benchmark | cdfi-benchmark | `cdfibenchmark` | 0.3.2 | CDFI/MDI peer benchmarking from FDIC call-report data — NIM, efficiency ratio, ROAA, capital, and more. **(wrapped: cdfi-peer-benchmark)** |
| hmda-analyzer | hmda-analyzer | `hmda_analyzer`, `hmdaanalyzer` | >=0.6.0 (pin resolves 0.6.1, py>=3.9; 0.6.0 itself is py>=3.11) | HMDA mortgage-lending analyzer — denial rates, disparities, lending deserts, lender benchmarking; carries the descriptive CRA-proxy transform and the geography-vintage refusal. **(wrapped: hmda-analysis, descriptive subset only)** |
| nmtc-calc | nmtc-calc | `nmtccalc` | 0.2.1 | Calculator for NMTC leveraged transactions. |
| nmtc-application-builder | nmtc-application-builder | `nmtcapp` | 1.7.1 | Flagship NMTC application intelligence platform — pipeline analysis, eligibility validation, readiness scoring, visualization for CDEs. The fastest-moving package here (28 releases); this row is the one most likely to be behind between CI runs. |
| cdfidata | cdfi-data | `cdfidata` | 0.4.0 | ETL pipeline for U.S. Treasury CDFI Fund public datasets — TLR, CLR, and Awards data. |
| cdfi-fund-tracker | cdfi-fund-tracker | `cdfifund` | 0.2.0 | CDFI Fund award tracker — CDFI Program, BEA, NACA, Native American, RAPID, CMF, and Bond Guarantee awards. **Bring your own data: no CDFI Fund ingestion path is implemented and the bundled sample is synthetic.** ⚠️ **0.1.0 is yanked** — it returned that synthetic sample as CDFI Fund data on HTTP success; 0.2.0 raises `CDFIFundDownloadError` instead. |
| cdfi-loan-pricing | cdfi-loan-pricing | `cdfipricing` | 0.2.0 | CDFI loan pricing model — cost of capital, target ROAA, expected loss, admin cost → minimum viable loan rate. |
| cdfi-stress-tester | cdfi-stress-tester | `cdfistress` | 0.2.0 | CDFI portfolio stress-testing engine — Monte Carlo with correlated NOI, rate, and property-value shocks. |
| cdfi-val | cdfi-val | `cdfival` | 0.1.0 | Valuation toolkit for CDFIs and Minority Depository Institutions. |
| dscr-tools | dscr-tools | `dscrtools` | 0.2.0 | Loan amortization, DSCR tracking, covenant monitoring, and loan sizing. |
| waterfall-py | waterfall-py | `waterfall` | 0.2.0 | Debt waterfall engine for structured finance — senior/mezz/equity tranches. |
| lihtc-calc | lihtc-calc | `lihtccalc` | 0.1.0 | LIHTC transaction calculator — qualified basis, applicable fraction, 4%/9% credit, 15-year compliance, recapture, investor IRR. |
| oz-tracker | oz-tracker | `oztracker` | 0.2.0 | Opportunity Zone tracker — QOF tax benefits, rural QORF, portfolio tracking. **OZ tract lookup is non-functional in 0.2.0**: both upstream sources answer 404, so it raises a typed error rather than guessing. The QOF modeling works. ⚠️ **0.1.0 is yanked** — it answered a confident `False` for 99.91% of designated OZ tracts via a silent sample fallback. |
| sbic-tracker | sbic-tracker | `sbictracker` | 0.2.0 | SBIC portfolio analyzer — fund-level IRR/TVPI/DPI and licensee modeling. **Unmaintained, per its own PyPI summary; live SBA data loading is not implemented** and sample data is returned only when explicitly asked for. ⚠️ **0.1.0 is yanked** — it returned fabricated sample data as live SBA program data. |
| bond-issuer-screener | bond-issuer-screener | `bondscreener` | 0.1.0 | CDFI Bond Guarantee Program eligibility screener — net asset, lending-volume, portfolio-quality thresholds, issuance feasibility. |
| credit-memo | credit-memo | `creditmemo` | 0.2.2 | Generate IC credit memos from structured deal inputs — CDFI loans, NMTC deals, impact investments. **(wrapped: credit-memo)** |
| impact-ledger | impact-ledger | `impactledger` | 0.2.1 | Impact-investment portfolio tracker for CDFIs, private debt, and community development finance. |
| fair-lending-screener | fair-lending-screener | `fair_lending_screener`, `fairlendingscreener` | 0.2.2 | Adjusted denial-disparity screening on public HMDA data — logistic regression with FFIEC-standard controls, open-sourced (0.2.2 relabeled it from "disparate-impact / examiner methodology" to lending-disparity screening *informed by* FFIEC). Inferential, alpha-status; screening signal, not a finding. **(wrapped: fair-lending-screening)** ⚠️ **0.1.1 is yanked** — release-process drift shipped a breaking API change in a patch release; superseded by 0.2.0. |
| cra-scraper | cra-scraper | `crascraper` | 0.1.1 | CRA exam ratings scraper/analyzer — search FFIEC database, parse Performance Evaluations. **Residential-only (Cloudflare blocks all cloud/datacenter IPs — unfixable by headers); no skill wraps it.** |
| h1b-tracker | **none reachable** | `h1btracker` | 0.1.0 | Analyze DOL H1B LCA disclosure data — rank employers by filing volume, salary, and sponsorship reliability. **Published on PyPI at 0.1.0 (one release, not yanked), but its PyPI `Homepage` — `github.com/Jaypatel1511/h1b-tracker` — does not resolve anonymously** (`git ls-remote` exits 128 where every other row's repo succeeds). Private or deleted; this session could not tell which. No source to read. |

**22 packages.** The count was established in the session that first wrote this
table. Every **version** cell above is re-derived from live PyPI on each CI run
(`scripts/check_package_versions.py`); the **repo**, **import** and **purpose**
cells are not, and remain hand-maintained.

Note that `docs/index.html` carries only **21** package cards — `h1b-tracker` has
never had one. The landing page is therefore not a substitute for this table.

## Note on the count

The build brief referenced "22 packages"; empirical enumeration confirms **22**
PyPI distributions owned by the PyPI user `thejaypatel1511` (GitHub owner
`Jaypatel1511`). Discovery method: the PyPI profile page is behind a Cloudflare
"Client Challenge" and could not be scraped, so the set was reconstructed from
the GitHub account and each candidate resolved against the live PyPI JSON, with
ownership confirmed via each dist's `Jaypatel1511` GitHub homepage. The initial
GitHub reconstruction thematically filtered on CDFI-named repos and so dropped
**h1b-tracker** — a portfolio package that is real and published but not
CDFI-named; adding it back reconciles the count to 22. One dist publishes under a
name (`cdfidata`) that differs from its repo name (`cdfi-data`).
`nmtc-screener`'s PyPI metadata is bare (no author/URL) — its ownership is
inferred from its GitHub repo and an exactly-matching summary string.

**Ownership evidence has since weakened for one row.** `h1b-tracker`'s GitHub
homepage, the evidence that placed it in this portfolio, no longer resolves
anonymously (checked 2026-09-21). The dist is still live on PyPI at 0.1.0 and
still declares that URL, so the row stays — but its ownership now rests on the
declared homepage and the original session's reading, not on a repo anyone can
open today.
