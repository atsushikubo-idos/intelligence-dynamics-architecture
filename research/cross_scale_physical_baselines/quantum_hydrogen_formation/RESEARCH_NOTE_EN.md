# IDOS Cross-Scale Audit: First-Principles Hydrogen Bonding Baselines v0.4

## Research question
Can physical models of atomic interactions demonstrate conditions under which a bound molecular structure exists, before evaluating any proposed analogy to relational dynamics among heterogeneous intelligences?

## What was actually computed
The hydrogen molecule H2 (two electrons and two protons) was calculated using restricted Hartree–Fock (RHF) in the standard contracted STO-3G hydrogen 1s basis. The hydrogen molecular ion H2+ (one electron and two protons) was solved by generalized diagonalization of the one-electron Hamiltonian in the same basis. Gaussian overlap, kinetic, nuclear-attraction and electron-repulsion integrals are evaluated analytically; nuclear repulsion is included. The Born–Oppenheimer approximation fixes the internuclear distance at each calculation point.

This is an **ab initio electronic-structure potential-energy scan**, not an empirically tuned Morse curve. It is **not** an atom-collision trajectory, chemical kinetics, spontaneous formation simulation, exact quantum dynamics, or a demonstration that two hydrogen atoms bind by themselves in free space. In an isolated environment formation of a stable molecule requires a mechanism to carry away energy and conserve momentum, e.g. radiation, a third-body process or a suitable collision pathway.

## Methods
For contracted s-type Gaussian orbitals chi_mu, form overlap S, core Hamiltonian H, and two-electron repulsion integrals (mu nu|lambda sigma). H2+ solves H C = S C epsilon; E(R) = epsilon_min + 1/R. H2 solves self-consistent closed-shell RHF (two electrons in the bonding orbital): F = H + J[P] - 1/2 K[P], P = 2 C_occ C_occ^T, E = (1/2) Tr[P(H+F)] + 1/R. Internal distances and energies use atomic units; outputs are in Å and Hartree.

## Measured numerical results (minimal basis)
- H2 RHF/STO-3G energy minimum: R = 0.71223 Å, E = -1.11750589 Hartree.
- H2+ STO-3G one-electron energy minimum: R = 1.06058 Å, E = -0.58269665 Hartree.
- H2 at 0.74 Å: -1.11675931 Hartree, consistent with the standard RHF/STO-3G benchmark.
- Both curves have a finite-distance minimum; closely approaching nuclei are repulsive.

These are **method-specific approximations**, not precise experimental bond lengths or measured dissociation energies. The experimental H2 equilibrium distance is roughly 0.741 Å. In particular, RHF does **not** correctly describe H2 dissociation to two neutral hydrogen atoms at large separation; the broken-symmetry/static-correlation problem is substantial. The one-electron H2+ calculation is exact only within the selected finite basis and Born–Oppenheimer assumptions.

## Falsification and validation
Ten unit tests check contracted-orbital normalization, matrix symmetry, electron-repulsion integral permutation, reproduction of a standard numerical benchmark, existence of minima, short-range repulsion, and an explicit RHF dissociation limitation. `run_experiment.py` produces full CSV scans, JSON summary and two independent curves.

## What maps (and does not map) to IDOS
- **Conditioned existence of a bound configuration**: A finite-distance energy minimum is an objective physical definition within the Hamiltonian. For IDOS, an analogue would need independently defined constraints and measurable relational stability, not a metaphorical `social energy`.
- **Emergent relational state**: A bound electronic state is a property of the total system, not just either isolated atom. In IDOS, comparable claims require demonstrating additional predictive content of interaction terms beyond independently described agents.
- **History and path dependence**: The equilibrium electronic potential alone does not establish path dependence or reopening. Additional dynamical/environmental modelling would be required.
- **Autonomy, consent, CFV/MU, provenance**: These have no physical equivalents in an H2 Hamiltonian. No direct transfer is justified.
- **Future updateability**: The energy minimum is not an updateability measure. A novel IDOS operationalization must be separately defined and tested against fair baselines.

## Next experiments, in order
1. **Better H2 dissociation:** compute full configuration interaction (FCI) in the same two-orbital basis, compare RHF and FCI potential curves, then distinguish improvements due to correlation from IDOS-specific claims.
2. **Formation dynamics and environment:** add nuclear dynamics and a physically justified energy-loss channel. Without dissipation, entering a potential well does not imply permanent capture.
3. **H2O structure:** extend to three-atom geometry optimization and vibrational behaviour with established quantum chemistry software, to study nontrivial many-body interaction.
4. **Cross-scale prediction:** only afterward compare physical coarse-graining with IDOS's explicitly defined future-event predictions; test proper baselines under matched information budgets.

## References
- IUPAC Gold Book, “Morse potential,” DOI: 10.1351/goldbook.MT07073 (comparison model; not used in the ab initio computation).
- NIST CCCBDB, experimental diatomic vibrational data: https://cccbdb.nist.gov/expdiatomicsx.asp
- P. M. Morse, Phys. Rev. 34, 57 (1929), DOI: 10.1103/PhysRev.34.57.
- Physical Review X, accepted 31 August 2026, “Ionization and dissociation energies of molecular hydrogen,” DOI: 10.1103/42c4-pc1s.

## Reproduce
Requires Python 3.10+, numpy, scipy, matplotlib. From this directory:

```bash
python -m unittest -v test_quantum_hydrogen.py
python run_experiment.py
```

All files remain within `research/cross_scale_physical_baselines/quantum_hydrogen_formation/`; no root-level repository files are created. This experiment does not modify existing IDOS modules or theory.
