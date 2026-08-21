# Changelog

All notable changes to `cdfi-superpowers`. Versioning is CalVer (`YYYY.M.MINOR`).

## 2026.8.3

**An addition and a sharpening — not a retraction. Nothing 2026.8.2 asserted was
false.** The commitment-basis rule it shipped was already careful: the
When-to-use line answering *"Does my pipeline meet the 85% investment
commitment?"* already said **"answered by pointing at that rule, never by
returning a number,"** and the worked example already said **"a tract does not
'qualify for' a commitment — a CDE makes one, over its own QLICI dollars."**
Both stand unchanged.

**What the skill did not say is the SHAPE of the Question 25 fields** — and
without that, a reader could still infer that a CDE files a computed 85% figure
somewhere. It does not. That inference is the harm this entry closes.

**Primary source, retrieved and hash-verified this session, not relayed.** The CY
2024-2025 NMTC Program Allocation Application — 142 pp., 1,525,626 bytes, SHA-256
`0280c6bc…12834f`, downloaded from `cdfifund.gov/system/files/2024-11/` and
text-extracted locally with `pypdf`. The hash and byte count match the pin
`nmtc-application-builder` carries at `nmtcapp/renderers/_question_25.py:52`, so
both repos read the same instrument. Every Q25 quotation below was read off this
download; none is carried forward.

### Added
- **A field-shape block inside the commitment-basis rule** in
  `.agents/skills/nmtc-eligibility/SKILL.md`, placed immediately after the
  review-process citation and before the QLICI-denominator paragraph. It carries
  a table of every Question 25 field with its printed page, Response column and
  **Field Type**, read verbatim from the instrument:
  - **Q25(a) is a `Dropdown Menu`, `☐ Yes` / `☐ No`** (printed p. 38). The 85% is
    the threshold printed in the question text, not a figure the Applicant
    supplies. **There is no percentage field for Q25(a) anywhere in Question 25.**
  - **Q25(b)(i) is a `Dropdown Menu`** — `0 / 5 / 10 / 15 / 20` (printed p. 41).
    Only selecting 20 reaches a free numeric field, and that field is
    **25(b)(ii)**, a *separate* question of Field Type `Numerical – Percentage`
    admitting *"any percentage amount starting from 20% and up to 100%."* It is
    the only free-entry percentage in the whole of Question 25.
  - **Items 1–12 under Q25(a) and items 1–4 under Q25(b) are themselves Yes/No
    dropdowns** — so the Applicant declares *which area types it will serve*,
    again without supplying a share.
  - **Both commitments bind forward**, quoted verbatim with its page — Q25(a)
    Question Notes, printed p. 38: *"If the Applicant receives an NMTC
    Allocation, it will be required to meet the percentage figure identified, and
    such requirement will be a term of its Allocation Agreement."*
  - **The pipeline is not the deployment**, quoted verbatim with pages — the NOTE
    immediately above Q25 (printed p. 38): *"NOTE: The CDFI Fund does not expect
    that each and every investment will be in an area identified in Question
    25."*; Table A5 at printed p. 23: *"It is not expected that the Applicant will
    invest in all of the listed projects"*, those transactions being
    *"representative of the types of projects that will be undertaken with an
    NMTC Allocation"*; and Q25(b)(i)'s notes at printed p. 41: *"Applicants will
    not be held to the individual commitments to any of the areas listed below."*
- **The operational consequence, stated as plainly as the rest of the rule:** a
  CDE asking *"what is my Q25(a) percentage"* is asking for something the
  Application does not collect — answer what the commitment means and what
  evidence bears on it, **never a computed share, and never a recommendation to
  answer No because a current pipeline falls short.**
- **The harm case, named.** A CDE at 60% pipeline told *"your Q25(a) share is
  60%"* checks **No** and forfeits points **it was entitled to claim**, because
  the commitment governs future QLICIs. Understating an Applicant to a federal
  agency is the mirror of the fabricated negative the third-state rule exists to
  stop — pointed at the Applicant instead of the tract.
- **A field-shape clause in the Caveats list**, so a reader who skims to the
  bottom still learns that Q25(a) collects no percentage.

### Changed
- **`DISTRESS_LEVELS["severe"]` gloss — "85% numerator" retired.** The claim was
  true and the noun was wrong: *numerator* implies a computed quotient the
  Applicant files. Was: *"a QLICI made in tract `36005023702` **would count
  toward a CDE's 85% numerator**, on item 1 of the Q25 area list."* Now: *"a
  QLICI made in tract `36005023702` **would satisfy item 1 of the Q25(a) area
  list**"* — one of the five single-item routes — plus *"whether to commit to the
  85% is a **Yes/No the CDE answers for itself**, and no percentage is filed for
  it."* The verbatim-quotation rule for `DISTRESS_LEVELS` and the *"a tract does
  not 'qualify for' a commitment"* sentence are untouched.
- **The same noun, one paragraph earlier.** *"Q25(a)'s numerator is a QLICI in an
  area characterized by…"* asserted that Q25(a) *has* a numerator; it now reads
  *"A QLICI counts toward the Q25(a) commitment when it is made in an area
  characterized by…"* The item lists are unchanged and were re-verified against
  the instrument this session (items 1–12 confirmed, including item 10 as MUA
  **or geographic HPSA** and item 12 as LILA-to-supermarkets).
- **Q25(b)(i) described as a selection, not a request.** The rule's opening
  paragraph said the Application *"asks … for the percentage"*; the instrument
  says *"**select** the percentage."* Now reads *"a figure it selects, not one it
  enters."*
- **The nesting quotation now carries its page** — Q25(b)(i) Question Notes,
  printed p. 41, verified verbatim this session.

### Unchanged after review
- **The When-to-use line on the 85% (`SKILL.md` "When to use")** — *"answered by
  pointing at that rule, never by returning a number: these packages never see a
  QLICI amount."* Correct as written; the rule it points at now says more.
- **`A severe_distress=False is therefore not a "does not count toward the 85%"`**
  — correct as written and kept. Only the sentence *following* it carried the
  numerator defect.
- **"Never render a distress flag as a share of anything"** (output-presentation
  rules) and the `severe`/`deep` string critiques in the field list — all correct
  as written.
- **`hmda-analysis` and `cdfi-peer-benchmark`** — spot-checked again this cycle
  for `85%`/`20%`/`QLICI`/`QEI`/`distress`/`NMTC`: **zero hits in either.** Still
  clean, not rewritten.

### Known, not fixed
- **`nmtc-mapper` 0.5.0's `DISTRESS_LEVELS["severe"]` still reads *"Severe
  Distress — qualifies for 85% investment commitment."*** The skill quotes
  package constants verbatim by rule, so it cannot fix this upstream string — it
  can only frame it, which the worked-example gloss now does more precisely. **A
  GitHub issue against `nmtc-mapper` is owed.**

