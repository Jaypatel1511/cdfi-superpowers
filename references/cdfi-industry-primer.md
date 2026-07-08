# CDFI Industry Primer

A plain-language orientation to community development finance — enough context to
use the skills in this plugin correctly. Roughly two pages.

## What a CDFI is

A **Community Development Financial Institution (CDFI)** is a mission-driven
lender that channels capital into low-income and underserved communities that
mainstream finance often skips. CDFIs come in four main forms: **banks** (and
bank holding companies), **credit unions**, **loan funds**, and **venture
capital funds**. They are certified by the **CDFI Fund**, part of the U.S.
Treasury.

Why the form matters for this plugin: only **bank CDFIs** file FDIC call reports,
so the peer-benchmark skill covers banks only. Credit unions (NCUA-regulated) and
loan funds (largely unregulated) don't have comparable public financial data in
that source.

## Key actors

- **CDFI Fund** — the Treasury body that certifies CDFIs and administers the
  award/allocation programs below. It publishes eligibility tables and award
  data (some of which move URLs, which is why lookups can fail).
- **CDE (Community Development Entity)** — the intermediary that receives an NMTC
  allocation and deploys it into projects. A CDFI is often also a CDE.
- **QALICB (Qualified Active Low-Income Community Business)** — the operating
  business or project that ultimately receives NMTC-subsidized capital.
- **QEI (Qualified Equity Investment)** — the investment a tax-credit investor
  makes into a CDE; the NMTC is calculated as a percentage of the QEI.
- **QLICI (Qualified Low-Income Community Investment)** — the loan/investment the
  CDE makes from QEI proceeds into the QALICB.

## Programs you'll encounter

### NMTC — New Markets Tax Credit
A federal credit (39% of the QEI, claimed over 7 years) that draws private
capital into businesses and real estate in **Low-Income Communities (LICs)**.
Eligibility is a **census-tract** determination: a tract qualifies by poverty
rate / area-median-income thresholds, with extra "distress" tiers (**severe** and
**deep** distress) that unlock stronger investment commitments. This is exactly
what the **nmtc-eligibility** skill checks — geocode an address to a tract, look
the tract up in the CDFI Fund's LIC eligibility table, and (optionally) score a
project's feasibility.

### LIHTC — Low-Income Housing Tax Credit
The primary federal subsidy for affordable **rental housing**, delivered as a
**4%** or **9%** credit on qualified basis over a 15-year compliance period.
(Portfolio package: `lihtc-calc`.)

### CRA — Community Reinvestment Act
A 1977 law requiring banks to serve the credit needs of their **assessment
areas**, including LMI neighborhoods. Regulators grade banks (Outstanding /
Satisfactory / Needs to Improve / Substantial Noncompliance) via periodic exams.
Crucial distinction for this plugin: a CRA **rating** is the official regulatory
output (retrieved by `cra-scraper`); the **CRA-proxy** distribution in the
hmda-analysis skill is *not* a CRA metric — it approximates one dimension a CRA
exam looks at, using HMDA data, with heavy caveats.

### HMDA — Home Mortgage Disclosure Act
Requires most mortgage lenders to report application-level records (the **LAR** —
Loan/Application Register): who applied, loan terms, action taken, geography, and
borrower characteristics. It is the richest public window into mortgage lending.
The **hmda-analysis** skill pulls LAR data (2018+ schema) and produces
**descriptive** cuts — never inferential fair-lending conclusions.

### BEA — Bank Enterprise Award
A CDFI Fund program that rewards FDIC-insured banks for increasing their
investment in CDFIs and in distressed communities. (Tracked by
`cdfi-fund-tracker`.)

### CMF — Capital Magnet Fund
A CDFI Fund competitive grant program that provides capital to CDFIs and
nonprofit housing developers to finance affordable housing and related economic
development, with a required leverage of other investment.

## How the pieces fit together

A typical NMTC deal: an **investor** makes a **QEI** into a **CDE** (often a
**CDFI**); the CDE makes a **QLICI** loan/investment into a **QALICB** located in
an NMTC-eligible **LIC census tract**; the investor claims the **NMTC** over
seven years. Separately, **CRA** obligations motivate banks to lend and invest in
LMI areas, and **HMDA** data lets analysts and advocates *describe* mortgage
lending patterns in those areas. This plugin gives an AI grounded tools for the
eligibility, benchmarking, and descriptive-data steps — and firm boundaries where
inference, ratings, and legal determinations begin.
