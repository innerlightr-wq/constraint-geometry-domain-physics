"""
Positive state-dependent time reparameterization of the one-loop
gauge-running system, and the direction/rate distinction it makes precise.

This module implements exactly the results established in the Milestone-3
research audit and its direction-rate follow-up audit -- nothing broader.
It reuses examples/gauge_running.py's domain model (B_I, B_J,
dchi_dt_closed, dS_dt_closed, integrate_running, alpha_from_chi_S) rather
than duplicating it.

============================================================
1. MATHEMATICALLY DERIVED -- the reparameterized chi equation
============================================================

Starting from the Milestone-2 result dchi/dt = (1-chi^2)*S/(8*pi)*bracket
(bracket = (b_i-b_j)+(b_i+b_j)*chi), define d(tau) = S dt with S > 0
(guaranteed in the physical coupling domain). Then dt/dtau = 1/S, so

    dchi/dtau = (dchi/dt) * (dt/dtau) = (1-chi^2)/(8*pi) * bracket(chi)

which no longer contains S. This is a standard consequence of positive
time reparameterization / orbital equivalence between vector fields
related by a positive scalar factor (see e.g. Perko, "Differential
Equations and Dynamical Systems"; the Sundman transformation in celestial
mechanics is the same trick). It is NOT presented here as a new theorem.

============================================================
2. MATHEMATICALLY DERIVED -- the S(chi) closed form and K
============================================================

dS/dtau = (dS/dt)/S = S/(8*pi)*[(b_i+b_j)(1+chi^2)+2(b_i-b_j)chi] is
LINEAR in S (unlike dS/dt, which is quadratic in S). The resulting
separable ODE dS/dchi = (dS/dtau)/(dchi/dtau) integrates exactly to

    S(chi) = K * bracket(chi) / (1-chi^2),   K = S(1-chi^2)/bracket(chi)

with K conserved along any non-singular trajectory (a first integral of
the full (chi,S) flow). K is undefined exactly where bracket(chi)=0 --
the reduced flow's own equilibrium -- and is never silently evaluated
there (see k_of below).

Note: S being removable from the *projected chi equation* via the
reparameterization does not mean S is "merely a clock" for the system as
a whole. S remains necessary for full coupling reconstruction (Section 1)
and evolves nontrivially in its own right (dS/dtau above is linear, not
zero, in S). K is not itself dynamical (d K/d tau = 0 by construction),
but it is real, non-clock information: it labels which member of the
family a given trajectory belongs to.

============================================================
3. EXACT ALGEBRA -- the direction comparator
============================================================

On the open interval -1 < chi < 1, (1-chi^2) > 0 strictly, so

    D(chi) = sign(bracket(chi)) = sign(dchi/dtau)

and, because S > 0 always in the physical domain,

    sign(dchi/dt) = sign(S) * sign(dchi/dtau) = sign(dchi/dtau) = D(chi)

S changes the TRAVERSAL RATE of chi in the original clock t; for S > 0
it does not change the ORIENTED chi phase line. This is a standard
dynamical-systems fact (positive-scalar orbital equivalence), stated
here in the specific closed form this domain model admits.

============================================================
4. STRUCTURAL INTERPRETATION -- why D is not redundant here
============================================================

The repository's existing effective-potential normal form,
V_eff^(1)(chi) = -1/2*(dchi/dx)^2/(1-chi^2) (src/constraint_geometry/
normal_form.py), depends on the SQUARE of the velocity and is therefore
invariant under velocity reversal: V_eff(chi,+v) = V_eff(chi,-v) for any
v != 0 (EXACT ALGEBRA, demonstrate_V_eff_sign_blindness below). D(chi)
restores exactly the orientation information that squaring discards. D
is not multiplied into V_eff and does not replace it -- they carry
different, complementary information (speed-like normal-form content vs.
signed direction), never combined into one quantity anywhere in this
module.

Run directly:

    python examples/gauge_reparameterization.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from scipy.integrate import cumulative_trapezoid

import gauge_running as gr

__all__ = [
    "dchi_dtau_closed",
    "dF_dchi",
    "D",
    "interior_fixed_point",
    "k_of",
    "tau_from_trajectory",
    "demonstrate_reparameterization",
    "demonstrate_K_conservation",
    "demonstrate_direction_comparator",
    "demonstrate_V_eff_sign_blindness",
    "demonstrate_fixed_points",
    "demonstrate_stability_preserved_under_positive_S",
]


# ---------------------------------------------------------------------------
# MATHEMATICALLY DERIVED reduced-flow equations
# ---------------------------------------------------------------------------

def dchi_dtau_closed(chi, b_i=gr.B_I, b_j=gr.B_J):
    """dchi/dtau = (1-chi^2)/(8*pi) * [(b_i-b_j)+(b_i+b_j)*chi]. S-independent."""
    chi = np.asarray(chi, dtype=float)
    A = b_i - b_j
    B = b_i + b_j
    bracket = A + B * chi
    return (1.0 - chi**2) * bracket / (8.0 * np.pi)


def dF_dchi(chi, b_i=gr.B_I, b_j=gr.B_J):
    """Analytic derivative d(dchi/dtau)/dchi = [B - 2*A*chi - 3*B*chi^2]/(8*pi),
    used for fixed-point stability. MATHEMATICALLY DERIVED (closed form, not
    a finite-difference approximation)."""
    chi = np.asarray(chi, dtype=float)
    A = b_i - b_j
    B = b_i + b_j
    return (B - 2.0 * A * chi - 3.0 * B * chi**2) / (8.0 * np.pi)


def D(chi, b_i=gr.B_I, b_j=gr.B_J):
    """EXACT ALGEBRA: D(chi) = sign((b_i-b_j)+(b_i+b_j)*chi) = sign(dchi/dtau)
    on -1 < chi < 1 (since 1-chi^2 > 0 there strictly)."""
    chi = np.asarray(chi, dtype=float)
    A = b_i - b_j
    B = b_i + b_j
    return np.sign(A + B * chi)


def interior_fixed_point(b_i=gr.B_I, b_j=gr.B_J):
    """Return chi* = -A/B if B != 0 and chi* is interior-admissible
    (-1 < chi* < 1), else None. MATHEMATICALLY DERIVED."""
    A = b_i - b_j
    B = b_i + b_j
    if B == 0.0:
        return None
    chi_star = -A / B
    return chi_star if -1.0 < chi_star < 1.0 else None


def k_of(chi, S, b_i=gr.B_I, b_j=gr.B_J, bracket_floor=1e-9):
    """K = S*(1-chi^2)/bracket(chi), the conserved orbit label. Raises
    ValueError instead of silently dividing when bracket is within
    bracket_floor of zero -- that locus is the reduced flow's own
    equilibrium, where K in this form is genuinely singular (see the
    module docstring, Section 2)."""
    chi = np.asarray(chi, dtype=float)
    S = np.asarray(S, dtype=float)
    A = b_i - b_j
    B = b_i + b_j
    bracket = A + B * chi
    if np.any(np.abs(bracket) < bracket_floor):
        raise ValueError(
            f"K is undefined at/near the reduced-flow equilibrium "
            f"bracket=0 (|bracket| < {bracket_floor}); this is not a "
            f"coding error to silently divide through."
        )
    return S * (1.0 - chi**2) / bracket


def tau_from_trajectory(t, S):
    """NUMERICAL DEMONSTRATION: tau(t) = integral of S dt via cumulative
    trapezoid, tau(t[0]) = 0."""
    t = np.asarray(t, dtype=float)
    S = np.asarray(S, dtype=float)
    return np.concatenate([[0.0], cumulative_trapezoid(S, t)])


# ---------------------------------------------------------------------------
# Demonstrations
# ---------------------------------------------------------------------------

def demonstrate_reparameterization(
    chi0=1.0 / 3.0, S0_1=0.15, S0_2=0.30, t_max=2.0, n=20000,
    b_i=gr.B_I, b_j=gr.B_J,
):
    """Two full (alpha_i,alpha_j) trajectories sharing chi0 but differing
    S0: chi_1(t) != chi_2(t) in general, but chi_1(tau) ~= chi_2(tau) after
    each trajectory is reparameterized by its OWN tau(t)=int S dt.
    NUMERICAL DEMONSTRATION."""
    alpha_i1, alpha_j1 = gr.alpha_from_chi_S(chi0, S0_1)
    alpha_i2, alpha_j2 = gr.alpha_from_chi_S(chi0, S0_2)
    t1, chi1, S1, _, _ = gr.integrate_running(alpha_i1, alpha_j1, t_max, n, b_i=b_i, b_j=b_j)
    t2, chi2, S2, _, _ = gr.integrate_running(alpha_i2, alpha_j2, t_max, n, b_i=b_i, b_j=b_j)

    tau1 = tau_from_trajectory(t1, S1)
    tau2 = tau_from_trajectory(t2, S2)

    t_common = min(t1[-1], t2[-1])
    mask_t = t1 <= t_common
    chi2_on_t = np.interp(t1[mask_t], t2, chi2)
    residual_t_max = float(np.max(np.abs(chi1[mask_t] - chi2_on_t)))

    tau_common = min(tau1[-1], tau2[-1])
    mask_tau = tau1 <= tau_common
    chi2_on_tau = np.interp(tau1[mask_tau], tau2, chi2)
    residual_tau_max = float(np.max(np.abs(chi1[mask_tau] - chi2_on_tau)))

    return {
        "chi0": chi0, "S0_1": S0_1, "S0_2": S0_2,
        "t1": t1, "chi1": chi1, "S1": S1, "tau1": tau1,
        "t2": t2, "chi2": chi2, "S2": S2, "tau2": tau2,
        "t_common": t_common, "tau_common": tau_common,
        "residual_t_max": residual_t_max,
        "residual_tau_max": residual_tau_max,
    }


def demonstrate_K_conservation(
    chi0=1.0 / 3.0, S0=0.15, t_max=2.0, n=20000, b_i=gr.B_I, b_j=gr.B_J,
):
    """K conserved along a single full trajectory, away from the singular
    locus bracket=0. NUMERICAL DEMONSTRATION."""
    alpha_i0, alpha_j0 = gr.alpha_from_chi_S(chi0, S0)
    t, chi, S, _, _ = gr.integrate_running(alpha_i0, alpha_j0, t_max, n, b_i=b_i, b_j=b_j)
    K = k_of(chi, S, b_i=b_i, b_j=b_j)
    K0 = K[0]
    abs_drift = float(np.max(np.abs(K - K0)))
    rel_drift = float(np.max(np.abs((K - K0) / K0)))
    return {"chi": chi, "S": S, "K": K, "K0": K0, "abs_drift": abs_drift, "rel_drift": rel_drift}


def demonstrate_direction_comparator(
    chis=None, S_values=(0.01, 0.15, 1.0, 50.0), b_i=gr.B_I, b_j=gr.B_J,
):
    """sign(dchi/dtau) == D(chi) and, for every tested S>0,
    sign(dchi/dt) == D(chi), on a dense deterministic grid.
    EXACT ALGEBRA / NUMERICAL DEMONSTRATION (grid check of an exact fact)."""
    if chis is None:
        chis = np.linspace(-0.999, 0.999, 2001)
    d_tau = dchi_dtau_closed(chis, b_i=b_i, b_j=b_j)
    d_comp = D(chis, b_i=b_i, b_j=b_j)
    mismatches_tau = int(np.sum(np.sign(d_tau) != d_comp))
    mismatches_t = {}
    for S in S_values:
        d_t = S * d_tau
        mismatches_t[S] = int(np.sum(np.sign(d_t) != d_comp))
    return {"n_points": len(chis), "mismatches_tau": mismatches_tau, "mismatches_t": mismatches_t}


def demonstrate_V_eff_sign_blindness(chi=0.2, v=0.37):
    """EXACT ALGEBRA: V_eff(chi,+v) = V_eff(chi,-v) since V_eff depends only
    on v^2, while D(+v)=+1, D(-v)=-1. Uses the same V_eff^(1) definition as
    src/constraint_geometry/normal_form.py (-1/2*v^2/(1-chi^2)), evaluated
    directly rather than through extract_normal_form since only two bare
    velocity values (not a trajectory) are being compared here."""
    if v == 0.0:
        raise ValueError("v must be nonzero -- direction is undefined at v=0")

    def V_eff(chi, vel):
        return -0.5 * vel**2 / (1.0 - chi**2)

    V_plus = V_eff(chi, v)
    V_minus = V_eff(chi, -v)
    return {
        "chi": chi, "v": v,
        "V_plus": V_plus, "V_minus": V_minus,
        "difference": abs(V_plus - V_minus),
        "D_plus": float(np.sign(v)), "D_minus": float(np.sign(-v)),
    }


def demonstrate_fixed_points(b_i=gr.B_I, b_j=gr.B_J):
    """Reduced fixed points of dchi/dtau=F(chi): boundary chi=+-1 (treated
    as boundary zeros of the extended algebraic vector field; the working
    partition domain itself remains open, per repository convention) and
    the interior equilibrium chi*=-A/B when it exists and is admissible.
    MATHEMATICALLY DERIVED."""
    candidates = [(-1.0, "boundary chi=-1"), (1.0, "boundary chi=+1")]
    chi_star = interior_fixed_point(b_i, b_j)
    if chi_star is not None:
        candidates.append((chi_star, "interior chi*=-A/B"))
    results = []
    for chi_fp, label in candidates:
        fprime = float(dF_dchi(chi_fp, b_i, b_j))
        stability = "stable" if fprime < 0 else ("unstable" if fprime > 0 else "marginal")
        results.append({"chi": chi_fp, "label": label, "fprime": fprime, "stability": stability})
    return results


def demonstrate_stability_preserved_under_positive_S(
    b_i=gr.B_I, b_j=gr.B_J, S_values=(0.01, 0.5, 1.0, 10.0, 100.0),
):
    """sign(S*F'(chi*)) == sign(F'(chi*)) for every tested S>0: stability
    classification is invariant under positive multiplicative rescaling of
    the vector field. STANDARD DYNAMICAL-SYSTEMS RESULT, verified in this
    model's specific closed form."""
    fps = demonstrate_fixed_points(b_i, b_j)
    rows = []
    for fp in fps:
        base_sign = np.sign(fp["fprime"])
        preserved = all(np.sign(S * fp["fprime"]) == base_sign for S in S_values)
        rows.append({**fp, "sign_preserved_for_all_S": bool(preserved)})
    return rows


