"""
Numerical over-determination / falsifiability machinery.

Implements the numerical form of the shared-V family test described in
docs/protocol.md (Step 5, route 1) and examples/effective_potentials.md:
a candidate autonomous potential V(chi) is asked to reproduce a FAMILY of
independently generated trajectories that differ by an external parameter
(here, conserved energy), rather than being fit to a single curve. A
construction that reports a residual which could be large is no longer a
tautology (see normal_form.py for the single-trajectory case that is).

For a family member k with conserved energy E_k and G(chi) = 1/(1-chi^2):

    U_k(chi) = E_k - 1/2 * G(chi) * (dchi/dx)_k^2

A genuine shared potential collapses every U_k(chi) onto a common curve,
within a residual; this module computes that residual.

Epistemic rule enforced by this module's API (docs/software_scope.md):
NO FUNCTION HERE RETURNS A DEFAULT PASS/FAIL VERDICT. shared_V_family_test
and heldout_V_test return residual numbers and metadata only. The one
function that produces a boolean, `pass_fail`, requires the threshold as
an explicit, non-defaulted argument -- there is no built-in notion of
"small enough". Choosing that threshold is a domain judgment left to the
caller; see docs/protocol.md, Step 5, and docs/safeguards.md, Safeguard 8.
"""

from dataclasses import dataclass, field

import numpy as np

__all__ = [
    "G",
    "FamilyMember",
    "FamilyTestResult",
    "shared_V_family_test",
    "pass_fail",
    "HeldoutTestResult",
    "heldout_V_test",
]


def G(chi):
    """Fisher metric coefficient G(chi) = 1/(1-chi^2). Requires |chi| < 1."""
    chi = np.asarray(chi, dtype=float)
    if np.any(np.abs(chi) >= 1.0):
        raise ValueError("|chi| must be < 1 (partition-boundary singularity)")
    return 1.0 / (1.0 - chi**2)


@dataclass
class FamilyMember:
    """One trajectory in a candidate shared-V family.

    Attributes
    ----------
    chi : np.ndarray
        chi(x) samples, strictly monotonic (increasing or decreasing) so
        that chi can be used as an interpolation axis. |chi| < 1 required.
    dchi_dx : np.ndarray
        dchi/dx at the same sample points (analytic or numerical).
    E : float
        The conserved energy (or other external family parameter) used
        to form U(chi) = E - 1/2 * G(chi) * dchi_dx^2.
    label : str
        Free-text identifier for reporting, e.g. "orbit 1".
    """

    chi: np.ndarray
    dchi_dx: np.ndarray
    E: float
    label: str = ""

    def U(self) -> np.ndarray:
        """Pointwise U(chi) = E - 1/2 * G(chi) * (dchi/dx)^2."""
        return self.E - 0.5 * G(self.chi) * self.dchi_dx**2


@dataclass
class FamilyTestResult:
    """Result of a shared-V family collapse test. Contains no verdict.

    Attributes
    ----------
    residual_max : float
        max_i |U_j(chi_i) - U_k(chi_i)| across all pairs of members and
        all points of the common comparison grid (worst-case pairwise gap).
    residual_rms : float
        RMS of the same pairwise differences over the comparison grid.
    chi_overlap_range : tuple[float, float]
        The chi-domain over which all members overlap and were compared.
    n_grid : int
        Number of points used on the comparison grid.
    member_labels : list[str]
        Labels of the members included, in input order.
    label : str
        Fixed epistemic label.
    """

    residual_max: float
    residual_rms: float
    chi_overlap_range: tuple
    n_grid: int
    member_labels: list
    label: str = field(default="SYNTHETIC FALSIFIABILITY TEST", init=False)


def shared_V_family_test(members, n_grid: int = 200) -> FamilyTestResult:
    """Test whether a family's U_k(chi) curves collapse onto one V(chi).

    Parameters
    ----------
    members : list[FamilyMember]
        At least two family members. Each member's chi array must be
        strictly monotonic and must overlap the others' chi ranges.
    n_grid : int
        Number of points on the common comparison grid, placed within the
        intersection of every member's chi range.

    Returns
    -------
    FamilyTestResult
        Residuals only. This function does NOT decide pass or fail; use
        `pass_fail` with a threshold you supply, per docs/protocol.md.

    Raises
    ------
    ValueError
        If fewer than two members are supplied, or if their chi ranges do
        not overlap.
    """
    if len(members) < 2:
        raise ValueError("shared_V_family_test requires at least two members")

    lo = max(np.min(m.chi) for m in members)
    hi = min(np.max(m.chi) for m in members)
    if not (hi > lo):
        raise ValueError(
            f"family members' chi ranges do not overlap: overlap=({lo!r}, {hi!r})"
        )

    grid = np.linspace(lo, hi, n_grid)

    U_on_grid = []
    for m in members:
        chi_sorted_idx = np.argsort(m.chi)
        chi_sorted = m.chi[chi_sorted_idx]
        U_sorted = m.U()[chi_sorted_idx]
        U_on_grid.append(np.interp(grid, chi_sorted, U_sorted))
    U_on_grid = np.stack(U_on_grid, axis=0)  # shape (n_members, n_grid)

    pairwise_diffs = []
    n = len(members)
    for i in range(n):
        for j in range(i + 1, n):
            pairwise_diffs.append(np.abs(U_on_grid[i] - U_on_grid[j]))
    pairwise_diffs = np.concatenate(pairwise_diffs)

    return FamilyTestResult(
        residual_max=float(np.max(pairwise_diffs)),
        residual_rms=float(np.sqrt(np.mean(pairwise_diffs**2))),
        chi_overlap_range=(float(lo), float(hi)),
        n_grid=n_grid,
        member_labels=[m.label for m in members],
    )


