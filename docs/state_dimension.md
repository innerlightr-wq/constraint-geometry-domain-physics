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

See also [`epistemic_tiers.md`](epistemic_tiers.md), [`safeguards.md`](safeguards.md)
(Safeguard 2, chart contributions), and [`software_scope.md`](software_scope.md).
