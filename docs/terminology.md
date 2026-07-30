# Terminology

Terms are used in exactly these senses throughout the repository and the manuscript.

### Binary partition

Two positive quantities normalized so that $a+b=1$. The normalization is trivially available for any pair; the term is reserved here for cases where the closure has a domain-internal reason — a conservation law, an exact decomposition, a definitionally complete budget.

### Constraint geometry

The layer of structure that follows from $a+b=1$ alone: the coordinates $h,\chi,R,\xi$, the identities among them, and the relational landmarks they define. Exact, parameter-free, and independent of any domain. Used consistently in preference to looser phrases like "the geometry" or "the framework."

### Domain physics

Everything the constraint layer cannot supply: which sectors are being partitioned, why they close, how physical variables map in, how the state evolves, what range is admissible, and what any landmark means.

### Domain embedding

The map $a/b=F(X)$ from a physical variable $X$ into the partition, together with the induced $a=F/(1+F)$ and $b=1/(1+F)$. An embedding is **derived** when $F$ follows from domain physics independent of any partition consideration, and **chosen** otherwise. The distinction is the single most consequential one in the framework.

### Intrinsic relational landmark

A locus on the partition manifold specified by a condition written in the partition coordinates alone. Examples: the apex $\chi=0$; the altitude–ratio crossing $h=a/b$, equivalent to $a=b^{3}$. Landmarks are exactly located, domain-free, and carry no physical content by themselves.

### Physical realization

The solution $X_{*}$ of $F(X_{*})=r_{*}$: where a given intrinsic landmark sits in a domain's own coordinate. The landmark does not move; its realization moves with $F$.

### Occupancy

Whether a physical system is actually observed at or near the realization of a landmark. An empirical property of the system, not of the geometry.

### Mechanism

Whether the domain's own dynamics distinguishes the landmark state — a critical point of a flow, a change of sign in a rate, a transition in an observable. A property of the domain's physics, not of the geometry, and logically independent of occupancy.

### Diagnostic

A landmark that has a derived embedding, a domain-assigned meaning, and either an independently justified map or a falsifiable consequence. A landmark lacking any of these is a **candidate** diagnostic at best. Nothing in the note is claimed to be a diagnostic in the full sense.

### Response coordinate

$R=(1-\chi^{2})^{-1}=1/(4h^{2})$, taking values in $[1,\infty)$. Bounded state, unbounded response: divergence of $R$ records boundary approach in the partition, not a physical singularity. Note also that $R$ is symmetric under $a\leftrightarrow b$, so identifying a state by its $R$ value specifies an unordered pair of states.

### Fisher metric

The information metric on the binary partition, $ds_{F}^{2}=da^{2}/a+db^{2}/b=d\chi^{2}/(1-\chi^{2})=R\,d\chi^{2}$. Its flat coordinate is $u=\arcsin\chi$ — **not** the rapidity $\xi$, which is flat for the distinct hyperbolic metric $d\chi^{2}/(1-\chi^{2})^{2}$. Pairing the Fisher denominator with $\xi$ leaves a residual $\operatorname{sech}^{2}\xi$ weight that is a signature of the metric–coordinate choice and not of domain physics. Any comparison must declare the pairing.

### Normal-form extraction

Recovering an effective potential from a single known trajectory via $V^{(1)}_{\mathrm{eff}}(\chi)=-\tfrac12(\partial_x\chi)^{2}/(1-\chi^{2})$. Exact, useful for classification, and tautological as explanation: the free function absorbs the input curve and reconstructs it. A normal form is Tier 1 and carries no discovery claim.

### Family test

The strongest available over-determination route: require one potential to reproduce a family of trajectories that independent physics says should share it but differ by an external parameter, and report the residual. A construction that reports a residual which could be large is no longer a tautology. Failure of the test is informative — it shows the domain is not governed by an autonomous partition potential.

### Structural compactness

$C=2GM/(rc^{2})$ with $r$ a radius **of the configuration itself**. A fixed property of a star or a static geometry. This is the quantity used throughout the note.

### Orbital post-Newtonian parameter

$v^{2}/c^{2}\sim GM/(rc^{2})$ with $r$ the orbital **separation** in a binary. A dynamical quantity that sweeps upward through an inspiral, and the quantity that actually governs post-Newtonian accuracy.

> **These two are not interchangeable.** They share the algebraic form $GM/(rc^{2})$ and are both routinely called "compactness," but one is a fixed structural property and the other a time-dependent orbital parameter. A landmark value of one is not a landmark value of the other. In particular, an observation that some number is close both to the compactness of massive neutron stars and to the regime where post-Newtonian accuracy degrades is **not one coincidence but two claims about two different quantities that happen to share a symbol.**
