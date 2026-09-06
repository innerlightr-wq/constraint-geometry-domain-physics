# Dynamic Constraint Diagnostics

This note extends the repository's static constraint-intersection
diagnostics (`constraint_intersection_diagnostics.md`) to constraints
whose configuration changes in time or evolves with the state. The
underlying mathematics is standard differential-algebraic /
constrained-dynamics theory (consistent initialization, hidden
constraints, tangent-space kinematics). The purpose here is
organizational: to separate instantaneous existence and regularity from
constraint *transport*, and from the dynamics actually *selected* within
the set of velocities that transport permits. This is not a new field,
not a new theorem, and not a dynamics solver.

## Four regimes

**Evolving state is not the same thing as an evolving constraint.**

- **Regime I — fixed constraint, fixed state.** `\Phi(x)=0`. Pure static
  geometry; this is all of `constraint_intersection_diagnostics.md`.
- **Regime II — fixed constraint, evolving state.** `\Phi(x)=0`,
  `\dot x=F(x)`, with `D\Phi\cdot F=0`. The admissible *set* never moves;
  only the state moves along it.
- **Regime III — externally time-dependent constraint.** `\Phi(x,t)=0`,
  consistency `D_x\Phi\cdot\dot x+\partial_t\Phi=0`. The set can move,
  driven by a clock external to the state.
- **Regime IV — state-coupled dynamic constraint.** `\Phi(x,C)=0`,
  `\dot x=F(x,C)`, `\dot C=G(x,C)`, with
  `D_x\Phi\cdot F+D_C\Phi\cdot G=0` on the constraint surface. Genuine
  two-way coupling between state and constraint configuration.

This note documents Regime IV (which contains III as the special case
`\dot C=1`, `C=t`) and its relationship to the fixed Regime I already
covered by M4.

## The constraint-preservation equation

For `\Phi(x(t),C(t))=0` differentiable in `t`, the chain rule gives

$$\frac{d}{dt}\Phi(x(t),C(t)) = D_x\Phi\cdot\dot x + D_C\Phi\cdot\dot C = 0$$

**STANDARD MATHEMATICAL RESULT** — this is exactly the statement that
`(\dot x,\dot C)` lies in the tangent space (kernel) of `D_{(x,C)}\Phi`.
It is sometimes called the *invariance condition*, *tangency condition*,
or *constraint-preservation condition* for the pair `(F,G)`; all three
names are standard and used interchangeably in the constrained-dynamics
literature.

## The affine compatible-velocity space

Write `A=D_x\Phi` and `b=-D_C\Phi\cdot\dot C`. Compatible state
velocities solve the linear system

$$A\,\dot x = b$$

**STANDARD DAE / LINEAR-ALGEBRA STRUCTURE** — this is exactly the
consistent-initialization / hidden-constraint equation of
differential-algebraic-equation theory.

- **No solution** if `b\notin\mathrm{im}(A)` — the proposed `\dot C` is
  incompatible with *any* continuous state motion maintaining `\Phi=0`.
- **Unique solution** if `\ker(A)=\{0\}` (i.e. `\mathrm{rank}(A)=n`, the
  full state dimension) — an isolated admissible state, no remaining
  freedom.
- **Affine family**, otherwise, when consistent:
  `\dot x=\dot x_{particular}+\ker(A)`, of dimension `n-\mathrm{rank}(A)`.

This affine space — not a single vector — is the central object of this
note: **constraint evolution fixes which velocities are compatible, not
generally which one is realized.**

## Five-channel diagnostic decomposition

The minimal, nonredundant organization found by direct testing (not
assumed):

1. **Existence** — does `\Phi(x,C)=0` admit a solution at all?
2. **Regularity** — what is `\mathrm{rank}(D_x\Phi)`?
3. **Conditioning** — how sensitive is the local solution set to changes
   in `x` or `C`? (Requires a declared metric/normalization, exactly as
   in the static M4 case.)
4. **Transport** — how does changing `C` move or deform the admissible
   set (governed by `D_C\Phi\cdot\dot C`, the right-hand side `b` above)?
5. **Selected dynamics** — which compatible velocity does the actual law
   `F` choose?

**The compatible-velocity affine space is derived jointly from channels
2 (regularity, giving `A`) and 4 (transport, giving `b`) — it is a
useful named object, but not a sixth independent channel.**
Rate/time-reparameterization robustness (§ Direction vs. rate, below) is
a **cross-cutting audit criterion** applied to these five channels, not
a further peer layer.

## Worked model: translating line

