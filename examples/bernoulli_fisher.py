"""
EXACT ALGEBRA -- Bernoulli Fisher information as a binary-partition
readout.

Reproduces the identity documented in the Two-Face Problem source paper
and consistent with this repository's own Fisher-metric material
(docs/terminology.md, "Fisher metric"; examples/effective_potentials.md):

    I_F(p) = 1 / [p(1-p)]

With the conserved partition a = p, b = 1-p (a + b = 1):

    h^2 = a*b = p(1-p)   =>   I_F = 1/h^2 = 4R

using this repository's response convention R = 1/(1-chi^2) = 1/(4h^2).

This is a re-expression of the standard Cramer-Rao bound in partition
coordinates. It is EXACT ALGEBRA, not a new physical or statistical
result: I_F is the classical Fisher information of a Bernoulli trial, and
h, R are the constraint-geometry coordinates of the (p, 1-p) partition.
Nothing here claims that estimation theory and any other domain that
normalizes to a+b=1 "share physics" -- see NON_CLAIMS.md and
docs/safeguards.md, Safeguard 1 (universality trap).

Run directly:

    python examples/bernoulli_fisher.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from constraint_geometry.coordinates import (  # noqa: E402
    partition_from_a,
    compute_h,
    compute_chi_signed,
    compute_R,
)


def bernoulli_fisher_information(p: float) -> float:
    """I_F(p) = 1/[p(1-p)], the classical Bernoulli Fisher information."""
    return 1.0 / (p * (1.0 - p))


def check_partition_reading(p: float, tol: float = 1e-10) -> dict:
    """Verify I_F(p) = 1/h^2 = 4R for the partition a=p, b=1-p.

    Returns a dict of the computed quantities for inspection, and raises
    AssertionError if the exact identity fails to the given tolerance.
    """
    a, b = partition_from_a(p)
    h = compute_h(a, b)
    chi = compute_chi_signed(a, b)
    R = compute_R(chi)

    I_F = bernoulli_fisher_information(p)
    I_F_from_h = 1.0 / h**2
    I_F_from_R = 4.0 * R

    assert abs(I_F - I_F_from_h) < tol, (I_F, I_F_from_h)
    assert abs(I_F - I_F_from_R) < tol, (I_F, I_F_from_R)

    return {
        "p": p,
        "a": a,
        "b": b,
        "h": h,
        "chi": chi,
        "R": R,
        "I_F": I_F,
        "I_F_from_h=1/h^2": I_F_from_h,
        "I_F_from_R=4R": I_F_from_R,
    }


def main():
    print("EXACT ALGEBRA: Bernoulli Fisher information as a partition readout")
    print("I_F(p) = 1/[p(1-p)] = 1/h^2 = 4R,  with a=p, b=1-p, h=sqrt(ab), R=1/(1-chi^2)")
    print()
    header = f"{'p':>8} {'h':>10} {'chi':>10} {'R':>10} {'I_F':>12} {'1/h^2':>12} {'4R':>12}"
    print(header)
    print("-" * len(header))
    for p in (0.05, 0.1, 0.25, 0.3176721962, 0.5, 0.6823278038, 0.75, 0.9, 0.95):
        result = check_partition_reading(p)
        print(
            f"{result['p']:8.4f} {result['h']:10.6f} {result['chi']:10.6f} "
            f"{result['R']:10.6f} {result['I_F']:12.6f} "
            f"{result['I_F_from_h=1/h^2']:12.6f} {result['I_F_from_R=4R']:12.6f}"
        )
    print()
    print("All rows: I_F, 1/h^2, and 4R agree to numerical precision. EXACT ALGEBRA only --")
    print("no claim of a new statistical or physical result. See NON_CLAIMS.md.")


if __name__ == "__main__":
    main()
