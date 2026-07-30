# Bibliographic Status

Internal maintenance record. This is the only public file in the repository that tracks unresolved bibliographic information; alongside `citation/zenodo_metadata.md`, it exists so that the manuscript, the README, and the documentation can stay free of unresolved placeholders.

**No DOI value in this repository has been invented.** Where a deposit identifier does not yet exist, the entry is listed below as unresolved and the manuscript cites the work without an identifier.

## This work

| Field | Value |
| --- | --- |
| Title | Constraint Geometry and Domain Physics: A Two-Layer Architecture for Binary Partition Diagnostics |
| DOI | 10.5281/zenodo.21695430 |
| Status | Verified |

## Verified DOI entries

Author's own work:

| Short key | Work | DOI |
| --- | --- | --- |
| `TwoFace` | The Two-Face Problem: A Practitioner's Guide to Bridging Inconsistencies Across Physics | 10.5281/zenodo.20221967 |
| `EffPot` | Two-Face Series: Effective Potentials on the Binary Partition Manifold | 10.5281/zenodo.21430864 |
| `IntrinsicCubic` | The Partition-Intrinsic Cubic: The Unique Altitude–Ratio Crossing, Supergolden Coordinates, and Algebraic Evaluation on the Thales Partition Manifold (Version 3) | 10.5281/zenodo.21543445 |
| `CubicThreshold` | The Cubic Compactness Threshold in Perturbative General Relativity | 10.5281/zenodo.20564050 |
| `NormNulls` | Two Normalization Nulls and the Tests That Tell Them Apart | 10.5281/zenodo.20774968 |
| `Newtonian2Body` | Newtonian Two-Body Gravity on the Thales Semicircle | 10.5281/zenodo.18496501 |
| `DynSelSuperseded` | Dynamical Selection of the Cubic Compactness Threshold (June 2026) — **superseded**, see below | 10.5281/zenodo.20603097 |

External literature:

| Short key | Work | DOI |
| --- | --- | --- |
| `Blanchet2024` | L. Blanchet, "Post-Newtonian theory for gravitational waves," *Living Reviews in Relativity* **27**, 4 (2024) | 10.1007/s41114-024-00050-z |
| `Planck18` | Planck Collaboration, "Planck 2018 results. VI. Cosmological parameters," *A&A* **641**, A6 (2020) | 10.1051/0004-6361/201833910 |

Monographs cited without DOI, by convention: Wald, *General Relativity* (1984); Misner, Thorne & Wheeler, *Gravitation* (1973); Landau & Lifshitz, *The Classical Theory of Fields*, 4th ed. (1975); Choquet-Bruhat, *General Relativity and the Einstein Equations* (2009); Amari & Nagaoka, *Methods of Information Geometry* (2000); Lovelock, *J. Math. Phys.* **12**, 498 (1971). The OEIS entry A000930 is cited by URL.

## Missing DOI entries

The following three companion notes are cited in the manuscript without an identifier, because none has been supplied:

| Short key | Work | Status |
| --- | --- | --- |
| `ReverseThales` | Iterated Similarity Composition and the Structure of the Einstein Field Equations: A Reverse Thales Construction | DOI not yet available |
| `PartitionFlow` | Matter–Dark-Energy Balance as a Partition Flow: Velocity, Acceleration, and Constant Rapidity in Flat ΛCDM | DOI not yet available |
| `AltitudeRelax` | Altitude–Ratio Relaxation on the Thales Partition Manifold: the Cubic Compactness Threshold as a Robust Interior Attractor for a Class of Imbalance-Driven Flows | DOI not yet available |

These records should be updated after the final Zenodo deposits are available. Do not invent DOI values.

`PartitionFlow` is load-bearing: it supplies the cosmological flow identities, the landmark $R_{J}=3/2$, the rapidity identity, the linear Fisher potential, and the redshift placement of the landmarks — that is, the entire ΛCDM section. `AltitudeRelax` is load-bearing for the corrected relaxation-class statement. Both should be prioritized when depositing.

## Supersession and edition notes

1. **The June 2026 dynamical-selection note is superseded.** `DynSelSuperseded` (10.5281/zenodo.20603097) is superseded by `AltitudeRelax`. The revision withdraws the $C(1-C)$ prefactor and replaces the "dynamically selected" framing with the attracting equilibrium of a class of imbalance-driven relaxations. Cite the June version only for provenance.
2. **The revised relaxation note should be cited for forward use.** Any new work that needs the relaxation result should cite `AltitudeRelax`, so that the withdrawn constructions are not carried forward. Earlier notes in the programme that cite the June version should be updated.
3. **Blanchet 2024 replaces the older 2014 review citation.** The current edition (*Living Rev. Relativ.* **27**, 4, 2024) is a revised, updated, and expanded version of the 2014 edition (*Living Rev. Relativity* **17**, 2). The two should not be cited side by side.
4. **No numerical post-Newtonian compactness threshold is attributed to Blanchet.** The review supports a qualitative loss of accuracy as merger is approached. It supplies no threshold value, and none is attributed to it anywhere in this repository. An earlier note in the programme attributed a numerical range to that review; that attribution should be weakened to the qualitative form or removed.

## Verification checklist before any new deposit

- [ ] Every DOI resolves.
- [ ] No entry cites two editions of the same living review.
- [ ] Superseded works are labelled as such at the point of citation.
- [ ] No numerical value is attributed to a source that does not state it.
- [ ] Unresolved identifiers appear only in this file and in `citation/zenodo_metadata.md`.
