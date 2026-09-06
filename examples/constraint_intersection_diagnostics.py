"""
Constraint-Intersection Diagnostics -- a narrow, standard result about how
two constraints F(x)=0, G(x)=0 relate at a shared zero, worked out for the
intrinsic-cubic family. See docs/constraint_intersection_diagnostics.md
for the full statement.

NOT a new theory. NOT a comparator framework. NOT a universal
transversality score. Every mathematical fact demonstrated here is
STANDARD MATHEMATICAL RESULT (rank of a Jacobian / the regular value
theorem / exterior-algebra independence of covectors) or EXACT ALGEBRA
(the intrinsic-cubic computations). No physical meaning is assigned to
R* = 0.465571231876...

============================================================
The central negative result (EXACT ALGEBRA)
============================================================

For F(a,b)=a+b-1 and G_q(a,b)=a-b^q, q>0:

    J_q = [[1, 1], [1, -q*b^(q-1)]]
    det J_q = -(1 + q*b^(q-1)) < 0   for all q>0, b>0

EVERY member q>0 of this family is transversal against a+b=1. q=3 is
NOT selected by transversality.

Separately, within the unconstrained power family a=b^q (not a+b=1):

    h = sqrt(ab) = b^((q+1)/2)
    r = a/b      = b^(q-1)

h == r for EVERY b>0 forces (q+1)/2 = q-1, i.e. q=3 uniquely. This is a
different fact from transversality, not a consequence of it.

Run directly:

    python examples/constraint_intersection_diagnostics.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np

from constraint_geometry.coordinates import compute_h

__all__ = [
    "jacobian_F_Gq",
    "det_and_rank",
    "h_and_ratio",
    "demonstrate_power_family_transversality",
    "demonstrate_constraint_rescaling",
    "demonstrate_angle_under_rescaling",
    "demonstrate_diffeomorphism_effect",
    "demonstrate_tangency",
    "demonstrate_first_order_limitation",
]


# ---------------------------------------------------------------------------
# EXACT ALGEBRA -- the intrinsic-cubic family
# ---------------------------------------------------------------------------

def jacobian_F_Gq(b, q):
    """J_q = [[1,1],[1,-q*b^(q-1)]] for F=a+b-1, G_q=a-b^q, evaluated at
    the point (a,b)=(b^q, b). EXACT ALGEBRA."""
    return np.array([[1.0, 1.0], [1.0, -q * b ** (q - 1.0)]])


def det_and_rank(J):
    """Plain determinant and rank of a 2x2 (or general) matrix. No scoring,
    no threshold -- returns both raw quantities for the caller to interpret."""
    return float(np.linalg.det(J)), int(np.linalg.matrix_rank(J))


def h_and_ratio(a, b):
    """h=sqrt(ab) (reusing the repository's own compute_h) and r=a/b, the
    ratio. Named 'r', not 'R', to avoid collision with this repository's
    own response coordinate R=1/(1-chi^2) (docs/terminology.md) -- a
    different object. EXACT ALGEBRA."""
    return compute_h(a, b), a / b


# ---------------------------------------------------------------------------
# Demonstrations
# ---------------------------------------------------------------------------

def demonstrate_power_family_transversality(qs=(0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0), b=0.6823278038):
    """EXACT ALGEBRA: det J_q < 0 and rank J_q = 2 for every tested q>0.
    q=3 is not distinguished on this axis."""
    rows = []
    for q in qs:
        J = jacobian_F_Gq(b, q)
        det, rank = det_and_rank(J)
        rows.append({"q": q, "det": det, "rank": rank})
    return rows


def demonstrate_constraint_rescaling(alpha=3.0, beta=-2.0, q=3.0, b=0.6823278038):
    """STANDARD MATHEMATICAL RESULT: rank D(alpha*F, beta*G) = rank D(F,G);
    det scales exactly by alpha*beta. Demonstrates raw |det J| must never
    be read as an absolute 'strength of transversality'."""
    J = jacobian_F_Gq(b, q)
    J_rescaled = np.diag([alpha, beta]) @ J
    det0, rank0 = det_and_rank(J)
    det1, rank1 = det_and_rank(J_rescaled)
    return {
        "alpha": alpha, "beta": beta,
        "det_original": det0, "det_rescaled": det1,
        "ratio": det1 / det0, "alpha_times_beta": alpha * beta,
        "rank_original": rank0, "rank_rescaled": rank1,
    }


def _cos_angle(u, v):
    return float((u @ v) / (np.linalg.norm(u) * np.linalg.norm(v)))


def demonstrate_angle_under_rescaling(alphas_betas=((2.0, 3.0), (-1.0, 5.0), (0.01, 100.0), (-3.0, -7.0)),
                                       q=3.0, b=0.6823278038):
    """STANDARD MATHEMATICAL RESULT: the gradient-angle magnitude is
    invariant under F->alpha*F, G->beta*G (alpha,beta nonzero), up to a
    sign flip when alpha*beta<0."""
    J = jacobian_F_Gq(b, q)
    gradF, gradG = J[0], J[1]
    base_cos = _cos_angle(gradF, gradG)
    rows = []
    for alpha, beta in alphas_betas:
        cos_r = _cos_angle(alpha * gradF, beta * gradG)
        rows.append({
            "alpha": alpha, "beta": beta, "cos": cos_r,
            "magnitude_matches": abs(abs(cos_r) - abs(base_cos)) < 1e-12,
            "sign_matches_alpha_beta_sign": bool(
                np.sign(cos_r) == np.sign(base_cos) * np.sign(alpha * beta)
            ),
        })
    return {"base_cos": base_cos, "rescaled": rows}


def demonstrate_diffeomorphism_effect(lam=2.5, q=3.0, b=0.6823278038):
    """NUMERICAL DEMONSTRATION: rank is preserved under a genuine smooth
    local diffeomorphism (u=x, v=y+lambda*x^2, Jacobian determinant 1
    EVERYWHERE -- not the flawed v=y^2 map, which fails to be a local
    diffeomorphism at y=0). A naively recomputed Euclidean gradient angle
    in the new coordinates generally differs from the original value even
    though the qualitative transversality classification does not change.
    Checked both at the intrinsic-cubic point and at a degenerate
    (tangency) point."""

    def duv_dxy(x, y):
        return np.array([[1.0, 0.0], [2.0 * lam * x, 1.0]])

    # At the intrinsic-cubic point.
    a0 = b ** q
    x0, y0 = a0, b
    J = jacobian_F_Gq(b, q)
    gradF, gradG = J[0], J[1]
    Jfwd = duv_dxy(x0, y0)
    coordchange_det = float(np.linalg.det(Jfwd))
    dxy_duv = np.linalg.inv(Jfwd)
    gradF_uv = dxy_duv.T @ gradF
    gradG_uv = dxy_duv.T @ gradG
    rank_xy = int(np.linalg.matrix_rank(J))
    rank_uv = int(np.linalg.matrix_rank(np.array([gradF_uv, gradG_uv])))
    cos_xy = _cos_angle(gradF, gradG)
    cos_uv = _cos_angle(gradF_uv, gradG_uv)

    # At the tangency point (0,0): F=y, G=y-x^2.
    gradF0 = np.array([0.0, 1.0])
    gradG0 = np.array([0.0, 1.0])
    Jfwd0 = duv_dxy(0.0, 0.0)
    dxy_duv0 = np.linalg.inv(Jfwd0)
    gradF0_uv = dxy_duv0.T @ gradF0
    gradG0_uv = dxy_duv0.T @ gradG0
    rank0_xy = int(np.linalg.matrix_rank(np.array([gradF0, gradG0])))
    rank0_uv = int(np.linalg.matrix_rank(np.array([gradF0_uv, gradG0_uv])))

    return {
        "lambda": lam,
        "coordchange_det": coordchange_det,
        "cubic_point": {"rank_xy": rank_xy, "rank_uv": rank_uv, "cos_xy": cos_xy, "cos_uv": cos_uv},
        "tangency_point": {"rank_xy": rank0_xy, "rank_uv": rank0_uv},
    }


def demonstrate_tangency():
    """F=y, G=y-x^2 at the origin: rank 1 -- degenerate, not transversal.
    EXACT ALGEBRA."""
    J = np.array([[0.0, 1.0], [0.0, 1.0]])
    det, rank = det_and_rank(J)
    return {"J": J, "det": det, "rank": rank}


def demonstrate_first_order_limitation():
    """F=y, G1=y, G2=y-x^2 at the origin: identical gradients (first-order
    data agrees) but different second derivatives (d2G1/dx2=0,
    d2G2/dx2=-2) -- first-order rank data alone cannot classify every kind
    of degeneracy. EXACT ALGEBRA."""
    gradF = np.array([0.0, 1.0])
    gradG1 = np.array([0.0, 1.0])
    gradG2 = np.array([0.0, 1.0])  # d/dx(y-x^2)=-2x=0 at x=0; d/dy=1
    d2G1_dx2 = 0.0
    d2G2_dx2 = -2.0
    return {
        "gradF": gradF, "gradG1": gradG1, "gradG2": gradG2,
        "gradients_equal": np.array_equal(gradG1, gradG2),
        "d2G1_dx2": d2G1_dx2, "d2G2_dx2": d2G2_dx2,
    }


def main():
    print("CONSTRAINT-INTERSECTION DIAGNOSTICS -- narrow, standard mathematics")
    print("applied to the intrinsic-cubic family. Not a new theory, not a")
    print("comparator framework, not a universal transversality score.")
    print()

    print("--- Power-family transversality: det J_q < 0 for all tested q>0 ---")
    for row in demonstrate_power_family_transversality():
        print(f"  q={row['q']:>5}: det={row['det']:+.6f}  rank={row['rank']}")
    print("  -> q=3 is NOT distinguished by transversality; every q>0 qualifies.")
    print()

    print("--- Constraint rescaling: F->alpha*F, G->beta*G (alpha=3, beta=-2) ---")
    rs = demonstrate_constraint_rescaling()
    print(f"  det(F,G)             = {rs['det_original']:+.6f}")
    print(f"  det(alpha*F,beta*G)  = {rs['det_rescaled']:+.6f}")
    print(f"  ratio                = {rs['ratio']:+.6f}  (alpha*beta = {rs['alpha_times_beta']:+.6f})")
    print(f"  rank(F,G) = {rs['rank_original']}, rank(alpha*F,beta*G) = {rs['rank_rescaled']}")
    print("  -> |det J| is NOT rescaling-invariant; rank IS.")
    print()

    print("--- Gradient-angle magnitude under constraint rescaling ---")
    ang = demonstrate_angle_under_rescaling()
    print(f"  base cos(angle) = {ang['base_cos']:+.6f}")
    for row in ang["rescaled"]:
        print(f"  alpha={row['alpha']:+.3f}, beta={row['beta']:+.3f}: cos={row['cos']:+.6f}  "
              f"magnitude matches base: {row['magnitude_matches']}")
    print("  -> angle MAGNITUDE is rescaling-invariant (sign follows sign(alpha*beta)).")
    print()

    print("--- Effect of a genuine smooth local diffeomorphism (u=x, v=y+lambda*x^2) ---")
    dif = demonstrate_diffeomorphism_effect()
    print(f"  coordinate-change Jacobian determinant = {dif['coordchange_det']} (constant, nonzero everywhere)")
    cp = dif["cubic_point"]
    print(f"  at the intrinsic-cubic point: rank(x,y)={cp['rank_xy']}, rank(u,v)={cp['rank_uv']}  (unchanged)")
    print(f"    cos(angle) in (x,y) = {cp['cos_xy']:+.6f}")
    print(f"    cos(angle) in (u,v) = {cp['cos_uv']:+.6f}  (naive Euclidean recomputation -- CHANGED)")
    tp = dif["tangency_point"]
    print(f"  at the tangency point: rank(x,y)={tp['rank_xy']}, rank(u,v)={tp['rank_uv']}  (both degenerate)")
    print("  -> rank/transversality survives the diffeomorphism; a naively")
    print("     recomputed Euclidean angle does not, without transforming the metric too.")
    print()

    print("--- Tangency: F=y, G=y-x^2 at the origin ---")
    tan = demonstrate_tangency()
    print(f"  J = {tan['J'].tolist()}, det={tan['det']}, rank={tan['rank']}  (degenerate, not transversal)")
    print()

    print("--- First-order limitation: F=y, G1=y, G2=y-x^2 at the origin ---")
    fol = demonstrate_first_order_limitation()
    print(f"  grad F = {fol['gradF'].tolist()}, grad G1 = {fol['gradG1'].tolist()}, "
          f"grad G2 = {fol['gradG2'].tolist()}")
    print(f"  gradients equal (first-order data agrees): {fol['gradients_equal']}")
    print(f"  d2G1/dx2 = {fol['d2G1_dx2']}, d2G2/dx2 = {fol['d2G2_dx2']}  (second-order data differs)")
    print("  -> first-order rank data alone cannot classify every kind of degeneracy.")
    print()

    print("NOT ESTABLISHED: q=3 as universally preferred; R* as a physical")
    print("constant or threshold. See docs/constraint_intersection_diagnostics.md")
    print("and NON_CLAIMS.md.")


if __name__ == "__main__":
    main()
