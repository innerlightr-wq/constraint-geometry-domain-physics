# Constraint Geometry and Domain Physics

This repository accompanies the conceptual synthesis note:

**Constraint Geometry and Domain Physics: A Two-Layer Architecture for Binary Partition Diagnostics**
Elias De Jesús — Independent Researcher — July 2026
ORCID: [0009-0007-0190-9143](https://orcid.org/0009-0007-0190-9143)
DOI: [10.5281/zenodo.21695430](https://doi.org/10.5281/zenodo.21695430)

The note clarifies the division of labor between a universal binary-partition geometry and the domain-specific physics required to give that geometry empirical meaning.

---

## Overview

A conserved two-sector decomposition — a probability allocation, a mass fraction, an energy budget, a density partition, a ratio of operator norms — always makes the same small piece of geometry available. That availability is not a physical result. This note states what it is instead: constraint geometry supplies a constrained state space, a coordinate vocabulary, and a short list of exactly located intrinsic landmarks, while domain physics supplies the sectors, the normalization, the map from physical variables into the partition, the dynamics, and any empirical meaning a landmark may have. Neither layer produces a physical diagnostic alone, and a candidate diagnostic becomes scientifically meaningful only after independent justification or falsifiable testing of the map between them.

## The architecture

```
        Constraint geometry
                 +
          Domain physics
                 ↓
   Candidate physical diagnostic
                 ↓
     Independent test required
```

The final arrow is not decoration. A candidate is a candidate until the embedding is justified by domain physics or the diagnostic makes a prediction that could fail.

## Core partition definitions

$$a+b=1,\qquad h=\sqrt{ab},\qquad \chi=a-b,\qquad R=\frac{1}{1-\chi^{2}}=\frac{1}{4h^{2}},\qquad \xi=\operatorname{arctanh}\chi$$

with the exact constraint identity $4h^{2}+\chi^{2}=1$. The state coordinate is bounded, $\chi\in(-1,1)$, while the response is not, $R\in[1,\infty)$ — so a divergence in $R$ records approach to a partition boundary, not by itself a physical singularity.

## The main distinction

> Constraint geometry determines which relational structures and intrinsic landmarks are available. Domain physics determines which sectors are being partitioned, how physical variables map into the partition, how the system evolves, and whether any landmark has empirical meaning.

The landmark used throughout is the altitude–ratio crossing:

$$h=\frac{a}{b}\iff a=b^{3}\iff b^{3}+b-1=0$$

$$b_{*}\approx 0.6823278038,\qquad a_{*}\approx 0.3176721962,\qquad r_{*}=\frac{a_{*}}{b_{*}}\approx 0.4655712319$$

This is an **exact partition-space landmark and not a physical threshold by itself**. Its physical realization solves $F(X_{*})=r_{*}$ for a domain map $a/b=F(X)$: the geometry does not move, but $X_{*}$ moves whenever $F$ changes.

## Primary example: perturbative general relativity

The Einstein tensor separates exactly into its linear and higher-order parts, and the field equation rearranges so that matter and gravitational self-energy together form the effective source of the linear operator. Normalizing those two sectors and taking the schematic operator ratio as the embedding,

$$\frac{a}{b}=C,\qquad a=\frac{C}{1+C},\qquad b=\frac{1}{1+C}$$

the constraint geometry supplies $h=\sqrt{ab}=\sqrt{C}/(1+C)$, and imposing the intrinsic crossing gives

$$\frac{\sqrt C}{1+C}=C\quad\Longrightarrow\quad C(1+C)^{2}=1,\qquad C_{\mathrm{crit}}=0.4655712\ldots$$

Read this with all four qualifications:

- The Einstein equations supply the physical linear–nonlinear decomposition; the partition supplies the intrinsic crossing. Neither supplies the other.
- The compactness value inherits the uncertainty of the schematic embedding. If the sector ratio is more accurately $a/b=\alpha C$ with $\alpha$ unpinned by an order-of-magnitude estimate between gauge-dependent norms, then $C_{*}=r_{*}/\alpha$.
- No universal onset of nonlinear gravity is claimed. The higher-order sector is nonzero for every $C>0$ and grows smoothly.
- The value is **not** identified with a post-Newtonian breakdown threshold. See [`docs/terminology.md`](docs/terminology.md) on structural compactness versus the orbital post-Newtonian parameter — two different quantities that share the form $GM/(rc^{2})$.

## Paired example: flat ΛCDM

With $a=\Omega_{m}$, $b=\Omega_{\Lambda}$, the closure is a constraint of the Friedmann system and the embedding follows from the conservation laws rather than being chosen. Two landmarks appear on the same trajectory, and they fail in opposite ways.

**Meaning without occupancy.** The domain-derived landmark $R_{J}=3/2$ is the extremum of the partition-flow acceleration — an exact dynamical feature of the flow. The present universe is not there.

**Occupancy without meaning.** The cubic partition state is numerically close to the present matter–dark-energy split. But the independently derived flat-ΛCDM flow has

$$U(\chi)=-\tfrac{3}{2}\chi\quad\Longrightarrow\quad U'(\chi)=-\tfrac{3}{2}\ \text{everywhere,}$$

so the flow has no interior critical point and no domain mechanism selects the cubic state. The universe passes through it at ordinary speed.

$$\boxed{\ \text{meaning without occupancy}\ \neq\ \text{occupancy without meaning}\ }$$

Neither is sufficient for a physical diagnostic. Reporting only the second would look like a success; reporting only the first would look like a mechanism.

## Repository map

| Path | Contents |
| --- | --- |
| [`paper/`](paper/) | The manuscript (LaTeX source and PDF), its bibliography, and build notes |
| [`docs/`](docs/) | Framework overview, terminology, the five-step protocol, safeguards, epistemic tiers, prior-work map, limitations |
| [`examples/`](examples/) | Worked readings of perturbative GR, flat ΛCDM, effective potentials, and Newtonian two-body mechanics |
| [`figures/`](figures/) | Editable SVG diagrams of the architecture, diagnostic requirements, tiers, and the failure matrix |
| [`citation/`](citation/) | Suggested citation text and Zenodo deposit metadata |
| [`NON_CLAIMS.md`](NON_CLAIMS.md) | What the framework does not claim, and what it does provide |
| [`bibliography_status.md`](bibliography_status.md) | Internal bibliographic maintenance record |
| [`REPOSITORY_MAP.md`](REPOSITORY_MAP.md) | File-by-file description |

A full description of every file is in [`REPOSITORY_MAP.md`](REPOSITORY_MAP.md).

There is no executable research code in this repository. All results in the note are analytic, and the figures are documentation rather than computed output.

## Citation

De Jesús, E. (2026). *Constraint Geometry and Domain Physics: A Two-Layer Architecture for Binary Partition Diagnostics.* Zenodo. https://doi.org/10.5281/zenodo.21695430

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff); plain text is in [`citation/suggested_citation.txt`](citation/suggested_citation.txt).

## License

Paper and documentation are released under the **Creative Commons Attribution 4.0 International** license (CC BY 4.0). See [`LICENSE`](LICENSE). No software license is applied, because the repository contains no code.

## Status

Conceptual synthesis note. The manuscript introduces no new theorem, physical law, or empirical validation. It consolidates the architecture, terminology, safeguards, and epistemic boundaries developed across earlier work.
