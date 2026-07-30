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

## `paper/`

| File | Description |
| --- | --- |
| `constraint_geometry_domain_physics.tex` | Authoritative LaTeX source of the manuscript. All equations, terminology, and limitations derive from this file. |
| `constraint_geometry_domain_physics.pdf` | Compiled release PDF, free of editorial markers and unresolved citation flags. |
| `references.bib` | BibTeX form of the bibliography, provided for reuse. The manuscript itself uses an embedded `thebibliography` environment. |
| `build_notes.md` | How to compile, which packages are required, and the pre-release checks. |

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

## `examples/`

| File | Description |
| --- | --- |
| `perturbative_gr.md` | The primary example: exact operator decomposition, schematic norm ratio, the cubic, and the normalization ambiguity. |
| `lcdm.md` | The paired failure modes, the ordered-branch issue, and the linear Fisher potential. |
| `effective_potentials.md` | The Fisher kinetic skeleton, the universal-denominator/contextual-numerator split, and why single-trajectory extraction is tautological. |
| `newtonian_two_body.md` | The cleanest empty case: an exact embedding with a physically meaningless landmark. |

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
