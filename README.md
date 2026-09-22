# cdfi-superpowers

**Your AI, grounded in audited CDFI tooling instead of hallucinating tract
eligibility.**

`cdfi-superpowers` is an **AI skill layer for the CDFI industry** — NMTC
eligibility, bank CDFI peer benchmarking, HMDA lending analysis, IC credit
memos, and fair-lending disparity screening, built for lenders, CDEs,
compliance teams, and community development researchers.

Generic AI assistants confidently invent answers in this domain: wrong tract
eligibility, fabricated peer medians, "CRA performance" claims from proxy data.
In a field where numbers end up in loan committees, applications, and compliance
reviews, that's not a quirk — it's a liability. These skills fix that by making
your AI call real, open-source, audited tools and report exactly what they
return — including N/A and errors — rather than inventing a plausible-sounding
number.

The skills contain **no new analytical code**. Each one `pip install`s
independently versioned, openly published Python packages (MIT-licensed, on
[PyPI](https://pypi.org/user/thejaypatel1511/)) and teaches the AI to use them
correctly, with the methodology caveats those tools ship with.

## The five skills

| Skill | What it does | Backed by |
|---|---|---|
| **nmtc-eligibility** | Is this address/tract NMTC eligible? Distress tier? Project feasibility? | nmtc-mapper >=0.6.1, nmtc-screener 0.1.0 |
| **cdfi-peer-benchmark** | Benchmark a **bank** CDFI against FDIC peers (NIM, ROAA, capital, …) | cdfi-benchmark >=0.3.0 |
| **hmda-analysis** | Pull HMDA LAR data and produce **descriptive** cuts + a CRA-**proxy** distribution | hmda-analyzer >=0.6.0 |
| **credit-memo** | Generate a structured IC credit memo from the user's deal inputs — CDFI loans, NMTC deals, equity, grants, guarantees | credit-memo >=0.2.2 |
| **fair-lending-screening** | Adjusted denial-disparity **screening** on public HMDA data — logistic regression with FFIEC-standard controls; the **inferential** counterpart to hmda-analysis | fair-lending-screener >=0.2.2 |

Versions were verified against live PyPI at time of writing; every code example
in each skill was actually executed and shows real output. Where a floor is shown
as `>=`, it is **load-bearing** and the skill says why. `nmtc-mapper >=0.6.1` is
the floor because **`>=0.6.0` admits an install that cannot load its data**: the
CDFI Fund retired the eligibility-workbook URL on 2026-09-03, every release
through 0.6.0 pins it, and it answers **403** — so a 0.6.0 install raises
`EligibilityDownloadError` on its first cold call and answers nothing. 0.6.1
retargets the loader. (0.6.0 remains the release where `eligibility_status`
gains its fifth value, `not-covered-territory`, and exports the vocabulary as
`ELIGIBILITY_STATUS_VALUES` — below it an Island Area
tract (AS, GU, MP, VI — outside the CDFI Fund table's universe by scope) is
reported with the same status as a mistyped GEOID, indistinguishable from it, and
the five-way vocabulary the skill teaches does not exist; 0.5.0 was where
`is_opportunity_zone` stopped returning a confident `False` about 78,039 tracts
it cannot distinguish from a 2010/2020 vintage miss.) And
`hmda-analyzer >=0.6.0` is where the geography-vintage refusal exists at all;
and `cdfi-benchmark >=0.3.0` is where `loans_to_deposits` stops being graded
backwards — below it a bank lending 200% of its deposits grades STRONG and one
at 55% grades WEAK, with `rank_institution`'s percentile inverted to match. The
floor is deliberately not `>=0.3.1`: 0.3.1 changed no library code, and its
package tree is byte-identical to the published 0.3.0 wheel, so `>=0.3.1` would
be a floor with no runtime justification.

`hmda-analyzer 0.6.0` alone required **Python >=3.11**; **0.6.1 relaxed that back
to >=3.9** while keeping the refusal (verified 2026-08-13 against the `>=0.6.0`
floor, which resolved to 0.6.1 at the time; its `__all__` still exports
`GeographyVintageError` and the three basis maps). The pinned floor stays
`>=0.6.0` because 0.6.1 changed nothing the skill layer depends on.

`credit-memo >=0.2.2` is the floor because 0.2.2 is where the memo itself
discloses that four `NMTCTerms` inputs (the leverage-loan rate, both QLICI
rates, and the compliance period) are accepted and never rendered — below it an
NMTC Structure table reaches the committee with nothing marking it partial.
`fair-lending-screener >=0.2.2` is the floor because **0.1.1 is yanked** (a
breaking API change in a patch release) and because 0.2.2 is where the package
retracted its own "methodology federal examiners use" and "disparate-impact
analysis" labels — below it the generated report describes itself falsely.

### What these skills refuse to do

- **Fabricate eligibility or metrics.** If a tool errors, the skill reports the
  error; it never estimates NMTC eligibility from general knowledge or fills a
  NaN with a number.
- **Inferential fair-lending analysis from descriptive data.** hmda-analysis is
  descriptive only — no disparity-ratio, protected-class, or fair-lending
  inference, and no reading the CRA-proxy as CRA performance. The plugin now
  **offers** inferential work through the dedicated fair-lending-screening
  skill, which carries its own guardrails: alpha-status package, a required
  screening-not-finding statement on every result, the omitted-variable
  (credit score, AUS) upper-bound caveat, race-only comparisons, and typed
  errors surfaced rather than smoothed. Neither skill crosses into the other's
  side of the descriptive/inferential line.
- **Invent a number for a credit memo.** credit-memo structures the user's
  inputs; a field the user did not supply stays unset, and the recommendation
  is the user's, never the skill's.
- **Benchmark non-banks.** cdfi-peer-benchmark is FDIC bank CDFIs only — no
  credit unions, no unregulated loan funds.

See `references/caveats-and-limits.md` for the full boundary list.

## Version

**cdfi-superpowers 2026.9.3** (CalVer, `YYYY.M.MINOR`; MINOR restarts at 0 when
the month changes). The version lives at **five sites and they move together**:
`.claude-plugin/plugin.json` (1), `.claude-plugin/marketplace.json` (2 — the
marketplace `metadata` block and the plugin entry), this line, and the top
heading of `CHANGELOG.md`. There are two manifest *files* carrying three version
*fields*; an earlier version of this sentence said "three manifests" and did not
count the changelog heading. It versions the *skills*, not
the wrapped PyPI packages — those are independently versioned and are listed in
the table above. See `CHANGELOG.md` for what changed under each release.

## Install

The skills live in **`.agents/skills/`** — the agent-neutral location defined by
the [Agent Skills spec](https://github.com/agentskills/agentskills). At project
scope that directory is shared by GitHub Copilot, Cursor, Codex, Gemini CLI,
Antigravity, Amp, Cline, OpenCode and Warp, which is the list `gh skill install
--help` names as resolving to it.

**Claude Code is not in that list and does not scan `.agents/skills/`** — it
scans `.claude/skills/`. It reaches these five skills through the plugin
manifest instead: `.claude-plugin/plugin.json` enumerates the five paths
explicitly, which is what makes install method (a) work. Dropping a skill folder
into a project's `.agents/skills/` does nothing in Claude Code, silently.

> ### Runtime requirement — read this first
>
> These skills are not self-contained prose. Each one **`pip install`s a package
> from PyPI and executes Python**, and each calls a public federal data endpoint
> at run time. They need:
>
> - **Python >=3.9** and **pip**
> - **Network access to `pypi.org`**, plus the endpoints the skill you use hits:
>   `geocoding.geo.census.gov` and `www.cdfifund.gov` (nmtc-eligibility),
>   `api.fdic.gov` (cdfi-peer-benchmark), `ffiec.cfpb.gov` (hmda-analysis and
>   fair-lending-screening). credit-memo calls no endpoint — every figure is
>   user-supplied.
>
> In a locked-down enterprise environment where PyPI or those hosts are blocked,
> **these skills cannot work** — the agent will load the skill and then fail at the
> install or the first call. Check egress before installing. See
> `references/data-source-map.md` for the full host list and which are known to be
> blocked from cloud/datacenter IPs.

### (a) Claude Code / Cowork — plugin marketplace

```
/plugin marketplace add Jaypatel1511/cdfi-superpowers
/plugin install cdfi-superpowers
```

**To upgrade**, refresh the marketplace, then update the plugin by its
**marketplace-qualified** name. `update` rejects the bare name that `install`
accepts — `claude plugin update cdfi-superpowers` fails with `Plugin
"cdfi-superpowers" not found`. A restart is required to apply:

```
claude plugin marketplace update cdfi-superpowers
claude plugin update cdfi-superpowers@cdfi-superpowers
```

### (b) claude.ai — upload a `.skill`

Build the archives and upload the one(s) you want in the claude.ai skills UI:

```
bash scripts/make_skills.sh
```

This writes `dist/nmtc-eligibility.skill`, `dist/cdfi-peer-benchmark.skill`,
`dist/hmda-analysis.skill`, `dist/credit-memo.skill`, and
`dist/fair-lending-screening.skill` — each a zip with `SKILL.md` at its root.

### (c) GitHub Copilot

Copilot discovers skills from `.agents/skills/` in a project, or from
`~/.copilot/skills/` for every project. It does **not** scan a bare `skills/`
directory — which is why this repo uses `.agents/skills/`.

**Project scope** — clone the repo into a workspace and Copilot reads
`.agents/skills/` directly, no copying:

```
git clone https://github.com/Jaypatel1511/cdfi-superpowers.git
```

**Personal scope (all projects)** — copy the skill folders into your personal
skills directory, then reload:

```
git clone https://github.com/Jaypatel1511/cdfi-superpowers.git /tmp/cdfi-superpowers
mkdir -p ~/.copilot/skills
cp -R /tmp/cdfi-superpowers/.agents/skills/* ~/.copilot/skills/
```

Then in Copilot CLI run `/skills reload` and confirm the five skills are listed.

**Or with the GitHub CLI** (requires `gh` >= 2.90; installs one skill at a time):

```
gh skill install Jaypatel1511/cdfi-superpowers nmtc-eligibility \
  --allow-hidden-dirs --agent github-copilot --scope user
```

`--allow-hidden-dirs` is **required**, not optional: `gh skill` treats
`.agents/skills/` as a hidden directory and finds nothing without it (it reports
"no standard skills found, but 5 skill(s) exist in hidden directories"). The
skill name is also required when running non-interactively. Repeat for
`cdfi-peer-benchmark`, `hmda-analysis`, `credit-memo` and
`fair-lending-screening`, or drop `--scope user` to install into the current
repository instead.

### (d) Cursor, Codex, Warp and the other agents that read `.agents/skills/`

**Who this is for:** Cursor, Codex, Gemini CLI, Antigravity, Amp, Cline,
OpenCode, Warp and GitHub Copilot — the agents that share the project-scope
`.agents/skills/` directory.

**Who this is not for: Claude Code.** It does not scan `.agents/skills/`, so
copying a folder there gets you nothing and reports no error. Use (a) instead.

Copy the skill folder(s) you want into your project's `.agents/skills/`,
creating that directory first — it does not exist in a fresh project, and
`cp -R` fails with `No such file or directory` if you skip this:

```
mkdir -p /path/to/your-project/.agents/skills
cp -R .agents/skills/nmtc-eligibility /path/to/your-project/.agents/skills/
```

Each `SKILL.md` is self-contained — one file, no assets, no build step.

### (e) Crawler index — not an install

`llms.txt` at the repo root indexes the skills and references for AI crawlers.
It is a discovery aid, **not an installation method**; an assistant reading it
still needs the runtime above to actually run anything.

## How it relates to the packages

Each wrapped package is **independently published and versioned on PyPI** under
`thejaypatel1511` and installs on its own (`pip install nmtc-mapper`, etc.). This
repo does not vendor or fork them — the skills install them at their current
published version and call their public API. The full portfolio (22 packages) is
catalogued in `references/package-index.md`.

## License

MIT © 2026 Jay Patel. Each wrapped PyPI package carries its own license and
version.
