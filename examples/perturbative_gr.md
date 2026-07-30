# Example: Perturbative General Relativity

The primary example of the note. It is the case where the partition is least open to the charge of being imposed, because the two sectors come from an exact rearrangement of a field equation.

## The exact decomposition

Write $g_{\mu\nu}=\bar g_{\mu\nu}+h_{\mu\nu}$ with $\bar g$ a background and $h$ the perturbation. The Einstein tensor separates exactly into its linear part and the remainder:

$$G_{\mu\nu}[g]=G^{(1)}_{\mu\nu}[h]+G^{(\ge2)}_{\mu\nu}[h]$$

so the field equation may be rewritten as

$$G^{(1)}_{\mu\nu}[h]=8\pi G\left(T_{\mu\nu}+t_{\mu\nu}\right),\qquad t_{\mu\nu}\equiv-\frac{1}{8\pi G}G^{(\ge2)}_{\mu\nu}[h]$$

**This is a rearrangement, not an approximation.** The matter source and the gravitational self-energy contribution together form the effective source of the linear operator, and the two channels exhaust that source by construction. The object $t_{\mu\nu}$ is gauge-dependent and is related in harmonic gauge to the standard gravitational stress pseudotensor.

The significance for Step 1 of the protocol: the *domain*, not the geometry, says there are exactly two channels and that they close.

## The schematic norm ratio

For a quasi-spherical configuration with compactness $C=2GM/(rc^{2})$, the perturbation scales as $|h|\sim C$, and the leading higher-order terms, being quadratic in $h$ and its derivatives, motivate

$$\frac{\|G^{(\ge2)}\|}{\|G^{(1)}\|}\sim C$$

This belongs to standard perturbation theory and is not derived in the note. It is **schematic in two respects that matter**:

- it is an order-of-magnitude relation between norms, not an equality;
- both norms are gauge- and slicing-dependent.

## The intersection

Normalizing the two sectors, with $F(C)=C$ as the embedding:

$$\frac{a}{b}=C,\qquad a=\frac{C}{1+C},\qquad b=\frac{1}{1+C}$$

Independently, the constraint geometry supplies $h=\sqrt{ab}=\sqrt{C}/(1+C)$. Imposing the intrinsic crossing $h=a/b$:

$$\frac{\sqrt C}{1+C}=C\;\Longrightarrow\;C(1+C)^{2}=1\;\Longleftrightarrow\;C^{3}+2C^{2}+C-1=0$$

with unique positive root $C_{\mathrm{crit}}=\psi-1=0.465571231876768\ldots$

**Division of labor:**

| Ingredient | Supplied by |
| --- | --- |
| Two sectors exhausting the effective source | the exact rearrangement |
| The sector ratio $a/b=C$ | general relativity, via the norm estimate |
| The altitude $h=\sqrt{ab}$ | constraint geometry |
| The intrinsic condition $h=a/b$, i.e. $a=b^{3}$ | constraint geometry |
| The cubic and its root | the intersection of the two |
| Any physical meaning of that root | neither, so far |

## The normalization ambiguity

This is the load-bearing limitation. Suppose the sector ratio is more accurately

$$\frac{a}{b}=\alpha C$$

for some dimensionless $\alpha$ that an order-of-magnitude estimate between gauge-dependent norms does not fix. Then

$$C_{*}=\frac{r_{*}}{\alpha}$$

and the physical threshold scales inversely with a quantity the derivation never pinned down. More generally, $F(C)=\alpha C^{n}$ gives $C_{*}=(r_{*}/\alpha)^{1/n}$.

So: the intrinsic marker is exact, the number $0.4656$ is exact **as a partition ratio**, and the compactness value inherits the full indeterminacy of the normalization. **The compactness number is no firmer than the embedding normalization.**

## The two routes are one route

The equality $C_{\mathrm{crit}}=h_{*}$ is algebraic, not evidential. Both computations impose $a=b^{3}$ on the same partition and differ only in which coordinate is solved for; the compactness polynomial $C^{3}+2C^{2}+C-1$ and the altitude polynomial $h^{3}+2h^{2}+h-1$ are the same polynomial. This is recorded so that it is not mistaken for an independent cross-check. See Safeguard 3.

## Structural versus orbital compactness

Two distinct quantities share the form $GM/(rc^{2})$ and are both called compactness.

- **Structural:** $C=2GM/(rc^{2})$ with $r$ a radius of the configuration itself — a fixed property of a star or a static geometry. **This is the quantity used here.**
- **Orbital:** $v^{2}/c^{2}\sim GM/(rc^{2})$ with $r$ the orbital separation in a binary — a dynamical quantity that sweeps upward through an inspiral, and the one that actually governs post-Newtonian accuracy.

A landmark value of one is not a landmark value of the other. Consequently an observation that some number is close both to the compactness of massive neutron stars and to the regime where post-Newtonian accuracy degrades is **not one coincidence but two claims about two quantities that happen to share a symbol.**

## What is explicitly not claimed

- Constraint geometry does not derive the Einstein field equations. The uniqueness of $G_{\mu\nu}+\Lambda g_{\mu\nu}$ is a separate result with a separate proof.
- The cubic is not a universal law of gravity.
- $C_{\mathrm{crit}}$ is not a point at which nonlinear gravity begins. The higher-order sector is nonzero for every $C>0$ and grows smoothly; no onset is asserted.
- No numerical post-Newtonian threshold is claimed. The literature supports a qualitative loss of accuracy as a binary approaches merger, where resummation methods or numerical relativity become necessary; it attaches no compactness value, and neither does the note. Establishing one would require a dedicated study specifying the gauge, the waveform family, the post-Newtonian order, and the error measure against which degradation is defined.
- "Loses accuracy" is the defensible statement and is weaker than "diverges": the post-Newtonian series is an asymptotic expansion whose convergence properties are not established, so what degrades is truncation accuracy at fixed order.

## Status

Candidate diagnostic. Tier 1 for the algebra, **not Tier 2**: the embedding is schematic and no test is performed.
