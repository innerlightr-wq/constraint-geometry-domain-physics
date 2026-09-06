# Software Scope

This page states, precisely, what the code in `src/constraint_geometry/`
computes and what it deliberately refuses to decide. It exists because
code is easier to overtrust than prose: a function that returns a number
invites the reader to treat that number as a verdict. Everything here is
the software-layer restatement of [`NON_CLAIMS.md`](../NON_CLAIMS.md) and
the safeguards in [`safeguards.md`](safeguards.md).

## What Milestone 1 adds

A small, dependency-light reference implementation (`numpy` for the
library; `scipy` and `pytest` for tests only) of material that was
already documented in this repository in prose: the exact binary-partition
coordinate algebra, the Tier-1 normal-form extraction, and a numerical
form of the shared-V family falsifiability test. See
[`../CHANGELOG.md`](../CHANGELOG.md) for the release note.

The code makes **no claim beyond what the manuscript and docs already
make**. It does not enlarge the theory; it makes a subset of it
executable and checkable.

## Formally / mathematically defined software operations

These are pure functions of their numeric inputs. Given the same inputs
they always return the same outputs, and every one of them is exact
algebra checkable against a closed-form identity:

- **Binary partition coordinate conversion** — `coordinates.py`:
  `partition_from_a`, `partition_from_ratio`, `compute_h`,
  `compute_chi_signed`, `compute_chi_unsigned`, `compute_R`,
  `compute_R_from_h`, `compute_xi`, `compute_theta`, `chi_from_xi`,
  `gudermannian`, `response_from_xi`.
- **Exact identity evaluation** — the relationships these functions
  satisfy (`4h^2+chi^2=1`, `R=1/(1-chi^2)=1/(4h^2)`, `chi=tanh(xi)`,
  `theta=asin(chi)=gd(xi)`, `R=cosh(xi)^2`) are checked in
  `tests/test_identities.py`.
- **Normal-form extraction** — `normal_form.extract_normal_form`
  computes `V_eff^(1)(chi) = -1/2*(dchi/dx)^2/(1-chi^2)` from a *supplied*
  trajectory. This is Tier 1: exact, and tautological as explanation for
  a single trajectory (`docs/epistemic_tiers.md`).
- **Numerical residual calculation** — `falsifiability.shared_V_family_test`
  and `falsifiability.heldout_V_test` compute how well a family of
  trajectories' reconstructed `U_k(chi)` curves agree. They return
  `residual_max`, `residual_rms`, and metadata — numbers, not verdicts.
- **Synthetic shared-V tests** — `tests/test_family_test_synthetic.py`
  demonstrates the above machinery on ODE-generated trajectories from
  known potentials, including a deliberately mismatched pair, so that the
  test suite can itself fail. This is a **numerical demonstration on
  synthetic data**, not an empirical physical result.

## Things the software does not decide

None of the following is computable from the coordinate algebra alone,
and no function in this package attempts to compute it:

- **Whether a domain really admits a binary partition.** Step 1 of
  `docs/protocol.md` — "a conserved total for a reason internal to the
  domain" — is a domain-physics judgment. The software accepts whatever
  `(a, b)` or `chi` values it is given; it cannot tell a genuine
  conserved partition from two unrelated numbers someone divided by their
  sum.
- **Whether an embedding is physically justified.** The map
  `a/b = F(X)` from a physical variable into the partition
  (`docs/terminology.md`, "domain embedding") is not represented in this
  package at all. Nothing here chooses, fits, or validates an `F`.
- **Whether two domains share a mechanism.** A small `shared_V_family_test`
  residual says the supplied numerical curves agree to within that
  residual — nothing more. It is not evidence that two domains share
  underlying physics (`docs/safeguards.md`, Safeguard 1 and Safeguard 2).
- **Whether a potential is fundamental.** `extract_normal_form` always
  succeeds on a single trajectory by construction (`docs/epistemic_tiers.md`,
  Tier 1). Its output is never elevated to a claim of discovery by this
  code.
- **Whether a numerical similarity constitutes physical equivalence.**
  `shared_V_family_test` and `heldout_V_test` return residuals only.
  `pass_fail(result, threshold)` is the *only* function in this package
  that returns a boolean, and it requires `threshold` as an explicit
  argument with **no default anywhere in the codebase**. An unstated
  default tolerance would be the software equivalent of the
  arbitrary-embedding hazard in Safeguard 8 (`F(X) = r*X/X_0` manufactures
  any desired agreement) — so the package refuses to supply one. Choosing
  a threshold, and justifying it, is left entirely to the caller.
- **Whether an Exact/Partial/Mismatch label is scientifically warranted.**
  The Two-Face Problem source paper's three-way translation classifier is
  **not implemented** in Milestone 1 (see `../CHANGELOG.md`, deferred
  items). If a future milestone adds it, the same rule applies: it must
  report the residual and the translation used, and require the
  tolerance for "exact" versus "partial" versus "mismatch" from the
  caller, never assume one.

## A concrete illustration of the boundary

`tests/test_family_test_synthetic.py` integrates two orbits of a chosen
potential `V(chi) = 1/2 * chi^2` and shows their reconstructed `U_k(chi)`
curves collapse to a small residual, while an orbit of a different
potential `V(chi) = 1/4 * chi^4` does not. The software:

- **does** compute the residuals, correctly, for whatever trajectories it
  is given;
- **does not** know that `V(chi) = 1/2 * chi^2` was "the same potential"
  in some deeper sense — it only ever sees `(x, chi)` arrays and a
  declared energy `E`;
- **does not** decide that a residual of `5×10⁻⁴` "passes" — the test
  file declares `1e-2` as its own threshold and states why, exactly as
  `pass_fail` requires.

## Relationship to the manuscript

The manuscript (`paper/constraint_geometry_domain_physics.tex`) remains
the authoritative source for all equations, terminology, and
interpretations, per `CHANGELOG.md`. This code implements a subset of
that manuscript's Tier-1 content plus the numerical falsifiability
machinery already described in `docs/protocol.md` and
`examples/effective_potentials.md`. It does not extend the manuscript's
claims.
