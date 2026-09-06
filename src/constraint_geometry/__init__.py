"""
constraint_geometry — exact binary-partition coordinate algebra and
Tier-1 normal-form / falsifiability machinery.

Scope
-----
This package implements ONLY the mathematically well-defined operations
documented in README.md, docs/terminology.md, docs/epistemic_tiers.md,
docs/protocol.md, and docs/safeguards.md. It makes no physical claims,
supplies no domain embeddings, and decides no questions of physical
equivalence. See docs/software_scope.md for the explicit boundary between
what this code computes and what it deliberately leaves as a required,
caller-supplied judgment.

Modules
-------
coordinates     Exact binary-partition coordinate algebra (Tier 1).
normal_form     Tier-1 normal-form extraction from a supplied trajectory.
falsifiability  Numerical shared-V family / held-out over-determination
                tests. Returns residuals only; never a default verdict.
"""

__all__ = ["coordinates", "normal_form", "falsifiability"]
