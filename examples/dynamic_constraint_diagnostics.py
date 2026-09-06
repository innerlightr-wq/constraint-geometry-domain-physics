"""
Dynamic constraint diagnostics -- small, exact/local illustrations of the
constraint-preservation equation and the affine compatible-velocity space.
See docs/dynamic_constraint_diagnostics.md for the full statement.

This is STANDARD DAE / linear-algebra structure (consistent
initialization / hidden-constraint theory), not new mathematics. No
integrator, no simulation, no mechanics engine: every function here
evaluates an exact local relation at a single instant, mirroring the
"worked models" in the accompanying document. Plain NumPy only.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np

__all__ = [
    "translating_line_compatible_velocity",
    "rotating_line_constraint_residual",
    "expanding_circle_residual",
    "affine_velocity_solution_demo",
    "rescale_and_check_invariance",
]


def translating_line_compatible_velocity(v):
    """Model: Phi(x,y,c)=y-c, cdot=v. Consistency D_x Phi . (xdot,ydot) +
    dPhi/dc * cdot = 0 gives ydot=v exactly, xdot free.
    STANDARD MATHEMATICAL RESULT, derived here via the general A,b form
    rather than hard-coded, so the machinery is exercised, not assumed."""
    A = np.array([[0.0, 1.0]])          # D_x Phi = (dPhi/dx, dPhi/dy) = (0,1)
    dPhi_dc = -1.0
    b = np.array([-dPhi_dc * v])        # b = -D_C Phi * Cdot
    ydot = b[0] / A[0, 1]               # A xdot = b, only ydot is constrained
    return {"A": A, "b": b, "ydot": ydot, "xdot_free": True}


def rotating_line_constraint_residual(x, y, theta, xdot, ydot, omega):
    """Model: Phi(x,y,theta)=y*cos(theta)-x*sin(theta), thetadot=omega.
    Returns the signed residual of
        -xdot*sin(theta) + ydot*cos(theta) - omega*(x*cos(theta)+y*sin(theta))
    which is exactly zero for any velocity satisfying the
    constraint-preservation equation (verified symbolically in the
    accompanying document). EXACT ALGEBRA."""
    lhs = -xdot * np.sin(theta) + ydot * np.cos(theta)
    rhs = omega * (x * np.cos(theta) + y * np.sin(theta))
    return lhs - rhs


def expanding_circle_residual(x, y, xdot, ydot, R, Rdot):
    """Model: Phi(x,y,R)=x^2+y^2-R^2. Returns the residual of
        x*xdot + y*ydot - R*Rdot
    which is exactly zero for any velocity satisfying the
    constraint-preservation equation. EXACT ALGEBRA."""
    return x * xdot + y * ydot - R * Rdot


def affine_velocity_solution_demo(A, b):
    """General A xdot = b: return a particular solution and a basis for
    ker(A), so that xdot_particular + t*kernel_vector satisfies A.xdot=b
    for every real t when consistent. STANDARD DAE / LINEAR-ALGEBRA
    STRUCTURE.

    Raises ValueError if b is not in the range of A (no compatible
    velocity exists), rather than silently returning a least-squares
    approximation."""
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    rank_A = np.linalg.matrix_rank(A)
    augmented = np.column_stack([A, b])
    rank_aug = np.linalg.matrix_rank(augmented)
    if rank_aug != rank_A:
        raise ValueError(
            "b is not in im(A): no compatible velocity exists for this "
            "(A, b) -- this is a genuine incompatibility, not a numerical "
            "artifact to be silently smoothed over."
        )
    xdot_particular, *_ = np.linalg.lstsq(A, b, rcond=None)
    n = A.shape[1]
    if rank_A == n:
        kernel_basis = np.zeros((0, n))
    else:
        _, _, vt = np.linalg.svd(A)
        kernel_basis = vt[rank_A:]
    return {
        "xdot_particular": xdot_particular,
        "kernel_basis": kernel_basis,
        "rank": rank_A,
        "n": n,
        "freedom_dimension": n - rank_A,
        "unique": bool((n - rank_A) == 0),
    }


def rescale_and_check_invariance(A, b, scale_matrix):
    """Rescale (A,b) -> (M A, M b) for an invertible M (representing
    Psi = A(x,C) Phi with A "=" scale_matrix, evaluated on the constraint
    surface) and confirm the compatible-velocity solution set is
    unchanged. MATHEMATICALLY DERIVED / NUMERICAL DEMONSTRATION of the
    representation-invariance claim."""
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    M = np.asarray(scale_matrix, dtype=float)
    original = affine_velocity_solution_demo(A, b)
    rescaled = affine_velocity_solution_demo(M @ A, M @ b)
    return {
        "original": original,
        "rescaled": rescaled,
        "rank_matches": bool(original["rank"] == rescaled["rank"]),
        "particular_matches": np.allclose(
            original["xdot_particular"], rescaled["xdot_particular"], atol=1e-10
        ),
    }


def main():
    print("DYNAMIC CONSTRAINT DIAGNOSTICS -- exact local illustrations")
    print("STANDARD DAE / linear-algebra structure. No integrator, no")
    print("simulation. See docs/dynamic_constraint_diagnostics.md.")
    print()

    print("--- Translating line: Phi=y-c, cdot=v -> ydot=v ---")
    result = translating_line_compatible_velocity(v=2.5)
    print(f"  v=2.5  ->  ydot={result['ydot']}  (xdot free: {result['xdot_free']})")
    print()

    print("--- Rotating line: residual should be ~0 for a compatible velocity ---")
    theta, omega, r = np.pi / 6, 0.8, 3.0
    x, y = r * np.cos(theta), r * np.sin(theta)
    # a compatible (xdot,ydot): normal component = r*omega, tangential arbitrary (0 here)
    xdot = r * omega * (-np.sin(theta))
    ydot = r * omega * np.cos(theta)
    residual = rotating_line_constraint_residual(x, y, theta, xdot, ydot, omega)
    print(f"  theta={theta:.4f}, omega={omega}, r={r}: residual={residual:.3e}")
    print()

    print("--- Expanding circle: residual should be ~0 for a compatible velocity ---")
    R, Rdot = 4.0, 1.5
    phi = 0.9
    x, y = R * np.cos(phi), R * np.sin(phi)
    # pure "radial" compatible velocity (no tangential component)
    xdot, ydot = Rdot * np.cos(phi), Rdot * np.sin(phi)
    residual = expanding_circle_residual(x, y, xdot, ydot, R, Rdot)
    print(f"  R={R}, Rdot={Rdot}: residual={residual:.3e}")
    print()

    print("--- Affine compatible-velocity space: A xdot = b ---")
    A = np.array([[1.0, 2.0]])  # 1 constraint, 2 state vars -> 1D freedom
    b = np.array([3.0])
    demo = affine_velocity_solution_demo(A, b)
    print(f"  A={A.tolist()}, b={b.tolist()}")
    print(f"  rank={demo['rank']}, freedom dimension={demo['freedom_dimension']}, unique={demo['unique']}")
    print(f"  particular solution: {demo['xdot_particular']}")
    print(f"  kernel basis: {demo['kernel_basis']}")
    for t in (-1, 0, 1):
        candidate = demo["xdot_particular"] + t * demo["kernel_basis"][0]
        print(f"    t={t:+d}: candidate={candidate}, A@candidate={A @ candidate} (should equal b={b})")
    print()

    print("--- Representation invariance: Psi = M*Phi, M invertible ---")
    M = np.array([[3.0]])  # single-constraint rescaling
    inv = rescale_and_check_invariance(A, b, M)
    print(f"  rank matches: {inv['rank_matches']}")
    print(f"  particular solution matches: {inv['particular_matches']}")
    print(f"  original particular: {inv['original']['xdot_particular']}")
    print(f"  rescaled particular: {inv['rescaled']['xdot_particular']}")
    print()

    print("NOT ESTABLISHED: new DAE theory; GR equivalence; any M5-to-M6")
    print("mathematical bridge. See docs/dynamic_constraint_diagnostics.md.")


if __name__ == "__main__":
    main()
