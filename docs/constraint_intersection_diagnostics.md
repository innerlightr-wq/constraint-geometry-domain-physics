# Constraint-Intersection Diagnostics

This page documents a narrow, standard piece of mathematics — how two
constraints `F(x)=0` and `G(x)=0` relate to each other at a shared zero —
and how the intrinsic cubic serves as one worked reference example. It is
**not** a new theory, not a comparator framework, and not a universal
transversality score. The mathematics is standard (rank of a Jacobian, the
regular value theorem, exterior-algebra independence of covectors); the
only thing this page adds is a disciplined statement of what is and is not
invariant, so that a determinant or an angle is never silently promoted to
mean more than it does.

## Opening principle

**Mathematical equations alone do not determine whether two constraints
are "intra" or "inter."** That distinction depends on independently
justified provenance, subsystem boundaries, or modeling choices — it is a
**REPRESENTATIONAL CHOICE**, not an intrinsic algebraic invariant. Two
constraints can be written down and manipulated identically whether they
came from one governing law or two; nothing in the algebra records which.

- **INTRA**: a relation internal to one declared structure or subsystem —
  e.g. `a+b=1` treated as a single conserved-partition statement.
- **INTER**: a relation between two or more independently designated
  structures — e.g. treating `a+b=1` and `a=b^3` as two separately
  justified conditions and asking how they meet.

Given the same pair of equations, whether they are "intra" or "inter"
depends entirely on which of these two framings the modeler declares —
**not on anything recoverable from the equations by computation.**

## The four layers

### 1. Provenance

Stated by the modeler, not derived: which constraints were independently
justified (a conservation law, a separate measurement, a distinct governing
principle), and which are restatements of the same underlying condition.
This layer is outside the mathematics entirely.

### 2. Compatibility

At a candidate point `x*`:

$$F(x^*) = G(x^*) = 0$$

A statement about *values*, logically independent of the next layer.

### 3. Local independence / transversality

$$\operatorname{rank} D(F,G)\big|_{x^*} = 2$$

(for two independent scalar constraints on an appropriate ambient space),
equivalently, metric-free:

$$dF \wedge dG \neq 0 \quad \text{at } x^*$$

