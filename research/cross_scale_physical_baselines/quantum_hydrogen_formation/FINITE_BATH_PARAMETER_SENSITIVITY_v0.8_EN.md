# Explicit finite bath parameter sensitivity audit v0.8

## Scientific aim

Distinguish *mode count*, *total coupling strength*, and *frequency distribution* in the earlier v0.7 H₂ + classical oscillator environment. The electron-energy surface comes from STO-3G full CI in a fixed-nuclei Born–Oppenheimer approximation; the nuclear stretch and oscillator bath are classical.

## Controlled comparison

The v0.7 Hamiltonian and coupling profile are unchanged. Nine cases cross `N = 1,4,24` with total coupling `λ = 0.01,0.03,0.08` at the same nominal frequency range 0.005–0.027 a.u. Additional cases at `N=24, λ=0.03` use narrow 0.012–0.014 and higher 0.025–0.047 a.u. ranges. All begin at the same geometry and molecular incident energy; the oscillators start at q=0, p=0. Integration time is 180 fs, time step 0.12 a.u.

**Important confound:** for N=1 a linearly spaced frequency range yields one frequency at the low endpoint. Therefore the N=1 vs N>1 experiment is *not a pure isolated effect of mode count*: increasing the count also changes the sampled spectral distribution. Coupling λ is defined as sum(c_j²/ω_j²), with equal contributions per mode. No claim of a universally optimal bath size follows.

## Outcomes and scope

`tail_fraction_r_below_2A` is the fraction of recorded times during the last 45 fs for which the nuclei are separated by less than 2 Å. `retention_v07` additionally requires the molecular energy (excluding bath/coupling terms) to be below the dissociation reference throughout the final sampled quarter. These are finite-time *proxies*, not a quantum mechanically justified chemical product yield or a proof of asymptotic stability. `backflow_from_peak_Ha` quantifies loss of bath+interaction energy relative to its maximum; this is an operational indicator, **not a quantitative non-Markovianity measure**.

Numerical checks verify that total molecular+oscillator+interaction energy changes by less than 10⁻⁴ Ha over the recorded trajectory. The finite bath is Hamiltonian, so energy may flow back into the molecule. Altered oscillator ranges are phenomenological tests, not calibrated dust-grain phonons, photons, or realistic H₂ formation kinetics. No temperature ensemble, multidimensional collision, electronic excitation, quantum nuclear motion, surface adsorption, diffusion, or desorption is simulated.

## Existing theory before any IDOS interpretation

1. Born–Oppenheimer + electronic full CI (within the minimal basis) supplies a potential energy curve, not a reaction pathway.
2. Classical Hamiltonian molecular dynamics resolves the nuclear stretch along that curve.
3. Finite harmonic-oscillator bath models an energy-exchange environment. A finite bath does not generically yield irreversible relaxation.
4. Chemical-physics studies of dust-mediated H₂ formation additionally model adsorption, diffusion, reaction, transfer to surface modes, and possible desorption; our setup covers only a very small subset.

## Cautious IDOS research bridge

The transferable *questions*, not transferable physical conservation laws, concern (i) accessibility of a joint state, (ii) actual formation under a trajectory and environment, (iii) persistence for an explicitly chosen observation window, and (iv) the possibility of disconnection/reopening under later environmental changes. For IDOS, consent, refusal, agent autonomy, CFV/MU, and provenance must be added as independent variables. A third party is not automatically a stabilizing bath. No predictive advantage over standard physics or social models has been shown.

## Reproduction

Run `python h2_bath_sensitivity_v08.py` from this directory with the v0.4–v0.7 dependent modules already present. Run `python -m unittest test_h2_bath_sensitivity_v08.py`. Standard environment: NumPy, SciPy, Matplotlib. Artifacts are a JSON summary, CSV, and plot; no root-level files are added.

## Scientific references

- Wakelam et al. (2017), *Molecular Astrophysics* 9, 1–36, doi:10.1016/j.molap.2017.11.001 (surface-formation review).
- The 2025 physical-chemistry simulation study on H₂ energy partition in carbonaceous grains, DOI/article d5cp01585e, *Physical Chemistry Chemical Physics*.
- Yang et al. (2026), *Astrophysical Journal* 1006, 245, doi:10.3847/1538-4357/ae82f6, explicit multiscale adsorption/diffusion/association/desorption study.