`\Phi(x,y,c)=y-c`, `\dot c=v`. `D_x\Phi=(0,1)`, `\partial\Phi/\partial c=-1`.
Consistency gives exactly `\dot y=v`; `\dot x` remains free (tangential).
Regularity stays full throughout (`D_x\Phi\ne0` everywhere).

**Frame dependence.** In the co-moving coordinate `Y=y-c(t)` (a
time-dependent change of variables), the same constraint reads `Y=0`
identically — stationary. This does **not** mean the motion "was not
real": it means "the constraint is moving" is a statement relative to a
*declared ambient embedding*. In the fixed `(x,y)` frame the line
genuinely translates; in the co-moving `(x,Y)` frame it does not. Both
are correct descriptions of the same fact, not competing claims.

## Worked model: rotating line

`\Phi(x,y,\theta)=y\cos\theta-x\sin\theta`, `\dot\theta=\omega`. The
consistency equation is

$$-\dot x\sin\theta+\dot y\cos\theta = \omega\,(x\cos\theta+y\sin\theta)$$

(verified symbolically). Writing a point on the line as
`x=r\cos\theta,\ y=r\sin\theta`, this becomes

$$-\dot x\sin\theta+\dot y\cos\theta = r\omega$$

— the velocity component along the constraint's normal direction is
fixed at `r\omega` (standard rigid-rotation kinematics,
`v_\perp=\omega\times r`); the component *along* the line remains free.

## Worked model: expanding circle

`\Phi(x,y,R)=x^2+y^2-R^2`, `\dot R` arbitrary. Consistency:

$$x\dot x+y\dot y = R\dot R$$

Metric-free statement first: compatible `\dot x` form an affine coset of
`\ker(D_x\Phi)` — this fixes only the *image* of `\dot x` under
`D_x\Phi` (equivalently, `\dot x`'s class in the quotient
`T_xM/\ker(D_x\Phi)`), not `\dot x` itself. Only after choosing the
Euclidean metric does it become natural to call this the "radial"
condition and to say the remaining freedom is "tangential/angular" —
that language is a convenience layered on the coordinate-free fact, not
the fact itself. Without an additional law for `F`, the tangential
motion is entirely undetermined.

## Worked model: degeneracy control

`\Phi(y,c)=y^2-c`. For `c>0`: two regular branches `y=\pm\sqrt c`,
`\partial\Phi/\partial y=2y\ne0`. At `c=0`: the branches merge into
`y=0`, and `\partial\Phi/\partial y=0` there — regularity is lost *for
this particular defining function*. For `c<0`: no real admissible state.

**This single family exhibits existence, regularity loss, branching, and
disappearance all at once**, and comes with an important caveat: **the
rank defect of a particular defining function must not be confused
automatically with singularity of the underlying set.** At `c=0`, the
set `\{y=0\}` is, by itself, a perfectly smooth line — an alternative
defining function such as `\Psi(y)=y` would show full regularity there.
What *is* genuinely, representation-independently singular at `c=0` is
the **family**: the number of connected components changes
(`0\to1\to2` as `c` crosses `0` from below), a standard fold/saddle-node
bifurcation of the constraint set. The rank defect of `y^2-c`
specifically happens to coincide with this genuine transition here, but
the two facts (rank of *this* `\Phi`; genuine set-level change) are
logically distinct and should be checked separately.

## Representation invariance

For `\Psi(x,C)=A(x,C)\Phi(x,C)` with `A\ne0` on the constraint surface,
on that surface `D_x\Psi=A\cdot D_x\Phi` and `D_C\Psi=A\cdot D_C\Phi`
exactly (the `\Phi\cdot D_xA` cross-term vanishes there). **STANDARD /
MATHEMATICALLY DERIVED**, directly extending the M4 rescaling result:

| Invariant / geometrically meaningful | Not invariant without extra structure |
|---|---|
| Zero set (locally) | Raw derivative magnitudes (`D_x\Phi`, `D_C\Phi`) |
| Rank | Gradient norm |
| Kernel / tangent space | Raw determinant magnitude |
| The consistency condition itself | Naive Euclidean angle after an arbitrary coordinate change |
| The compatible-velocity affine space | — |

Verified directly (numeric check): rescaling `\Phi\to A\Phi` by a
constant invertible `A` reproduces an *identical* compatible-velocity
solution to machine precision, while the raw Jacobian entries change by
a factor of `A`. **"Dynamic constraint geometry" must be built from
rank, kernel, and the compatible-velocity space — never from raw
derivative magnitudes.**

