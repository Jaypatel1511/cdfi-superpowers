# Package Index

Jay Patel's published CDFI portfolio on PyPI (user `Jaypatel1511`). Every version
below was verified against a live PyPI JSON check **this session**; every import
name was read from the installed wheel's `top_level.txt` this session.

**Naming is not uniform — dist (PyPI) ≠ repo (GitHub) ≠ import (Python).** The
one mismatch between dist and repo is `cdfidata` (repo `cdfi-data`); the frequent
mismatch is dist vs. import (hyphen/underscore collapse). Do not assume.

| dist (PyPI) | repo (GitHub) | import | version | purpose |
|---|---|---|---|---|
| nmtc-mapper | nmtc-mapper | `nmtcmapper` | 0.3.3 | Automated NMTC eligibility checker — geocode addresses and check Low-Income Community status using CDFI Fund + Census data. **(wrapped: nmtc-eligibility)** |
| nmtc-screener | nmtc-screener | `nmtc_screener` | 0.1.0 | CLI tool for NMTC feasibility screening. **(wrapped: nmtc-eligibility)** |
| cdfi-benchmark | cdfi-benchmark | `cdfibenchmark` | 0.2.0 | CDFI/MDI peer benchmarking from FDIC call-report data — NIM, efficiency ratio, ROAA, capital, and more. **(wrapped: cdfi-peer-benchmark)** |
| hmda-analyzer | hmda-analyzer | `hmda_analyzer`, `hmdaanalyzer` | 0.5.0 | HMDA mortgage-lending analyzer — denial rates, disparities, lending deserts, lender benchmarking; carries the descriptive CRA-proxy transform. **(wrapped: hmda-analysis, descriptive subset only)** |
| nmtc-calc | nmtc-calc | `nmtccalc` | 0.2.1 | Calculator for NMTC leveraged transactions. |
| nmtc-application-builder | nmtc-application-builder | `nmtcapp` | 1.1.4 | Flagship NMTC application intelligence platform — pipeline analysis, eligibility validation, readiness scoring, visualization for CDEs. |
| cdfidata | cdfi-data | `cdfidata` | 0.4.0 | ETL pipeline for U.S. Treasury CDFI Fund public datasets — TLR, CLR, and Awards data. |
| cdfi-fund-tracker | cdfi-fund-tracker | `cdfifund` | 0.1.0 | CDFI Fund award tracker — CDFI Program, BEA, NACA, Native American, and Bond Guarantee awards with compliance status. |
| cdfi-loan-pricing | cdfi-loan-pricing | `cdfipricing` | 0.1.0 | CDFI loan pricing model — cost of capital, target ROAA, expected loss, admin cost → minimum viable loan rate. |
| cdfi-stress-tester | cdfi-stress-tester | `cdfistress` | 0.1.0 | CDFI portfolio stress-testing engine — Monte Carlo with correlated NOI, rate, and property-value shocks. |
| cdfi-val | cdfi-val | `cdfival` | 0.1.0 | Valuation toolkit for CDFIs and Minority Depository Institutions. |
| dscr-tools | dscr-tools | `dscrtools` | 0.2.0 | Loan amortization, DSCR tracking, covenant monitoring, and loan sizing. |
| waterfall-py | waterfall-py | `waterfall` | 0.1.0 | Debt waterfall engine for structured finance — senior/mezz/equity tranches. |
| lihtc-calc | lihtc-calc | `lihtccalc` | 0.1.0 | LIHTC transaction calculator — qualified basis, applicable fraction, 4%/9% credit, 15-year compliance, recapture, investor IRR. |
| oz-tracker | oz-tracker | `oztracker` | 0.1.0 | Opportunity Zone tracker — OZ 1.0/2.0 eligibility, QOF tax benefits, rural QORF, portfolio tracking. |
| sbic-tracker | sbic-tracker | `sbictracker` | 0.1.0 | SBIC portfolio analyzer — fund-level IRR/TVPI/DPI, licensee tracking, SBA program data. |
| bond-issuer-screener | bond-issuer-screener | `bondscreener` | 0.1.0 | CDFI Bond Guarantee Program eligibility screener — net asset, lending-volume, portfolio-quality thresholds, issuance feasibility. |
| credit-memo | credit-memo | `creditmemo` | 0.1.0 | Generate IC credit memos from structured deal inputs — CDFI loans, NMTC deals, impact investments. |
| impact-ledger | impact-ledger | `impactledger` | 0.2.1 | Impact-investment portfolio tracker for CDFIs, private debt, and community development finance. |
| fair-lending-screener | fair-lending-screener | `fair_lending_screener`, `fairlendingscreener` | 0.2.1 | Statistical disparate-impact analysis for HMDA data — examiner methodology, open-sourced. **Inferential fair-lending; deliberately NOT wrapped by any skill in this plugin (see caveats-and-limits.md).** |
| cra-scraper | cra-scraper | `crascraper` | 0.1.1 | CRA exam ratings scraper/analyzer — search FFIEC database, parse Performance Evaluations. **Residential-only (Cloudflare blocks all cloud/datacenter IPs — unfixable by headers); no skill wraps it.** |

**21 packages** verified this session.

## Note on the count

The build brief referenced "22 packages"; empirical enumeration found **21**
PyPI distributions owned by `Jaypatel1511`. Discovery method: the PyPI profile
page is behind a Cloudflare "Client Challenge" and could not be scraped, so the
set was reconstructed from the GitHub account (27 repos: 21 CDFI package repos +
`cdfi-superpowers` + two forks `pandas-datareader`/`yfinance` + three
profile/pages repos), each candidate resolved against the live PyPI JSON, and
each resolved dist's ownership confirmed via its `Jaypatel1511` GitHub homepage.
The 21st package publishes under a dist name (`cdfidata`) that differs from its
repo name (`cdfi-data`). **The 22nd could not be located empirically** (no
matching GitHub repo, no guessable PyPI name); it is flagged here rather than
invented. `nmtc-screener`'s PyPI metadata is bare (no author/URL) — ownership is
inferred from its GitHub repo and an exactly-matching summary string.
