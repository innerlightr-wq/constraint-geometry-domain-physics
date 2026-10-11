# The Two-Face Problem — Revision 3 (October 2026): changelog

Not uploaded or published. The LaTeX was rebuilt from the Revision 2 PDF.

## Added
- **The arc as a universal constraint locus.** (a−b)² + 4ab = (a+b)² holds for any budget, so lying on the arc is automatic.
- **Signed asymmetry.** χ = a − b replaces |2a − 1|. The symmetric quantities h, R and y are noted to be orientation-blind.
- **Shares and forces.** Mean and natural parameters of the Bernoulli family: χ = tanh ξ, and R = dξ/dχ is the force needed per unit change of share.
- **Instantiating the arc (Definition 1).** Six components: embedding, closure, coupling type, native coordinate, orientation, dynamics. Plus a pre-commitment rule.
- **Native coordinate by composition**, replacing "simplest-looking form". Examples:
  - Lorentz boosts
  - Bayesian log-odds
  - resistive impedance ratios (new: Γ = tanh(½ ln Z/Z₀))
  - cosmic e-folds
  - proportion estimation (variance-stabilizing angle)
- **Constraint-type table** (scarcity / pressure / conservation / dissipation), labelled Tier 3.
- **Leakage.** The angle-plus-radius half-disk and R_act amplification. Links to Stokes parameters, the Bloch vector and qubit leakage. Realized versus potential coupling (dephasing). Scale as a hidden coordinate (gauge running).
- **Normal forms versus over-determination tests**, imported from the revised effective-potentials note.
- **Instantiation case studies.**
  - SR: null components and odds composition.
  - Bernoulli.
  - ΛCDM in e-folds: dξ/dN = 3/2, V = −(9/8)(1−χ²), and dξ/dN = (3/2)(w_b − w_a) in general.
  - Damped oscillator.
  - Informative failures: gauge running, and the RH displacement.
- **SXS case study** (new data analysis, preregistered):
  - η = h² gives the most compact description, with repeated CV at degrees 1–3 reported in full.
  - The leakage law is consistent with the ISCO test-particle limit, but the data do not pin it (0.046–0.069 depending on the fit).
  - Recoil: Fitchett–González form; 173 km/s at η = 0.192.
- **Safeguards section and revised checklist.**

## Removed
- Equipartition differential (withdrawn). The null simulation reproduces it from bin widths; it does not replicate on SXS (ratio 1.8, Pearson −0.17).
- "Dimensional selection" from the powered metric family (threshold manufacturing).
- "Six Pythagorean powers".
- "Infinite half-step" remark.
- Pendulum and Kepler dynamics from a shared potential.
- The undefined "Tellegen budget" and "vantage angle" (the latter is replaced by the standard Bhattacharyya angle φ = arcsin√a).

## Corrected
- Generating function G(t): the Revision 2 rapidity and radial forms were those of θ/h, not of G = φ/h = (gd ξ + π/2) cosh ξ.
- Bernoulli native coordinate is now the Fisher/Bhattacharyya angle (Revision 2 said "Compound").
- ΛCDM orientation conventions made consistent; the scale-factor shape is attributed to the correct orientation.
- Radial metric noted to be degenerate at χ = 0.
- Notation clashes fixed: leakage λ versus half-asymmetry L, and latitude φ_lat versus angle φ.

## Verification
- verify_rev3.py: 48 PASS, 0 FAIL.
- SXS results reproduce from analyze.py, cv_repeat.py and data_simulations.json (sxscatalogdata v3.0.0).
- An independent referee pass found 14 issues. All were fixed, including the ΛCDM sign, the G(t) wording, the Bernoulli native coordinate, CV reporting, recoil wording, the ISCO overstatement, null-bin attribution, notation, and tiering.

## Still open
- The SDSS results are withdrawn pending re-analysis; no data were available here.
- The DeJesus2026HL, EP and SR self-citations have no DOI in the bibliography. Add them if they exist.
- The RH citation points to the weil-window-control repository rather than a paper.
