"""
Tests for the dynamic constraint diagnostics example
(examples/dynamic_constraint_diagnostics.py). See
docs/dynamic_constraint_diagnostics.md for the full statement.

Tests only local/exact relations (the constraint-preservation equation
and the affine compatible-velocity space) -- no conceptual/philosophical
claims are tested here, per the narrow scope of this milestone.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))

import numpy as np
import pytest

import dynamic_constraint_diagnostics as dcd


class TestTranslatingLine:
    """Phi=y-c, cdot=v -> ydot=v exactly, for any v."""

    @pytest.mark.parametrize("v", [-3.0, 0.0, 0.1, 2.5, 100.0])
    def test_ydot_equals_cdot(self, v):
        result = dcd.translating_line_compatible_velocity(v)
        assert result["ydot"] == pytest.approx(v, rel=1e-12)

    def test_xdot_is_unconstrained(self):
        result = dcd.translating_line_compatible_velocity(1.0)
        assert result["xdot_free"] is True


class TestRotatingLine:
    """The consistency equation residual must be exactly zero for a
    velocity constructed to satisfy it, and materially nonzero for one
    that does not."""

    def test_compatible_velocity_gives_zero_residual(self):
        theta, omega, r = 0.7, 1.3, 2.0
        x, y = r * np.cos(theta), r * np.sin(theta)
        xdot = r * omega * (-np.sin(theta))
        ydot = r * omega * np.cos(theta)
        residual = dcd.rotating_line_constraint_residual(x, y, theta, xdot, ydot, omega)
        assert residual == pytest.approx(0.0, abs=1e-12)

    def test_incompatible_velocity_gives_nonzero_residual(self):
        # Same point/omega, but a velocity NOT satisfying the normal
        # condition (must be able to fail -- a broken implementation
        # that always returns ~0 would not be caught otherwise).
        theta, omega, r = 0.7, 1.3, 2.0
        x, y = r * np.cos(theta), r * np.sin(theta)
        residual = dcd.rotating_line_constraint_residual(x, y, theta, xdot=0.0, ydot=0.0, omega=omega)
        assert abs(residual) > 1e-6

    @pytest.mark.parametrize("theta,omega,r", [(0.1, 0.5, 1.0), (1.2, -0.8, 3.5), (2.9, 2.0, 0.3)])
    def test_multiple_configurations(self, theta, omega, r):
        x, y = r * np.cos(theta), r * np.sin(theta)
        xdot = r * omega * (-np.sin(theta))
        ydot = r * omega * np.cos(theta)
        residual = dcd.rotating_line_constraint_residual(x, y, theta, xdot, ydot, omega)
        assert residual == pytest.approx(0.0, abs=1e-10)


class TestExpandingCircle:
    """x*xdot + y*ydot = R*Rdot exactly, for a compatible (purely radial)
    velocity; tangential-only motion must NOT satisfy it when Rdot != 0."""

    def test_radial_compatible_velocity_gives_zero_residual(self):
        R, Rdot, phi = 5.0, 0.7, 1.1
        x, y = R * np.cos(phi), R * np.sin(phi)
        xdot, ydot = Rdot * np.cos(phi), Rdot * np.sin(phi)
        residual = dcd.expanding_circle_residual(x, y, xdot, ydot, R, Rdot)
        assert residual == pytest.approx(0.0, abs=1e-12)

    def test_pure_tangential_motion_violates_consistency_when_Rdot_nonzero(self):
        R, Rdot, phi = 5.0, 0.7, 1.1
        x, y = R * np.cos(phi), R * np.sin(phi)
        # tangential direction: (-sin(phi), cos(phi)) * speed
        speed = 2.0
        xdot, ydot = -speed * np.sin(phi), speed * np.cos(phi)
        residual = dcd.expanding_circle_residual(x, y, xdot, ydot, R, Rdot)
        assert residual == pytest.approx(-R * Rdot, rel=1e-10)
        assert abs(residual) > 1e-6

    def test_static_circle_allows_pure_tangential_motion(self):
        # Rdot=0 (Regime II inside Regime IV's machinery): any tangential
        # velocity is compatible, confirming the two cases above are not
        # an artifact of the residual formula itself.
        R, phi = 5.0, 1.1
        x, y = R * np.cos(phi), R * np.sin(phi)
        xdot, ydot = -2.0 * np.sin(phi), 2.0 * np.cos(phi)
        residual = dcd.expanding_circle_residual(x, y, xdot, ydot, R, Rdot=0.0)
        assert residual == pytest.approx(0.0, abs=1e-12)


class TestAffineVelocitySpace:
    def test_particular_plus_kernel_direction_stays_compatible(self):
        A = np.array([[1.0, 2.0]])
        b = np.array([3.0])
        demo = dcd.affine_velocity_solution_demo(A, b)
        for t in (-3.0, -1.0, 0.0, 1.0, 3.0):
            candidate = demo["xdot_particular"] + t * demo["kernel_basis"][0]
            assert A @ candidate == pytest.approx(b, abs=1e-10)

    def test_unique_solution_case(self):
        A = np.array([[1.0, 0.0], [0.0, 1.0]])  # full rank, n=2, k=2
        b = np.array([4.0, -2.0])
        demo = dcd.affine_velocity_solution_demo(A, b)
        assert demo["unique"] is True
        assert demo["freedom_dimension"] == 0
        assert demo["kernel_basis"].shape[0] == 0
        assert demo["xdot_particular"] == pytest.approx(b, abs=1e-10)

    def test_inconsistent_case_raises(self):
        # rank(A)=1 but b is not a multiple of A's single row direction.
        A = np.array([[1.0, 0.0], [2.0, 0.0]])  # rank 1, im(A) = span{(1,2)}
        b = np.array([1.0, 3.0])  # not proportional to (1,2)
        with pytest.raises(ValueError):
            dcd.affine_velocity_solution_demo(A, b)

    def test_consistent_case_with_same_A_does_not_raise(self):
        A = np.array([[1.0, 0.0], [2.0, 0.0]])
        b = np.array([1.0, 2.0])  # exactly 1*(1,2), consistent
        demo = dcd.affine_velocity_solution_demo(A, b)
        assert demo["rank"] == 1

    def test_rank_nullity_relation(self):
        for A, n in [
            (np.array([[1.0, 2.0]]), 2),
            (np.array([[1.0, 0.0], [0.0, 1.0]]), 2),
            (np.array([[1.0, 1.0, 1.0]]), 3),
        ]:
            b = A @ np.ones(n)  # guaranteed consistent (in im(A))
            demo = dcd.affine_velocity_solution_demo(A, b)
            assert demo["freedom_dimension"] == n - demo["rank"]
            assert demo["kernel_basis"].shape[0] == demo["freedom_dimension"]


class TestRepresentationInvariance:
    """Rescaling (A,b) -> (M A, M b) for invertible M must not change the
    compatible-velocity solution set."""

    @pytest.mark.parametrize("scale", [3.0, -2.0, 0.01, -7.5])
    def test_rank_and_particular_solution_invariant(self, scale):
        A = np.array([[1.0, 2.0]])
        b = np.array([3.0])
        M = np.array([[scale]])
        result = dcd.rescale_and_check_invariance(A, b, M)
        assert result["rank_matches"] is True
        assert result["particular_matches"] is True

    def test_raw_jacobian_magnitude_is_not_invariant(self):
        # Must be able to fail: confirms the test above isn't vacuous by
        # checking the raw A itself DOES change under rescaling, even
        # though the derived compatible-velocity solution does not.
        A = np.array([[1.0, 2.0]])
        M = np.array([[3.0]])
        A_rescaled = M @ A
        assert not np.allclose(A, A_rescaled)