## 2026.8.2

**This is a missing rule, not a retraction. Nothing 2026.8.1 asserted was
false.** `nmtc-eligibility` never said a CDE meets the 85% or 20% commitment, and
never divided anything to produce a share. What it never said was that it
*cannot* — and it carried one When-to-use example inviting a reader to try.

The gap was located by a defect one repo over. `nmtc-application-builder` 1.2.1
(shipped 2026-08-16, `3e436dc`) closed a bug whose root is a distinction this
repo defines correctly in `references/cdfi-industry-primer.md` and applied
nowhere: the flagship bucketed and divided **QEI** and rendered the quotient
under a label asserting the Fund's 85%/20% bars. Same shape as the
`benchmark_thresholds.py` defect — **the correct fact was in the repo and the
wrong one was on the page.** This skill had the same latent invitation and no
rule standing against it.

**Primary source, downloaded and quoted this session, not relayed.** The CY
2024-2025 Allocation Application, **Q25(a)**, asks whether the Applicant commits
to *"providing at least 85% of its QLICIs **(in terms of aggregate dollar
amounts)**"* in the qualifying areas; **Q25(b)(i)** asks for *"the percentage of
its QLICIs (in terms of aggregate dollar amounts)"* in the 20% tier. The
review-process document (`CY_2024_25_NMTC_Program_Review_Process.pdf`, §C.1)
states both on **QLICIs**. The parenthetical is the load-bearing half and no
relayed version of this quote carried it.

### Added
- **The commitment-basis rule (non-negotiable)** in
  `.agents/skills/nmtc-eligibility/SKILL.md`, placed as the fourth rule block
  after the vintage-scope rule and immediately above the worked example whose
  `summary()` output prints *"qualifies for 85% investment commitment"*. It
  states: the denominator is a CDE's **QLICI dollars** (not QEI, not project
  count, not tract count); these packages **never see a QLICI amount**, so they
  answer *"would a QLICI made here count?"* and cannot answer *"what share of
  this CDE's QLICIs qualifies?"*; and no output of this layer may support a claim
  that a CDE meets, clears, is on track for, or fails either commitment.
- **The routes the flags do not cover, enumerated from the Application rather
  than assumed.** Q25(a)'s numerator is **≥1 of items 1–5 or ≥2 of items 6–12**.
  Severe Distress is item 1; this package returns exactly two of the twelve
  (`severe_distress` and `is_non_metro`, item 4) and computes **no** multi-indicia
  measure. Q25(b)'s 20% is **any one of four** — Deep Distress, NMTC Native
  Areas, High Migration Rural Counties, U.S. Island Areas — so `deep_distress`
  is one route of four, not the tier. Two of the unreachable routes are ones the
  skill already declines: Native Areas and Island Areas.
- **Three counts derived against the live 85,395-row table this session**, on a
  fresh `nmtc-mapper` 0.5.0 install with an isolated `HOME` and a cold cache
  (downloaded workbook SHA-256 `3a6f5851…72d49`): `deep_distress` is a **strict
  subset** of `severe_distress` — **8,061 / 0 / 13,121** against **21,182**
  severe-flagged. Also derived and stated in the rule: **10,532 tracts non-metro
  and not severe** (3,754 of them LIC), **1,185 high-migration-rural and not
  deep**. The nesting itself is stated the Fund's way — *"A QLICI that meets this
  commitment will also automatically meet the commitment made in Question
  25(a)"* — because the flag subset is a fact about two columns, not the reason
  the commitments nest.
- Two cross-references so the rule is reachable from the sections an AI skims:
  one output-presentation bullet (never render a distress flag as a share) and
  one caveat bullet.

