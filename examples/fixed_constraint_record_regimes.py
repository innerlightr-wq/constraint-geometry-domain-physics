"""
Fixed-constraint record regimes -- balance vs. boundary, closed forms only.

See docs/fixed_constraint_record_regimes.md for the full statement. This
is a small, purely numerical illustration of two STANDARD / ESTABLISHED
closed-form record sequences under the identical control
(C = quarter-circle Pythagorean geometry, A = primitive triples,
H = ordering by hypotenuse c). No enumeration or search is performed --
both sequences have known exact closed forms, used directly.

Does NOT include the 15-degree/GM-HM adversarial case (OPEN, not a solved
regime -- see the "Why target alone is insufficient" section of the doc).

Run directly:

    python examples/fixed_constraint_record_regimes.py
"""

import math

__all__ = [
    "pell_hypotenuses",
    "boundary_hypotenuses",
    "lambda_limit",
    "N_balance",
    "N_boundary",
]

LAMBDA = 3.0 + 2.0 * math.sqrt(2.0)


def pell_hypotenuses(n_terms):
    """Balance regime: c_1=5, c_2=29, c_{j+1}=6c_j-c_{j-1}. STANDARD /
    ESTABLISHED RESULT (Pell equation x^2-2y^2=+-1)."""
    cs = [5, 29]
    while len(cs) < n_terms:
        cs.append(6 * cs[-1] - cs[-2])
    return cs[:n_terms]


def boundary_hypotenuses(n_terms):
    """Boundary regime: c_n = 2n^2+2n+1, n=1,2,3,.... ESTABLISHED RESULT
    (exact closed form from m=n+1 in the Euclid parametrization)."""
    return [2 * n * n + 2 * n + 1 for n in range(1, n_terms + 1)]


def lambda_limit():
    """3 + 2*sqrt(2), the balance-regime relative-spacing limit."""
    return LAMBDA


def N_balance(C):
    """N_P(C) ~ log C / log lambda. NUMERICAL DEMONSTRATION of the stated
    asymptotic counting law (not a claim of exact equality at finite C)."""
    return math.log(C) / math.log(LAMBDA)


def N_boundary(C):
    """N_B(C) ~ sqrt(C/2). NUMERICAL DEMONSTRATION of the stated
    asymptotic counting law (not a claim of exact equality at finite C)."""
    return math.sqrt(C / 2.0)


def main():
    print("FIXED-CONSTRAINT RECORD REGIMES -- balance vs. boundary")
    print("Same C (quarter circle), A (primitive triples), H (order by c).")
    print("Closed forms only; standard/established results. See")
    print("docs/fixed_constraint_record_regimes.md for the full statement.")
    print()

    print("--- Balance: Pell hypotenuses c_{j+1}=6c_j-c_{j-1} ---")
    cs = pell_hypotenuses(8)
    print("  c_j =", cs)
    print("  ratios c_{j+1}/c_j:")
    for i in range(1, len(cs)):
        print(f"    c_{i}/c_{i-1} = {cs[i]/cs[i-1]:.6f}")
    print(f"  lambda = 3+2*sqrt(2) = {lambda_limit():.6f}")
    print()

    print("--- Boundary: c_n = 2n^2+2n+1 ---")
    bs = boundary_hypotenuses(8)
    print("  c_n =", bs)
    print("  ratios c_{n+1}/c_n (-> 1):")
    for i in range(1, len(bs)):
        print(f"    c_{i+1}/c_{i} = {bs[i]/bs[i-1]:.6f}")
    print()

    print("--- Counting-law comparison at a few C ---")
    print(f"  {'C':>12} {'N_P(C) ~ logC/log(lambda)':>28} {'N_B(C) ~ sqrt(C/2)':>20}")
    for C in (1e3, 1e6, 1e9, 1e12):
        print(f"  {C:>12.0e} {N_balance(C):>28.3f} {N_boundary(C):>20.3f}")
    print()

    print("Balance: sparse chronology, persistent envelope oscillation.")
    print("Boundary: denser chronology, envelope oscillation collapses.")
    print("Neither behavior is claimed universal for its target's")
    print("arithmetic type -- see docs/fixed_constraint_record_regimes.md,")
    print("'Why target alone is insufficient'.")


if __name__ == "__main__":
    main()
