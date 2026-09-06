# Constraint-State Dimension vs. Domain-Dynamical-State Dimension

The gauge-coupling-running example (`examples/gauge_running.py`) surfaces a
distinction worth stating on its own, separate from that example's specific
domain content.

## The constraint state

For any conserved binary partition `a+b=1`, the constraint layer supplies a
single coordinate, `chi = a-b`, capturing **relative composition**: which of
the two sectors dominates, and by how much. This is exact, parameter-free,
and — as always in this repository — carries no domain content by itself.

## The domain-dynamical state

For gauge-coupling running at one loop (`d(ln alpha_i)/dt = (b_i/2*pi)*alpha_i`,
domain model input), writing `chi = (alpha_i-alpha_j)/(alpha_i+alpha_j)` and
`S = alpha_i+alpha_j`, the derived evolution is

$$\frac{d\chi}{dt}=\frac{S}{8\pi}(1-\chi^{2})\big[(b_{i}-b_{j})+(b_{i}+b_{j})\chi\big],\qquad
\frac{dS}{dt}=\frac{S^{2}}{8\pi}\big[(b_{i}+b_{j})(1+\chi^{2})+2\chi(b_{i}-b_{j})\big]$$

Both equations depend on `S` as well as `chi`. The system does not close on
`chi` alone: the **domain-dynamical state** required to know the evolution
rate is `(chi, S)`, not `chi` by itself.

## The extracted potential factors exactly

Substituting `dchi/dt` into the repository's existing Tier-1 normal form,
`V_eff^(1)(chi) = -1/2*(dchi/dt)^2/(1-chi^2)`, gives

$$V_{\mathrm{eff}}^{(1)}(\chi;S)=S^{2}\,v(\chi),\qquad
v(\chi)=-\frac{1}{128\pi^{2}}(1-\chi^{2})\big[(b_{i}-b_{j})+(b_{i}+b_{j})\chi\big]^{2}$$

`v(chi)` is genuinely independent of `S` — an exact algebraic
**separability** of the potential's shape from its overall scale.

## Two statements that must not be conflated

- **A. Algebraic separability** — `V(chi;S) = S^2 * v(chi)`. This holds
  exactly, verified in `tests/test_gauge_running.py::TestSeparabilityExact`.
- **B. Autonomous dynamical reduction** — `dchi/dt = F(chi)` alone. This does
  **not** hold: `dchi/dt` above retains an explicit `S` factor under the
  original running parameter. No legitimate reparameterization, coordinate
  change, or restriction to a special family of one-loop coefficients
  removes it (see the Milestone-2 rescue-attempt table in the audit report).

Dividing `V_eff^(1)` by `S^2` recovers the universal shape `v(chi)` exactly
(`examples/gauge_running.py::rescue_attempt_normalize_by_S`, confirmed
numerically to a `~4200x` residual improvement over the unnormalized
comparison). This is a genuine structural fact about the potential's shape —
but it does **not** make `chi` dynamically sufficient: reconstructing the
actual evolution rate `dchi/dt` still requires `S`, supplied externally at
every point where it is used. Separability of the shape and sufficiency of
the state are different properties, and only the first holds here.

## The general statement, and its scope

$$\boxed{\text{constraint-state dimension} \neq \text{domain-dynamical-state dimension}}$$

This is a **STRUCTURAL INTERPRETATION** for the one-loop gauge-running model
specifically — a property this milestone's derivation establishes for *this*
domain map, under *this* domain model input (one-loop running, arbitrary
illustrative `b_i, b_j`). It is not asserted as a universal physical law, and
it says nothing about whether other domains close on `chi` alone or require
additional state. Each domain's dynamical closure is a fact about that
domain's dynamics, to be established the same way this one was: by deriving
the evolution equations and checking, not by analogy.

## Projected orbit dimension, rate, and direction

A further distinction, sharpened after the domain-dynamical-state result
above: *within* the two-dimensional `(chi, S)` state, how much of the
`chi`-motion is genuinely one-dimensional, and how much needs `S`?

