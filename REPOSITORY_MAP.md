# Repository Map

A file-by-file description of the repository.

## Top level

| File | Description |
| --- | --- |
| `README.md` | Landing page: overview, architecture, core definitions, the two worked headline examples, repository map, citation, license, status. |
| `LICENSE` | CC BY 4.0 declaration for the paper and documentation, with suggested attribution. No software license is applied. |
| `CITATION.cff` | Machine-readable citation metadata (Citation File Format 1.2.0), including ORCID, keywords, and the deposit DOI. |
| `.gitignore` | LaTeX build artifacts, editor and OS noise. The release PDF is explicitly retained. |
| `CHANGELOG.md` | Release history, beginning with v1.0.0, plus notes on unresolved citations and superseded references. |
| `CONTRIBUTING.md` | What contributions are welcome, and the four items a new domain application must identify. |
| `NON_CLAIMS.md` | Ten explicit non-claims, and five things the framework does provide. |
| `REPOSITORY_MAP.md` | This file. |
| `bibliography_status.md` | Internal bibliographic maintenance record: verified DOIs, unresolved DOIs, supersession notes. The only place unresolved bibliographic gaps are tracked, alongside `citation/zenodo_metadata.md`. |
| `pyproject.toml` | Minimal packaging metadata for `src/constraint_geometry` (numpy runtime dependency; pytest and scipy as test-only extras). |
| `conftest.py` | Pytest bootstrap: makes `src/constraint_geometry` importable without an install step, so `pytest` from the repository root works immediately. |

## `paper/`

| File | Description |
| --- | --- |
| `constraint_geometry_domain_physics.tex` | Authoritative LaTeX source of the manuscript. All equations, terminology, and limitations derive from this file. |
| `constraint_geometry_domain_physics.pdf` | Compiled release PDF, free of editorial markers and unresolved citation flags. |
| `references.bib` | BibTeX form of the bibliography, provided for reuse. The manuscript itself uses an embedded `thebibliography` environment. |
| `build_notes.md` | How to compile, which packages are required, and the pre-release checks. |

## `src/constraint_geometry/`

Reference implementation. Pure `numpy`; no domain-physics inputs, no
default pass/fail thresholds. See [`docs/software_scope.md`](docs/software_scope.md)
for the boundary between what this code computes and what it leaves as a
caller-supplied judgment.

| File | Description |
| --- | --- |
| `__init__.py` | Package docstring and module listing. |
| `coordinates.py` | Exact binary-partition coordinate algebra: `a,b`, `h`, signed/unsigned `chi`, `R`, `xi`, `theta`, the Gudermannian bridge. |
| `normal_form.py` | Tier-1 normal-form extraction `V_eff^(1)(chi)` from a supplied trajectory. |
| `falsifiability.py` | Numerical shared-V family test and held-out prediction test. Returns residuals only; `pass_fail` requires an explicit, non-defaulted threshold. |

## `tests/`

| File | Description |
| --- | --- |
| `test_identities.py` | Exact coordinate identities (`4h^2+chi^2=1`, `R=1/(1-chi^2)=1/(4h^2)`, `chi=tanh(xi)`, `theta=asin(chi)=gd(xi)`, `R=cosh(xi)^2`) at multiple interior points, including near-boundary and both chi signs. |
| `test_normal_form.py` | Normal-form extraction verified against trajectories with a known analytic derivative; boundary guard tests. |
| `test_family_test_synthetic.py` | The central falsifiability demonstration: synthetic trajectories from a shared potential collapse to a small residual, while trajectories from a deliberately mismatched potential are rejected with a materially larger one. |
| `test_gauge_running.py` | Tests for the gauge-coupling-running adversarial example: exact partition algebra, the closed-form cross-check, exact separability (`V=S^2*v(chi)`), the lambda^2 scale-transformation law, non-collapse of a genuine different-S family (with a fixed-S control that does collapse), and the S-normalization rescue attempt. |
| `test_gauge_reparameterization.py` | Tests for the positive-time-reparameterization example: the reduced `chi(tau)` equation, direction invariance under `S>0` on a dense grid, `chi(tau)` collapse vs. `chi(t)` non-collapse across different-`S0` trajectories, `K`-conservation (with explicit handling of the singular locus), fixed-point/stability preservation under positive `S`, and `V_eff` sign blindness. |

