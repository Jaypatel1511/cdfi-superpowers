# Changelog

All notable changes to `cdfi-superpowers`. Versioning is CalVer (`YYYY.M.MINOR`).

## 2026.7.0 — Phase 1

Initial public skeleton — an AI skill layer over Jay Patel's published CDFI PyPI
portfolio. No new analytical code; skills install and call the existing packages.

### Added

- **Three skills**, each with executed worked examples and firm failure/caveat rules:
  - `nmtc-eligibility` — nmtc-mapper 0.3.3 + nmtc-screener 0.1.0.
  - `cdfi-peer-benchmark` — cdfi-benchmark 0.2.0 (bank CDFIs only; NaN-not-fabrication contract).
  - `hmda-analysis` — hmda-analyzer 0.5.0 (descriptive only; CRA-proxy with verbatim caveat; fair-lending firewall).
- **References**: `cdfi-industry-primer.md`, `data-source-map.md`,
  `package-index.md` (21 packages, PyPI-verified), `caveats-and-limits.md`.
- **Plugin packaging**: `.claude-plugin/plugin.json`,
  `.claude-plugin/marketplace.json` (single-plugin marketplace),
  `scripts/make_skills.sh` (builds `dist/*.skill` archives), `llms.txt`.

### Verified this session

- All cited PyPI versions checked against live PyPI JSON.
- Every skill code example executed in a fresh `/tmp` venv; real output pasted in.
- CRA-proxy caveat language copied verbatim from the package constant /
  bundled methodology, not paraphrased.

### Known gaps (flagged, not papered over)

- The build brief referenced 22 packages; 21 were located empirically. The 22nd
  could not be found (no matching GitHub repo, no guessable PyPI name).
- `nmtc-screener` PyPI metadata is bare; ownership inferred from its GitHub repo.
