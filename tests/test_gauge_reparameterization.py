"""
Tests for the positive-time-reparameterization / direction-rate example
(examples/gauge_reparameterization.py). See that module's docstring for
the full derivation and epistemic labeling.

These tests implement exactly the results of the Milestone-3 research
audit and its direction-rate follow-up audit: the reparameterized reduced
flow, the conserved orbit label K, the direction comparator D(chi), and
the sign-blindness of the existing V_eff normal form. Nothing broader.
Positive-scalar-time-rescaling / orbital equivalence is standard
dynamical-systems mathematics, not presented here as novel; only the
specific closed-form instance for this domain model is new content.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))

import numpy as np
import pytest

import gauge_running as gr
import gauge_reparameterization as reparam


class TestReducedEquationMatchesAnalyticFormula:
    """dchi/dtau = (1-chi^2)/(8*pi) * bracket(chi), independent of S, and
    equal to dchi_dt_closed(chi, S) / S for every tested S -- an internal
    cross-check that the reparameterized formula and the Milestone-2
    original-t formula are the same function related by division by S."""

    def test_dchi_dtau_matches_dchi_dt_over_S(self):
        for chi in (-0.9, -0.3, 0.0, 0.2, 0.5, 0.9):
            for S in (0.01, 0.15, 1.0, 50.0):
                lhs = reparam.dchi_dtau_closed(chi)
                rhs = gr.dchi_dt_closed(chi, S) / S
                assert lhs == pytest.approx(rhs, rel=1e-12)

    def test_dchi_dtau_is_S_independent_by_signature(self):
        import inspect

        assert "S" not in inspect.signature(reparam.dchi_dtau_closed).parameters


class TestPositiveSPreservesDirection:
    """sign(dchi/dt) == sign(dchi/dtau) for S > 0 -- EXACT ALGEBRA."""

    def test_sign_preserved_across_S_values(self):
        chis = np.linspace(-0.9, 0.9, 25)
        d_tau = reparam.dchi_dtau_closed(chis)
        for S in (1e-6, 0.01, 0.15, 1.0, 50.0, 1e6):
            d_t = gr.dchi_dt_closed(chis, S)
            assert np.array_equal(np.sign(d_t), np.sign(d_tau))


class TestComparatorZeroMismatches:
    """The dense-grid check from the audit: chi in [-0.999, 0.999], 2001
    points, S in {0.01, 0.15, 1.0, 50.0}. Expected: zero mismatches."""

    def test_zero_mismatches_on_audit_grid(self):
        result = reparam.demonstrate_direction_comparator()
        assert result["n_points"] == 2001
        assert result["mismatches_tau"] == 0, (
            f"expected zero mismatches between D(chi) and sign(dchi/dtau), "
            f"got {result['mismatches_tau']}"
        )
        for S, mismatches in result["mismatches_t"].items():
            assert mismatches == 0, (
                f"expected zero mismatches between D(chi) and sign(dchi/dt) "
                f"at S={S}, got {mismatches}"
            )


class TestDifferentS0GivesDifferentOriginalTRate:
    """Same chi, different S -> different |dchi/dt| (rate), by exactly the
    ratio of the S values -- direct evidence chi alone does not determine
    the original-t rate."""

    def test_rate_ratio_equals_S_ratio(self):
        chi0 = 0.2
        base = gr.dchi_dt_closed(chi0, 0.1)
        for lam in (1.5, 2.0, 5.0):
            scaled = gr.dchi_dt_closed(chi0, lam * 0.1)
            assert scaled / base == pytest.approx(lam, rel=1e-12)


class TestDifferentS0CollapsesInTau:
    """The central falsifiability-style demonstration: chi(t) must differ
    materially between two trajectories sharing chi0 but not S0, while
    chi(tau) must collapse to near-zero residual. Both assertions are
    required -- a coding error that accidentally removed the S-dependence
    from the original system would make the first assertion fail; an
    error in the reparameterization itself would make the second fail."""

    @pytest.fixture(scope="class")
    def result(self):
        return reparam.demonstrate_reparameterization()

    def test_chi_of_t_differs_materially(self, result):
        assert result["residual_t_max"] > 1e-2, (
            f"expected chi(t) to differ materially between different-S0 "
            f"trajectories, got residual_t_max={result['residual_t_max']!r}"
        )

    def test_chi_of_tau_collapses(self, result):
        assert result["residual_tau_max"] < 1e-6, (
            f"expected chi(tau) to collapse across different-S0 "
            f"trajectories, got residual_tau_max={result['residual_tau_max']!r}"
        )

    def test_tau_collapse_dwarfs_t_residual(self, result):
        # Relational assertion, mirroring the M1/M2 falsifiability style:
        # guards against a degenerate implementation where both residuals
        # happen to be small or both happen to be large for unrelated
        # reasons.
        ratio = result["residual_t_max"] / result["residual_tau_max"]
        assert ratio > 1e4


class TestKConservation:
    """K = S*(1-chi^2)/bracket(chi) conserved along a full trajectory, away
    from the singular locus bracket=0."""

    def test_K_conserved_to_tight_tolerance(self):
        result = reparam.demonstrate_K_conservation()
        assert result["rel_drift"] < 1e-8, (
            f"expected K to be conserved to near machine precision, got "
            f"rel_drift={result['rel_drift']!r}"
        )

    def test_K_matches_initial_condition_formula(self):
        chi0, S0 = 1.0 / 3.0, 0.15
        result = reparam.demonstrate_K_conservation(chi0=chi0, S0=S0)
        A, B = gr.B_I - gr.B_J, gr.B_I + gr.B_J
        expected_K0 = S0 * (1.0 - chi0**2) / (A + B * chi0)
        assert result["K0"] == pytest.approx(expected_K0, rel=1e-10)

    def test_k_of_raises_near_singular_bracket(self):
        # bracket=0 at chi=-A/B; for B_I=7,B_J=-3 that is chi=-2.5, outside
        # the physical domain, so construct an explicit near-singular chi
        # relative to a different (b_i, b_j) pair with an interior zero.
        b_i, b_j = 1.0, 3.0  # A=-2, B=4 -> bracket=0 at chi=0.5
        with pytest.raises(ValueError):
            reparam.k_of(0.5, 0.2, b_i=b_i, b_j=b_j, bracket_floor=1e-6)

    def test_k_of_does_not_raise_away_from_singular_bracket(self):
        b_i, b_j = 1.0, 3.0
        # Far from chi=0.5, bracket is not near zero.
        value = reparam.k_of(-0.5, 0.2, b_i=b_i, b_j=b_j, bracket_floor=1e-6)
        assert np.isfinite(value)


class TestFullCouplingReconstructionRequiresS:
    """alpha_i, alpha_j cannot be recovered from chi alone -- S is required.
    EXACT ALGEBRA, unchanged from Milestone 2."""

    def test_same_chi_different_S_gives_different_couplings(self):
        chi0 = 0.25
        ai1, aj1 = gr.alpha_from_chi_S(chi0, 0.1)
        ai2, aj2 = gr.alpha_from_chi_S(chi0, 0.2)
        assert ai1 != pytest.approx(ai2)
        assert aj1 != pytest.approx(aj2)
        # But the ratio (and hence chi) is identical.
        assert (ai1 - aj1) / (ai1 + aj1) == pytest.approx((ai2 - aj2) / (ai2 + aj2))


class TestVEffSignBlindness:
    """EXACT ALGEBRA: V_eff(chi,+v) = V_eff(chi,-v); D(+v) != D(-v)."""

    def test_V_eff_identical_under_velocity_reversal(self):
        for chi, v in [(0.2, 0.37), (-0.5, 1.2), (0.0, 0.9), (0.8, 0.05)]:
            result = reparam.demonstrate_V_eff_sign_blindness(chi=chi, v=v)
            assert result["V_plus"] == pytest.approx(result["V_minus"], rel=1e-14)
            assert result["difference"] == pytest.approx(0.0, abs=1e-15)

    def test_direction_comparator_flips_under_velocity_reversal(self):
        result = reparam.demonstrate_V_eff_sign_blindness(chi=0.2, v=0.37)
        assert result["D_plus"] == 1.0
        assert result["D_minus"] == -1.0
        assert result["D_plus"] != result["D_minus"]

    def test_v_equals_zero_raises_rather_than_returning_undefined_direction(self):
        with pytest.raises(ValueError):
            reparam.demonstrate_V_eff_sign_blindness(chi=0.2, v=0.0)


class TestFixedPointsPreservedUnderPositiveS:
    """Multiplying the reduced vector field by a positive S does not move
    the fixed points, change direction on non-equilibrium intervals, or
    change stability classification -- standard consequences of positive
    scalar orbital equivalence, verified in this model's closed form."""

    def test_illustrative_case_has_no_interior_fixed_point(self):
        # b_i=7, b_j=-3 -> A=10, B=4 -> -A/B=-2.5, outside (-1,1).
        assert reparam.interior_fixed_point(b_i=7.0, b_j=-3.0) is None

    def test_second_case_has_interior_fixed_point(self):
        # b_i=1, b_j=3 -> A=-2, B=4 -> -A/B=0.5, inside (-1,1).
        chi_star = reparam.interior_fixed_point(b_i=1.0, b_j=3.0)
        assert chi_star == pytest.approx(0.5)

    def test_boundary_fixed_points_are_zeros_of_F(self):
        for chi_fp in (-1.0, 1.0):
            assert reparam.dchi_dtau_closed(chi_fp) == pytest.approx(0.0, abs=1e-12)

    def test_interior_fixed_point_is_a_zero_of_F(self):
        b_i, b_j = 1.0, 3.0
        chi_star = reparam.interior_fixed_point(b_i=b_i, b_j=b_j)
        assert reparam.dchi_dtau_closed(chi_star, b_i=b_i, b_j=b_j) == pytest.approx(0.0, abs=1e-12)

    def test_illustrative_case_stability_pattern(self):
        fps = reparam.demonstrate_fixed_points()
        by_label = {fp["label"]: fp for fp in fps}
        assert by_label["boundary chi=-1"]["stability"] == "unstable"
        assert by_label["boundary chi=+1"]["stability"] == "stable"

    def test_second_case_alternating_stability_pattern(self):
        # -1 stable, interior unstable, +1 stable -- an alternating
        # stable/unstable/stable pattern on a smooth 1D flow with three
        # fixed points, as required topologically.
        fps = reparam.demonstrate_fixed_points(b_i=1.0, b_j=3.0)
        by_label = {fp["label"]: fp for fp in fps}
        assert by_label["boundary chi=-1"]["stability"] == "stable"
        assert by_label["interior chi*=-A/B"]["stability"] == "unstable"
        assert by_label["boundary chi=+1"]["stability"] == "stable"


class TestStabilityClassificationPreservedUnderPositiveS:
    def test_sign_preserved_for_illustrative_case(self):
        rows = reparam.demonstrate_stability_preserved_under_positive_S()
        assert len(rows) == 2  # no interior fixed point for b_i=7, b_j=-3
        for row in rows:
            assert row["sign_preserved_for_all_S"] is True

    def test_sign_preserved_for_case_with_interior_fixed_point(self):
        rows = reparam.demonstrate_stability_preserved_under_positive_S(b_i=1.0, b_j=3.0)
        assert len(rows) == 3
        for row in rows:
            assert row["sign_preserved_for_all_S"] is True
