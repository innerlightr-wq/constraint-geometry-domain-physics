"""
EXACT COORDINATE IDENTITY tests for the binary-partition coordinate
algebra (README.md; docs/terminology.md; docs/epistemic_tiers.md, Tier 1).

    4h^2 + chi^2 = 1
    R = 1/(1-chi^2)
    R = 1/(4h^2)
    chi = tanh(xi)
    theta = asin(chi)
    theta = gd(xi)
    R = cosh(xi)^2

Exercised at multiple interior points, including both signed-chi cases,
and near (but not at) the partition boundary |chi| -> 1.
"""

import math

import pytest

from constraint_geometry.coordinates import (
    partition_from_a,
    partition_from_ratio,
    compute_h,
    compute_chi_signed,
    compute_chi_unsigned,
    compute_R,
    compute_R_from_h,
    compute_xi,
    compute_theta,
    chi_from_xi,
    gudermannian,
    response_from_xi,
)

# Interior sample points spanning negative, near-zero, and positive chi,
# plus values close to (but strictly inside) the partition boundary.
CHI_SAMPLES = [-0.999, -0.9, -0.5, -0.1, 0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 0.999]

A_SAMPLES = [0.001, 0.05, 0.2, 0.3176721962, 0.5, 0.6823278038, 0.8, 0.95, 0.999]


class TestPartitionConstruction:
    def test_partition_from_a_sums_to_one(self):
        for a in A_SAMPLES:
            a_out, b_out = partition_from_a(a)
            assert a_out == pytest.approx(a)
            assert a_out + b_out == pytest.approx(1.0)

    def test_partition_from_a_rejects_boundary_and_outside(self):
        for bad in (0.0, 1.0, -0.1, 1.1):
            with pytest.raises(ValueError):
                partition_from_a(bad)

    def test_partition_from_ratio_matches_a_over_b(self):
        for r in (0.1, 0.4655712319, 1.0, 2.1479, 10.0):
            a, b = partition_from_ratio(r)
            assert a + b == pytest.approx(1.0)
            assert a / b == pytest.approx(r)

    def test_partition_from_ratio_rejects_nonpositive(self):
        for bad in (0.0, -1.0):
            with pytest.raises(ValueError):
                partition_from_ratio(bad)


class TestConstraintIdentity:
    """4h^2 + chi^2 = 1."""

    def test_4h2_plus_chi2_equals_one(self):
        for a in A_SAMPLES:
            a_, b_ = partition_from_a(a)
            h = compute_h(a_, b_)
            chi = compute_chi_signed(a_, b_)
            assert 4.0 * h**2 + chi**2 == pytest.approx(1.0, abs=1e-12)


class TestResponseIdentities:
    """R = 1/(1-chi^2) = 1/(4h^2)."""

    def test_R_from_chi_and_R_from_h_agree(self):
        for a in A_SAMPLES:
            a_, b_ = partition_from_a(a)
            h = compute_h(a_, b_)
            chi = compute_chi_signed(a_, b_)
            R_chi = compute_R(chi)
            R_h = compute_R_from_h(h)
            assert R_chi == pytest.approx(R_h, rel=1e-12)

    def test_R_matches_direct_formula(self):
        for chi in CHI_SAMPLES:
            assert compute_R(chi) == pytest.approx(1.0 / (1.0 - chi**2))

    def test_R_rejects_boundary_and_outside(self):
        for bad in (1.0, -1.0, 1.5, -2.0):
            with pytest.raises(ValueError):
                compute_R(bad)

    def test_R_symmetric_in_sign_of_chi(self):
        for chi in (0.1, 0.5, 0.9):
            assert compute_R(chi) == pytest.approx(compute_R(-chi))

    def test_R_near_boundary_grows_without_bound(self):
        # Not AT the boundary -- approaching it. Confirms the chart
        # divergence (docs/safeguards.md, Safeguard 2) without dividing by
        # zero.
        r_far = compute_R(0.9)
        r_near = compute_R(0.999)
        r_nearer = compute_R(0.99999)
        assert r_far < r_near < r_nearer