def main():
    print("MATHEMATICALLY DERIVED: positive time reparameterization of the")
    print("one-loop gauge-running system (d(tau) = S dt, S > 0)")
    print("This is a standard dynamical-systems result (orbital equivalence")
    print("under a positive scalar time-rescaling) applied to this domain model.")
    print()

    print("--- Direction comparator: D(chi) = sign((b_i-b_j)+(b_i+b_j)*chi) ---")
    dc = demonstrate_direction_comparator()
    print(f"  grid points = {dc['n_points']}")
    print(f"  mismatches vs sign(dchi/dtau) = {dc['mismatches_tau']}")
    for S, m in dc["mismatches_t"].items():
        print(f"  mismatches vs sign(dchi/dt), S={S:>5}: {m}")
    print()

    print("--- Fixed points of the reduced flow (b_i=7, b_j=-3) ---")
    for fp in demonstrate_fixed_points():
        print(f"  {fp['label']}: chi={fp['chi']:.6f}  f'={fp['fprime']:+.6f}  -> {fp['stability']}")
    print("  (interior fixed point exists only if |b_i-b_j| < |b_i+b_j|;")
    print(f"   here -A/B = {-(gr.B_I-gr.B_J)/(gr.B_I+gr.B_J):.4f}, outside (-1,1) -- none)")
    print()

    print("--- Stability preserved under positive S (pointwise rescaling) ---")
    for row in demonstrate_stability_preserved_under_positive_S():
        print(f"  {row['label']}: {row['stability']}, sign preserved for all tested S: "
              f"{row['sign_preserved_for_all_S']}")
    print()

    print("--- K conservation along a single full trajectory ---")
    kc = demonstrate_K_conservation()
    print(f"  K0 = {kc['K0']:.10f}")
    print(f"  max absolute drift = {kc['abs_drift']:.3e}")
    print(f"  max relative drift = {kc['rel_drift']:.3e}")
    print()

    print("--- chi(t) vs chi(tau) for two trajectories, same chi0, different S0 ---")
    rep = demonstrate_reparameterization()
    print(f"  chi0={rep['chi0']:.4f}, S0_1={rep['S0_1']}, S0_2={rep['S0_2']}")
    print(f"  max|chi1(t)-chi2(t)|     over common t   = {rep['residual_t_max']:.6e}  (expect large)")
    print(f"  max|chi1(tau)-chi2(tau)| over common tau = {rep['residual_tau_max']:.6e}  (expect ~0)")
    print("  -> different original-t rate, same reduced tau-orbit.")
    print()

    print("--- V_eff sign blindness (repository-specific point) ---")
    vb = demonstrate_V_eff_sign_blindness()
    print(f"  chi={vb['chi']}, v={vb['v']}")
    print(f"  V_eff(chi,+v) = {vb['V_plus']:.10f}")
    print(f"  V_eff(chi,-v) = {vb['V_minus']:.10f}")
    print(f"  |difference|  = {vb['difference']:.3e}")
    print(f"  D(+v) = {vb['D_plus']:+.0f},  D(-v) = {vb['D_minus']:+.0f}")
    print()

    print("STRUCTURAL INTERPRETATION: V_eff encodes speed-like normal-form")
    print("information; it cannot see direction because it is built from the")
    print("squared velocity. D(chi) is an orthogonal, complementary signed")
    print("channel -- not multiplied into V_eff, not a replacement for it.")
    print()
    print("Full state (chi,S), dimension 2, is required to reconstruct")
    print("alpha_i, alpha_j and evolution in the original RG parameter t.")
    print("The reduced, oriented chi(tau) orbit is one-dimensional and")
    print("autonomous. Both statements hold simultaneously; see")
    print("docs/state_dimension.md.")


if __name__ == "__main__":
    main()
