"""
NORMAL-FORM EXTRACTION tests.

Verifies the numerical extraction

    V_eff^(1)(chi) = -1/2 * (dchi/dx)^2 / (1 - chi^2)

against trajectories with a KNOWN ANALYTIC derivative, both by supplying
the analytic derivative directly and by letting extract_normal_form
compute it numerically from samples (docs/epistemic_tiers.md, Tier 1).

Also confirms the boundary guard: a trajectory that touches |chi| = 1 is
rejected rather than silently producing inf/nan.
"""

import numpy as np
import pytest

from constraint_geometry.normal_form import extract_normal_form


class TestAnalyticDerivativeSupplied:
    """chi(x) = 0.5 * tanh(x) has known analytic derivative
    dchi/dx = 0.5 * sech(x)^2 = 0.5 * (1 - tanh(x)^2)."""

    def _trajectory(self, n=500):
        x = np.linspace(-4.0, 4.0, n)
        chi = 0.5 * np.tanh(x)
        dchi_dx = 0.5 * (1.0 - np.tanh(x) ** 2)
        return x, chi, dchi_dx

    def test_extraction_matches_hand_derived_V(self):
        x, chi, dchi_dx = self._trajectory()
        result = extract_normal_form(x, chi, dchi_dx=dchi_dx)
        expected_V = -0.5 * dchi_dx**2 / (1.0 - chi**2)
        assert np.allclose(result.V, expected_V, atol=1e-12)
        assert np.allclose(result.dchi_dx, dchi_dx)
        assert np.allclose(result.chi, chi)

    def test_label_is_fixed_and_not_a_physical_claim(self):
        x, chi, dchi_dx = self._trajectory()
        result = extract_normal_form(x, chi, dchi_dx=dchi_dx)
        assert result.label == "NORMAL-FORM EXTRACTION"


class TestNumericalDerivativeAgreesWithAnalytic:
    """When dchi_dx is omitted, the np.gradient numerical derivative
    should converge to the known analytic one as sampling is refined."""

    def _run(self, n):
        x = np.linspace(-3.0, 3.0, n)
        chi = 0.5 * np.tanh(x)
        result = extract_normal_form(x, chi)  # numerical derivative
        analytic_dchi_dx = 0.5 * (1.0 - np.tanh(x) ** 2)
        return np.max(np.abs(result.dchi_dx - analytic_dchi_dx))

    def test_numerical_derivative_converges_with_resolution(self):
        err_coarse = self._run(50)
        err_fine = self._run(2000)
        assert err_fine < err_coarse
        assert err_fine < 2e-5

    def test_extracted_V_close_to_analytic_at_fine_resolution(self):
        n = 2000
        x = np.linspace(-3.0, 3.0, n)
        chi = 0.5 * np.tanh(x)
        analytic_dchi_dx = 0.5 * (1.0 - np.tanh(x) ** 2)
        expected_V = -0.5 * analytic_dchi_dx**2 / (1.0 - chi**2)

        result = extract_normal_form(x, chi)
        assert np.max(np.abs(result.V - expected_V)) < 1e-6


class TestBoundaryGuard:
    def test_rejects_trajectory_touching_boundary(self):
        x = np.linspace(-1.0, 1.0, 5)
        chi = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])  # touches +-1
        with pytest.raises(ValueError):
            extract_normal_form(x, chi)

    def test_rejects_shape_mismatch(self):
        x = np.linspace(0.0, 1.0, 5)
        chi = np.linspace(-0.5, 0.5, 4)  # wrong length
        with pytest.raises(ValueError):
            extract_normal_form(x, chi)

    def test_rejects_dchi_dx_shape_mismatch(self):
        x = np.linspace(0.0, 1.0, 5)
        chi = np.linspace(-0.5, 0.5, 5)
        bad_dchi_dx = np.linspace(0.0, 1.0, 4)
        with pytest.raises(ValueError):
            extract_normal_form(x, chi, dchi_dx=bad_dchi_dx)


class TestTautologyIsExact:
    """The defining property from examples/effective_potentials.md: feed
    an arbitrary monotone pullback in, extract V^(1), and the construction
    exactly reconstructs the kinetic data it was given -- this is the
    documented tautology, not a bug."""

    def test_reconstruction_is_exact_by_construction(self):
        x = np.linspace(-2.0, 2.0, 300)
        chi = 0.7 * np.sin(0.3 * x) / (1.0 + 0.01 * x**2)  # arbitrary pullback
        assert np.all(np.abs(chi) < 1.0)
        result = extract_normal_form(x, chi)
        # By definition, V was built FROM dchi_dx and chi -- re-deriving
        # dchi_dx^2 from V and chi must recover the same kinetic term.
        recovered_dchi_dx_sq = -2.0 * result.V * (1.0 - result.chi**2)
        assert np.allclose(recovered_dchi_dx_sq, result.dchi_dx**2, atol=1e-12)