## Moving-constraint taxonomy

These four levels should not be conflated under one vague phrase such as
"the geometry changed":

- **Level 1 — representation change only.** Example:
  `\Phi(x,C)=a(C)\Phi_0(x)`, `a(C)\ne0`. The zero set is unchanged;
  only the formula depends on `C`.
- **Level 2 — rigid embedding motion.** Translating and rotating line.
  The set moves relative to a fixed ambient frame, but its intrinsic
  form (a flat line) is unchanged — recoverable as stationary in a
  co-moving frame.
- **Level 3 — deformation.** Expanding circle. Intrinsic geometry
  (curvature `1/R`) genuinely changes; no coordinate change, even a
  time-dependent one, can undo this.
- **Level 4 — degeneration / branching / dimension or existence
  change.** The `y^2-c` family; also a circle collapsing as `R\to0`
  (dimension drops from 1 to 0 at `R=0`). Diffeomorphism-invariant facts
  change; unrecoverable by any coordinate change.

## State motion vs. constraint motion

Constraint transport (channel 4) determines **which velocities are
compatible**. It does not generally determine **which compatible
velocity is realized** — that is a separate choice, supplied by `F`
(channel 5). The expanding circle is the clearest control: the
consistency equation fixes only the component of `\dot x` along
`\nabla\Phi`; the actual tangential dynamics is not determined by the
constraint at all. Admissible location, constraint transport, and
selected dynamics are three distinct pieces of information.

## Direction vs. rate

Reusing the existing repository control (`gauge_reparameterization.py`):
`\dot x=\mu(x,C)F_0(x)`, `\mu>0`, changes the *rate* of traversal without
changing the *oriented* state-space trajectory. **Rate modulation alone
is not dynamic constraint transport.** The distinguishing test: does
`D_C\Phi\ne0` *on the constraint surface*? If `\Phi` does not actually
depend on `C` there, no amount of `C`-dependence elsewhere (e.g. inside
`\mu`) makes the constraint itself dynamic — it remains Regime II with a
rate-modulated selected dynamics.

## Algebraically slaved configuration

If `C=C(x)` algebraically, then `\Phi(x,C(x))=\Psi(x)` is simply another
fixed constraint — substitution, nothing more. **State dependence does
not automatically create an independent dynamical configuration
variable.** A genuine additional configuration variable needs its own
independent initial data and evolution law, not one that is
algebraically fixed by `x` alone. Whether a given `C` is eliminable can
be model-dependent, and this wording is deliberately conservative:
absence of an *obvious* algebraic reduction does not by itself prove `C`
is independent.

## Connection to M4

M4's diagnostics — compatibility, rank, transversality, wedge
non-vanishing — remain evaluable pointwise at each instant along a
trajectory `(x(t),C(t))`; nothing changes about their static definition.
What they do **not** do, by themselves, is characterize the evolution:
that requires the additional constraint-preservation equation and the
compatible-velocity space above. **This note is a narrow extension of
M4, not a replacement for it or a new framework alongside it.**

## M5 firewall

Milestone 5's arithmetic record chronology (Pell spine, boundary ladder)
provides **no mathematical dynamical model here**. Hypotenuse ordering is
not physical time; record density is not a dynamical rate; a record
family is not a trajectory. Any resemblance between "fixed background +
varied auxiliary input" in M5 and "fixed constraint + varied evolution"
here is thematic only. **NOT ESTABLISHED**: any mathematical bridge from
M5 to this note. None is attempted.

## GR firewall

The generic architecture — evolving state, evolving admissible
structure, coupling between them — has a broad structural resemblance to
many dynamical systems in which the arena and the state co-evolve. **This
is not general relativity.** GR requires a Lorentzian metric, tensor
field equations, diffeomorphism covariance, causal structure, and
genuine field-theoretic coupling between geometry and matter, none of
which appears anywhere in this note. **STRUCTURAL ANALOGY ONLY**, not
developed further here.

## What this note does not claim

- No new differential-algebraic-equations theorem — everything here is
  standard consistent-initialization / tangent-space theory.
- No new invariant.
- No dynamics solver, integrator, or mechanics engine.
- No claim that M5's record chronology transfers into this setting.
- No claim of GR equivalence or GR-derived content.
- No physical interpretation of any quantity in this note.

See also [`constraint_intersection_diagnostics.md`](constraint_intersection_diagnostics.md)
(the static predecessor this note extends) and
[`state_dimension.md`](state_dimension.md) (a related but separate
state/direction/rate distinction for the one-loop gauge-running example).
