# The Two-Face Problem — Revision 3

Supporting files for Revision 3 of the Bridge Guide ("The Two-Face Problem"), by Elias De Jesús.

## Layout

| Folder | Contents |
|---|---|
| `paper/` | LaTeX source, bibliography, figure, compiled PDF |
| `scripts/` | Everything needed to reproduce the checks and the SXS section |
| `outputs/` | Recorded output of each script for this revision |
| top level | `CHANGELOG_rev3.md`, `sxs_PREREGISTRATION.md`, `sxs_RESULT.md` |

## Reproduce

```bash
cd scripts
python3 fetch_data.py              # downloads SXS catalog metadata v3.0.0 (~32 MB), checks MD5
python3 verify_rev3.py             # symbolic/numeric checks of the identities — expect 48 PASS, 0 FAIL
python3 analyze.py                 # SXS analysis (Section 9)
python3 cv_repeat.py               # 200-repeat 5-fold CV, polynomial degrees 1–3
python3 equipartition_null_test.py # null test showing the equipartition differential is a binning artifact
python3 figure.py                  # regenerates fig_sxs.png
```

Requires Python 3 with `numpy`, `sympy`, `matplotlib`. The data file is not committed; `fetch_data.py`
pins the source (`sxs-collaboration/sxscatalogdata`, tag `v3.0.0`, `simulations.json`) with a checksum.

## Related work

- De Jesús, E. (2026). *The Minkowski Interval as a Thales Coupling Diagnostic.* SSRN. doi:10.2139/ssrn.6734698
- De Jesús, E. (2026). *Hamiltonian–Lagrangian Quadrature on the Thales Partition Manifold.* Zenodo. doi:10.5281/zenodo.21135133
- De Jesús, E. (2026). *Two-Face Series: Effective Potentials on the Binary Partition Manifold.* Zenodo. doi:10.5281/zenodo.21430864
- De Jesús, E. (2026). *Constraint Geometry and Domain Physics.* Zenodo. doi:10.5281/zenodo.21695430

SXS data: Scheel et al. (2025), *Class. Quantum Grav.*, doi:10.1088/1361-6382/adfd34.