### Changed
- **`SKILL.md:30`, the one line that was mis-framed rather than merely silent.**
  It read *"Does this tract qualify for severe distress / the 85% investment
  commitment?"* — a category error: a tract carries a flag, a **CDE** makes a
  commitment, and the example presented both as one lookup this skill performs.
  Split into the question the tool answers (*"Is tract 36005023702 flagged severe
  distress — or deep distress — in the CDFI Fund's eligibility table?"*) and a
  commitment-flavoured example answered **by pointing at the rule** (*"Does my
  pipeline meet the 85% investment commitment?"*) rather than by returning a
  number. No factual claim changed; a routing invitation did.
- **The two verbatim quotations of `nmtcmapper.data.schema.DISTRESS_LEVELS` are
  untouched, and qualified on the adjacent line instead.** `:295` (inside
  executed `summary()` output) and the `distress_description` example in the
  field list are quotations of a package constant; paraphrasing one into skill
  text is the banned pattern that produces exactly this class of defect. Both now
  carry an adjacent note in the skill's own voice.
- `SKILL.md`'s screener caveat — *"not underwriting or a commitment"* — is a
  different sense of the word, is correct, and was **deliberately not swept**.

### Reported, not fixed (upstream)
- **`nmtc-mapper`'s `DISTRESS_LEVELS` strings are the upstream defect**, and the
  skill cannot repair them without breaking the verbatim rule. Both are house
  claims wearing a Fund label: `"severe"` names the 85% commitment with no QLICI
  denominator and no *"and/or multiple indicia"* route; `"deep"` asserts
  *"strongest NMTC application score"* with no citation — directionally true
  against the real Q25(b) commitment and still unsourced. Replacement strings
  proposed for a 0.5.1; no branch opened.

### Verified, no change needed
- **The two pins recorded as stale in the prior cycle are not stale.**
  `README.md:27`, `llms.txt:16` and `references/package-index.md:13` all carry
  `nmtc-mapper >=0.5.0`, and `llms.txt` carries `cdfi-benchmark 0.2.1` — 2026.8.1
  swept all of them. The standing note is retired.
- `cdfi-peer-benchmark` and `hmda-analysis` **read** (not grepped) end-to-end
  through their When-to-use and scope sections: neither mentions QLICI, QEI, or
  NMTC, and neither would route a commitment question inward. Their guardrails
  (FDIC-insured banks only; descriptive-only firewall) hold independently.

### Version
`2026.8.1` → **`2026.8.2`**, at four sites — `.claude-plugin/marketplace.json`
(two), `.claude-plugin/plugin.json`, `README.md:61` — swept and re-grepped, not
enumerated from memory.

## 2026.8.1

**`nmtc-eligibility` named a field the dependency had removed, and asserted a
type the dependency had changed.** Both defects entered the repo the moment
`nmtc-mapper 0.5.0` published, and 2026.8.0 could not have caught them: **0.5.0
went to PyPI at 2026-08-13 20:46:38 CDT and the 2026.8.0 merge (`fc9d900`)
landed at 21:02:01 — fifteen minutes and twenty-three seconds later**, verified
against 0.4.3. Nothing was done wrong; the release arrived mid-cycle. This entry
records it because the *shape* of the miss is the useful part: 2026.8.0's own
provenance-line change was written to survive exactly this, and it did — the
line it produced, `SKILL.md:48`, read

> "Verified 2026-08-13 (PyPI) against **`nmtc-mapper>=0.4.2`** (resolved 0.4.3 at
> the time)"

which was true when written and is the evidence that located the drift. The
floor + date + as-of pattern works. What it cannot do is bump the floor for you.

Both defects are the same class the skill exists to prevent — **an unknowable
negative reported as a negative** — arriving through the dependency rather than
through the prose. Re-verified in clean venvs on Python 3.14 before any edit:
`is_nmtc_native_area` PRESENT on 0.4.2 and 0.4.3, **GONE on 0.5.0**;
`is_opportunity_zone` a plain `bool` on 0.4.2/0.4.3, **`Optional[bool]` on
0.5.0 with `False` unreachable.**

### Changed
- **Install floor raised `>=0.4.2` → `>=0.5.0`, at six line-sites across five
  files** — `.agents/skills/nmtc-eligibility/SKILL.md` (45 and the provenance
  line at 48), `README.md` (27 and the load-bearing-floor note at 33),
  `llms.txt:16`, and **`references/package-index.md:13`**. The last was not on
  the sync brief's list and was found by grep; a floor that lives in five files
  has to be swept, not enumerated from memory.
- **The floor's justification changes with it, and is stated from the skill's own
  rule.** `>=0.4.2` was load-bearing because 0.4.2 stopped reporting 168
  statutorily-eligible tracts as ineligible. **`>=0.5.0` is load-bearing because
  below it `is_opportunity_zone` returns a confident `False` for 78,039 of the
  85,395 tracts** — every row outside the 8,764-tract designation set — plus a
  hardcoded `False` on the geocode-no-match branch, for an address that never
  resolved to a tract. The skill already calls an unknowable negative reported as
  a negative the thing that "kills a deal that may genuinely qualify."
- **The OZ output-presentation rule rewritten: the compensation goes, the posture
  stays.** `SKILL.md:450` asserted *"`is_opportunity_zone` is a plain `bool`, so
  a `False` means EITHER not-designated OR a vintage miss"* — false at 0.5.0 —
  and `:456` said *"the fix to `Optional[bool]` is slated for 0.5.0"*, describing
  a released change as future. The rule now teaches the **`opportunity_zone_status`
  property** (0.5.0: `designated` / `not-confirmed` / `no-tract`) with one honest
  rendering per value, and says explicitly that an AI must **no longer add the
  caveat by hand, because the type and the printed line now carry it**. This is
  the same inversion `hmda-analysis` went through at 2026.7.5: what was an
  instruction the AI had to remember is now enforced by the package.
- **The 1,408 / 16.1% figure re-derived on 0.5.0 and re-stated — it was never
  what the old sentence said it was.** Re-executed against the live load: the OZ
  file is **8,764** designated tracts, **7,356** have a row in the 85,395-row
  2020-basis table and **1,408 (16.1%) do not**. The figures are identical to the
  0.4.2 session; **the sentence attached to them was wrong then and is retired.**
  It was quoted as the size of the confident-`False` harm; the harm was 78,039
  tracts, and 1,408 measured something else — how much of the designation list is
  unreachable from a 2020 GEOID at all. That is the quantity that still means
  something at 0.5.0, where it sizes the **not-confirmed** population rather than
  a fabricated negative. Newly derived and added: **75 of the 1,408 are Island
  Area tracts** (GU 25, MP 20, AS 16, VI 14) — a scope hole, not a vintage miss,
  cross-referenced to the Island Areas paragraph — and the remaining **1,333 are
  2010→2020 vintage misses.** `not-confirmed` therefore has three inseparable
  causes, which is why it cannot be read as a "no."
- **`is_nmtc_native_area` removed from five sites in `SKILL.md` (257, 276, 278,
  280, 482) and replaced rather than deleted.** A skill that exists to stop an AI
  fabricating an answer has to state the absence, not leave a gap. The new note
  says: the field was dropped in 0.5.0 and reading it now raises; **the CDFI Fund
  publishes no tract-keyed NMTC Native Areas resource** (April 2025 NMTC
  Compliance & Monitoring FAQs **Q31** enumerates eleven and this is not among
  them, while the Fund's CIMS service does carry tract-level native-area
  qualification layers **for Native Initiatives and the BEA, not for NMTC**);
  **the criterion is nonetheless live** — the same FAQ's **Q32** names "NMTC
  Native Areas" as one of the *Areas of Deep Distress* criteria added in the CY
  2024–2025 Application, so "unknown" here is not "irrelevant"; and the
  determination is a **polygon intersection** against Census **AIANNH**
  geographies, whose GEOIDs are four-digit codes with no state or county
  component and therefore cannot nest into `SSCCCTTTTTT`. An AI asked about
  Native Area status must say it cannot be determined from this package, and
  route to CIMS.
- **`SKILL.md:479-482`'s field-set sentence rewritten, not just shortened.** It read
  "Normalized columns include …" with the dropped field inside a list presented
  as a coherent set. Deleting a name from a list does not make the surrounding
  sentence true, so the sentence now states the exact shape verified against the
  live 0.5.0 load: indexed on `tract_id`, **exactly nine** normalized columns,
  with the tenth named as dropped.
- **The tri-state section extended to the contract 0.5.0 actually ships.** 0.4.0
  made the verdict tri-state and left its neighbours fabricating **inside the very
  branches written to protect it**. Six fields are now `Optional[bool]`
  (`nmtc_eligible`, `is_non_metro`, `is_high_migration_rural`, `severe_distress`,
  `deep_distress`, `is_opportunity_zone`), and the section states the rule that
  ties them: when `eligibility_status` is `not-found` or `geocode-failed`, every
  tract-derived field is `None`. Added with it: `None` is falsy, so
  `if r.severe_distress:` silently keeps meaning the wrong thing; and the three
  demographic rates now have **two** kinds of missing — `None` ("tract not read")
  versus `NaN` ("the Fund published no value", 1,583 poverty / 2,358 AMI rows,
  re-derived this session), which `summary()` prints as two different sentences.
- **Every worked example re-executed on a clean-venv 0.5.0 install** (cold cache,
  isolated `HOME`, live CDFI Fund and Census downloads), and the actual output
  pasted. No output was hand-edited.
  - **`36005023702` (Bronx)**: every demographic and eligibility figure identical
    to the 0.4.2 run; the `Opportunity Zone` line is the one line that moved, from
    `No` to `❓ NOT CONFIRMED — not on the 2018 designation list, which is
    2010-tract-based (indeterminate, NOT "not an Opportunity Zone")`. The skill's
    warning at `:245` — "Do not repeat the `Opportunity Zone: No` line as fact" —
    **became a description**: the line may now be reported as printed, which is
    the point of the release. Executed values: `is_opportunity_zone is None`,
    `opportunity_zone_status == 'not-confirmed'`.
  - **`36061980000` (absent tract)** — the skill's teaching case for the third
    state — **changed most.** On 0.4.3 it printed `Non-Metro: No`, `Opportunity
    Zone: No` and `High Migration: No`, and omitted the three demographic lines
    entirely: three fabricated negatives and three silent omissions sitting
    directly under a correct `❓ UNKNOWN` verdict. All six lines now print and
    qualify themselves inline.
  - **`11001980000` (verified-ineligible, null demographics)**: the printed
    values are unchanged (`False ineligible nan nan`), but `summary()` now renders
    the two null rates as "not available — the CDFI Fund published no value for
    this tract" where 0.4.3 rendered `nan%`. Added to the example, with the point
    that this wording is deliberately **different** from "tract not read" — the
    tract was read and its `NO` is real.
  - **All four geocoder branches re-executed on 0.5.0** and unchanged from 0.4.2
    (no-match and agree live; transport failure induced against a closed local
    port; ambiguity induced with two matches on different tracts). The provenance
    line now names 0.5.0 rather than "the installed 0.4.2 wheel".
  - **The pre-0.4.2 hard load failure re-executed**: a 0.4.1 install against the
    workbook the Fund serves today raises `EligibilitySchemaError` naming column
    index 2's renamed header, and loads nothing.
  - **nmtc-screener 0.1.0's example re-executed** — `HIGH 95` and all four
    reasons byte-identical.
- **A second 0.5.0 loader guard documented** under Data dependencies & fragility.
  The header check pins header *strings*, so a re-publish that leaves every header
  byte-identical and rewrites a *cell value* passes it — and the `== "YES"` tests
  would map the unrecognized value to `False`, a fabricated negative on the LIC
  verdict and both distress flags. 0.5.0 checks each categorical cell against a
  per-column value allowlist and raises instead.

### Not changed — verified, and recorded so the next cycle does not re-open them
- **No eligibility number moved.** Re-derived on 0.5.0 against the live table and
  identical to 0.4.3: **85,395** rows, `nmtc_eligible True` **35,335**, distress
  `{ineligible 50060, lic 14153, severe 13121, deep 8061}`,
  `is_high_migration_rural True` **1,422**, and the **168** HMR tracts failing
  both the ≥20%-poverty and ≤80%-AMI prongs — all non-metro, all in the
  (80%, 85%] MFI band, first-sorted `01013953500`, all now eligible.
- **…even though 0.5.0 corrected three structural defects in
  `_compute_eligibility`** (a missing `LIC AND` conjunction on severe/deep,
  `is_non_metro` standing in for the high-migration-rural 85% band, and `>=` vs
  `>` on the distress poverty prongs). **The mechanism prose is unaffected**, and
  the reason is worth writing down: that function **backs `load_sample_table()`
  only** — the twelve synthetic demo tracts. The official `.xlsb` path reads the
  Fund's own published columns C/N/O/P and never calls it. The skill documents
  the `.xlsb` path and correctly describes the C-or-N verdict, so no sentence
  about *how* eligibility is computed was left wrong behind a right number.
- **`SKILL.md:496`'s "the loader binds columns positionally" is CORRECT and was
  not touched.** It matches the package's own source comment and the
  `EligibilitySchemaError` message the 0.4.1 re-execution printed verbatim. A
  prior cycle nearly swept this word because a *different* sentence, about
  validation, was wrong; the restraint is recorded again because a justification
  must be scoped as tightly as the edit it justifies.
- **No Native Areas distress-tier correction exists to make in this repo.**
  `nmtc-mapper`'s own methodology document withdrew a claim that this skill
  called Native Areas an *Areas of Higher Distress* criterion. Re-verified at
  `fc9d900`: `"higher distress"`, case-insensitive, across all tracked files
  returns **zero** matches. The skill never made a tier claim at all. A grep that
  finds nothing here is the expected result, not a search to widen.
- **`hmda-analysis` and `cdfi-peer-benchmark` untouched**, and the CHANGELOG's
  historical entries for released versions left as written — including
  `CHANGELOG.md:182` and `:358-359`, which name `is_nmtc_native_area`. They are
  correct as history of 0.4.1/0.4.2 and are not defects.
- **`llms.txt`'s `cdfi-benchmark` pin needed no restraint after all** — 2026.8.0
  already corrected it to `0.2.1`, matching `README.md:28` and
  `references/package-index.md:15`. There is no `0.2.0` left in the repo.
- **`nmtc-screener` stays unpinned at `0.1.0`** and `nmtc-calc 0.2.1` remains the
  transitive dependency; neither released.

### Version
`2026.8.0` → **`2026.8.1`**, continuing 2026.8.0's deliberate CalVer correction
rather than reopening it: the month segment is in true (this release is August
2026) and this is a patch on the same month. Bumped at `README.md:58`,
`.claude-plugin/plugin.json` and both `.claude-plugin/marketplace.json` entries.

### Known limits of this sync
- **`NMTCMapper.eligible_count()` changed incompatibly in 0.5.0** — `pct_eligible`
  is removed (`KeyError`) in favour of `pct_eligible_of_determined`, whose
  denominator is `determined` rather than `total`, alongside new `determined` /
  `indeterminate` / `ineligible` keys. **No edit was made**, because no file in
  this repo documents `eligible_count()` or `enrich()`; there is no stale text to
  fix. Recorded so a future cycle that adds batch coverage starts from the 0.5.0
  contract — including that `~df["severe_distress"]` now raises `TypeError` on a
  frame with indeterminate rows and must be written `!= True`.
- **`is_opportunity_zone` is still absent from `enrich()`'s columns** — batch
  callers get no OZ answer, single-address callers do. 0.5.0 declines to close
  that gap deliberately. The skill documents only the single-address path, so
  nothing here is wrong; it is a gap in coverage, not a defect.

## 2026.8.0

**CalVer discontinuity, noted deliberately.** `2026.7.3` shipped **Jul 31**, but
`2026.7.4` through `2026.7.6` all shipped in **August** (Aug 1, 5 and 7) while
keeping the `7` minor, so the month segment had drifted out of true. (The Aug 9
commit `4705124` changed no version and was not a release.) This release resets it to the
actual month rather than continuing the drift: `2026.7.6` → **`2026.8.0`**. Nothing
pins a `2026.7.x` string outside this repo — the plugin is not listed in any
external directory (see below) — so the jump breaks no installed pin.

### Added
- **The three skills are now installable by any spec-conformant agent, not just
  Claude Code.** The skills moved from `skills/` to **`.agents/skills/`**, the
  agent-neutral path in the Agent Skills spec. GitHub Copilot discovers skills
  from `.agents/skills/` (project) and `~/.copilot/skills/` (personal) and never
  scanned a bare `skills/`, which is why a Copilot user could not install this
  repo at all. Moved with `git mv` so history follows; **no SKILL.md was copied** —
  there is exactly one on-disk copy of each, as before.
- **A `compatibility:` frontmatter field on all three skills** (spec-defined,
  ≤500 chars), naming the real runtime requirement per skill: Python, pip, PyPI,
  and the specific federal endpoints that skill actually calls, sourced from
  `references/data-source-map.md`. Beyond this, the only skill-body edits in this
  release are the two corrections recorded below: the retired bare-install claim
  and the provenance-line pattern. No worked example was touched, and none was
  re-executed.
- **README: a runtime-requirement block above the platform list.** These skills
  `pip install` and execute Python against public federal endpoints; in a
  locked-down enterprise that is what decides whether they can work at all, and
  the README never said so.

### Changed
- **README install section rewritten with real per-platform paths.** Section (c)
  previously read "Point any assistant at the raw Markdown," which is the shrug
  that the Copilot user hit. Now: (a) Claude Code/Cowork marketplace, (b)
  claude.ai `.skill` upload, (c) **GitHub Copilot** — project scope, personal
  scope, and a verified `gh skill install` form, (d) Cursor and other
  spec-conformant agents via `.agents/skills/`, (e) `llms.txt` labelled honestly
  as a crawler index rather than an install method.
- **`scripts/make_skills.sh`, `llms.txt` and `plugin.json` re-pointed** to
  `.agents/skills/`. The `.skill` archives are unaffected in shape — each is still
  a zip with `SKILL.md` at its root, because the script `cd`s into the skill
  directory before zipping and the source path is never recorded in the archive.
- **`hmda-analyzer`'s Python floor corrected in README and
  `references/package-index.md`.** Both said the pin implied **Python >=3.11**.
  That was true of `0.6.0` alone; **`0.6.1` (2026-08-07) relaxed `requires_python`
  back to `>=3.9`** while keeping the refusal. Verified this session: `pip install
  "hmda-analyzer>=0.6.0"` resolves to `0.6.1`, whose `__all__` is still 33 and
  still exports `GeographyVintageError`, `UnreachableFlagError`,
  `EmptyUniverseError` and the three basis maps. **The `>=0.6.0` floor is
  therefore kept, not bumped** — `0.6.1` changed nothing the skill layer depends
  on, and the pin already resolves to it everywhere.
- **The bare-install hazard was retired by `0.6.1`, and the claim has been
  deleted rather than kept.** Every `hmda-analyzer` release except `0.6.0`
  declares `requires_python >=3.9`; below 3.9 nothing installs at all, and at
  3.9+ bare resolution wins `0.6.1`. **There is no interpreter on which `pip
  install hmda-analyzer` yields `0.5.0`** — verified on Python 3.10 in a clean
  venv with a cold cache, where the bare install and the `>=0.6.0` pin both
  resolve to `0.6.1` (`__all__` = 33, `GeographyVintageError` and the three basis
  maps present). The claim is removed from `README.md`, the `hmda-analysis`
  `compatibility:` frontmatter, and the skill body in both places it appeared.
  The `>=0.6.0` floor stays, for the reason that is still true and that the
  surrounding text already gave: `0.6.0` is where the geography-vintage refusal
  first exists.
- **`llms.txt`: the PyPI user corrected from `Jaypatel1511` to
  `thejaypatel1511`.** `Jaypatel1511` is the **GitHub** handle; the PyPI account
  is `thejaypatel1511`, confirmed against the Maintainers panel of a published
  project page. The README was already correct. Both handles are now named
  explicitly so the two namespaces stop being conflated.
- **README: the `.agents/skills/` discovery claim corrected — Claude Code does
  not read that path.** The install intro said Claude Code, GitHub Copilot "and
  other spec-conformant agents all read" `.agents/skills/`. Claude Code does not:
  it scans `.claude/skills/`, and it loads these three skills only because
  `.claude-plugin/plugin.json` enumerates the paths. Verified on Claude Code
  **2.1.232**: a decoy skill in a project's `.claude/skills/` loaded while a
  decoy in the same project's `.agents/skills/` did not, and the string
  `.agents/skills` does not occur in the binary. The accurate sharer list is
  GitHub Copilot, Cursor, Codex, Gemini CLI, Antigravity, Amp, Cline, OpenCode
  and Warp — the list `gh skill install --help` gives (gh 2.92.0). Section (d),
  which is addressed to those agents, now says plainly that it is **not** for
  Claude Code; a Claude Code user who followed it got nothing, with no error.
- **README section (d)'s `cp -R` fixed — it failed as printed.** A fresh project
  has no `.agents/skills/`, so `cp -R` exited 1 with `No such file or directory`
  for exactly its intended audience. Section (c) already printed the equivalent
  `mkdir -p`; (d) now does too.
- **README: an upgrade path, which the file did not document at all.** `install`
  accepts the bare plugin name but `update` does not — `claude plugin update
  cdfi-superpowers` fails with `Plugin "cdfi-superpowers" not found`, while
  `cdfi-superpowers@cdfi-superpowers` succeeds. Both forms were run. The
  marketplace refresh that has to precede it is documented alongside.
- **Provenance lines now name the floor and the date, not the resolved point
  version.** `hmda-analysis` said "Verified this session: 0.6.0" and "both report
  v0.6.0"; `nmtc-eligibility` said "Verified this session (PyPI): nmtc-mapper
  0.4.2". Neither was wrong about what was verified, and both went stale the
  moment the packages released — `>=0.6.0` now resolves to `0.6.1` and `>=0.4.2`
  to `0.4.3`. This is a drift generator, not two typos, so the pattern changed:
  floor + verification date, with the resolved version marked as of that date.
  The `must read 0.6.0 or later` gate is untouched. (`nmtc-mapper` 0.4.3 changes
  no behaviour — wheel-diffed against 0.4.2, its sole change is a comment block
  in `data/schema.py`; every constant is byte-identical.)
- **`llms.txt`: `cdfi-benchmark` corrected from `0.2.0` to `0.2.1`.** It was the
  last stale version string in the repo — README, `references/package-index.md`
  and the skill body all already said `0.2.1`, and PyPI's latest is `0.2.1`
  (uploaded 2026-07-10). It is an index entry, not a floor.
- **`references/package-index.md`: the `hmda-analyzer` Python note made precise.**
  `>=0.6.0 (py>=3.9)` was true of the pin's resolution but not of `0.6.0` itself,
  which is `py>=3.11`. The cell now says which is which.

### Verified — the plugin loader reads the dot-prefixed path
Tested from the working tree before the other two skills were moved, then again
with all three moved (`claude plugin install` + `claude plugin details`):

- All three skills load from `.agents/skills/` and are invocable. **No mirror, no
  symlink, no `.github/skills` fallback was needed.**
- **The `skills` array in `plugin.json` is *not* the only thing binding skill
  locations.** With the array emptied entirely, the two skills still sitting in
  `skills/` continued to load, while the one in `.agents/skills/` did not. The
  loader globs the conventional `skills/` directory *in addition to* the explicit
  array; the array is what makes a **non-conventional** path load. Moving the
  directories is therefore necessary **and** sufficient only because the array was
  repointed with them — and leaving any copy behind in `skills/` would have
  double-loaded it. `skills/` is now removed outright.

### Known — noticed, not changed
- **`llms.txt` still pins `cdfi-benchmark 0.2.0`** against `>=0.2.1` everywhere
  else. Unchanged for the same reason as the last three releases: it belongs to
  the cdfi-peer-benchmark sync, and correcting it here would assert a verification
  that has not happened. (Recorded here for the **fourth** time.)
- **`gh skill install` requires `--allow-hidden-dirs` against this layout.**
  `gh skill` classifies `.agents/skills/` as a hidden directory and, without the
  flag, reports "no standard skills found, but 3 skill(s) exist in hidden
  directories" and installs nothing. This is a real cost of the move: the plain
  `gh skill install <repo> <skill>` form worked against the old `skills/` layout
  and now needs one extra flag. The README prints the flag. Not worked around,
  because the Copilot discovery paths are the point of the move.
- **Two `SKILL.md` files exceed the 500-line guideline** — `hmda-analysis` (730)
  and `nmtc-eligibility` (561). Both **pass** `agentskills validate`; the limit is
  a guideline the reference validator does not enforce. Left alone rather than
  cut, since trimming correct, executed content to hit a soft target is not a
  change this release is scoped to make.
- **`cdfi-superpowers` is not listed in `anthropics/claude-plugins-community`.**
  Checked this session against that repo's `marketplace.json` (2,281 plugins):
  zero occurrences of `cdfi`, `nmtc`, `hmda` or `Jaypatel1511`. The 2026-07-19
  submission never landed. No stale SHA pins the old layout — which is the only
  reason this release's path move carries no external breakage.

## 2026.7.6

### Changed
- **nmtc-eligibility synced to nmtc-mapper 0.4.2** (published to PyPI 2026-08-05). Verified against
  a clean-venv, cold-cache, isolated-`HOME` install of the published wheel; every executed block in
  the skill was re-run against it and **no figure moved**.
  - **Install floor raised `>=0.4.1` → `>=0.4.2`, and the floor paragraph gained its third
    reason.** A tract reaches LIC status by three routes; the CDFI Fund publishes the poverty and
    80%-AMI routes in the eligibility workbook's column C and the §45D(e)(5) high-migration-rural
    route in column N. Pre-0.4.2 read column C alone as the entire verdict while separately
    parsing, storing and surfacing column N as `is_high_migration_rural`. Re-derived from the live
    table this session: 1,422 tracts carry the high-migration-rural designation and **168 qualify
    on that route alone** — all non-metro, all in the (80%, 85%] MFI band. Those 168 were reported
    ineligible by a package simultaneously surfacing the evidence of their eligibility. This is the
    skill's own third-state rule — "a false 'ineligible' is exactly as damaging as a false
    'eligible'" — shipped as a defect in its own backing dependency, which is why the floor is
    load-bearing rather than version hygiene. 0.4.2 reads the verdict as **C or N**.
  - **Corrected the release history the sync was scoped from.** The CDFI Fund moved the C/N
    boundary in **July 2026**, folding the high-migration-rural route into column C and renaming
    that column's header. Against the workbook the loader downloads today the 168-tract divergence
    is therefore **no longer reproducible** (HMR-yes/column-C-no is now an empty set), and 0.4.1
    does not answer at all — its positional header validation raises `EligibilitySchemaError` and
    loads nothing (executed this session). The skill states both presentations rather than the
    unreachable one.
  - **Added an `is_high_migration_rural` diagnostic** at the field list, written to what is
    actually observable on a stale install: `EligibilitySchemaError` against the current workbook,
    or a self-contradicting `is_high_migration_rural=True` / `nmtc_eligible=False` against a cached
    pre-July-2026 one. Remedy named (upgrade) and checkable with tract `01013953500`, the first of
    the 168 — `nmtc_eligible=True`, `is_high_migration_rural=True`, `distress_level='lic'` on 0.4.2.
  - **The 1,408 OZ vintage-miss figure re-derived rather than carried forward.** Previously cited to
    the 0.4.1 Known Issues; independently recomputed this session as 1,408 of the 8,764 designated
    OZ tracts (16.1%) absent from the 85,395-row 2020-basis table. Figure holds on 0.4.2.
  - **`is_nmtc_native_area` re-verified** as `True`-count 0 across all 85,395 rows on 0.4.2;
    citation moved to the 0.4.2 Known Issues. Field retained — its removal is coordinated with
    nmtc-mapper 0.5.0.
  - **Geocoder failure-mode provenance corrected to 0.4.2**, with all four branches re-executed:
    agreement and no-match against the live Census endpoint, transport failure and ambiguous-address
    both induced. `0.4.0`/`0.3.4+` attributions elsewhere in the file are accurate history and were
    left as written.
- **Stale `nmtc-mapper` pins corrected in three places** — `README.md`, `llms.txt` and
  `references/package-index.md` all read `>=0.4.1` against the skill's new `>=0.4.2` floor; now
  `>=0.4.2`. Manifests to 2026.7.6 and the README version line with them.

### Noticed, not changed
- **`llms.txt` pins `cdfi-benchmark 0.2.0`** against `>=0.2.1` everywhere else in the repo. Different
  package, and the cdfi-peer-benchmark skill has not been verified against an install; correcting the
  string without that verification would assert a sync that has not happened. Left for that skill's
  own release. (Recorded here for the third time.)

## 2026.7.5

### Fixed
- **hmda-analysis: corrected a false safe-list.** 2026.7.4 stated that
  "`lending_by_county` and `lending_by_state` are likewise unaffected — county and state FIPS did
  not change at this boundary." **County FIPS did change at exactly that boundary.** Alaska retired
  `02261` (Valdez-Cordova) into `02063` (Chugach) + `02066` (Copper River), landing in the LAR at
  2021→2022. Verified against live LAR this session, full-state Alaska pulls with
  `limit_truncated=False` in both years: `02261` carries 323 rows in 2021 and 0 in 2022; `02063`
  and `02066` carry 0 in 2021 and 158 and 40 in 2022. A pooled 2021+2022 `lending_by_county`
  fragments one county into three rows. This was worse than over-warning: a safe-list broader than
  the safety, telling an AI to confidently pool a cut the package now refuses. `lending_by_state`
  remains correct and is still listed as unaffected. Scope is stated narrowly — one county at one
  boundary — so the correction does not over-swing into "all county work is unsafe."

### Added
- **hmda-analysis: the 2023→2024 boundary, which the skill did not know existed.** Connecticut
  replaced its eight legacy counties (`09001`…`09015`) with nine planning regions
  (`09110`…`09190`) for federal statistical use (87 FR 34235, 2022-06-06; Census lists it as the
  sole county-equivalent change of the 2020s), landing in the LAR at 2023→2024 and moving every CT
  tract GEOID's first five digits. It is a different shape from 2021→2022: there GEOIDs are reused
  for different ground (silent collision), here the key sets are disjoint (a pooled frame doubles
  rows). Confined to one state; the refusal is national, and the package's message says so and
  prices the cost.

### Changed
- **hmda-analysis synced to hmda-analyzer 0.6.0** (published to PyPI 2026-08-05). Verified against
  a clean-venv install of the published wheel; every figure below was re-read from it.
  - **The vintage section rewritten around the refusal.** In 0.5.0 the rule was an instruction an
    AI had to remember; in 0.6.0 the package enforces it. Six guarded geography-keyed aggregation
    sites across five public functions (`lending_by_tract`, `lending_by_county`,
    `lending_desert_score`, `racial_composition_by_tract`, and `lender_summary` — guarded twice,
    once per key) raise `GeographyVintageError`. `lending_by_state` is deliberately unguarded.
    Added a rule-zero prohibition on routing around it: no `try`/`except` that proceeds (every
    refusal subclasses `ValueError`, so a bare `except ValueError` catches it), no hand-rolled
    `groupby` to recover the declined number, no self-improvised crosswalk.
  - **The two refusals separated, because conflating them yields advice that does not work.**
    (1) *Unmapped year* — 2024 and 2025 have no cited tract basis, so pooling either with any other
    year refuses; excluding a state does not help, because the verdict is computed from the years
    the frame spans, never from the rows it contains. (2) *Two cited bases in one frame* — e.g. the
    county map across 2023→2024, where the refusal names the Connecticut cause. Both messages are
    quoted verbatim from the installed wheel. Also documents that which refusal fires is a function
    of the key, not the boundary: at 2023→2024 a tract-keyed call hits (1) while a county-keyed
    call hits (2), and only the county key surfaces the Connecticut text.
  - **"Filtering rows is never a way through" stated explicitly**, because it is the intuitive
    thing to try. Both refusals resolve the same two ways, both of which change the years rather
    than the rows: split at the boundary into two labelled panels (endorsed), or narrow with
    `vintage=` — which takes the *basis* year, not the data year.
  - **The bundled `tract_vintage_methodology.md` (242,085 bytes) named as authoritative.**
    `get_methodology_path` now takes a filename; the old no-argument call still returns
    `cra_proxy_methodology.md` (22,313 bytes) unchanged.
  - **`lender_vs_market` small-N suppression surfaced.** A silent 5-application threshold
    (`MIN_APPLICATIONS_FOR_RATE`) was dropping race groups entirely in 0.5.0 with nothing recording
    it; 0.6.0 discloses it in six columns, three per side, because the two frames are suppressed
    independently. The skill now requires surfacing them whenever the table is rendered, the same
    way it requires the CRA-proxy caveat — an absent group that is not named reads as a group with
    no lending. Verified on a 60-row frame: five protected classes suppressed market-side, 10
    applications, all named.
  - **`lending_desert_score` documented as it actually computes.** `is_lending_desert` is a
    conjunction (`app_percentile < 25` **and** `denial_rate > 0.15`), not a cut on `desert_score`;
    below `DESERT_TRACT_FLOOR` (5) tracts the flag is arithmetically unreachable and the call raises
    `UnreachableFlagError` rather than returning a fabricated `False`. No housing-unit figure is
    read anywhere — the "expected volume based on housing units" claim was removed from the package
    in 0.6.0 as unfounded, and the skill now forbids it in output. (It never appeared in this
    repo's prose; nothing had to be deleted.)
  - **`cra_proxy_distribution(include_purchased=True)` now raises `EmptyUniverseError`** on a frame
    with no action-6 rows — which is always, for API-loaded frames, since `API_ACTIONS_TAKEN` never
    fetches action 6. Purchased-loan analysis requires `load_from_file` with data obtained another
    way. The signature line also now shows the 0.6.0 keyword-only arguments.
  - **`limit=` documented as truncation, not sampling.** Every loaded frame carries
    `limit_truncated`, written even when `False`; under `load_range` it is per year and therefore
    not uniform across the frame. A truncated pull must never be described as a sample, and
    `limit_truncated=True` must be disclosed beside the number.
  - **Constants section added, with definition paths rather than re-export paths.** The three basis
    maps and `basis_year` are top-level exports; the thresholds are not.
    `MIN_APPLICATIONS_FOR_RATE`, `API_ACTIONS_TAKEN` and `TRUNCATED_COLUMN` are defined in
    `hmdaanalyzer.data.schema`; `DESERT_PERCENTILE_THRESHOLD`, `DESERT_DENIAL_RATE_FLOOR` and
    `DESERT_TRACT_FLOOR` in `hmdaanalyzer.geography_vintage`. The `analysis.disparity`,
    `analysis.geographic` and `data.loader` paths resolve to the same objects but are re-exports;
    citing them sends a reader to a file where the constant cannot be changed. `DESERT_TRACT_FLOOR`
    is *derived* from the percentile threshold at import, not configured.
  - **Python floor is now `>=3.11`** (0.5.0 was `>=3.9`), and the install section leads with it: on
    Python 3.10 or older a bare `pip install hmda-analyzer` does not fail — pip resolves backwards
    and silently installs 0.5.0, the version with none of the above. The skill now pins
    `"hmda-analyzer>=0.6.0"` and requires checking `h.__version__` before quoting any number.
  - All four new typed errors added to the "Data source & typed errors" and "Failure modes" lists.
- **hmda-analysis firewall: `denial_rate_by_income_band` added to the not-wrapped list.** Re-checked
  against 0.6.0's `__all__`, which grew 25 → 33. The eight additions are three basis maps, four
  exception classes and the `basis_year` helper — no new analysis function, so nothing *new* belongs
  behind the firewall. But `denial_rate_by_income_band` shipped in 0.5.0, was never named in the
  firewall paragraph, and was neither wrapped nor firewalled: it lives in
  `hmdaanalyzer.analysis.disparity` and its own docstring states its purpose as identifying
  "income-based disparities." Now firewalled, with the reasoning stated.
  `racial_composition_by_tract` was named in the prose but missing from the enumerated list; added.
  No firewalled function was wrapped; the descriptive/inferential firewall is unchanged.
- **README, `llms.txt`, `references/package-index.md`: stale package pins corrected.** All three
  pinned `nmtc-mapper 0.3.3` against the nmtc-eligibility skill's load-bearing `>=0.4.1` floor, and
  `hmda-analyzer 0.5.0`. Now `>=0.4.1` and `>=0.6.0` respectively, with the Python floor noted.
  Nothing in the nmtc-eligibility skill body was touched.
- **README now states the plugin version** (`2026.7.5`), which both manifests carried and it did
  not.

### Known — noticed, not changed
- `llms.txt` line 17 pins `cdfi-benchmark 0.2.0`, while the README, the cdfi-peer-benchmark skill,
  and the 2026.7.3 CHANGELOG entry all carry `>=0.2.1`. Same class of stale-index defect as the
  pins fixed above, but it belongs to the cdfi-peer-benchmark sync and was left for it rather than
  corrected here unverified.

## 2026.7.4

### Fixed
- **hmda-analysis: added the tract-vintage boundary rule.** HMDA LAR carries 2010 census tracts for
  data years 2018–2021 and 2020 census tracts from 2022 onward. The skill had no mention of vintage
  or tract boundaries, documented `lending_by_tract` without qualification, and its own "When to use"
  example (`2020–2023`) spanned the boundary — so an AI following it would produce a tract-level cut
  that silently merges two different geographies under identical GEOID strings. Confirmed empirically
  in King County WA, DC, and Fulton County GA (August 2026): 308 colliding GEOIDs in King County
  alone, ~71% of each year's rows on a colliding key, nothing raised. Added a non-negotiable
  tract-vintage section, corrected the example, annotated `lending_by_tract`, and added a caveat
  bullet. Also states explicitly what is *not* affected (`cra_proxy_distribution`, which classifies
  per-row; `lending_by_county` / `lending_by_state`, whose FIPS did not change) so the rule does not
  over-warn.
- No package version change. The underlying defect is tracked for `hmda-analyzer` 0.6.0, where
  `lending_by_tract` will fail loud on a vintage-spanning frame; this skill change is the interim
  guard for skill-mediated use.

## 2026.7.3

### Fixed
- **cdfi-peer-benchmark: added the missing annualization / period-basis disclosure.** The skill
  covered data quality, heuristic peer groups, and synthetic sample peers, but carried no reference
  to `cdfi-benchmark` 0.2.1's disclosed non-annualization of NIM, ROAA, and ROAE at interim report
  dates — the skill's core output. An AI following the prior text would compare an interim NIM
  against a peer median and state the level as fact, understated by up to ~4×. Added a
  non-negotiable period-basis rule (disclosure quoted verbatim from the package CHANGELOG), a
  caveat bullet, and a note marking the worked example's 12/31 `report_date` as the one basis at
  which the issue does not arise. No package version change; floor remains `cdfi-benchmark>=0.2.1`.

### Changed
- **Marketplace/plugin metadata, released here rather than under 2026.7.2.** Commits `542152c` and
  `ce37550` (July 18 2026) added `displayName`, `author`, `repository`, `category`, `keywords`, and
  `tags`, and expanded the plugin description — all after 2026.7.2 was cut, so they sat on `main`
  unversioned. No skill text, no analytical behavior, and no dependency floors changed. Recorded
  here so the version history reflects what actually shipped under each tag.

## 2026.7.2

- Synced `nmtc-eligibility` skill to nmtc-mapper 0.4.1. Install floor raised to
  `>=0.4.1`.
  - **Tri-state answer space (0.4.0):** `nmtc_eligible` is `Optional[bool]`.
    `None` / `"unknown"` means could-not-determine and is never "not eligible".
    New non-negotiable third-state rule; new `eligibility_status` four-way
    property; absent-tract worked example.
  - **Geocoder vintage bind (0.4.1):** the geocoder now resolves onto the
    eligibility table's 2020 tract basis (`schema.TRACT_VINTAGE`). Documented as
    data-source fragility context.
  - **OZ "No" is ambiguous:** a `Yes` may be reported as fact; a `No` cannot
    distinguish not-designated from a 2010/2020 tract-vintage miss (~16% of
    designations unreachable). Flagship example annotated accordingly.
  - **`is_nmtc_native_area` is always `False`** — no data source populates it; a
    `False` means "not determined", not "not a Native Area".
  - **FAQ citations re-pointed** to the current Feb 1 2024 version of the NMTC
    LIC ACS FAQ (was the superseded Sept 1 2023 version).
  - **Island Areas scope corrected:** not covered by the 2016-2020 ACS; the CDFI
    Fund publishes a separate territory file this package does not carry.
  - **Vintage-scope rule:** the three-window QLICI transition keyed to close
    date.

## 2026.7.1

- Synced `cdfi-peer-benchmark` skill to cdfi-benchmark 0.2.1 (leverage-ratio
  metric, real institution names, working name search, corrected efficiency
  ratio); examples re-executed against the published wheel.

## 2026.7.0 — Phase 1

Initial public skeleton — an AI skill layer over Jay Patel's published CDFI PyPI
portfolio. No new analytical code; skills install and call the existing packages.

### Added

- **Three skills**, each with executed worked examples and firm failure/caveat rules:
  - `nmtc-eligibility` — nmtc-mapper 0.3.3 + nmtc-screener 0.1.0.
  - `cdfi-peer-benchmark` — cdfi-benchmark 0.2.0 (bank CDFIs only; NaN-not-fabrication contract).
  - `hmda-analysis` — hmda-analyzer 0.5.0 (descriptive only; CRA-proxy with verbatim caveat; fair-lending firewall).
- **References**: `cdfi-industry-primer.md`, `data-source-map.md`,
  `package-index.md` (22 packages, PyPI-verified), `caveats-and-limits.md`.
- **Plugin packaging**: `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json` (single-plugin marketplace),
  `scripts/make_skills.sh` (builds `dist/*.skill` archives), `llms.txt`.

### Verified this session

- All cited PyPI versions checked against live PyPI JSON.
- Every skill code example executed in a fresh `/tmp` venv; real output pasted in.
- CRA-proxy caveat language copied verbatim from the package constant /
  bundled methodology, not paraphrased.

### Known gaps (flagged, not papered over)

- `nmtc-screener` PyPI metadata is bare; ownership inferred from its GitHub repo.
