"""
Exact coordinate algebra for the binary partition manifold.

EXACT COORDINATE IDENTITY. This module implements only the algebraic
identities documented in README.md and docs/terminology.md:

    a + b = 1,  h = sqrt(a*b),  chi = a - b,
    R = 1/(1-chi^2) = 1/(4h^2),  xi = arctanh(chi),  theta = arcsin(chi)

with 4h^2 + chi^2 = 1, chi = tanh(xi), theta = asin(chi), R = cosh(xi)^2,
and the Gudermannian bridge theta = gd(xi) = atan(sinh(xi)).

These functions are pure coordinate algebra. They carry no physical
interpretation, decide no question of domain embedding, and make no claim
about which two quantities a domain should identify as (a, b). See
docs/software_scope.md and NON_CLAIMS.md.

Sign convention
----------------
Two chi conventions occur across the material this repository cites:

- SIGNED (this repository's own convention -- README.md, docs/terminology.md,
  and the Effective-Potentials source paper): chi = a - b, range (-1, 1).
  This is the convention every function in this module uses unless its
  name says "unsigned".
- UNSIGNED (the Two-Face Problem source paper's convention):
  chi = |2a - 1| = |chi_signed|, range [0, 1).

xi = arctanh(chi) and theta = arcsin(chi) are odd functions of chi, so they
depend on its SIGN. Passing an unsigned chi into compute_xi or
compute_theta silently discards which sector (a or b) dominates. Use
compute_chi_signed for anything that will reach xi or theta.
"""

import math

__all__ = [
    "partition_from_a",
    "partition_from_ratio",
    "compute_h",
    "compute_chi_signed",
    "compute_chi_unsigned",
    "compute_R",
    "compute_R_from_h",
    "compute_xi",
    "compute_theta",
    "chi_from_xi",
    "gudermannian",
    "response_from_xi",
]


def partition_from_a(a: float) -> tuple[float, float]:
    """Return (a, b) with b = 1 - a, the conserved partition a + b = 1.

    Requires 0 < a < 1 (open interval: the partition boundary a=0 or a=1
    is excluded, matching the domain on which h, R, xi are all defined).
    """
    if not (0.0 < a < 1.0):
        raise ValueError(f"a must be in the open interval (0, 1), got {a!r}")
    return a, 1.0 - a


def partition_from_ratio(r: float) -> tuple[float, float]:
    """Return (a, b) for a/b = r, via a = r/(1+r), b = 1/(1+r).

    Requires r > 0.
    """
    if not (r > 0.0):
        raise ValueError(f"r must be > 0, got {r!r}")
    a = r / (1.0 + r)
    b = 1.0 / (1.0 + r)
    return a, b


def compute_h(a: float, b: float) -> float:
    """Thales altitude h = sqrt(a*b). Requires a > 0 and b > 0."""
    if a <= 0.0 or b <= 0.0:
        raise ValueError(f"a and b must both be > 0, got a={a!r}, b={b!r}")
    return math.sqrt(a * b)


def compute_chi_signed(a: float, b: float) -> float:
    """Signed asymmetry chi = a - b, range (-1, 1).

    This repository's own convention (README.md, docs/terminology.md) and
    the Effective-Potentials source paper's convention.
    """
    return a - b


def compute_chi_unsigned(a: float) -> float:
    """Unsigned asymmetry chi = |2a - 1|, range [0, 1).

    The Two-Face Problem source paper's convention. Equal to
    abs(compute_chi_signed(a, 1-a)). Do not pass this into compute_xi or
    compute_theta: it has discarded the sector-dominance sign.
    """
    return abs(2.0 * a - 1.0)


def compute_R(chi: float) -> float:
    """Response coordinate R = 1/(1-chi^2).

    Requires |chi| < 1 (R diverges at the partition boundary; this is a
    chart property, not a physical singularity -- see docs/safeguards.md,
    Safeguard 2). Symmetric under chi -> -chi, so R alone does not
    distinguish signed from unsigned chi.
    """
    if abs(chi) >= 1.0:
        raise ValueError(
            f"|chi| must be < 1 (approach to partition boundary), got chi={chi!r}"
        )
    return 1.0 / (1.0 - chi * chi)


def compute_R_from_h(h: float) -> float:
    """R = 1/(4h^2). Requires h > 0."""
    if h <= 0.0:
        raise ValueError(f"h must be > 0, got {h!r}")
    return 1.0 / (4.0 * h * h)


def compute_xi(chi: float) -> float:
    """Rapidity xi = arctanh(chi).

    Requires SIGNED chi, |chi| < 1. See module docstring on sign
    convention: passing an unsigned chi here discards which sector
    dominates.
    """
    if abs(chi) >= 1.0:
        raise ValueError(f"|chi| must be < 1, got chi={chi!r}")
    return math.atanh(chi)


def compute_theta(chi: float) -> float:
    """Fisher angle theta = arcsin(chi).

    Requires SIGNED chi, chi in [-1, 1] (arcsin's closed domain; the
    partition-boundary endpoints chi=+-1 map to theta=+-pi/2 and are
    included here, unlike compute_R/compute_xi, which exclude them).
    """
    if not (-1.0 <= chi <= 1.0):
        raise ValueError(f"chi must be in [-1, 1], got {chi!r}")
    return math.asin(chi)


def chi_from_xi(xi: float) -> float:
    """Inverse rapidity map: chi = tanh(xi). Defined for all real xi."""
    return math.tanh(xi)


def gudermannian(xi: float) -> float:
    """Gudermannian bridge: gd(xi) = atan(sinh(xi)).

    Connects the Poincare (rapidity) and Fisher (angle) descriptions:
    theta = gd(xi). Defined for all real xi; odd function, so it
    preserves the sign of xi (and hence of the underlying signed chi).
    """
    return math.atan(math.sinh(xi))


def response_from_xi(xi: float) -> float:
    """R = cosh(xi)^2. Defined for all real xi; always >= 1."""
    return math.cosh(xi) ** 2
