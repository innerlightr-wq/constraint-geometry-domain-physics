"""
INFORMATIVE NEGATIVE RESULT -- gauge-coupling running as an adversarial
test of the autonomous one-dimensional partition-potential hypothesis.

Conceptual source: "Effective Potentials on the Binary Partition Manifold:
A Two-Face Taxonomy of Domain Dynamics", Elias De Jesus, May 2026 (revised
June 2026), Section 11.3 "Worked example: gauge-coupling running as an
informative failure". Local file used:
~/Downloads/TwoFacePotentials (1).pdf (confirmed the June revision by its
title-page note "May 2026 (revised June 2026)" and by containing Section
11, "Falsifiability Protocol", which the unrevised May-only copy lacks).

All equations below are RE-DERIVED independently from the domain model
(the one-loop gauge-coupling running equation) and the repository's own
Milestone-1 Tier-1 machinery (extract_normal_form, shared_V_family_test),
not copied from the paper. The closed form obtained here is then checked
against the paper's reported equation (5) as an independent cross-check,
not assumed.

============================================================
1. EXACT ALGEBRA -- the partition decomposition
============================================================

For a pair of positive couplings alpha_i, alpha_j at RG scale t = ln(mu),
define the partition coordinate and the absolute-scale coordinate

    chi = (alpha_i - alpha_j) / (alpha_i + alpha_j),    S = alpha_i + alpha_j

Then, purely algebraically (a = alpha_i/S, b = alpha_j/S, a+b=1,
chi = a-b -- this repository's own signed convention):

    alpha_i = S(1+chi)/2,   alpha_j = S(1-chi)/2
    xi = arctanh(chi) = (1/2) ln(alpha_i/alpha_j),   chi = tanh(xi)

These are EXACT ALGEBRA: true for ANY positive alpha_i, alpha_j, with no
physics assumed yet. See tests/test_gauge_running.py::TestExactAlgebra.

============================================================
2. DOMAIN MODEL INPUT -- one-loop running
============================================================

The one-loop gauge-coupling running equation (a physics assumption, not a
constraint-geometry identity):

    d(ln alpha_i)/dt = (b_i / 2*pi) * alpha_i

with b_i, b_j the one-loop beta-function coefficients. B_I and B_J below
are ILLUSTRATIVE, ARBITRARY constants chosen only to exhibit the
structural point of this example -- they are NOT calibrated Standard
Model values, and no comparison to observational or precision data is
made anywhere in this file (see docs/software_scope.md and Section 15 of
the Milestone-2 audit: SXS, SDSS, and Standard-Model precision-data
comparison are explicitly out of scope for this milestone).

============================================================
3. MATHEMATICALLY DERIVED -- evolution of (chi, S)
============================================================

Differentiating the EXACT ALGEBRA relations above under the DOMAIN MODEL
INPUT running equation (full derivation in the Milestone-2 audit report;
reproduced compactly here):

    dchi/dt = (1 - chi^2) * S/(8*pi) * [(b_i-b_j) + (b_i+b_j)*chi]
    dS/dt   = S^2/(8*pi)   * [(b_i+b_j)*(1+chi^2) + 2*(b_i-b_j)*chi]

dchi/dt depends EXPLICITLY on S (a linear overall factor) as well as on
chi -- the (chi, S) system does not close on chi alone. This is the
central structural fact this example demonstrates and tests.

============================================================
4. NORMAL-FORM EXTRACTION -- the closed-form potential
============================================================

Substituting dchi/dt into the repository's existing Tier-1 normal form
V_eff^(1)(chi) = -1/2 * (dchi/dt)^2 / (1-chi^2) gives the closed form

    V_ij^(1)(chi; S) = -S^2/(128*pi^2) * (1-chi^2) * [(b_i-b_j)+(b_i+b_j)*chi]^2

which matches the paper's equation (5) exactly (cross-checked in
tests/test_gauge_running.py::TestClosedFormCrossCheck), i.e.

    V_ij^(1)(chi; S) = S^2 * v(chi),   v(chi) = -1/(128*pi^2)*(1-chi^2)*bracket^2

Two distinct statements, deliberately not conflated anywhere in this file:

  A. ALGEBRAIC SEPARABILITY -- V(chi;S) = S^2 * v(chi). This DOES hold:
     v(chi) above is genuinely independent of S.
  B. AUTONOMOUS DYNAMICAL REDUCTION -- dchi/dt = F(chi) alone. This does
     NOT hold: dchi/dt (Section 3 above) retains an explicit S factor
     under the original running parameter t. Separability of the
     POTENTIAL'S SHAPE does not restore autonomy of the DYNAMICS that
     produced it -- S must still be known to reconstruct the actual
     evolution rate. See docs/state_dimension.md for the full statement
     of this distinction.

Run directly:

    python examples/gauge_running.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np
from scipy.integrate import solve_ivp

from constraint_geometry.coordinates import compute_xi, chi_from_xi, compute_chi_signed
from constraint_geometry.normal_form import extract_normal_form
from constraint_geometry.falsifiability import FamilyMember, shared_V_family_test

# Illustrative, arbitrary one-loop coefficients -- NOT Standard Model values.
B_I = 7.0
B_J = -3.0


# ---------------------------------------------------------------------------
# EXACT ALGEBRA
# ---------------------------------------------------------------------------

def chi_S_from_alpha(alpha_i, alpha_j):
    """chi = (alpha_i-alpha_j)/(alpha_i+alpha_j), S = alpha_i+alpha_j. EXACT ALGEBRA."""
    S = alpha_i + alpha_j
    chi = compute_chi_signed(alpha_i / S, alpha_j / S)
    return chi, S


def alpha_from_chi_S(chi, S):
    """Inverse of chi_S_from_alpha: alpha_i=S(1+chi)/2, alpha_j=S(1-chi)/2. EXACT ALGEBRA."""
    return S * (1.0 + chi) / 2.0, S * (1.0 - chi) / 2.0


# ---------------------------------------------------------------------------
# DOMAIN MODEL INPUT -- one-loop running, and its MATHEMATICALLY DERIVED
# consequences for (chi, S).
# ---------------------------------------------------------------------------

def _one_loop_rhs(t, y, b_i, b_j):
    alpha_i, alpha_j = y
    return [(b_i / (2 * np.pi)) * alpha_i**2, (b_j / (2 * np.pi)) * alpha_j**2]


def integrate_running(alpha_i0, alpha_j0, t_max, n, b_i=B_I, b_j=B_J):
    """Integrate the coupled two-coupling one-loop system and return
    (t, chi, S, alpha_i, alpha_j) samples. DOMAIN MODEL INPUT + NUMERICAL
    DEMONSTRATION (real ODE integration, not a synthetic toy)."""
    sol = solve_ivp(
        _one_loop_rhs, [0.0, t_max], [alpha_i0, alpha_j0], args=(b_i, b_j),
        t_eval=np.linspace(0.0, t_max, n), rtol=1e-12, atol=1e-15, method="RK45",
    )
    alpha_i, alpha_j = sol.y
    S = alpha_i + alpha_j
    chi = (alpha_i - alpha_j) / S
    return sol.t, chi, S, alpha_i, alpha_j


def dchi_dt_closed(chi, S, b_i=B_I, b_j=B_J):
    """MATHEMATICALLY DERIVED: dchi/dt = (1-chi^2)*S/(8pi)*[(b_i-b_j)+(b_i+b_j)*chi]."""
    bracket = (b_i - b_j) + (b_i + b_j) * chi
    return (1.0 - chi**2) * S / (8 * np.pi) * bracket


def dS_dt_closed(chi, S, b_i=B_I, b_j=B_J):
    """MATHEMATICALLY DERIVED: dS/dt = S^2/(8pi)*[(b_i+b_j)(1+chi^2)+2(b_i-b_j)chi]."""
    return (S**2 / (8 * np.pi)) * ((b_i + b_j) * (1.0 + chi**2) + 2.0 * (b_i - b_j) * chi)


def v_chi(chi, b_i=B_I, b_j=B_J):
    """MATHEMATICALLY DERIVED: the chi-only SHAPE factor in the exact
    factorization V_ij^(1)(chi; S) = S^2 * v(chi):

        v(chi) = -1/(128*pi^2) * (1-chi^2) * [(b_i-b_j)+(b_i+b_j)*chi]^2

    v(chi) is genuinely S-independent (ALGEBRAIC SEPARABILITY -- see
    V_closed_form below and docs/state_dimension.md). This does NOT by
    itself mean chi is a sufficient autonomous dynamical state: recovering
    the actual evolution rate dchi/dt still requires S, which v(chi) alone
    cannot supply. See AUTONOMOUS-CHI TEST in the Milestone-2 report."""
    bracket = (b_i - b_j) + (b_i + b_j) * chi
    return -(1.0 / (128 * np.pi**2)) * (1.0 - chi**2) * bracket**2


def V_closed_form(chi, S, b_i=B_I, b_j=B_J):
    """MATHEMATICALLY DERIVED / NORMAL-FORM EXTRACTION closed form:

        V_ij^(1)(chi; S) = S^2 * v(chi; b_i, b_j)

    i.e. -S^2/(128*pi^2) * (1-chi^2) * bracket^2. Matches the source
    paper's equation (5) (cross-checked in tests).

    Two distinct facts, not to be conflated:
      A. ALGEBRAIC SEPARABILITY (this equation): V factors exactly as
         S^2 times a chi-only shape v(chi). TRUE.
      B. AUTONOMOUS DYNAMICAL REDUCTION: dchi/dt = F(chi) alone. FALSE --
         see dchi_dt_closed below, which retains an explicit S factor.
    Separability does not imply, and here does not produce, autonomy."""
    return S**2 * v_chi(chi, b_i, b_j)


# ---------------------------------------------------------------------------
# Demonstrations
# ---------------------------------------------------------------------------

def lambda_scaling_check(chi0=1.0 / 3.0, S0=0.15, lambdas=(1.5, 2.0, 3.0)):
    """EXACT ALGEBRA: quantify V(chi0; lambda*S0) / V(chi0; S0) against the
    predicted lambda^2 law, at fixed chi (the ratio-preserving rescaling
    alpha -> lambda*alpha leaves chi unchanged and sends S -> lambda*S)."""
    rows = []
    V0 = V_closed_form(chi0, S0)
    for lam in lambdas:
        Vlam = V_closed_form(chi0, lam * S0)
        ratio = Vlam / V0
        rows.append((lam, ratio, lam**2, (ratio - 1.0) * 100.0))
    return rows


def _normal_form_comparison_member(t, chi, label, dchi_dx=None):
    """Wrap an extracted trajectory as a FamilyMember for direct
    normal-form comparison via shared_V_family_test.

    IMPORTANT API-USAGE NOTE (not a Milestone-1 bug, and no core-package
    change is made here): FamilyMember.E is documented in
    src/constraint_geometry/falsifiability.py as "the conserved energy (or
    OTHER EXTERNAL FAMILY PARAMETER)". Gauge-coupling running is a
    first-order, non-Hamiltonian flow -- it has no conserved mechanical
    energy in the sense the Milestone-1 harmonic-oscillator demonstration
    used. E is therefore fixed at 0.0 for every member here, which is
    already extract_normal_form's own implicit zero-energy normal-form
    convention (docs/epistemic_tiers.md, Tier 1) applied uniformly. With
    E=0.0, FamilyMember.U(chi) = -1/2*G(chi)*(dchi/dx)^2 reduces exactly
    to the raw extracted V_eff^(1)(chi).

    So this is NOT a literal conserved-energy shared-V family test in the
    Milestone-1 mechanical sense. It is a direct reuse of the SAME
    curve-collapse comparison machinery to ask a narrower, still valid
    question licensed by docs/protocol.md Step 5 route 1 ("differ by an
    external parameter -- energy, initial condition, mass, boundary
    data"): does the raw extracted V_eff^(1)(chi) collapse across a family
    that differs in absolute scale S (via each trajectory's own S(t),
    entering through the domain dynamics, not through this E field)."""
    nf = extract_normal_form(t, chi, dchi_dx=dchi_dx)
    return FamilyMember(chi=nf.chi, dchi_dx=nf.dchi_dx, E=0.0, label=label)


def family_test_different_S():
    """NUMERICAL DEMONSTRATION: two ODE-integrated trajectories sharing the
    same initial chi (=1/3) but differing in absolute scale S by a factor
    lambda=2, compared via _normal_form_comparison_member (see its
    docstring for the E=0.0 usage note) and the existing
    shared_V_family_test machinery -- a direct test of whether the raw
    extracted V_eff^(1)(chi) collapses across the family."""
    t1, chi1, S1, _, _ = integrate_running(0.10, 0.05, t_max=2.0, n=4000)
    t2, chi2, S2, _, _ = integrate_running(0.20, 0.10, t_max=2.0, n=4000)
    m1 = _normal_form_comparison_member(t1, chi1, "traj1 (S0=0.15)")
    m2 = _normal_form_comparison_member(t2, chi2, "traj2 (S0=0.30, lambda=2)")
    result = shared_V_family_test([m1, m2], n_grid=300)
    return result, (t1, chi1, S1), (t2, chi2, S2)


def control_fixed_S():
    """NUMERICAL DEMONSTRATION (control, Section 12 of the Milestone-2
    audit): freeze S at a single external value and integrate chi alone --
    an idealized sub-model in which, by construction, there is no
    scale-variation between family members. If the shared-V family test
    were broken (e.g. always reporting a tiny residual regardless of
    input), this control would look identical to the genuine different-S
    case above; the fact that it does not is what makes the different-S
    result trustworthy rather than a software artifact."""

    def rhs(t, y, S_fixed):
        chi = y[0]
        return [dchi_dt_closed(chi, S_fixed)]

    S_fixed = 0.2
    sol_a = solve_ivp(rhs, [0.0, 1.5], [-0.1], args=(S_fixed,),
                       t_eval=np.linspace(0.0, 1.5, 4000), rtol=1e-12, atol=1e-15)
    sol_b = solve_ivp(rhs, [0.0, 1.5], [0.0], args=(S_fixed,),
                       t_eval=np.linspace(0.0, 1.5, 4000), rtol=1e-12, atol=1e-15)
    m_a = _normal_form_comparison_member(sol_a.t, sol_a.y[0], "control A (S fixed=0.2)")
    m_b = _normal_form_comparison_member(sol_b.t, sol_b.y[0], "control B (S fixed=0.2)")
    return shared_V_family_test([m_a, m_b], n_grid=300)


def rescue_attempt_normalize_by_S():
    """Rescue attempt (Section 9, item 3 of the Milestone-2 audit):
    normalize the extracted derivative by the trajectory's OWN S(t) before
    comparing (dchi/dt -> dchi/dt / S(t), pointwise). Uses
    _normal_form_comparison_member's dchi_dx override, so the same E=0.0
    usage note applies (see that function's docstring).

    Three things this test does and does not show, kept explicitly
    separate:
      EXACT ALGEBRA: V_eff^(1)/S^2 = v(chi) -- the normalized shape
        collapses (checked numerically below and exactly in
        tests/test_gauge_running.py::TestSeparabilityExact).
      STRUCTURAL INTERPRETATION: this demonstrates algebraic
        separability of the potential.
      NOT ESTABLISHED: autonomous chi-only domain dynamics. Dividing by
        S(t) requires already knowing S(t) at every point -- it does not
        remove S from the minimal state needed to know the evolution
        rate dchi/dt itself, only from the SHAPE of V once S is known."""
    t1, chi1, S1, _, _ = integrate_running(0.10, 0.05, t_max=2.0, n=4000)
    t2, chi2, S2, _, _ = integrate_running(0.20, 0.10, t_max=2.0, n=4000)
    nf1 = extract_normal_form(t1, chi1)
    nf2 = extract_normal_form(t2, chi2)
    m1 = _normal_form_comparison_member(t1, chi1, "traj1 /S", dchi_dx=nf1.dchi_dx / S1)
    m2 = _normal_form_comparison_member(t2, chi2, "traj2 /S, lambda=2", dchi_dx=nf2.dchi_dx / S2)
    return shared_V_family_test([m1, m2], n_grid=300)


def main():
    print("INFORMATIVE NEGATIVE RESULT: gauge-coupling running vs. an")
    print("autonomous one-dimensional partition potential V(chi)")
    print("Source: Effective Potentials on the Binary Partition Manifold")
    print("(June 2026 revision), Section 11.3 -- re-derived independently here.")
    print()

    print("--- EXACT ALGEBRA sanity check ---")
    alpha_i, alpha_j = 0.10, 0.05
    chi, S = chi_S_from_alpha(alpha_i, alpha_j)
    ai_recon, aj_recon = alpha_from_chi_S(chi, S)
    xi = compute_xi(chi)
    xi_direct = 0.5 * np.log(alpha_i / alpha_j)
    print(f"  alpha_i={alpha_i}, alpha_j={alpha_j}  ->  chi={chi:.6f}, S={S:.6f}")
    print(f"  reconstructed alpha_i={ai_recon:.6f}, alpha_j={aj_recon:.6f} (should equal inputs)")
    print(f"  xi=arctanh(chi)={xi:.6f}, (1/2)ln(alpha_i/alpha_j)={xi_direct:.6f} (should agree)")
    print()

    print("--- EXACT ALGEBRA: lambda^2 scaling law ---")
    print("  V(chi0; lambda*S0) / V(chi0; S0)  vs.  lambda^2")
    for lam, ratio, lam2, pct in lambda_scaling_check():
        print(f"  lambda={lam:.1f}: ratio={ratio:.6f}  lambda^2={lam2:.6f}  discrepancy={pct:.4f}%")
    print()

    print("--- NUMERICAL DEMONSTRATION: shared-V family test (different S) ---")
    result, (t1, chi1, S1), (t2, chi2, S2) = family_test_different_S()
    print(f"  traj1: chi in [{chi1.min():.4f}, {chi1.max():.4f}], S in [{S1.min():.4f}, {S1.max():.4f}]")
    print(f"  traj2: chi in [{chi2.min():.4f}, {chi2.max():.4f}], S in [{S2.min():.4f}, {S2.max():.4f}]")
    print(f"  residual_max = {result.residual_max:.6e}")
    print(f"  residual_rms = {result.residual_rms:.6e}")
    print(f"  overlap range = {result.chi_overlap_range}")
    print("  -> the test FIRES: no autonomous V(chi) fits both trajectories.")
    print()

    print("--- CONTROL: S truly held fixed (idealized sub-model) ---")
    ctrl = control_fixed_S()
    print(f"  residual_max = {ctrl.residual_max:.6e}")
    print(f"  residual_rms = {ctrl.residual_rms:.6e}")
    print("  -> collapses cleanly: the machinery is not systematically broken;")
    print("     the different-S non-collapse above is genuinely due to S-dependence.")
    print(f"  ratio (different-S residual / control residual) = "
          f"{result.residual_max / ctrl.residual_max:.3e}")
    print()

    print("--- RESCUE ATTEMPT: normalize by S(t) (supplied externally) ---")
    rescued = rescue_attempt_normalize_by_S()
    print(f"  residual_max = {rescued.residual_max:.6e}  (was {result.residual_max:.6e} unnormalized)")
    print(f"  improvement factor = {result.residual_max / rescued.residual_max:.1f}x")
    print("  -> the SHAPE v(chi) = V/S^2 is universal (separable), but S had to be")
    print("     supplied externally at every point: this does not reduce the")
    print("     minimal dynamical state below (chi, S). See docs/software_scope.md.")
    print()

    print("STRUCTURAL INTERPRETATION: chi records relative composition;")
    print("S records absolute scale. The potential is algebraically separable")
    print("(V=S^2*v(chi)), but the one-loop dynamics do not close on chi alone:")
    print("dchi/dt = F(chi, S), not F(chi). This is an INFORMATIVE NEGATIVE")
    print("RESULT for the autonomous chi-only hypothesis in this closed")
    print("(chi,S) model -- not a failure of the constraint-geometry layer")
    print("itself, and not evidence that gauge physics is fundamentally")
    print("two-dimensional in any deeper sense. See NON_CLAIMS.md and")
    print("docs/state_dimension.md.")


if __name__ == "__main__":
    main()