class TestRapidityIdentities:
    """chi = tanh(xi); inverse of xi = arctanh(chi)."""

    def test_chi_from_xi_inverts_compute_xi(self):
        for chi in CHI_SAMPLES:
            xi = compute_xi(chi)
            assert chi_from_xi(xi) == pytest.approx(chi, abs=1e-10)

    def test_compute_xi_rejects_boundary_and_outside(self):
        for bad in (1.0, -1.0, 1.2, -1.2):
            with pytest.raises(ValueError):
                compute_xi(bad)

    def test_compute_xi_is_odd(self):
        for chi in (0.1, 0.5, 0.9):
            assert compute_xi(-chi) == pytest.approx(-compute_xi(chi))

    def test_chi_from_xi_defined_for_large_rapidity(self):
        # xi unbounded, chi mathematically stays strictly inside (-1, 1).
        # Note: float64 tanh saturates to exactly 1.0 for xi beyond ~19.06
        # (1 - 2*exp(-2*xi) rounds to 1.0), so this checks a large-but-not
        # -saturating rapidity rather than an arbitrarily large one.
        assert -1.0 < chi_from_xi(15.0) < 1.0
        assert -1.0 < chi_from_xi(-15.0) < 1.0


class TestResponseFromXi:
    """R = cosh(xi)^2."""

    def test_R_equals_cosh_xi_squared(self):
        for chi in CHI_SAMPLES:
            xi = compute_xi(chi)
            assert compute_R(chi) == pytest.approx(response_from_xi(xi), rel=1e-10)


class TestFisherAngleAndGudermannian:
    """theta = asin(chi); theta = gd(xi)."""

    def test_theta_matches_direct_asin(self):
        for chi in CHI_SAMPLES + [-1.0, 1.0]:
            assert compute_theta(chi) == pytest.approx(math.asin(chi))

    def test_theta_rejects_outside_closed_domain(self):
        for bad in (1.0001, -1.0001, 2.0):
            with pytest.raises(ValueError):
                compute_theta(bad)

    def test_theta_includes_boundary_unlike_xi_and_R(self):
        # theta = asin(chi) is defined at chi = +-1 (theta = +-pi/2), even
        # though compute_xi and compute_R correctly exclude that boundary.
        assert compute_theta(1.0) == pytest.approx(math.pi / 2)
        assert compute_theta(-1.0) == pytest.approx(-math.pi / 2)

    def test_theta_equals_gudermannian_of_xi(self):
        # theta = gd(xi) -- the Gudermannian bridge between the Fisher
        # (circular) and Poincare (hyperbolic) descriptions.
        for chi in CHI_SAMPLES:
            xi = compute_xi(chi)
            theta = compute_theta(chi)
            assert theta == pytest.approx(gudermannian(xi), abs=1e-10)

    def test_gudermannian_is_odd(self):
        for xi in (0.1, 0.5, 1.0, 3.0):
            assert gudermannian(-xi) == pytest.approx(-gudermannian(xi))

    def test_gudermannian_matches_atan_sinh_directly(self):
        for xi in (-3.0, -1.0, -0.1, 0.0, 0.1, 1.0, 3.0):
            assert gudermannian(xi) == pytest.approx(math.atan(math.sinh(xi)))


class TestUnsignedConvention:
    """compute_chi_unsigned matches the Two-Face Problem paper's |2a-1|."""

    def test_unsigned_equals_absolute_signed(self):
        for a in A_SAMPLES:
            a_, b_ = partition_from_a(a)
            signed = compute_chi_signed(a_, b_)
            unsigned = compute_chi_unsigned(a_)
            assert unsigned == pytest.approx(abs(signed))

    def test_unsigned_is_nonnegative(self):
        for a in A_SAMPLES:
            assert compute_chi_unsigned(a) >= 0.0
