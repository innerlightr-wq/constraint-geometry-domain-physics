"""
Tier-1 normal-form extraction for the binary-partition Fisher structure.

NORMAL-FORM EXTRACTION. Implements the existing Tier-1 identity
(docs/epistemic_tiers.md; examples/effective_potentials.md):

    V_eff^(1)(chi) = -1/2 * (dchi/dx)^2 / (1 - chi^2)

recovered from a *single supplied trajectory* chi(x).

This is EXACT algebra, applied to one known trajectory, and is
TAUTOLOGICAL as explanation: the free function V(chi) has exactly enough
freedom to absorb any supplied monotone trajectory and reconstruct it, so
this function cannot by itself demonstrate a physical mechanism, an
independent potential derivation, or a discovery. It carries no such
claim, returns no physical verdict, and its numerical output should be
labelled NORMAL-FORM EXTRACTION wherever it is reported.

Escaping the tautology requires asking the extracted structure to do
something it was not built to do -- see falsifiability.py and
docs/protocol.md, Step 5.
"""

from dataclasses import dataclass, field

import numpy as np

__all__ = ["NormalFormResult", "extract_normal_form"]


@dataclass
class NormalFormResult:
    """Output of a single-trajectory Tier-1 normal-form extraction.

    Attributes
    ----------
    chi : np.ndarray
        The supplied chi(x) samples (echoed back for convenience).
    dchi_dx : np.ndarray
        The derivative used (supplied analytically, or computed
        numerically via np.gradient).
    V : np.ndarray
        V_eff^(1)(chi) = -1/2 * dchi_dx^2 / (1 - chi^2), pointwise.
    label : str
        Fixed epistemic label. Do not reinterpret as a physical result.
    """

    chi: np.ndarray
    dchi_dx: np.ndarray
    V: np.ndarray
    label: str = field(default="NORMAL-FORM EXTRACTION", init=False)


def extract_normal_form(x, chi, dchi_dx=None) -> NormalFormResult:
    """Extract the Tier-1 normal form V_eff^(1)(chi) from one trajectory.

    Parameters
    ----------
    x : array-like
        Strictly increasing sample points along the trajectory. Only used
        to compute a numerical derivative when `dchi_dx` is not supplied.
    chi : array-like
        chi(x) samples. Must satisfy |chi| < 1 strictly everywhere: the
        partition-boundary singularity chi = +-1 is excluded (guarded
        explicitly below, not left to produce inf/nan silently).
    dchi_dx : array-like, optional
        Analytic derivative dchi/dx, same shape as `chi`. If omitted, a
        numerical derivative is computed from (x, chi) via `np.gradient`.

    Returns
    -------
    NormalFormResult

    Raises
    ------
    ValueError
        If any |chi| >= 1, or if the input shapes are inconsistent.

    Notes
    -----
    This is an EXACT relabeling of the single supplied trajectory (Tier 1,
    docs/epistemic_tiers.md). It does not test whether a domain admits an
    autonomous potential across a family; see
    falsifiability.shared_V_family_test for that over-determination test.
    """
    x = np.asarray(x, dtype=float)
    chi = np.asarray(chi, dtype=float)
    if chi.shape != x.shape:
        raise ValueError(
            f"x and chi must have the same shape, got {x.shape} and {chi.shape}"
        )
    if np.any(np.abs(chi) >= 1.0):
        raise ValueError(
            "chi must satisfy |chi| < 1 everywhere (partition-boundary "
            "singularity); the supplied trajectory reaches or crosses "
            "the boundary."
        )

    if dchi_dx is None:
        dchi_dx = np.gradient(chi, x)
    else:
        dchi_dx = np.asarray(dchi_dx, dtype=float)
        if dchi_dx.shape != chi.shape:
            raise ValueError(
                f"dchi_dx must have the same shape as chi, got {dchi_dx.shape} "
                f"and {chi.shape}"
            )

    V = -0.5 * dchi_dx**2 / (1.0 - chi**2)
    return NormalFormResult(chi=chi, dchi_dx=dchi_dx, V=V)