def pass_fail(result: FamilyTestResult, threshold: float) -> bool:
    """Explicit, caller-supplied pass/fail check on a family-test residual.

    `threshold` has NO default anywhere in this package (see module
    docstring and docs/software_scope.md): what counts as "small enough"
    is a domain judgment, not a mathematical fact, and an unstated default
    threshold would be the software equivalent of the arbitrary-embedding
    hazard in docs/safeguards.md, Safeguard 8.

    Returns True if `result.residual_max <= threshold`.
    """
    return result.residual_max <= threshold


@dataclass
class HeldoutTestResult:
    """Result of a fit-on-subset / predict-on-holdout diagnostic.

    Minimal Milestone-1 implementation. Fits no free parameters: it forms
    the common U(chi) curve implied by the fit members' overlap (their
    average on the comparison grid, valid only insofar as they already
    agree -- see `fit_agreement`) and compares it against the held-out
    member's own curve. `fit_agreement` should itself be inspected before
    trusting `prediction_residual_max`: predicting from a fit family that
    does not already collapse is not a meaningful test.

    Attributes
    ----------
    fit_agreement : FamilyTestResult
        Collapse residual among the fit members alone.
    prediction_residual_max : float
        max_i |U_fit(chi_i) - U_heldout(chi_i)| on the grid over the
        overlap of the fit members' comparison domain and the held-out
        member's chi range.
    prediction_residual_rms : float
        RMS of the same differences.
    chi_overlap_range : tuple[float, float]
    n_grid : int
    heldout_label : str
    label : str
    """

    fit_agreement: FamilyTestResult
    prediction_residual_max: float
    prediction_residual_rms: float
    chi_overlap_range: tuple
    n_grid: int
    heldout_label: str
    label: str = field(default="SYNTHETIC FALSIFIABILITY TEST (held-out)", init=False)


def heldout_V_test(fit_members, heldout_member, n_grid: int = 200) -> HeldoutTestResult:
    """Fit U(chi) on `fit_members`, then compare it to a held-out member.

    Parameters
    ----------
    fit_members : list[FamilyMember]
        At least two members, used only to form the fit curve (their
        pointwise average U(chi) on their mutual overlap grid).
    heldout_member : FamilyMember
        Not used to form the fit curve. Its own U(chi) is compared against
        the fit curve on the overlap of the fit domain and its own range.
    n_grid : int
        Grid resolution for both the internal fit-agreement check and the
        held-out comparison.

    Returns
    -------
    HeldoutTestResult
        Residuals only; no pass/fail verdict (use `pass_fail`-style logic
        with a caller-supplied threshold if a verdict is needed).

    Notes
    -----
    This is a deliberately minimal Milestone-1 implementation (a mean
    over `fit_members`, not a genuine parametric fit). It documents and
    exercises the held-out-prediction API named in docs/protocol.md, Step
    5, route 2; a richer fitting procedure is deferred (OPEN).
    """
    fit_result = shared_V_family_test(fit_members, n_grid=n_grid)

    lo = max(np.min(m.chi) for m in fit_members)
    hi = min(np.max(m.chi) for m in fit_members)
    lo = max(lo, np.min(heldout_member.chi))
    hi = min(hi, np.max(heldout_member.chi))
    if not (hi > lo):
        raise ValueError(
            "held-out member's chi range does not overlap the fit members' "
            f"comparison domain: overlap=({lo!r}, {hi!r})"
        )
    grid = np.linspace(lo, hi, n_grid)

    fit_U_on_grid = []
    for m in fit_members:
        idx = np.argsort(m.chi)
        fit_U_on_grid.append(np.interp(grid, m.chi[idx], m.U()[idx]))
    fit_curve = np.mean(np.stack(fit_U_on_grid, axis=0), axis=0)

    idx = np.argsort(heldout_member.chi)
    heldout_curve = np.interp(grid, heldout_member.chi[idx], heldout_member.U()[idx])

    diff = np.abs(fit_curve - heldout_curve)
    return HeldoutTestResult(
        fit_agreement=fit_result,
        prediction_residual_max=float(np.max(diff)),
        prediction_residual_rms=float(np.sqrt(np.mean(diff**2))),
        chi_overlap_range=(float(lo), float(hi)),
        n_grid=n_grid,
        heldout_label=heldout_member.label,
    )