## `docs/`

| File | Description |
| --- | --- |
| `framework_overview.md` | The two-layer architecture in prose: what the constraint layer supplies, what the domain layer supplies, and what their intersection means. |
| `terminology.md` | Definitions of the fifteen terms used consistently across the repository, including the structural-versus-orbital compactness distinction. |
| `protocol.md` | The five-step protocol, with what must be supplied, what can go wrong, and what evidence would suffice at each step. |
| `safeguards.md` | Nine safeguards against the characteristic failure modes of partition-based reasoning. |
| `epistemic_tiers.md` | The three-tier classification: exact mathematics, domain diagnostic, speculative interpretation. |
| `prior_work_map.md` | How the note relates to eight earlier papers, with novelty stated conservatively. |
| `limitations.md` | What the note does not settle, and what would be required to settle it. |
| `software_scope.md` | What `src/constraint_geometry` computes (formally defined operations) versus what it deliberately never decides (domain embeddings, physical equivalence, pass/fail verdicts without a caller-supplied threshold). |
| `state_dimension.md` | Constraint-state dimension (`chi`, relative composition) versus domain-dynamical-state dimension (`(chi,S)`, required to close the one-loop gauge-running system) — the distinction between algebraic separability of a potential's shape and autonomous reduction of its dynamics. Also covers projected-orbit dimension, rate, direction, and why the existing `V_eff` normal form is direction-blind. |

## `examples/`

| File | Description |
| --- | --- |
| `perturbative_gr.md` | The primary example: exact operator decomposition, schematic norm ratio, the cubic, and the normalization ambiguity. |
| `lcdm.md` | The paired failure modes, the ordered-branch issue, and the linear Fisher potential. |
| `effective_potentials.md` | The Fisher kinetic skeleton, the universal-denominator/contextual-numerator split, and why single-trajectory extraction is tautological. |
| `newtonian_two_body.md` | The cleanest empty case: an exact embedding with a physically meaningless landmark. |
| `bernoulli_fisher.py` | Executable EXACT ALGEBRA example: the Bernoulli Fisher information `I_F(p)=1/[p(1-p)]` re-expressed as `1/h^2 = 4R` in partition coordinates. Runs directly with `python examples/bernoulli_fisher.py`. |
| `gauge_running.py` | Executable adversarial example: gauge-coupling running as a test of the autonomous-partition-potential hypothesis. Derives the closed `(chi,S)` system, the separable closed-form potential, the exact lambda^2 scale-transformation law, and an INFORMATIVE NEGATIVE RESULT (no autonomous `V(chi)` fits the family) with a passing control. Runs directly with `python examples/gauge_running.py`. |
| `gauge_reparameterization.py` | Executable example: the positive state-dependent reparameterization `d(tau)=S dt` that makes the reduced `chi(tau)` flow autonomous, the conserved orbit label `K`, the direction comparator `D(chi)`, and `V_eff` sign blindness under velocity reversal. Reuses `gauge_running.py`'s domain model. Runs directly with `python examples/gauge_reparameterization.py`. |

## `figures/`

All figures are hand-written, editable SVG — not screenshots, and not computed output.

| File | Description |
| --- | --- |
| `architecture_diagram.svg` | Constraint geometry plus domain physics, yielding a candidate diagnostic that requires an independent test. |
| `diagnostic_requirements.svg` | The three simultaneous requirements for a diagnostic. |
| `epistemic_tiers.svg` | The three tiers, stacked vertically. |
| `landmark_failure_matrix.svg` | A 2×2 of domain-derived meaning against empirical occupancy, with the four cases placed. |

## `citation/`

| File | Description |
| --- | --- |
| `suggested_citation.txt` | Plain-text citation. |
| `zenodo_metadata.md` | Metadata prepared for the Zenodo deposit record, including related identifiers and notes. |
