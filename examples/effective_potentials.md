# Example: Effective Potentials on the Partition Manifold

The dynamical instance of the architecture, and the source of the framework's sharpest self-criticism.

## The Fisher kinetic skeleton

The information metric on the binary partition is

$$ds_{F}^{2}=\frac{da^{2}}{a}+\frac{db^{2}}{b}=\frac{d\chi^{2}}{1-\chi^{2}}=R\,d\chi^{2}$$

This is proposed as a **universal kinetic skeleton**, with a domain potential $V_{\mathrm{domain}}(\chi)$ carrying the contextual dynamics. The split is the dynamical form of the two-layer architecture:

$$\text{universal Fisher denominator}+\text{contextual numerator}\ \longleftrightarrow\ \text{universal constraint structure}+\text{domain-specific dynamics}$$

## The first-integral extraction

For a static one-dimensional pullback $\chi=\chi(x)$, the zero-energy first integral gives

$$V^{(1)}_{\mathrm{eff}}(\chi)=-\frac{1}{2}\,\frac{(\partial_{x}\chi)^{2}}{1-\chi^{2}}=-\frac{1}{2}\,\frac{\text{contextual numerator}}{\text{universal denominator}}$$

**Universal denominator.** The factor $1-\chi^{2}$ is fixed by the Fisher metric and encodes the partition-boundary response as $|\chi|\to1$. It is a **chart contribution**. Every member of the standard family shares it, so a shared boundary divergence is evidence of shared response geometry and nothing more.

**Contextual numerator.** The factor $(\partial_{x}\chi)^{2}$ encodes how the particular domain approaches the boundary through its pullback. This is where domain content lives — but note that the numerator exponent is not coordinate-free: reparameterizing $x$ changes it, so numerator classes are meaningful only after a physically justified gauge is fixed.

## Why single-trajectory extraction is tautological

The extraction is **exact** and, applied to one known trajectory, **explains nothing**.

Counting degrees of freedom: the data is one function, the model contains one free function $V(\chi)$, and the single available first-integral constraint is consumed by the zero-energy normalization. The fit therefore has exactly enough freedom to absorb any monotone trajectory, leaving zero residual. Feed in an arbitrary pullback, extract $V^{(1)}$, re-integrate the zero-energy equation, and the input is regenerated — because it was inserted.

**A model that cannot fail explains nothing.** So the extraction is a Tier-1 **normal form**: a canonical relabeling useful for classifying numerator/denominator structure, carrying no discovery claim.

## What is required to escape the tautology

An extracted structure acquires falsifiable content only when it is asked to do something it was not built to do. Four routes, in decreasing order of practical strength:

1. **Shared-potential family test.** Do not fix the energy and do not fit a single curve. Require one autonomous potential to reproduce a family of trajectories that independent physics says should share it but differ by an external parameter — energy, initial condition, mass, boundary data — and report the residual, including for held-out members. *A construction that reports a residual which could be large is no longer a tautology.*
2. **Independent determination.** Fix the potential from an action, a free energy, an equation of state, a conservation law, or a measured response curve, then **predict** the trajectory and compare. In this direction the framework is translation and prediction rather than backward fitting. The cosmological embedding is the closest available instance.
3. **Cross-domain recurrence under pre-declared normalization.** If two unrelated domains yield the same normalized shape, that may indicate a shared dynamical class — but the normalization protocol must be declared *before* comparison, or rescaling manufactures agreement.
4. **Compression.** A complex trajectory reducing to a simple low-parameter potential carries information, because a short description has replaced a long one. If the extracted potential is as complex as the original curve, the result is a relabeling.

## Failure is a result

If a domain admits no autonomous potential across its natural family, that is a **positive structural finding**: the domain is not governed by an autonomous one-dimensional partition potential. The worked instance in the source paper is gauge-coupling running, where the extracted object depends explicitly on an absolute scale and not on the partition coordinate alone — so the family test correctly rejects autonomy and identifies the flow as irreducibly two-dimensional. The negative *is* the finding.

## A coordinate caution

The flat coordinate of the Fisher metric is $u=\arcsin\chi$, **not** the rapidity $\xi=\operatorname{arctanh}\chi$, which is flat for the distinct hyperbolic metric $d\chi^{2}/(1-\chi^{2})^{2}$. Writing a Fisher-denominator kinetic term in $\xi$ leaves a residual $\operatorname{sech}^{2}\xi$ weight that is a signature of the metric–coordinate pairing and not of domain physics. Comparisons must declare the pairing.

## Relation to the static architecture

The present note's landmark story is the static analogue of this dynamical one. There, geometry supplies the arena and the landmarks while physics supplies the trajectory and the meaning; here, geometry supplies the denominator while physics supplies the numerator. The discipline transfers directly: **exact is not the same as explanatory, and a construction that always succeeds tests nothing.**

## Status

Tier 1 for the metric, the split, and the extraction. Tier 2 only after an over-determination test.
