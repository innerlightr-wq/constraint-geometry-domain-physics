"""
Tests for the fixed-constraint record regimes example
(examples/fixed_constraint_record_regimes.py). See
docs/fixed_constraint_record_regimes.md for the full statement.

Tests only the closed-form claims: the Pell recurrence and its ratio
limit, the boundary closed form and its ratio limit, and counting-law
sanity. Does NOT test the 15-degree case (OPEN, no closed form claimed).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "examples"))

import math

import pytest

import fixed_constraint_record_regimes as fcr


class TestPellRecurrence:
    """STANDARD / ESTABLISHED RESULT: c_1=5, c_2=29, c_{j+1}=6c_j-c_{j-1}."""

    def test_first_two_terms(self):
        cs = fcr.pell_hypotenuses(2)
        assert cs == [5, 29]

    def test_recurrence_holds(self):
        cs = fcr.pell_hypotenuses(8)
        for i in range(2, len(cs)):
            assert cs[i] == 6 * cs[i - 1] - cs[i - 2]

    def test_ratio_converges_to_lambda(self):
        cs = fcr.pell_hypotenuses(10)
        ratio = cs[-1] / cs[-2]
        assert ratio == pytest.approx(fcr.lambda_limit(), rel=1e-10)

    def test_lambda_matches_closed_form(self):
        assert fcr.lambda_limit() == pytest.approx(3.0 + 2.0 * math.sqrt(2.0), rel=1e-14)


class TestBoundaryClosedForm:
    """ESTABLISHED RESULT: c_n = 2n^2+2n+1."""

    def test_closed_form_values(self):
        bs = fcr.boundary_hypotenuses(5)
        assert bs == [5, 13, 25, 41, 61]

    def test_matches_formula_directly(self):
        bs = fcr.boundary_hypotenuses(10)
        for i, c in enumerate(bs, start=1):
            assert c == 2 * i * i + 2 * i + 1

    def test_ratio_tends_to_one(self):
        bs = fcr.boundary_hypotenuses(2000)
        early_ratio = bs[1] / bs[0]
        late_ratio = bs[-1] / bs[-2]
        assert late_ratio < early_ratio
        assert late_ratio == pytest.approx(1.0, abs=1e-2)
        assert late_ratio > 1.0  # must be able to fail: strictly >1, not =1 at finite n


class TestCountingLawSanity:
    """N_P(C) ~ log C / log lambda; N_B(C) ~ sqrt(C/2). Sanity checks on
    the asymptotic forms only, not exact-count claims at finite C."""

    def test_N_balance_matches_formula(self):
        for C in (1e3, 1e6, 1e9, 1e12):
            assert fcr.N_balance(C) == pytest.approx(
                math.log(C) / math.log(fcr.lambda_limit()), rel=1e-12
            )

    def test_N_boundary_matches_formula(self):
        for C in (1e3, 1e6, 1e9, 1e12):
            assert fcr.N_boundary(C) == pytest.approx(math.sqrt(C / 2.0), rel=1e-12)

    def test_boundary_grows_faster_than_balance(self):
        # Sanity: sqrt(C) dominates log(C) for large C -- boundary's
        # counting law must overtake balance's, consistent with "denser
        # chronology" vs. "sparse chronology" in the doc.
        for C in (1e6, 1e9, 1e12):
            assert fcr.N_boundary(C) > fcr.N_balance(C)

    def test_balance_grows_slower_than_boundary_at_small_C_too(self):
        # Must be able to fail: confirms this isn't just a large-C
        # artifact of the specific formulas chosen.
        assert fcr.N_balance(10.0) < fcr.N_boundary(10.0)
