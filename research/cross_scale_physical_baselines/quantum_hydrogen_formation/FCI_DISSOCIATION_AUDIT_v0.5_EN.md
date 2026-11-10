# IDOS Cross-Scale Physical Baselines — H₂ Full CI Dissociation Audit v0.5

## Research question
How does retaining the two-electron configuration space change the prediction of H₂ bonding and bond dissociation compared with restricted Hartree–Fock (RHF)? What *structural* issues does this raise for IDOS without implying that human/AI relationships obey molecular physics?

## Model and reproduction
- Same **ab initio** STO-3G contracted Gaussian integrals as the pre-existing v0.4 `quantum_hydrogen.py` (required dependency).
- Two hydrogen nuclei held fixed at separation R: Born–Oppenheimer potential-energy surface.
- RHF: one doubly occupied spatial orbital with mean-field electron interaction.
- Full configuration interaction (FCI): **all six** occupation determinants spanning two electrons in four spin orbitals from two orthonormalized STO-3G spatial orbitals, using the nonrelativistic second-quantized electronic Hamiltonian. Exact diagonalization **within this restricted basis**, not an exact solution of the real molecule.
- Both include the same nuclear-nuclear Coulomb energy.
- Requires Python, NumPy, SciPy and Matplotlib. From this folder, run `python -m unittest test_h2_fci.py -v` and `python run_fci_comparison.py`. No external quantum chemistry software required.
- The v0.4 `quantum_hydrogen.py` must reside alongside the new v0.5 files.

## Reproduced results

| R (Å) | RHF energy (Ha) | FCI energy (Ha) | RHF−FCI (Ha) |
|---:|---:|---:|---:|
| 0.74 | -1.11675931 | -1.13728383 | 0.02052453 |
| 1.00 | -1.06610865 | -1.10115033 | 0.03504168 |
| 2.00 | -0.78379265 | -0.94864111 | 0.16484846 |
| 3.00 | -0.65604825 | -0.93363184 | 0.27758359 |

At R = 8 Å, FCI = -0.9331636991 Ha, equal (at the stated precision) to twice the STO-3G hydrogen atom energy (-0.4665818496 Ha). The restricted RHF determinant has the wrong asymptotic separated-atom physics. Note that long-distance RHF SCF may fail to converge using the elementary v0.4 solver; only reported converged values appear in the table and plot.

## What was and was not established
**Established numerically:** an explicit finite-basis many-electron treatment handles H₂ dissociation qualitatively correctly, while the single-determinant RHF approximation increasingly departs from it as the bond is stretched. All twelve v0.5 unit tests passed.

**Not established:** real-time creation of H₂ from colliding atoms; emission of energy to a photon, surface, or third body; reaction rate; quantum nuclear motion; large-basis chemical accuracy; a new physics result; IDOS-specific predictive or explanatory advantage.

An attractive Born–Oppenheimer potential or an energy minimum is **not sufficient** evidence that two initially separated gas-phase hydrogen atoms will form a stable molecular product. Stabilization needs an available energy/momentum disposal mechanism, and direct radiative association of H+H is exceptionally inefficient. Literature on interstellar chemistry identifies grain-assisted formation as an important channel.

## Relation to IDOS — hypotheses, not physical identity
1. **Representation matters:** an individual-state approximation can lose predictively necessary interactions/configurations. The precise analogue in IDOS, if any, must be measured—not assumed.
2. **Context-dependent connection:** bonding energy depends on geometry and quantum interaction, but human/AI connections involve consent, meaning, control and institutional constraints outside molecular Hamiltonians.
3. **State vs process:** a stable molecular configuration does not prove a feasible kinetic pathway. Likewise, predicting a possible social connection does not establish its real emergence or persistence.
4. **Multi-scale sufficiency:** compare compressed relational states against full-history and non- IDOS information-theoretic baselines on matched prediction tasks, including shifts and refusal events.

## Scientific next experiment
Use the FCI energy curve as a fixed-nuclei potential, then add **explicit nuclear dynamics** under clearly controlled initial conditions, with two separate experimental arms: an isolated conservative model (no energy loss), and a stated phenomenological dissipative or externally coupled model. Such classical/semiclassical nuclei dynamics would still **not** constitute rigorous real H₂ reaction-rate prediction; quantitative formation requires quantum nuclear and environment coupling appropriate to a specified mechanism.

## References (external literature)
- Tokyo University of Science, *Chapter 37: The Self-Consistent Field (SCF) and the Roothaan–Hall Equations*, H₂ STO-3G dissociation, table of RHF vs FCI energies: https://mochizuki-tus.github.io/QM_Textbook_EN/ch37_scf_roothaan_hall.html
- RSC, 2025, *Energy partitioning in H₂ formation on interstellar carbonaceous grains*: https://pubs.rsc.org/en/content/articlehtml/2025/cp/d5cp01585e
- Morisset et al., 2004, *Quantum dynamics of H₂ formation on a graphite surface*, J. Chem. Phys. DOI:10.1063/1.1781118.
