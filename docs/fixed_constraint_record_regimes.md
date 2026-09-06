# Fixed-Constraint Record Regimes

This note records a controlled comparison inside one fixed Pythagorean
constraint system. The ambient geometry, admissibility class, and
chronological height are held fixed while the target and observable are
varied. The result is a comparison of record regimes, not a universal
theorem about target arithmetic.

Every quantitative claim below is standard Diophantine approximation on a
conic (Euclid parametrization, Pell equations, best-approximation theory).
What this note adds is only the side-by-side comparison — the fact that
two independently-solved extremal problems, run over the *identical*
constraint/admissibility/height triple, produce visibly different record
statistics. This is a **REPOSITORY-SPECIFIC SYNTHESIS** of standard
results, not new mathematics, and not a universal rule.

## The control tuple

Notation: `(C, A, H; P, O)` where `C` is the ambient constraint geometry,
`A` the admissible state/arithmetic class, `H` the height/cost ordering,
`P` the target, and `O` the observable.

For the control held fixed throughout this note:

- **`C`**: `a²+b²=c²`, the rational points of the open quarter circle.
- **`A`**: primitive Pythagorean triples via Euclid parameters
  `a=m²-n², b=2mn, c=m²+n²`, with `m>n≥1, gcd(m,n)=1, m-n` odd.
- **`H`**: chronological ordering by hypotenuse `c`.

**`C`, `A`, and `H` are held identically fixed in the balance-vs-boundary
comparison below.** This is the central methodological control: only `P`
(the target) and `O` (the observable) change between the two cases.

## Regime A: balance

Target `P_bal=(1/\sqrt2,1/\sqrt2)`; observable `\Delta_k=|b-a|/c`.

Record minima of `\Delta_k` occur exactly on the Pell spine `|b-a|=1`,
with hypotenuse chronology

$$c_1=5,\quad c_2=29,\quad c_{j+1}=6c_j-c_{j-1}$$

and `c_{j+1}/c_j\to\lambda=3+2\sqrt2` (**STANDARD / ESTABLISHED RESULT** —
the Pell equation `x^2-2y^2=\pm1`). Record count `N_P(C)\sim\log C/\log\lambda`.
Matched first-order target distance `\epsilon_{bal}(c_j)\sim1/(\sqrt2\,c_j)`.
Scaled envelope `E_{bal}(C)=C\cdot\min_{c(T)\le C}\epsilon_{bal}(T)` satisfies

$$\liminf E_{bal}=1/\sqrt2,\qquad \limsup E_{bal}=\lambda/\sqrt2$$

**Description**: a geometrically sparse chronology with persistent
multiplicative envelope oscillation. This is a property of *this* target
under *this* control, not a claim that every quadratic-irrational target
behaves the same way.

## Regime B: boundary

Target: the coordinate boundary/pole. Boundary defect `g=c-\max(a,b)`,
`w=g/c`.

Record minima of `w` occur exactly on `g=1`, equivalently `m=n+1`, giving
the record family

$$(a_n,b_n,c_n)=(2n+1,\ 2n(n+1),\ 2n^2+2n+1)$$

(**ESTABLISHED RESULT** — an exact closed form, direct from `m=n+1` in
the Euclid parametrization). Record count `N_B(C)\sim\sqrt{C/2}`; relative
spacing `c_{n+1}/c_n\to1`. Matched first-order angular distance
`\epsilon_{pole}(c_n)\sim\sqrt2/\sqrt{c_n}`. Scaled envelope
`E_{pole}(C)=\sqrt C\cdot\min_{c(T)\le C}\epsilon_{pole}(T)\to\sqrt2`.

**Description**: a relatively dense chronology with collapsing envelope
oscillation. Again, a property of *this* target under *this* control, not
a claim that every rational target behaves the same way.

## Comparison table

| Feature | Balance | Boundary |
|---|---|---|
| Ambient constraint `C` | `a²+b²=c²` | `a²+b²=c²` |
| Admissible class `A` | primitive triples, `m-n` odd | primitive triples, `m-n` odd |
| Height ordering `H` | chronological by `c` | chronological by `c` |
| Target `P` | `(1/\sqrt2,1/\sqrt2)` | coordinate boundary |
| Record family | Pell spine `\|b-a\|=1` | boundary ladder `g=1` (`m=n+1`) |
| Counting law | `N_P(C)\sim\log C/\log\lambda` | `N_B(C)\sim\sqrt{C/2}` |
| Relative spacing | `\to\lambda=3+2\sqrt2` | `\to1` |
| First-order target error | `\epsilon_{bal}\sim c^{-1}` | `\epsilon_{pole}\sim c^{-1/2}` |
| Scaled-envelope behavior | persistent oscillation, `[1/\sqrt2,\lambda/\sqrt2]` | converges to `\sqrt2` |

The first three rows are identical by construction. That is the visual
point: **same `C, A, H`; different `P, O`; different record chronology.**

