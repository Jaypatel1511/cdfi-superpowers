# cdfi-superpowers

**Your AI, grounded in audited CDFI tooling instead of hallucinating tract
eligibility.**

`cdfi-superpowers` is an **AI skill layer** over Jay Patel's published CDFI
Python portfolio (PyPI user [`Jaypatel1511`](https://pypi.org/user/Jaypatel1511/)).
It contains **no new analytical code** — only skills, reference docs, and thin
usage patterns that `pip install` and call the already-published, independently
versioned packages. When your AI answers a question about NMTC eligibility, a
bank CDFI's peer metrics, or HMDA lending distributions, these skills make it
call real, audited tools and report what they return — including N/A and errors —
rather than inventing a plausible-sounding number.

## The three skills

| Skill | What it does | Backed by |
|---|---|---|
| **nmtc-eligibility** | Is this address/tract NMTC eligible? Distress tier? Project feasibility? | nmtc-mapper 0.3.3, nmtc-screener 0.1.0 |
| **cdfi-peer-benchmark** | Benchmark a **bank** CDFI against FDIC peers (NIM, ROAA, capital, …) | cdfi-benchmark 0.2.0 |
| **hmda-analysis** | Pull HMDA LAR data and produce **descriptive** cuts + a CRA-**proxy** distribution | hmda-analyzer 0.5.0 |

Versions were verified against live PyPI this session; every code example in
each skill was actually executed and shows real output.

### What these skills refuse to do

- **Fabricate eligibility or metrics.** If a tool errors, the skill reports the
  error; it never estimates NMTC eligibility from general knowledge or fills a
  NaN with a number.
- **Inferential fair-lending analysis.** hmda-analysis is descriptive only — no
  disparate-impact, disparity-ratio, protected-class, or fair-lending inference,
  and no reading the CRA-proxy as CRA performance.
- **Benchmark non-banks.** cdfi-peer-benchmark is FDIC bank CDFIs only — no
  credit unions, no unregulated loan funds.

See `references/caveats-and-limits.md` for the full boundary list.

## Install

### (a) Claude Code / Cowork — plugin marketplace

Add this repo as a marketplace, then install the plugin:

```
/plugin marketplace add Jaypatel1511/cdfi-superpowers
/plugin install cdfi-superpowers
```

### (b) claude.ai — upload a `.skill`

Build the skill archives and upload the one(s) you want in the claude.ai skills UI:

```
bash scripts/make_skills.sh
```

This writes `dist/nmtc-eligibility.skill`, `dist/cdfi-peer-benchmark.skill`, and
`dist/hmda-analysis.skill` — each a zip with `SKILL.md` at its root.

### (c) Any other AI — raw markdown / llms.txt

Point any assistant at the raw Markdown. `llms.txt` at the repo root indexes the
skills and references for AI crawlers; each `skills/*/SKILL.md` is
self-contained.

## How it relates to the packages

Each wrapped package is **independently published and versioned on PyPI** under
`Jaypatel1511` and installs on its own (`pip install nmtc-mapper`, etc.). This
repo does not vendor or fork them — the skills install them at their current
published version and call their public API. The full portfolio (21 packages) is
catalogued in `references/package-index.md`.

## License

MIT © 2026 Jay Patel. Each wrapped PyPI package carries its own license and
version.
