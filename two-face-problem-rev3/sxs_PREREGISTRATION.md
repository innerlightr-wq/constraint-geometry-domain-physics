# SXS through the Thales framework — preregistered plan (written before running tests)

Data: SXS catalog metadata (sxscatalogdata main = v3.0.0 simulations.json; 4148 BBH rows).
Filters (fixed now): non-deprecated; reference_eccentricity < 0.01; 0.001 < E_rad/M < 0.2.

## Instantiation (decided from the mechanism, before fitting)
1. Embedding: a = heavier mass share m1/M, b = lighter share m2/M, M = m1+m2 at reference time.
2. Closure: NOT closed through merger. Leakage L = E_rad/M = 1 - M_f/M. Use the leakage reading:
   remnant fraction 1-L is the radius; the question is how L depends on the state on the arc.
3. Coupling: h^2 = ab = eta (symmetric mass ratio), the standard post-Newtonian parameter.
4. Native coordinate: predicted to be eta (= h^2), because PN/NR theory expands in eta. Test it.
5. Orientation: SXS labels m1 >= m2, so chi = a-b >= 0 by convention; sign carries no physics
   except through which body carries which spin (not tested here).

## Tests
T1 (replicate the Bridge Guide's "equipartition differential"): Y = E_rad/M, context
   [chi_eff, b_bind, 1/D], six two-feature bases, partial R^2 per chi-bin. Run with the paper's
   bins AND equal-width bins; report within-bin Var(chi). Prediction (from the null simulation):
   the growth of partial R^2 with chi tracks bin width and shrinks or vanishes with equal bins.
T2 (native coordinate, nonspinning quasicircular subset): 5-fold CV RMSE of degree-1/2/3
   polynomials in each coordinate {eta, h, chi, xi, R, theta} for E_rad/M and final spin a_f.
   Prediction: eta (or h) wins; Fisher angle / rapidity do not.
T3 (leakage law): E_rad/M -> (1 - sqrt(8/9)) * eta as eta -> 0 (test-particle ISCO binding
   energy). Prediction: the small-eta slope of E_rad/eta approaches 0.0572.
T4 (mixed object): recoil |v_kick| for nonspinning systems vs the Fitchett/Gonzalez form
   A eta^2 sqrt(1-4 eta)(1 + B eta) = A h^4 chi (1+B h^2). Prediction: needs BOTH coupling (h)
   and asymmetry (chi); single-coordinate low-order fits do worse.