## Observable vanishing order (a caution, not a theorem)

Suppose an approximation error scales as `\epsilon(H)\sim H^{-\alpha}` and
an observable near the target satisfies a regular local expansion
`O(\epsilon)-O(0)=K\epsilon^p+o(\epsilon^p)` with `K\ne0`. Then, in a
regular worked case,

$$|O(\epsilon(H))-O(0)|\sim H^{-\alpha p}$$

This is a **STANDARD LOCAL ASYMPTOTIC MECHANISM** (a Taylor-expansion
consequence), not a new theorem, and not asserted here under general
hypotheses — only observed to hold in the two worked regimes above. The
observed exponent therefore mixes two effects: the *approximation
behavior* (`\alpha`) and the *observable's local vanishing order* (`p`).

**Concretely**: the balanced target is a generic point of the circle,
where a leg-difference observable vanishes to first order (`p=1`); the
boundary is a point where the coordinate's first angular derivative
vanishes, so a coordinate-deficit observable vanishes to *second* order
(`p=2`), giving the observed `\epsilon_{pole}\sim c^{-1/2}` rather than
`c^{-1}`. Comparing a **second**-order balance quantity such as
`\delta_{bal}\sim c^{-2}` directly against the **first**-order boundary
quantity `\epsilon_{pole}\sim c^{-1/2}`, and reading the exponent ratio as
a structural fact about the targets, would silently conflate the
approximation rate with the observable's vanishing order. Comparisons
across targets should use observables of matched local order when the
goal is to compare arithmetic approximation rates.

## Why target alone is insufficient

The balance/boundary comparison above might suggest a simple rule:
rational target → dense chronology, quadratic-irrational target → sparse
chronology. **This rule is not established and should not be inferred.**
It holds, descriptively, for these two solved single-target cases; it is
not shown to hold in general.

A third, adversarial case under the *same* ambient Pythagorean geometry,
the *same* primitivity/parity admissibility, and the *same* height `c`
defeats any such rule: a construction with **two** target slopes
(a parity-restricted, "first-kind" approximation problem whose admissible
candidates are filtered by the same primitivity/parity condition as `A`
above) produces a **merged chronology of two target branches**, in which
branch competition suppresses some records that either target's own
approximation theory alone would produce. This case is:

- computationally verified (exact-integer-arithmetic record search,
  cross-checked by two independent methods);
- only partially understood analytically;
- **not** a third solved regime of the same status as balance or boundary.

Its asymptotic counting law is **OPEN** and not stated here. Its only use
in this note is the conservative conclusion: **record chronology belongs
to the full approximation problem — ambient geometry, admissibility,
height, target, observable, and branch structure — not to target
arithmetic alone.**

## Strongest surviving claim

**REPOSITORY-SPECIFIC SYNTHESIS**, not a new theorem:

> In the solved quarter-circle controls, holding the ambient constraint
> geometry, admissibility class, and height ordering fixed while varying
> target and observable produces distinct record chronologies. However,
> the chronology is not determined by target arithmetic alone;
> admissibility, ordering, observable vanishing order, and branch
> structure can also matter.

## Connection to constraint geometry

This note supports: fixed constraint + varied target/observable →
different *static* record regimes. It does **not** establish dynamic
state flow or dynamically evolving constraints — there is no ODE, no
flow, and no time parameter anywhere in this material. At most: this
provides a fixed-geometry control case that helps distinguish
target-dependent structure from geometry-changing structure, should that
distinction matter elsewhere in this repository. No GR-style language
applies here.

## Connection to Structural Addresses

As a conceptual comparison only — not formalized, not implemented, and no
external repository is modified — a record state could in principle carry
several distinct information channels: continuous target proximity, exact
record-family membership, admissibility provenance, and height provenance.
Identical numerical approximation quality does not imply identical
arithmetic mechanism (the 15° case makes this concrete: two records with
comparable approximation quality can belong to entirely different
branches). This is a **PARTIAL STRUCTURAL CORRESPONDENCE** to the
Structural Addresses methodology, offered only as an observation.

## Terminology

This note avoids "static extremal skeleton" as a preferred term. The
established record families above are **record sequences** or **record
families** — the informal word "skeleton" is used nowhere here as a
defined term, since standard terminology (record sequence, best
approximants, convergents) already covers the content without risking an
implied richer structure the arithmetic does not have.

## What this note does not claim

- No new Diophantine-approximation theorem.
- No universal rule that target arithmetic type determines record density.
- The 15° case is not promoted to a solved third regime.
- No dynamic-constraint behavior is established or implied.
- No physical interpretation is assigned to any counting law, spacing
  limit, or envelope constant.

See also [`constraint_intersection_diagnostics.md`](constraint_intersection_diagnostics.md)
(a separate, unrelated fixed-vs-varied comparison for static constraint
*intersections* rather than Diophantine *records*) and
[`state_dimension.md`](state_dimension.md) (the repository's actual
dynamic-constraint material, which this note does not extend).