This is a **STANDARD MATHEMATICAL RESULT** (the regular value theorem /
exterior-algebra independence of covectors — see e.g. Guillemin & Pollack,
*Differential Topology*, or Milnor's differential topology notes). It is
invariant under any smooth local diffeomorphism of the ambient coordinates,
and under rescaling `F→αF, G→βG` for any nonzero `α,β` (constant or
smooth nonzero functions) — rank is preserved by left- and right-
multiplication by invertible matrices, which is exactly what both
operations amount to at the shared zero.

### 4. Conditioning / representation-sensitive diagnostics

Quantitative notions — `|det J|`, the Euclidean angle between gradients,
singular values, condition number, perturbation sensitivity — require
**additional declared structure** (a metric, a coordinate convention, a
normalization) before their numeric value means anything comparable across
representations. See the invariance table below.

**Qualitative transversality is invariant. Quantitative "strength" measures
are generally representation-dependent unless conventions are fixed.**

## Formal taxonomy

| Category | Condition | Coordinate/rescaling invariant? |
|---|---|---|
| A. Compatibility | `F(x*)=G(x*)=0` | Yes (a fact about the zero set) |
| B. Transversal / locally independent | `rank D(F,G)|_{x*}=2` | **Yes** |
| C. Degenerate / non-transversal | `rank D(F,G)|_{x*}<2` | **Yes** |
| D. Conditioning ("how transversal") | `|det J|`, angle, `σ_min`, `κ` | **No**, without declared structure |

## Invariance under constraint rescaling and coordinate change

Verified directly (see `examples/constraint_intersection_diagnostics.py`):

| Quantity | `F→αF, G→βG` (`α,β≠0`) | Smooth local diffeomorphism |
|---|---|---|
| Rank / transversality classification | **Invariant** | **Invariant** |
| `det J` | Scales exactly by `αβ` — **not invariant** | Not invariant |
| `cos θ` between gradients (magnitude) | **Invariant**, up to `sign(αβ)` | **Not invariant** — requires a declared metric |

`|det J|` must never be treated as a universal "strength of
transversality": multiplying a constraint equation by a large constant
changes it arbitrarily without changing the constraint's zero set at all.
The gradient-angle *magnitude* is more robust than it first appears — it
survives rescaling of the constraint functions themselves — but it still
requires a chosen metric/coordinate system to be numerically meaningful,
and a naively recomputed Euclidean angle after a genuine nonlinear change
of coordinates generally differs from the original value even though the
qualitative transversality classification does not change.

**Coordinate-change caution.** A coordinate map used to demonstrate this
must actually be a local diffeomorphism at the point of interest (nonzero
Jacobian determinant there) — a map like `v=y²` fails this at `y=0` and
proves nothing. See `examples/constraint_intersection_diagnostics.py` for
a map (`u=x, v=y+λx²`, Jacobian determinant `1` everywhere) that is valid
at every tested point, including a degenerate one.

## First-order limitation

Rank/gradient data is *first-order* information and cannot classify every
kind of degeneracy. Example:

$$F=y,\qquad G_1=y,\qquad G_2=y-x^2$$

At the origin, `grad F = grad G1 = grad G2 = (0,1)` — first-order data
cannot tell the *redundant* case (`G1` is literally the same constraint as
`F`) apart from the *tangent* case (`G2` touches `F=0` quadratically). Only
second-order information distinguishes them: `d²G1/dx²=0` while
`d²G2/dx²=-2`. The correct, narrow statement is that **first-order rank
data alone cannot classify every kind of degeneracy** — not that this
question is unresolved or requires global information in general; here, a
second derivative already suffices.

## The intrinsic cubic as a worked reference

$$F(a,b)=a+b-1,\qquad G_q(a,b)=a-b^q,\qquad q>0$$

$$J_q=\begin{pmatrix}1&1\\1&-qb^{q-1}\end{pmatrix},\qquad \det J_q=-(1+qb^{q-1})<0\ \text{for } q>0,\ b>0$$

**Every member `q>0` of this family is transversal against `a+b=1`.**
`q=3` is not selected by transversality — this negative result is
load-bearing (**EXACT ALGEBRA**, verified for representative `q` in the
test suite).

Separately, within the unconstrained power family `a=b^q` (not `a+b=1`):

$$h=\sqrt{ab}=b^{(q+1)/2},\qquad r=\frac{a}{b}=b^{q-1}$$

(using `r` for the ratio here, to avoid collision with this repository's
own `R = 1/(1-χ²)` response coordinate — a different object; see
`docs/terminology.md`.) Requiring `h≡r` for *every* `b>0` forces
`(q+1)/2=q-1`, i.e. **`q=3` uniquely** (**EXACT ALGEBRA**).

**These are two different facts, not one:**

- **TRANSVERSAL PROPERTY** — shared by every `q>0`.
- **FUNCTIONAL IDENTITY `h≡r`** — unique to `q=3` within this power-law
  family.
- **NORMALIZATION `a+b=1`** — selects one positive representative point on
  the `q=3` curve, `(a_*,b_*)=(\psi^{-3},\psi^{-1})`.
- **PHYSICAL SIGNIFICANCE OF `R*≈0.465571231876`** — **NOT ESTABLISHED**.

`q=3` should not be called "the transversal control case" — every `q>0`
is equally transversal, so that phrasing would misattribute a privilege
`q=3` doesn't have on that axis. The accurate description: **a worked
reference member of a transversal family that also has the unique `h≡r`
functional identity.**

## What this page does not claim

- That transversality or rank theory is new mathematics — it is
  **STANDARD MATHEMATICAL RESULT** throughout.
- That `q=3` is privileged by transversality — it is not (every `q>0`
  qualifies).
- That "intra"/"inter" are intrinsic algebraic categories — they are a
  **REPRESENTATIONAL CHOICE**, stated as such above.
- That `R*` has any physical meaning — **NOT ESTABLISHED**, consistent
  with `NON_CLAIMS.md` and every prior audit in this repository.

See also [`terminology.md`](terminology.md), [`epistemic_tiers.md`](epistemic_tiers.md),
[`safeguards.md`](safeguards.md), and [`state_dimension.md`](state_dimension.md)
(a related, separately-scoped diagnostic distinction for dynamical systems
rather than static constraint intersections).
