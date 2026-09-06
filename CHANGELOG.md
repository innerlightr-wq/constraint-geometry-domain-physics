# Changelog

## Milestone 3 — September 2026: reparameterization and direction-rate audit

- Added `examples/gauge_reparameterization.py` and
  `tests/test_gauge_reparameterization.py`, extending the Milestone-2
  gauge-running example with a positive state-dependent time
  reparameterization (`d(tau)=S dt`, `S>0`).
- Derived and verified the reduced, autonomous one-dimensional
  `chi(tau)` flow, and the conserved orbit label `K` (a first integral
  of the full `(chi,S)` system, undefined only at the reduced flow's own
  equilibrium and never silently evaluated there).
- Verified positive-`S` direction invariance: `sign(dchi/dt) =
  sign(dchi/dtau) = D(chi)` for `S>0`, on a dense deterministic grid
  (zero mismatches). This is a standard dynamical-systems result
  (positive-scalar orbital equivalence / Sundman-type time-rescaling),
  not presented as novel — only its specific closed form for this
  domain model is new content here.
- Verified that the repository's existing effective-potential normal
  form is direction-blind (`V_eff(chi,+v)=V_eff(chi,-v)`, built from
  squared velocity), and that the signed comparator `D(chi)` is a
  complementary, non-redundant channel relative to that specific
  existing tool — not multiplied into `V_eff`, not a replacement for it.
- Made explicit, and kept carefully unconflated: full state dimension
  `(chi,S)=2`, required for coupling reconstruction and evolution in
  the original RG parameter `t`, versus reduced autonomous
  `chi`-orbit dimension `=1`, holding only after the positive
  reparameterization.
- Added a "Projected orbit dimension, rate, and direction" subsection
  to the existing `docs/state_dimension.md` (no new directionality
  document created).
- No empirical data introduced; no claim of empirical validation; no
  claim of novelty for time reparameterization, orbital equivalence,
  phase-line direction, or sign/magnitude decomposition, all of which
  are standard dynamical-systems mathematics.

## Milestone 2 — September 2026: gauge-coupling-running adversarial example

- Added `examples/gauge_running.py` and `tests/test_gauge_running.py`, an
  adversarial test of the autonomous one-dimensional partition-potential
  hypothesis (docs/protocol.md, Step 5) against gauge-coupling running at
  one loop, reusing the Milestone-1 API unchanged.
- Derived the closed `(chi, S)` system for the one-loop running equations
  and independently re-derived the closed-form extracted potential,
  cross-checked against the source paper's own reported equation.
- Demonstrated exact `S^2` scaling of the extracted normal form under the
  ratio-preserving rescaling `alpha -> lambda*alpha` (`chi` fixed).
- Demonstrated failure of autonomous chi-only dynamics: a genuine
  different-`S` family does not collapse under the shared-V family test,
  while a deliberately constructed fixed-`S` control does — an
  INFORMATIVE NEGATIVE RESULT for the autonomous-partition-potential
  hypothesis in this domain, not a claim about gauge physics in general.
- Retained an explicit distinction, throughout the code and in the new
  `docs/state_dimension.md`, between ALGEBRAIC SEPARABILITY
  (`V(chi;S) = S^2 * v(chi)`, which holds exactly) and AUTONOMOUS
  DYNAMICAL REDUCTION (`dchi/dt = F(chi)` alone, which does not).
- Added `docs/state_dimension.md`, distinguishing constraint-state
  dimension (`chi`) from domain-dynamical-state dimension (`(chi,S)`, for
  this model) as a per-domain structural finding, not a universal claim.
- No empirical data introduced; no claim of empirical validation.

## Milestone 1 — September 2026: reference implementation

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
