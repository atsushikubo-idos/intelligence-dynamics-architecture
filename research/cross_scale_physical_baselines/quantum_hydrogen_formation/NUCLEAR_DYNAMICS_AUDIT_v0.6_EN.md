# IDOS Cross-Scale Physical Baselines — H₂ Nuclear Dynamics Audit v0.6

## Scope and positioning

This audit is a **physical baseline**, not a mathematical theorem about IDOS, and not an atomistic reproduction of measured H₂ formation rates. It extends the existing STO-3G FCI electronic energy audit (v0.5) to classical nuclear trajectories on the ground-state Born–Oppenheimer potential. The original v0.4 and v0.5 files are unchanged.

## Reproducible methodology

1. Read H₂ FCI energy points from the v0.5 `h2_fci_comparison.csv`.
2. Compute additional FCI points with the existing `h2_fci.solve_fci` (near short-range repulsion, near the binding minimum, and from 3.2 to 8.0 Å).
3. Use a shape-preserving piecewise cubic interpolation of the FCI/STO-3G potential. It is an interpolated numerical potential, not an exact ab initio force at every timestep.
4. Treat two hydrogen nuclei as a single classical reduced-mass radial coordinate with **zero impact parameter**; nuclear quantum effects and electronic non-adiabatic transitions are excluded.
5. Start all trajectories at 4 Å, directed inward, with equal asymptotic kinetic energy 0.008 Hartree above the two-isolated-H asymptote (−0.93316369911455 Hartree in the basis). Integrate with SciPy `solve_ivp` for up to 160 fs, stopping if the coordinate exits the interpolated domain.
6. Compare (a) no dissipation, (b) weak damping γ=0.0002 atomic-time⁻¹, and (c) stronger damping γ=0.001 atomic-time⁻¹. The damping acceleration is `−γ v`, with dissipated energy tracked as `∫ μγv² dt`.

The drag term is **synthetic**, not derived from optical transition matrix elements, photon radiation, a grain surface, or a heat bath. Its coefficient has no empirical calibration. In particular, the computed time to 'capture' must **not** be cited as a physical H₂ formation time.

## Results

| Case | Outcome | Final total mechanical energy relative to dissociation | End/exit time |
| --- | --- | ---: | ---: |
| Isolated | Leaves finite interpolation domain, outgoing | +0.008000 Ha | 94.59 fs |
| Weak damping | Energetically bound at the end of simulation | −0.114066 Ha | 160 fs |
| Moderate damping | Energetically bound at the end of simulation | −0.202874 Ha | 160 fs |

The interpolated minimum is near 0.740 Å (−1.137284 Ha); the agreement with the expected bond length is a result of the v0.5 physical model, not a fitted social-model parameter. Numerical energy accounting (`mechanical energy + accumulated dissipated energy`) is accurate to better than 10⁻⁶ Hartree in the cases tested. 15 targeted automated tests passed.

**Meaning:** For an initially unbound, positive-energy, two-body encounter on a conservative single Born–Oppenheimer curve, the atoms approach and recoil. Artificial energy transfer to an environment makes classical energetic capture possible under the tested conditions. These tests demonstrate the need to distinguish (i) an available bound configuration, (ii) a collision trajectory, and (iii) a stabilization pathway.

**Non-claims:** No photon is emitted in the calculation. No dust surface is simulated. No measured gas-phase association cross-section, binding probability or formation rate is predicted. A damped 1D classical system cannot validate quantum selection rules or general three-dimensional collision outcomes.

## IDOS research comparison (hypothesis, not an inferred physical law)

- **Affordance vs realization:** An energetically allowed configuration does not mean the dynamics will produce it. Corresponding IDOS hypothesis: an admissible relationship does not imply it will actually emerge.
- **Environment and resource exchange:** The dissipative channel alters reachable long-lived states. Corresponding IDOS hypothesis: the mediating environment and resource/constraint pathways must be part of the observation, rather than merely enumerating possible partner relationships.
- **Maintenance vs formation:** A stable configuration and a trajectory that reaches and remains there are distinct objects. IDOS should test these separately in Social Connection Architecture, while preserving consent, authority, refusals and provenance.

These hypotheses are not quantum social mechanics. They must be tested against ordinary dynamic network, Markov decision, and control baselines with equal inputs before claiming IDOS-specific added value.

## Next research step

Replace synthetic damping with an **explicit energy-accepting third degree of freedom** (e.g., a minimal classical surface oscillator) and track conservation of total energy across H–H and environment. Then test whether energy transferred to the third component can produce capture. Such a model would still be a stylized model, not validated interstellar dust chemistry.

## Reproduce

From `research/cross_scale_physical_baselines/quantum_hydrogen_formation/` after installing `numpy`, `scipy`, `matplotlib`, with v0.4 `quantum_hydrogen.py` and v0.5 `h2_fci.py` and `h2_fci_comparison.csv` present:

```bash
python run_nuclear_dynamics_v06.py
python -m unittest -v test_h2_nuclear_dynamics_v06.py
```

Generated files include `h2_nuclear_results_v06.json`, `h2_nuclear_dynamics_v06.csv` and `H2_nuclear_dynamics_v06.png`.

## Background sources

- [Energy partitioning in H₂ formation on interstellar carbonaceous grains, PCCP (2025)](https://pubs.rsc.org/en/content/articlehtml/2025/cp/d5cp01585e) — explicit stabilizing energy-disposal requirement, limitations of direct gas-phase association.
- [Radical reactions on interstellar icy dust grains, Proceedings of the Japan Academy Series B (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10196328/) — actual surface-mediated hydrogen recombination experiments and mechanisms.
