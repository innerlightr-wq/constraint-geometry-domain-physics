# SXS catalog through the Thales framework — results

Data: SXS catalog metadata (sxscatalogdata v3.0.0, 4148 BBH); filtered N = 3527
(non-deprecated, e < 0.01, 0.001 < E_rad/M < 0.2); nonspinning N = 81. Plan in PREREGISTRATION.md.
Scripts: load.py, analyze.py (-> analyze_output.txt), figure.py.

T1  Old "equipartition differential" (E_rad/M, six bases, context chi_eff/b_bind/1/D): NOT replicated.
    Paper's bins: ratio 1.8, Pearson(chi, partial R^2) = -0.17 (published: 13.7, +0.82).
    Equal-width bins: ratio 1.6, Pearson +0.11. Bin counts match the published table's pattern,
    so the chi definition appears the same; the remaining differences are filters/context details.
T2  Native coordinate (5-fold CV, nonspinning): eta = h^2 wins clearly at degree 2 for both
    E_rad/M (RMSE 2.05e-4 vs h 6.7, chi 9.5, Fisher 15.5, rapidity 20.0, R 61.0) and final spin
    (3.96e-4 vs h 14.8, chi 35.6, Fisher 79.1, rapidity 242.9). Prediction from the mechanism
    (PN theory expands in eta) confirmed. Fisher, rapidity and response coordinates are not native here.
T3  Leakage law: E_rad/(M eta) extrapolates to 0.0597-0.0598 at eta -> 0 vs the test-particle
    ISCO binding energy 1 - sqrt(8/9) = 0.0572 (about 5% high from 9-21 points). Consistent with
    the standard NR picture; small-eta sample is thin.
T4  Recoil is a mixed coupling x asymmetry object: A h^4 chi (1 + B h^2) with 2 parameters gives
    CV RMSE 2.07e-5 c vs best single-coordinate cubic 2.43e-5 c (4 parameters).
    A = 13,072 km/s, B = -1.34, peak 173 km/s at eta = 0.192 (literature: ~1.2e4 km/s, B ~ -0.93,
    ~175 km/s at eta ~ 0.195).
