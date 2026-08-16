# cdfi-superpowers

**Your AI, grounded in audited CDFI tooling instead of hallucinating tract
eligibility.**

`cdfi-superpowers` is an **AI skill layer for the CDFI industry** — NMTC
eligibility, bank CDFI peer benchmarking, and HMDA lending analysis, built for
lenders, CDEs, compliance teams, and community development researchers.

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

## The three skills

| Skill | What it does | Backed by |
|---|---|---|
| **nmtc-eligibility** | Is this address/tract NMTC eligible? Distress tier? Project feasibility? | nmtc-mapper >=0.5.0, nmtc-screener 0.1.0 |
| **cdfi-peer-benchmark** | Benchmark a **bank** CDFI against FDIC peers (NIM, ROAA, capital, …) | cdfi-benchmark 0.2.1 |
| **hmda-analysis** | Pull HMDA LAR data and produce **descriptive** cuts + a CRA-**proxy** distribution | hmda-analyzer >=0.6.0 |

Versions were verified against live PyPI at time of writing; every code example
in each skill was actually executed and shows real output. Where a floor is shown
as `>=`, it is **load-bearing** and the skill says why: `nmtc-mapper >=0.5.0` is
where `is_opportunity_zone` stops returning a confident `False` — below it the
package answers "not an Opportunity Zone" about 78,039 tracts it cannot
distinguish from a 2010/2020 vintage miss, and carries an
`is_nmtc_native_area` field that can only ever say "I don't know"; and
`hmda-analyzer >=0.6.0` is where the geography-vintage refusal exists at all.

`hmda-analyzer 0.6.0` alone required **Python >=3.11**; **0.6.1 relaxed that back
to >=3.9** while keeping the refusal (verified 2026-08-13 against the `>=0.6.0`
floor, which resolved to 0.6.1 at the time; its `__all__` still exports
`GeographyVintageError` and the three basis maps). The pinned floor stays
`>=0.6.0` because 0.6.1 changed nothing the skill layer depends on.

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

## Version

**cdfi-superpowers 2026.8.2** (CalVer, `YYYY.M.MINOR`). This is the plugin
version carried by `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`;
the three manifests and this line move together. It versions the *skills*, not
the wrapped PyPI packages — those are independently versioned and are listed in
the table above. See `CHANGELOG.md` for what changed under each release.

## Install

The skills live in **`.agents/skills/`** — the agent-neutral location defined by
the [Agent Skills spec](https://github.com/agentskills/agentskills). At project
scope that directory is shared by GitHub Copilot, Cursor, Codex, Gemini CLI,
Antigravity, Amp, Cline, OpenCode and Warp, which is the list `gh skill install
--help` names as resolving to it.

**Claude Code is not in that list and does not scan `.agents/skills/`** — it
scans `.claude/skills/`. It reaches these three skills through the plugin
manifest instead: `.claude-plugin/plugin.json` enumerates the three paths
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
>   `banks.data.fdic.gov` (cdfi-peer-benchmark), `ffiec.cfpb.gov` (hmda-analysis)
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

This writes `dist/nmtc-eligibility.skill`, `dist/cdfi-peer-benchmark.skill`, and
`dist/hmda-analysis.skill` — each a zip with `SKILL.md` at its root.

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

Then in Copilot CLI run `/skills reload` and confirm the three skills are listed.

**Or with the GitHub CLI** (requires `gh` >= 2.90; installs one skill at a time):

```
gh skill install Jaypatel1511/cdfi-superpowers nmtc-eligibility \
  --allow-hidden-dirs --agent github-copilot --scope user
```

`--allow-hidden-dirs` is **required**, not optional: `gh skill` treats
`.agents/skills/` as a hidden directory and finds nothing without it (it reports
"no standard skills found, but 3 skill(s) exist in hidden directories"). The
skill name is also required when running non-interactively. Repeat for
`cdfi-peer-benchmark` and `hmda-analysis`, or drop `--scope user` to install into
the current repository instead.

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
