# Safeguards

Nine safeguards against the characteristic failure modes of partition-based reasoning. Each corresponds to a way the framework has been, or could be, overread.

---

## 1. Universality trap

Many systems normalize to $a+b=1$. Shared arithmetic is not shared physics, and the recurrence of the partition across domains is **expected** rather than informative. The safeguard is to compare under a fixed, pre-declared normalization and to require an over-determination test — not to treat recurrence as evidence.

## 2. Chart contributions

Behaviour contributed by the coordinates must not be reported as a domain finding. The response divergence $R\to\infty$ as $|\chi|\to1$, the Fisher denominator $(1-\chi^{2})^{-1}$, and the boundary structure of the response face are all supplied by the chart. Two systems sharing a boundary divergence share a response geometry, not a mechanism. The domain-specific content lives in the numerator, not the denominator.

## 3. Algebraic identities are not independent cross-checks

When two computations impose the same condition on the same partition and differ only in which coordinate is solved for, their agreement is a tautology. Concretely: the compactness polynomial $C^{3}+2C^{2}+C-1$ and the altitude polynomial $h^{3}+2h^{2}+h-1$ are the same polynomial, so the equality $C_{\mathrm{crit}}=h_{*}$ is algebraic and not evidential. It is recorded in the note precisely so that it is not mistaken for a confirmation. A cross-check must involve independent inputs.

## 4. Admissible physical range

A partition coordinate normalized to $[0,1]$ need not have a physically admissible range that large. Every landmark must be located relative to the domain's own bounds, and a landmark outside them is not a diagnostic regardless of how exactly it is located. Endpoints of the normalized interval are especially suspect: they are frequently outside the regime in which the domain description holds at all.

## 5. Landmark crowding

Before reporting a landmark as occupied, check whether its neighbourhood contains generic constants within the measurement error of the domain. Near the cubic value, an interval of width comparable to current cosmological precision contains at least three unrelated numbers:

$$b_{*}\approx 0.682328,\qquad \operatorname{erf}(1/\sqrt2)\approx 0.682689,\qquad \Omega_{\Lambda,0}\approx 0.6835$$

with $\sigma_{\Omega_\Lambda}$ of order $0.007$. The separations are an order of magnitude below the uncertainty. The Gaussian one-sigma mass is a generic aggregation landmark with no domain-specific content, so proximity within measurement error cannot distinguish one landmark from generic nearby constants, and agreement with any one of them is not structural.

The safeguard generalizes beyond cosmology: **a landmark is only as informative as its neighbourhood is sparse.**

## 6. Information-content check

Before testing whether a partition coordinate organizes an observable, check whether it *can*.

> If $\mu,\chi,R,J,\xi$ are invertible functions of one scalar state, then they reorganize the same information and do not create a new predictive degree of freedom.

In flat ΛCDM all of them are functions of $\Omega_{m}(z)$ alone. Consequently any apparent value added by a higher-order coordinate over a lower-order one signals **leakage** — residual dependence re-entering through a nonlinear reparameterization — rather than new content. Genuine content requires leaving the regime in which the reduction holds; for the cosmological case that means $w_{\mathrm{DE}}\neq-1$, where the rapidity curvature $d^{2}\xi/(d\ln s)^{2}=-\tfrac32 w_{\mathrm{DE}}'$ is nonzero.

This is a screen to be applied **before** a test is run, not an explanation offered after one fails.

## 7. Order and level

The altitude is a geometric mean of the two fractions — an amplitude-level object — while the ratio $a/b$ compares them directly. A condition equating the two, such as $h=a/b$, is a partition-intrinsic relational condition and must be labelled as such. It is **not** a balance law between two physical quantities of like dimension and should not be read as one. This is why the crossing is called a landmark rather than an equilibrium or a threshold.

## 8. Arbitrary embedding: the threshold-manufacturing objection

Given any target value $X_{0}$ and the geometrically fixed $r_{*}$, the embedding

$$F(X)=\frac{r_{*}X}{X_{0}}$$

places the landmark exactly at $X_{0}$. Therefore **no agreement between a partition landmark and an observed value is evidence for anything** unless $F$ was fixed, in full, by domain physics before the comparison was made.

This is the single most important safeguard in the programme, and it is the reason the perturbative-GR case is the primary example: there, $F(C)=C$ follows from an operator estimate that exists independently of any partition consideration. Even so, the estimate is an order-of-magnitude relation between gauge-dependent norms, so an overall normalization $\alpha$ remains unpinned and $C_{*}=r_{*}/\alpha$. That ambiguity must be reported, not suppressed.

## 9. Ordered versus unordered branch ambiguity

The altitude $h=\sqrt{ab}$, the squared asymmetry $\chi^{2}$, and the response $R$ are all symmetric under $a\leftrightarrow b$. The landmark condition $a=b^{3}$ is **not**. Consequently, identifying a landmark by its response value specifies an unordered *pair* of states, not one state.

In the cosmological case, $R\approx1.15337$ is attained both where $\Omega_{m}=\Omega_{\Lambda}^{3}$ and where $\Omega_{\Lambda}=\Omega_{m}^{3}$ — and these are different epochs. Only the ordered condition selects a branch, and only domain physics can order the sectors. Reporting a landmark by its $R$ value alone, without declaring which sector is $a$, leaves the physical claim ambiguous by construction.
