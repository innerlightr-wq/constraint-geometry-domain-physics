"""
Tests for the gauge-coupling-running adversarial example
(examples/gauge_running.py). See that module's docstring for the full
derivation and epistemic labeling.

Structure:
  - EXACT ALGEBRA: the partition decomposition and rapidity identity,
    true for any positive alpha_i, alpha_j.
  - Closed-form cross-check: the independently derived potential matches
    -1/2*(dchi/dt)^2/(1-chi^2) applied to the derived dchi/dt.
  - The lambda^2 scaling law (EXACT ALGEBRA, no ODE integration needed).
  - The central falsifiability demonstration: a genuine different-S family
    does NOT collapse (must be a MATERIALLY LARGE residual, not just "not
    small" -- a coding error that accidentally removed the S-dependence
    must make this test fail), while a deliberately constructed S-FIXED
    control DOES collapse cleanly (the mandatory control case, Section 12
    of the Milestone-2 audit).
  - The S-normalization rescue attempt collapses the family much better
    than the unnormalized comparison, without eliminating the need for S.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))

import numpy as np
import pytest

from constraint_geometry.coordinates import compute_xi, chi_from_xi
from constraint_geometry.falsifiability import shared_V_family_test

import gauge_running as gr


A_ALPHA_PAIRS = [
    (0.1, 0.05),
    (0.05, 0.1),
    (0.02, 0.08),
    (0.3, 0.3),
    (0.15, 0.01),
]


class TestExactAlgebra:
    """alpha_i = S(1+chi)/2, alpha_j = S(1-chi)/2; chi = tanh(xi). True for
    ANY positive (alpha_i, alpha_j) -- no domain physics assumed here."""

    def test_chi_S_roundtrip(self):
        for alpha_i, alpha_j in A_ALPHA_PAIRS:
            chi, S = gr.chi_S_from_alpha(alpha_i, alpha_j)
            ai_recon, aj_recon = gr.alpha_from_chi_S(chi, S)
            assert ai_recon == pytest.approx(alpha_i, abs=1e-12)
            assert aj_recon == pytest.approx(alpha_j, abs=1e-12)

    def test_S_is_sum(self):
        for alpha_i, alpha_j in A_ALPHA_PAIRS:
            _, S = gr.chi_S_from_alpha(alpha_i, alpha_j)
            assert S == pytest.approx(alpha_i + alpha_j)

    def test_chi_bounded_and_signed_correctly(self):
        for alpha_i, alpha_j in A_ALPHA_PAIRS:
            chi, _ = gr.chi_S_from_alpha(alpha_i, alpha_j)
            assert -1.0 < chi < 1.0
            assert (chi > 0) == (alpha_i > alpha_j)

    def test_rapidity_matches_half_log_ratio(self):
        for alpha_i, alpha_j in A_ALPHA_PAIRS:
            chi, _ = gr.chi_S_from_alpha(alpha_i, alpha_j)
            xi = compute_xi(chi)
            xi_direct = 0.5 * np.log(alpha_i / alpha_j)
            assert xi == pytest.approx(xi_direct, abs=1e-10)

    def test_chi_equals_tanh_xi(self):
        for alpha_i, alpha_j in A_ALPHA_PAIRS:
            chi, _ = gr.chi_S_from_alpha(alpha_i, alpha_j)
            xi = compute_xi(chi)
            assert chi_from_xi(xi) == pytest.approx(chi, abs=1e-12)

    def test_chi_invariant_under_common_rescaling(self):
        # (alpha_i, alpha_j) -> (lambda*alpha_i, lambda*alpha_j): chi fixed,
        # S -> lambda*S. Pure EXACT ALGEBRA, no running equation involved.
        alpha_i, alpha_j = 0.1, 0.05
        chi0, S0 = gr.chi_S_from_alpha(alpha_i, alpha_j)
        for lam in (0.5, 1.5, 2.0, 3.0):
            chi_l, S_l = gr.chi_S_from_alpha(lam * alpha_i, lam * alpha_j)
            assert chi_l == pytest.approx(chi0, abs=1e-13)
            assert S_l == pytest.approx(lam * S0, abs=1e-13)


class TestClosedFormCrossCheck:
    """V_closed_form must equal the repository's own normal-form definition
    -1/2*(dchi/dt)^2/(1-chi^2) applied to the independently derived
    dchi_dt_closed -- an internal consistency check of the derivation
    itself, not copied from the paper."""

    def test_closed_form_matches_normal_form_definition(self):
        for chi, S in [(0.1, 0.1), (-0.3, 0.05), (0.5, 0.2), (0.0, 0.3)]:
            dchidt = gr.dchi_dt_closed(chi, S)
            V_from_definition = -0.5 * dchidt**2 / (1.0 - chi**2)
            V_from_closed_form = gr.V_closed_form(chi, S)
            assert V_from_definition == pytest.approx(V_from_closed_form, rel=1e-12)


class TestSeparabilityExact:
    """EXACT ALGEBRA: V(chi;S) = S^2 * v(chi), with v(chi) genuinely
    independent of S. This is ALGEBRAIC SEPARABILITY (statement A in
    examples/gauge_running.py's module docstring) -- deliberately NOT the
    same claim as AUTONOMOUS DYNAMICAL REDUCTION (statement B), which
    TestFamilyTestDoesNotCollapse below shows does not hold."""

    def test_V_divided_by_S_squared_equals_v_chi(self):
        for chi in (-0.9, -0.3, 0.0, 0.2, 0.5, 0.9):
            for S in (0.01, 0.1, 1.0, 7.3):
                assert gr.V_closed_form(chi, S) / S**2 == pytest.approx(
                    gr.v_chi(chi), rel=1e-12
                )

    def test_v_chi_is_independent_of_S_by_construction(self):
        # v_chi's signature takes no S argument at all -- separability is
        # enforced by the function's own definition, not merely observed
        # numerically for particular inputs.
        import inspect

        assert "S" not in inspect.signature(gr.v_chi).parameters


class TestLambdaScalingLaw:
    """EXACT ALGEBRA: under the ratio-preserving family alpha -> lambda*alpha
    (chi fixed, S -> lambda*S), V_closed_form scales as lambda^2 exactly.
    This is the clean adversarial counterexample: identical chi, different
    S, quantifiably different V."""

    def test_V_scales_as_lambda_squared(self):
        chi0, S0 = 1.0 / 3.0, 0.15
        V0 = gr.V_closed_form(chi0, S0)
        for lam in (1.2, 1.5, 2.0, 3.0):
            V_lam = gr.V_closed_form(chi0, lam * S0)
            assert V_lam / V0 == pytest.approx(lam**2, rel=1e-12)

    def test_1_5x_scaling_gives_125_percent_discrepancy(self):
        # Matches the source paper's own reported figure -- reproduced
        # here from the independently derived closed form, not copied.
        chi0, S0 = 1.0 / 3.0, 0.15
        V0 = gr.V_closed_form(chi0, S0)
        V15 = gr.V_closed_form(chi0, 1.5 * S0)
        discrepancy_pct = (V15 / V0 - 1.0) * 100.0
        assert discrepancy_pct == pytest.approx(125.0, abs=1e-9)

    def test_dchi_dt_at_fixed_chi_scales_linearly_with_S(self):
        # Direct evidence chi alone is not a sufficient dynamical state:
        # same chi, S -> lambda*S implies dchi/dt -> lambda*dchi/dt.
        chi0 = 0.2
        base = gr.dchi_dt_closed(chi0, 0.1)
        for lam in (1.5, 2.0, 5.0):
            scaled = gr.dchi_dt_closed(chi0, lam * 0.1)
            assert scaled / base == pytest.approx(lam, rel=1e-12)


class TestFamilyTestDoesNotCollapse:
    """The central falsifiability demonstration. Must be able to fail: if a
    coding error accidentally removed the S-dependence, this test would
    catch it via the materially-large-residual assertion below."""

    @pytest.fixture(scope="class")
    def result(self):
        result, _, _ = gr.family_test_different_S()
        return result

    def test_residual_is_materially_large(self, result):
        # V's magnitude at these (chi, S) is O(1e-3); a residual this size
        # is not a rounding artifact -- see examples/gauge_running.py
        # output for the direct relative-scale comparison.
        assert result.residual_max > 1e-3, (
            f"expected a materially large residual for genuinely different "
            f"absolute scales S, got residual_max={result.residual_max!r} "
            f"-- if this is small, the S-dependence may have been lost"
        )

    def test_residual_dwarfs_the_fixed_S_control(self, result):
        control = gr.control_fixed_S()
        ratio = result.residual_max / control.residual_max
        assert ratio > 1e3, (
            f"expected the different-S residual to dwarf the fixed-S "
            f"control residual; got different-S={result.residual_max!r}, "
            f"control={control.residual_max!r}, ratio={ratio!r}"
        )


class TestFixedSControlCollapses:
    """The mandatory control (Section 12): with S truly held fixed across
    the family (an idealized sub-model with no scale variation at all),
    the shared-V family test must collapse cleanly. This proves the
    non-collapse above is caused by genuine S-dependence, not by the test
    machinery being broken or biased toward failure."""

    def test_fixed_S_control_residual_is_small(self):
        control = gr.control_fixed_S()
        assert control.residual_max < 1e-5, (
            f"expected a small residual when S is genuinely held fixed "
            f"across the family, got residual_max={control.residual_max!r}"
        )


class TestNormalizationRescue:
    """Rescue attempt (Section 9, item 3): dividing dchi/dt by the
    trajectory's own S(t) before comparing collapses the family much
    better than the unnormalized comparison -- confirming V_eff^(1)
    factors exactly as S^2 * v(chi) -- but this requires S(t) supplied
    externally at every point, so it does not establish that chi alone is
    a sufficient autonomous state."""

    def test_normalized_residual_much_smaller_than_unnormalized(self):
        unnormalized, _, _ = gr.family_test_different_S()
        normalized = gr.rescue_attempt_normalize_by_S()
        improvement = unnormalized.residual_max / normalized.residual_max
        assert improvement > 100.0, (
            f"expected S-normalization to substantially collapse the "
            f"residual (separability); got improvement factor={improvement!r}"
        )

    def test_normalized_residual_still_not_as_small_as_true_autonomy(self):
        # Sanity floor: even after normalization, this is a numerical
        # comparison (finite-difference derivatives on real ODE-integrated
        # trajectories), not an exact algebraic identity -- it should be
        # small, not machine-precision zero.
        normalized = gr.rescue_attempt_normalize_by_S()
        assert normalized.residual_max > 0.0


class TestSharedVFamilyTestAPIReuse:
    """Confirms this example reuses the existing Milestone-1
    shared_V_family_test rather than duplicating its logic."""

    def test_family_test_different_S_uses_existing_api(self):
        result, _, _ = gr.family_test_different_S()
        # Same result type as the Milestone-1 machinery.
        from constraint_geometry.falsifiability import FamilyTestResult

        assert isinstance(result, FamilyTestResult)
        assert result.label == "SYNTHETIC FALSIFIABILITY TEST"
