"""
Tests for the constraint-intersection diagnostics example
(examples/constraint_intersection_diagnostics.py). See that module's
docstring and docs/constraint_intersection_diagnostics.md for the full
statement. Narrow scope: standard transversality/rank mathematics applied
to the intrinsic-cubic family, plus the invariance facts that govern which
diagnostics may be compared across representations.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))

import numpy as np
import pytest

import constraint_intersection_diagnostics as cid


B_VALUES = [0.1, 0.3, 0.6823278038, 0.9]
Q_VALUES = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]


class TestPowerFamilyTransversality:
    """EXACT ALGEBRA: det J_q < 0 and rank J_q = 2 for every tested q>0
    and b>0 -- transversality does not distinguish q=3."""

    def test_det_negative_for_all_q_and_b(self):
        for q in Q_VALUES:
            for b in B_VALUES:
                J = cid.jacobian_F_Gq(b, q)
                det, _ = cid.det_and_rank(J)
                assert det < 0.0, f"expected det<0 at q={q}, b={b}, got {det!r}"

    def test_rank_full_for_all_q_and_b(self):
        for q in Q_VALUES:
            for b in B_VALUES:
                J = cid.jacobian_F_Gq(b, q)
                _, rank = cid.det_and_rank(J)
                assert rank == 2, f"expected rank=2 at q={q}, b={b}, got {rank!r}"

    def test_det_matches_closed_form(self):
        for q in Q_VALUES:
            for b in B_VALUES:
                J = cid.jacobian_F_Gq(b, q)
                det, _ = cid.det_and_rank(J)
                expected = -(1.0 + q * b ** (q - 1.0))
                assert det == pytest.approx(expected, rel=1e-12)

    def test_q_equals_3_is_not_singled_out_by_transversality(self):
        # No test in this class treats q=3 differently -- confirmed by
        # construction: the same assertions pass for every q in Q_VALUES,
        # q=3 included, with no special-cased tolerance or threshold.
        dets = {q: cid.det_and_rank(cid.jacobian_F_Gq(0.5, q))[0] for q in Q_VALUES}
        assert all(d < 0 for d in dets.values())
        # q=3's determinant is not extremal (neither min nor max) among
        # the tested family at this b -- an explicit check that it has no
        # privileged magnitude either.
        assert dets[3.0] != max(dets.values())
        assert dets[3.0] != min(dets.values())


class TestCubicFunctionalIdentity:
    """EXACT ALGEBRA: h=sqrt(ab) equals r=a/b for q=3 along multiple
    positive b values with a=b^3; the identity does NOT hold generically
    for other q."""

    def test_h_equals_r_for_q_3_across_multiple_b(self):
        for b in (0.1, 0.3, 0.5, 0.6823278038, 0.9, 1.5, 3.0):
            a = b ** 3
            h, r = cid.h_and_ratio(a, b)
            assert h == pytest.approx(r, rel=1e-12), (
                f"expected h==r for q=3 at b={b}, got h={h!r}, r={r!r}"
            )

    def test_h_does_not_equal_r_generically_for_other_q(self):
        # Not "never equal at any point" (they can coincide at isolated b
        # for other q -- e.g. b=1 trivially gives h=r=1 for any q), but
        # NOT an identity across the tested range, unlike q=3.
        for q in (0.25, 0.5, 1.0, 2.0, 5.0, 10.0):
            mismatches = 0
            for b in (0.1, 0.3, 0.5, 0.6823278038, 0.9, 1.5, 3.0):
                if b == 1.0:
                    continue  # trivial coincidence point for every q
                a = b ** q
                h, r = cid.h_and_ratio(a, b)
                if abs(h - r) > 1e-9:
                    mismatches += 1
            assert mismatches > 0, f"expected h!=r somewhere in the tested range for q={q}"

    def test_q_3_closed_form_matches_exponent_derivation(self):
        # h = b^((q+1)/2), r = b^(q-1); confirms the closed forms
        # themselves, not just the resulting equality at q=3.
        q = 3.0
        for b in (0.2, 0.5, 0.6823278038, 1.3):
            a = b ** q
            h, r = cid.h_and_ratio(a, b)
            assert h == pytest.approx(b ** ((q + 1.0) / 2.0), rel=1e-12)
            assert r == pytest.approx(b ** (q - 1.0), rel=1e-12)


class TestConstraintRescaling:
    """STANDARD MATHEMATICAL RESULT: rank invariant, det scales by
    alpha*beta, under F->alpha*F, G->beta*G for nonzero alpha, beta."""

    @pytest.mark.parametrize("alpha,beta", [(2.0, 3.0), (-1.0, 5.0), (0.01, 100.0), (-3.0, -7.0), (5.0, -0.5)])
    def test_rank_invariant_under_rescaling(self, alpha, beta):
        result = cid.demonstrate_constraint_rescaling(alpha=alpha, beta=beta)
        assert result["rank_rescaled"] == result["rank_original"]

    @pytest.mark.parametrize("alpha,beta", [(2.0, 3.0), (-1.0, 5.0), (0.01, 100.0), (-3.0, -7.0), (5.0, -0.5)])
    def test_det_scales_by_alpha_beta(self, alpha, beta):
        result = cid.demonstrate_constraint_rescaling(alpha=alpha, beta=beta)
        assert result["det_rescaled"] == pytest.approx(
            result["det_original"] * alpha * beta, rel=1e-12
        )


class TestAngleUnderRescaling:
    """STANDARD MATHEMATICAL RESULT: gradient-angle magnitude invariant
    under constraint rescaling (constants), sign follows sign(alpha*beta)."""

    def test_magnitude_invariant_across_all_tested_rescalings(self):
        result = cid.demonstrate_angle_under_rescaling()
        for row in result["rescaled"]:
            assert row["magnitude_matches"] is True

    def test_sign_follows_alpha_beta_sign(self):
        result = cid.demonstrate_angle_under_rescaling()
        for row in result["rescaled"]:
            assert row["sign_matches_alpha_beta_sign"] is True

    def test_positive_rescaling_leaves_sign_unchanged(self):
        result = cid.demonstrate_angle_under_rescaling(alphas_betas=((2.0, 3.0),))
        row = result["rescaled"][0]
        assert np.sign(row["cos"]) == np.sign(result["base_cos"])

    def test_negative_product_rescaling_flips_sign(self):
        result = cid.demonstrate_angle_under_rescaling(alphas_betas=((-1.0, 5.0),))
        row = result["rescaled"][0]
        assert np.sign(row["cos"]) == -np.sign(result["base_cos"])


class TestNonlinearLocalDiffeomorphism:
    """Rank classification is preserved under a genuine smooth local
    diffeomorphism (nonzero Jacobian determinant at the evaluation point);
    a naively recomputed Euclidean gradient angle is NOT preserved."""

    def test_coordinate_change_is_a_genuine_diffeomorphism(self):
        result = cid.demonstrate_diffeomorphism_effect()
        assert result["coordchange_det"] == pytest.approx(1.0, abs=1e-12)

    def test_rank_unchanged_at_cubic_point(self):
        result = cid.demonstrate_diffeomorphism_effect()
        cp = result["cubic_point"]
        assert cp["rank_uv"] == cp["rank_xy"]
        assert cp["rank_xy"] == 2

    def test_rank_unchanged_at_degenerate_point(self):
        result = cid.demonstrate_diffeomorphism_effect()
        tp = result["tangency_point"]
        assert tp["rank_uv"] == tp["rank_xy"]
        assert tp["rank_xy"] == 1

    def test_naive_euclidean_angle_changes_for_nontrivial_lambda(self):
        result = cid.demonstrate_diffeomorphism_effect(lam=2.5)
        cp = result["cubic_point"]
        assert cp["cos_uv"] != pytest.approx(cp["cos_xy"], abs=1e-6), (
            "expected the naively recomputed Euclidean angle to change "
            "under a genuine nonlinear coordinate change"
        )

    def test_lambda_zero_is_the_identity_and_leaves_angle_unchanged(self):
        # Sanity floor: lambda=0 reduces the map to the identity, so the
        # angle must be exactly unchanged -- confirms the change observed
        # above is due to the nonlinearity, not a bug in the transform.
        result = cid.demonstrate_diffeomorphism_effect(lam=0.0)
        cp = result["cubic_point"]
        assert cp["cos_uv"] == pytest.approx(cp["cos_xy"], abs=1e-12)


class TestTangency:
    def test_rank_one_at_tangency(self):
        result = cid.demonstrate_tangency()
        assert result["rank"] == 1
        assert result["det"] == pytest.approx(0.0, abs=1e-12)


class TestFirstOrderLimitation:
    """First-order rank data alone cannot classify every kind of
    degeneracy: F=y, G1=y, G2=y-x^2 share identical gradients at the
    origin but differ at second order."""

    def test_gradients_identical_at_origin(self):
        result = cid.demonstrate_first_order_limitation()
        assert result["gradients_equal"] is True
        assert np.array_equal(result["gradF"], result["gradG1"])
        assert np.array_equal(result["gradF"], result["gradG2"])

    def test_second_derivatives_differ(self):
        result = cid.demonstrate_first_order_limitation()
        assert result["d2G1_dx2"] != result["d2G2_dx2"]
        assert result["d2G1_dx2"] == 0.0
        assert result["d2G2_dx2"] == -2.0
