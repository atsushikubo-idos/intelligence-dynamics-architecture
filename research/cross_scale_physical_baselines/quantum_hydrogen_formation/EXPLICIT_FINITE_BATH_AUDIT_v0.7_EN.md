# IDOS Cross-Scale Physical Baselines — Explicit Finite Environment Audit v0.7

## Research question
Can an explicit third-party/environmental degree of freedom receive energy from an approaching hydrogen pair, permitting temporary residence in the bonding region **without nonconservative drag**, and how does that depend on the environmental structure?

## Scope and actual model
This is **not** a microscopic simulation of hydrogen formation or an IDOS social model. It is a classical, one-dimensional nuclear trajectory on the previously computed Born–Oppenheimer H₂ STO-3G **FCI potential** (v0.5 and v0.6). The environment is a finite set of classical harmonic oscillators. No empirical parameters for radiation or interstellar grain interactions are used.

The conservative Hamiltonian (atomic units) is

\[
H=\frac{p_r^2}{2\mu}+V_{\rm FCI}(r)
+\sum_{j=1}^N \left[\frac{p_j^2}{2}+\frac{\omega_j^2}{2}\left(q_j-\frac{c_j f(r)}{\omega_j^2}\right)^2\right].
\]

The counterterm maintains the same *relaxed* BO potential. Here \(f(r)=(r-r_e)\exp[-(r-r_e)^2/(2\sigma^2)]\), with \(\sigma=2.2\) bohr. Couplings are parameterized by \(\sum c_j^2/\omega_j^2=\lambda_{\rm total}\). Frequencies are artificial, in the range 0.005–0.027 atomic units. The initial bath state is at rest. A symplectic velocity-Verlet integrator steps the whole Hamiltonian without a drag term.

## Experimental controls
- All cases: initial nuclear distance 4 Å, inward energy 0.008 Ha **above** the separated-H limit, trajectory up to 180 fs, time step 0.12 atomic units.
- Isolated system: zero oscillators.
- Single weakly coupled oscillator: \(N=1\), \(\lambda=0.01\).
- Single strongly coupled oscillator: \(N=1\), \(\lambda=0.08\).
- Distributed bath: \(N=24\), \(\lambda_{\rm total}=0.03\), evenly spaced oscillator frequencies.

## Reproduced outcomes
| Scenario | Endpoint H–H distance | Last H₂ mechanical energy relative to isolated dissociation | Endpoint or retention |
|---|---:|---:|---|
| Isolated | ~7.99 Å | +0.008 Ha | Exits the tabulated potential domain |
| One weak mode | ~8.00 Å | +0.00191 Ha | Exits the tabulated potential domain |
| One strong mode | ~0.98 Å | −0.13927 Ha | Still inside; fails strict last-quarter retention criterion |
| 24-mode environment | ~0.73 Å | −0.20394 Ha | Meets **finite-window retention** criterion |

The simulated total energy, *including oscillator and interaction terms*, remains constant numerically with maximum recorded drifts less than 0.00001 Ha for all four configurations. The bound-region event is **not** proven asymptotic or irreversible. All finite baths can return energy to the molecular coordinate; energy backflow is visible, particularly in the one-mode system. The 24-mode result is one deliberately specified illustrative parameter set, not a general law that more agents/modes improve formation.

**Operational retention**: throughout the final quarter of the simulated interval, H–H distance <2 Å and H₂ mechanical energy below the isolated dissociation reference. This is only a finite-window proxy, not an experimental capture probability.

## Interpretation for IDOS (hypothesis, NOT a physical deduction)
A structural possibility, distinct from a validated analogy, is to separate (i) existence of a feasible configuration, (ii) approach/entry into it, (iii) transfer or handling of destabilizing constraints, and (iv) retention over time. Third parties matter only when they contribute a functioning interaction channel and compatible constraints. A third party can also return a perturbation or destabilize an existing relation. In human/AI systems, consent, rights, meaning, refusal, reference frames, and agency cannot be represented by oscillator energies.

This physical demonstration **does not validate IDOS**, establish novel physics, prove a universal relation-formation principle, or measure CFV/MU/Future Updateability. It offers a controlled benchmark for later comparison against Social Connection Architecture v0.3 and the existing Connection Boundary audits.

## Limitations and falsification agenda
1. Classical nuclei and a 1-D zero-impact-parameter encounter ignore quantized nuclear vibration, rotational states, collision impact parameters, and radiative selection rules.
2. The finite STO-3G basis, BO approximation, interpolation and phenomenological bath couplings limit molecular accuracy. The bath is not calibrated to a physical environment.
3. Increasing the number of modes is confounded with frequency distribution, coupling allocation and observation window. A factorial parameter sweep is needed.
4. Finite Hamiltonian environments do not ensure irreversible stabilization; long-time recurrences and temperature dependence must be investigated.
5. Future: compare identical total couplings with a controlled mode spectrum, quantify recurrence time vs. time window, then inspect physically derived radiative/grain coupling before any claim of real H₂ formation kinetics.

## Reproduction
Keep this v0.7 set alongside v0.4–v0.6 in `research/cross_scale_physical_baselines/quantum_hydrogen_formation/`.

```
python run_explicit_bath_v07.py
python -m unittest -v test_h2_explicit_bath_v07.py
```

Requires `numpy`, `scipy`, `matplotlib`, the v0.5 `h2_fci.py` and `h2_fci_comparison.csv`, and v0.6 `h2_nuclear_dynamics_v06.py`.
