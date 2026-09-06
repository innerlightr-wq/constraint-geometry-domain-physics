# Changelog

## v1.1.0 — September 2026 (Milestone 1: reference implementation)

- Added a small executable Python package, `src/constraint_geometry/`,
  implementing the exact binary-partition coordinate algebra, the Tier-1
  normal-form extraction, and a numerical shared-V family / held-out
  falsifiability test. No new theoretical claims: this makes existing,
  already-documented Tier-1 material reproducible rather than only
  asserted in prose.
- Added `tests/` (pytest) covering the exact coordinate identities, the
  normal-form extraction, and a synthetic falsifiability demonstration
  that must be able to both pass (a genuine shared potential) and fail
  (a deliberately mismatched pair).
- Added `examples/bernoulli_fisher.py`, an executable EXACT ALGEBRA
  example.
- Added `docs/software_scope.md`, separating what the software computes
  from what it deliberately never decides (domain embeddings, physical
  equivalence, pass/fail verdicts without a caller-supplied threshold).
- Added `pyproject.toml` and `conftest.py` for a reproducible `pytest`
  run with no install step required.
- Updated `README.md` and `REPOSITORY_MAP.md` to reflect the new files.
  The manuscript in `paper/` is unchanged and remains authoritative for
  all equations, terminology, and interpretations.

### Notes on this release

- This milestone deliberately excludes: the SXS/SDSS empirical
  equipartition-differential analysis, the Schwarzschild and
  acoustic-horizon potential examples, the gauge-coupling-running
  numerical example, an automatic Exact/Partial/Mismatch classifier, the
  full Compound-chart (Gudermannian-adjacent) machinery beyond what the
  exact identities require, and any Lean formalization. These remain
  open for later milestones.
- See `docs/software_scope.md` for the epistemic boundary the code is
  designed never to cross on its own.

## v1.0.0 — July 2026

- Initial public repository.
- Added conceptual synthesis note.
- Added framework documentation.
- Added examples for perturbative GR, flat ΛCDM, effective potentials, and Newtonian two-body mechanics.
- Added explicit non-claims, epistemic tiers, and safeguards.

### Notes on this release

- The manuscript is the authoritative source for all equations, terminology, interpretations, and limitations. Documentation files restate; they do not extend.
- Three cited companion notes do not yet have deposited DOIs. The gap is recorded in `bibliography_status.md` rather than filled with invented identifiers.
- The June 2026 relaxation note is recorded as superseded by its revised version; forward citations should use the revision.
- The Blanchet living review is cited in its current (2024) edition, which replaces the 2014 edition cited in earlier notes.
