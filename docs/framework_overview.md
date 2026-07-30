# Framework Overview

## The problem the architecture solves

Normalize any two positive quantities by their sum and you get a binary partition. Because the operation is always available, the geometry that comes with it is always available too — and that creates a specific hazard. The same coordinates, the same identities, and the same landmarks will recur across unrelated domains, and their recurrence will look like a discovery when it is in fact an artifact of arithmetic.

The architecture is a way of keeping straight which parts of a result came from the geometry, which came from the physics, and which came from neither.

$$\text{constraint geometry}\;+\;\text{domain physics}\;\longrightarrow\;\text{physical diagnostic}$$

## The constraint layer

Supplies, for any partition whatsoever:

- $a+b=1$ with $a,b>0$ — the constraint itself
- $h=\sqrt{ab}$ — the Thales altitude, the geometric mean of the sectors
- $\chi=a-b$ — the signed asymmetry, bounded on $(-1,1)$
- $R=(1-\chi^{2})^{-1}$ — the response, equal to $1/(4h^{2})$, unbounded above
- $\xi=\operatorname{arctanh}\chi$ — the rapidity, unbounded in both directions
- exact identities among these coordinates, chiefly $4h^{2}+\chi^{2}=1$
- intrinsic relational landmarks — loci specified in these coordinates alone

The layer is exact, parameter-free, and empty of physics. Nothing in it refers to any physical system. The apex $h=\tfrac12$ at $\chi=0$ and the altitude–ratio crossing $a=b^{3}$ are on the same footing: both are facts about a constrained pair of numbers.

The bounded/unbounded split deserves separate emphasis, because it is a frequent source of overreading. The state coordinate is bounded while the response and rapidity are not. A divergence in $R$ therefore records approach to a partition boundary in whatever coordinate the domain supplies. It is not, by itself, evidence of a physical singularity.

## The domain layer

Supplies, and can only be supplied by the domain:

- **The identity of the sectors.** What, physically, $a$ and $b$ are.
- **Conservation or closure.** Why those two sectors exhaust a fixed total — a conservation law, a closure relation, an exact operator decomposition, a definitional completeness. Not "because they were divided by their sum."
- **Normalization.** Including any gauge, slicing, or norm choice the fractions depend on.
- **The map** $a/b=F(X)$ from a physical variable into the partition.
- **Dynamics.** The trajectory through the partition manifold, if the system evolves.
- **Admissible physical range.** The bounds the domain imposes, which are usually narrower than $[0,1]$.
- **Empirical interpretation.** Whether a landmark names anything observable.

## The intersection

A physical landmark satisfies

$$F(X_{*})=r_{*}$$

where $r_{*}=a_{*}/b_{*}$ is the intrinsic partition ratio at the landmark. Read this equation carefully, because the whole architecture is in it:

- $r_{*}$ is **fixed by the geometry**. For the altitude–ratio crossing, $r_{*}=\psi^{-2}\approx 0.4655712319$, always, in every domain, forever.
- $X_{*}$ **depends entirely on the embedding**. Change $F$ and the physical location of the landmark moves, even though the geometry has not moved at all.

The consequence is the central safeguard of the framework: given any target value $X_{0}$, the embedding $F(X)=r_{*}X/X_{0}$ places the landmark exactly at $X_{0}$. Numerical agreement between a landmark and an observation is therefore worthless unless $F$ was fixed, in full, by domain physics before the comparison was made.

## Three objects to keep apart

1. **The intrinsic geometric marker.** The locus $a=b^{3}$, with fixed values $(a_{*},h_{*},b_{*})=(\psi^{-3},\psi^{-2},\psi^{-1})$. Exact, domain-free, no physical content.
2. **The domain-specific embedding.** The map $a/b=F(X)$. This is where all the physics of the identification lives, and where all the freedom to be wrong lives.
3. **The physical interpretation.** A claim that $X_{*}$ names a transition, a bound, a degradation, an observable clustering. Requires evidence beyond (1) and (2).

Conflating (1) with (3) is the characteristic error the framework exists to prevent.

## Two independent things a landmark can lack

A landmark can have a domain-derived **mechanism** — the domain distinguishes that state for its own reasons — and it can have **occupancy** — the system is observed at or near it. These are supplied by different layers and neither implies the other. The flat-ΛCDM example in [`../examples/lcdm.md`](../examples/lcdm.md) exhibits one landmark of each kind on a single trajectory:

$$\boxed{\ \text{meaning without occupancy}\ \neq\ \text{occupancy without meaning}\ }$$

Neither is sufficient. A diagnostic needs both, plus an embedding that was not chosen to produce them.

## What the framework is for

Not derivation. Organization with declared seams: a fixed constrained state space, a coordinate vocabulary that translates between bounded, hyperbolic, and response descriptions, a short list of exactly located landmarks, and a protocol that makes the physical content — and the burden of proof — reside entirely in the embedding.

A domain in which every intrinsic landmark turns out to be a transit marker is a domain whose physics is not organized by its partition structure. That is a result about the domain, stated in a common language, and worth recording.