**A. Full state.** `(chi, S)` — dimension 2 — is required to reconstruct
`alpha_i = S(1+chi)/2`, `alpha_j = S(1-chi)/2`, and to evolve with respect
to the original RG parameter `t`. Unchanged from above.

**B. Reduced autonomous flow.** For `S > 0` (guaranteed here, since
`S=alpha_i+alpha_j` with both couplings positive), define `d(tau) = S dt`.
Then

$$\frac{d\chi}{d\tau}=\frac{1}{8\pi}(1-\chi^{2})\big[(b_{i}-b_{j})+(b_{i}+b_{j})\chi\big]$$

which contains no `S` at all: the projected `chi(tau)` orbit closes
autonomously in one dimension. This is a standard consequence of positive
time reparameterization — two vector fields related by a positive scalar
factor are *orbitally equivalent* (same fixed points, same direction on
every non-equilibrium interval, same stability classification; trajectories
differ only by how fast they traverse the same oriented path). See e.g.
Perko, *Differential Equations and Dynamical Systems*; the same idea
underlies the Sundman transformation in celestial mechanics. This is
**not** presented as new mathematics — only its specific closed form for
this domain model is new content here.

**C. Rate.** `S` sets the *traversal rate* of `chi` in the original clock:
`dchi/dt = S · dchi/dtau`. Two trajectories sharing `chi₀` but differing
`S₀` move through the identical sequence of `chi` values, just at
different speeds (`examples/gauge_reparameterization.py::demonstrate_reparameterization`
confirms `chi(t)` differs materially between such trajectories while
`chi(tau)` collapses to residual `~10⁻¹¹`). This is a statement about `S`'s
effect on `chi`'s equation specifically — it does **not** mean `S` is
"merely a clock" for the system as a whole. `S` is removable from the
*projected* `chi` equation by the reparameterization, but it remains
necessary for full coupling reconstruction (below), and it evolves
nontrivially in its own right: `dS/dtau = S/(8\pi)[(b_i+b_j)(1+\chi^2)+2(b_i-b_j)\chi]`
is linear, not zero, in `S`. The conserved quantity `K=S(1-\chi^2)/[(b_i-b_j)+(b_i+b_j)\chi]`
labels which member of the family a given trajectory belongs to; it is not
itself dynamical (its `tau`-derivative is exactly zero), but it is real,
non-clock information distinguishing different lifts of the same reduced
orbit.

**D. Direction.** On `-1<chi<1`, `(1-chi²)>0` strictly, so
`D(chi) = sign((b_i-b_j)+(b_i+b_j)chi) = sign(dchi/dtau)` exactly, and
because `S>0` always, `sign(dchi/dt) = sign(dchi/dtau) = D(chi)`. **`S`
changes the rate but, for `S>0`, never the oriented `chi` phase line.**

**E. Effective-potential limitation.** The repository's existing Tier-1
normal form, `V_eff^(1)(chi) = -1/2*(dchi/dx)^2/(1-chi^2)`
(`src/constraint_geometry/normal_form.py`), depends on the *squared*
velocity and is therefore invariant under `chi' → -chi'`:
`V_eff(chi,+v) = V_eff(chi,-v)` for any `v≠0` — exact algebra, not a
defect. **The effective-potential normal form is direction-blind because
it is constructed from squared velocity. A separate signed direction
channel is therefore complementary rather than redundant** — `D(chi)` is
never multiplied into `V_eff` and never replaces it; they carry different
information (speed-like normal-form content vs. orientation).

Full derivation, numerical verification, and an adversarial audit of how
much of this is standard dynamical-systems mathematics (most of it) versus
specific to this domain model (the closed forms above) are recorded in the
Milestone-3 research audit and its direction-rate follow-up.

See also [`epistemic_tiers.md`](epistemic_tiers.md), [`safeguards.md`](safeguards.md)
(Safeguard 2, chart contributions), and [`software_scope.md`](software_scope.md).
