# Changelog

All notable changes to `cdfi-superpowers`. Versioning is CalVer (`YYYY.M.MINOR`).

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
