# Data Source Map

Which upstream host backs which capability, whether it is reachable from
cloud/datacenter IPs, and the User-Agent convention. Hosts and UA strings below
were read from the installed package source **this session**; reachability marked
"verified" was exercised live this session.

| Host | Backs | Used by | Cloud-reachable? |
|---|---|---|---|
| `ffiec.cfpb.gov` | CFPB HMDA API (LAR records) | hmda-analyzer | **Yes — verified** (2,000 RI records pulled) |
| `api.fdic.gov/banks` | FDIC BankFind (institutions, call reports) | cdfi-benchmark | Not re-verified — blocked by the egress allowlist of the session that last updated this row. The former `banks.data.fdic.gov/api` host now answers HTTP 301 to this one; cdfi-benchmark 0.3.0 moved to the canonical host and keeps the old one only as `FDIC_API_BASE_LEGACY`. |
| `geocoding.geo.census.gov` | Census geocoder (address → tract) | nmtc-mapper | **Yes — verified** (no cloud WAF) |
| `www.cdfifund.gov` | CDFI Fund eligibility workbooks / award data | nmtc-mapper, cdfi-fund-tracker | Yes, but **URLs move, and a moved file answers 403 — not 404** — verified 2026-09-03, when the Fund replaced the NMTC LIC workbook and the retired `?file=` route began returning a Drupal access-denied page (host still 200). Every nmtc-mapper release through 0.6.0 pins the dead URL; 0.6.1 retargets it. |
| `www.ffiec.gov` | FFIEC public CRA / census resources | cra-scraper | Partial — see cra-scraper note |
| `crapes.fdic.gov` | FDIC CRA Performance Evaluation search | cra-scraper | **No — Cloudflare-blocked on cloud/datacenter IPs** |
| `www.occ.gov` | OCC CRA evaluation resources | cra-scraper | Partial — see cra-scraper note |

## Cloud-blocked: cra-scraper

`cra-scraper` is **residential-only**. Cloudflare blocks all cloud/datacenter IPs
fronting the CRA-evaluation hosts, and this is **not fixable by headers** — the
block is at the TLS/IP-reputation layer, not the User-Agent. No skill in this
plugin wraps cra-scraper for that reason. Do not attempt to route around it by
spoofing a browser UA; that will not work and is against the honest-UA
convention below.

## Honest User-Agent convention

Every network-touching package identifies itself with a clean tool-token
User-Agent and **deliberately does not mimic a browser**. Verified examples from
source this session:

```
User-Agent: hmda-analyzer/<version> (+https://github.com/Jaypatel1511/hmda-analyzer)
User-Agent: cra-scraper/<version> (+https://github.com/Jaypatel1511/cra-scraper)
```

The convention is intentional: identify the tool and its repo honestly so the
data host can see who is calling. Spoofing a browser UA is explicitly avoided,
and (for cra-scraper) would not defeat the Cloudflare IP-level block anyway.

## Practical implications for an AI using these skills

- nmtc-eligibility and hmda-analysis hit hosts that were cloud-reachable and
  verified live when their rows above were written. **cdfi-peer-benchmark's host
  was NOT re-verified in the 2026-09-07 pass** — `api.fdic.gov` was blocked by
  that session's egress allowlist, which is a property of that session and not
  evidence about the host. Check egress yourself before relying on it.
- The **CDFI Fund** dependency (nmtc-mapper's eligibility table) is the fragile
  one: files move, so a download can fail. On failure, report it — never guess
  eligibility. **A relocated Fund file answers 403, not 404**, so a dead pin
  reads as a blocked client and invites the wrong diagnosis; when the error is a
  403 on a cdfifund.gov workbook, suspect a moved file and check the package for
  a newer release before touching user agents or proxies (2026-09-03 was the
  last such move; `nmtc-mapper` 0.6.1 followed it).
- Anything touching CRA exam ratings will fail from a cloud runner; that is a
  property of the upstream host, not a bug to work around.
