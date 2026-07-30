# Example: Flat ΛCDM

The instructive case, because two landmarks appear on one trajectory and fail in **opposite** ways.

## A genuine partition with a derived embedding

In a flat cosmology the density parameters exhaust unity, so the closure is a constraint of the Friedmann system rather than a normalization of convenience. In the matter-plus-Λ regime where radiation is negligible:

$$a=\Omega_{m},\qquad b=\Omega_{\Lambda},\qquad a+b=1$$

giving $\mu=ab=\Omega_{m}\Omega_{\Lambda}$, $\chi=\Omega_{m}-\Omega_{\Lambda}$, and $R=(1-\chi^{2})^{-1}$.

The embedding follows from the conservation laws rather than being chosen. With scale factor $s$, matter dilution $\rho_{m}\propto s^{-3}$ and constant $\rho_{\Lambda}$:

$$\frac{a}{b}=F(s)=\frac{\Omega_{m,0}}{\Omega_{\Lambda,0}}\,s^{-3}$$

and more generally the density-ratio rapidity obeys

$$\frac{d\xi_{\mathrm{DE}}}{d\ln s}=-\tfrac{3}{2}\,w_{\mathrm{DE}}(s)$$

which follows from the two separate conservation laws alone — $w_{m}=0$ and $\rho'_{\mathrm{DE}}/\rho_{\mathrm{DE}}=-3(1+w_{\mathrm{DE}})$ — and requires neither flatness nor two-component closure. **This is an embedding of the stronger kind:** it is the independent-determination route, not a fitted map. ΛCDM is the case $w_{\mathrm{DE}}=-1$, for which the flow is a uniform translation in rapidity at rate $3/2$.

## The ordered-branch issue

$h=\sqrt{ab}$, $\chi^{2}$, and $R$ are symmetric under $a\leftrightarrow b$. The condition $a=b^{3}$ is **not**. So identifying a landmark by its response value specifies an unordered *pair* of states: $R\approx1.15337$ is attained both where $\Omega_{m}=\Omega_{\Lambda}^{3}$ and where $\Omega_{\Lambda}=\Omega_{m}^{3}$, and these are **different epochs**.

Only the ordered condition selects a branch, and only domain physics can order the sectors. The assignment $a=\Omega_{m}$, $b=\Omega_{\Lambda}$ is the one under which the occupied state is the marker:

- matter is at present the **minority** sector, $\Omega_{m}\approx0.317\approx a_{*}$;
- this matches the orientation of the perturbative-GR embedding, where the higher-order sector is the minority channel;
- it aligns the sign convention, since $\chi_{*}<0$ for the intrinsic landmark and $\chi_{\mathrm{today}}=\Omega_{m}-\Omega_{\Lambda}<0$.

Reversing the labels selects the **mirror epoch**, substantially earlier, and flips the sign of $\chi$. Nothing in the constraint geometry chooses between the two orderings.

---

## (a) Meaning without occupancy

The domain flow supplies its own landmark. With $J=\mu|\chi|$, flat ΛCDM satisfies exactly

$$\frac{d\Omega_{m}}{d\ln s}=-3\mu,\qquad \frac{d^{2}\Omega_{m}}{(d\ln s)^{2}}=9\mu\chi=9J\operatorname{sgn}\chi$$

so the coupling is the **velocity** of the matter-fraction flow and the coupling–asymmetry product is its **acceleration**. The acceleration extremum lies at $|\chi|=1/\sqrt3$, that is at

$$R_{J}=\frac32$$

equivalently at the state where the third logarithmic derivative of $\Omega_{m}$ vanishes.

This landmark is **derived from the domain mechanism** and therefore means something about the flow. But the present epoch is not there: $R_{J}$ is attained at $z\approx1.0$ and $z\approx-0.17$, some twenty standard deviations from today in the cosmological parameters.

**Mechanism: yes. Occupancy: no.**

## (b) Occupancy without meaning

The intrinsic marker $a=b^{3}$ is realized at $F(s_{*})=r_{*}$, that is at

$$s_{*}=\left(\frac{\Omega_{m,0}}{r_{*}\,\Omega_{\Lambda,0}}\right)^{1/3}$$

which for concordance parameters falls at $z\approx0.002$ — effectively now, with $R_{*}=1.15337$ against a present-day $R\approx1.156$.

Occupancy is excellent. And here the absence of a mechanism can be **proved** rather than merely conceded. Using $d\chi/d\ln s=\tfrac32(1-\chi^{2})$, the flow admits an exact Fisher-gradient representation

$$\frac{d\chi}{d\ln s}=-(1-\chi^{2})\,U'(\chi),\qquad U(\chi)=-\tfrac{3}{2}\chi$$

in which the potential is **linear**, so

$$U'(\chi)\equiv-\tfrac32\neq0\quad\text{everywhere.}$$

The flow therefore has **no interior critical point at all**: its only fixed points are the simplex edges $\chi=\pm1$, and at the cubic state $d\chi/d\ln s\approx1.30\neq0$. The universe passes through the cubic state at ordinary speed. A mechanism selecting it would require a domain potential with an interior minimum there, which is not ΛCDM.

**Occupancy: yes. Mechanism: provably no.**

---

## The lesson

$$\boxed{\ \text{meaning without occupancy}\ \neq\ \text{occupancy without meaning}\ }$$

Neither cosmological landmark is a diagnostic, and they miss for opposite reasons. Meaning and occupancy are supplied by different layers, and neither implies the other.

A framework reporting only (b) would look like a success. A framework reporting only (a) would look like a mechanism. Reporting both is what makes the architecture visible.

## Two further cautions specific to this case

**Landmark crowding.** The region near $0.68$ contains the cubic root $b_{*}\approx0.682328$, the Gaussian one-sigma mass $\operatorname{erf}(1/\sqrt2)\approx0.682689$, and the present-day $\Omega_{\Lambda,0}\approx0.6835$ with uncertainty of order $0.007$ — separations an order of magnitude below the precision. Proximity cannot discriminate among them.

**Information content.** Inside flat ΛCDM, $\mu,\chi,R,J,\xi$ are all invertible functions of $\Omega_{m}(z)$, so they reorganize the same information and add no predictive degree of freedom. Any apparent value added by a higher-order coordinate signals leakage. Genuine content requires $w_{\mathrm{DE}}\neq-1$, where the rapidity acquires curvature.

## Status

Tier 1 for the identities. Tier 2 **attempted and returning a negative** — which is the most informative outcome available here, and the reason this example carries the argument.
