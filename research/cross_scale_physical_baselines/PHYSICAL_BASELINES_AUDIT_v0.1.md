# IDOS Cross-Scale Physical Baselines Audit v0.1

Date: 2026-11-11. Status: standalone research controls; **no claim of an IDOS-specific predictive advantage**.

## Research question

Can a system's possible next interactions be predicted without complete access to its microstate, and when does coarse-graining erase the information needed for that prediction? What physical mechanisms generate conditional collective structure and history-dependent future trajectories?

## Method and falsifiability

We implement four **established baseline models** with no IDOS-specific dynamics, no agents, and no real-world social or molecular data. These establish precise comparison targets, not social-science validations. Each model includes a falsifiable numerical prediction and automated regression tests. Exact code, results and parameters are included in this directory. Only Python standard library required.

1. **Two-state equilibrium binding.** `P(bound)=1/(1+exp(ΔG/T))` with `k_B=1`. At `T=1`, ΔG ∈ {-4,0,4} gives bound probabilities ≈ {.9820,.5,.0180}. This is a simplified thermodynamic *state model*, not an atomistic bond calculation. It does not resolve quantum wavefunctions, orbital overlap, chemical species, or reaction kinetics.
2. **Finite 2D Ising lattice.** Exact enumeration of every `2^(3×3)=512` spin configuration on a 3×3 periodic square lattice; `J=1, h=0`. `H = -J Σ_(nearest neighbors) s_i s_j` and `m = Σ_i s_i/N`. For T=.8,2,5, `E[|m|] ≈ 0.999905, 0.925985, 0.459977`, respectively. The ensemble magnetization `E[m]` is zero by global spin-flip symmetry; therefore the reported quantity is absolute magnetization. No thermodynamic singularity or physical critical temperature is inferred from nine sites.
3. **Projection / coarse-graining counterexample.** Microstates `a,b` both map to macrostate X; `c,d` map to Y. From microstate a, P(Y next)=.9; from b, P(Y next)=.1. Consequently, the macrostate X *alone* is not sufficient to specify next-step dynamics independently of its underlying microstate: strong lumpability fails. A history-aware or microstate-aware observer can distinguish the cases. This is an existing Markov aggregation result, not IDOS novelty. The example does not prove that no alternative compact sufficient representation exists.
4. **Schlögl-type chemostatted autocatalytic reaction.** Reaction channels `A+2X -> 3X`, `3X -> A+2X`, `B -> X`, `X -> B`, with reservoir concentrations A=B=1 and rate coefficients 7,1,8,14. Mass action yields `dx/dt = 7x² - x³ + 8 -14x = -(x-1)(x-2)(x-4)`. Equilibria x=1 and x=4 are locally stable; x=2 is unstable. Fourth-order Runge–Kutta with dt=.002, 20,000 steps: x0=.5 and 1.5 approach 1, x0=2.5 and 5 approach 4. This is a deterministic, driven, well-mixed model with fixed chemostats, not spontaneous generation of new reaction rules; the two basins are **not evidence that actual social relationships obey chemical kinetics**.

## What the tests establish

- Physics provides nontrivial constraints on how structure, interaction and scale affect observable dynamics.
- The coarse-graining counterexample directly challenges naive summaries: if distinct underlying states map to the same macrostate but imply different futures, the macrostate cannot by itself support exact next-step prediction.
- Multistability shows how the same dynamical laws can yield different long-term trajectories depending on initial conditions.

## What the tests do **not** establish

- No atomistic or quantum-chemical simulation; no derivation from atomic orbitals to molecules.
- No evidence for objective social 'binding energies', temperatures, chemical rate constants or societal phase transitions.
- No representation of consent, refusal, agency, CFV/MU, provenance or actual intelligent agents in these baselines.
- No demonstration of emergent self-modification of rule-generating algorithms.
- No comparative advantage of IDOS over complete-history, predictive-state, Markov-state or other established models.

## Connection to existing IDOS components: a testable bridge, not a new axiom

- **Connection Boundary / Continuity:** represent admission/consent constraints as hard gates separate from physical analogy. A probabilistic binding model must never override explicit refusal.
- **Reference Frame / Provenance:** the Markov aggregation counterexample motivates testing whether a chosen relational summary preserves future-transition information; record which microstate/historical distinctions were erased.
- **Trajectory / Future Updateability:** distinguish occupancy of a currently stable configuration from the reachable state space following an environmental or boundary intervention.
- **Discovery Architecture:** future work should compare fixed proposal grammars to genuinely adaptive synthesis under identical information, compute and intervention budgets. The present audit cannot claim discovery of novel generative operators.

### Next pre-registered comparative tests

P1. Construct paired IDOS relational summaries and full-history/predictive-state baselines on the **same generated transition data**; use held-out one-step transition log-loss and multi-step reachability error, with identical feature budgets.

P2. Apply explicit interventions to microstate transition probabilities or boundary gates, then test the retention of predictive information, including refusal; do not infer causal effects solely from observational associations.

P3. Vary system size and interaction topology; quantify uncertainty and finite-size effects rather than asserting a phase transition.

P4. For a chemical network with competing pathways, compare a fixed kinetic network to an explicitly adaptive *network topology* under a controlled environment. Separate operator changes built in by the programmer from self-generated ones.

## Reproduction

From this folder:

```sh
python physical_baselines.py > results.json
python -m unittest -v test_physical_baselines.py
```

The repository root is not modified and this is **not** wired into the production Social Connection Architecture; the purpose is to preserve independent, scientifically recognized controls before attempting model transfer.

## Relevant external literature

- ALPS Software Package, Ising model documentation: https://alps.comp-phys.org/documentation/models/ising/
- van der Schaft, Rao & Jayawardhana, *On the Mathematical Structure of Balanced Chemical Reaction Networks Governed by Mass Action Kinetics*, SIAM J. Appl. Math.: https://doi.org/10.1137/11085431X
- MacDonald, *A coarse-grained Markov chain is a hidden Markov model*, Physica A (2020): https://doi.org/10.1016/j.physa.2019.123661
- Schlögl model example, Journal of Chemical Physics: https://pubs.aip.org/aip/jcp/article/149/18/185101/566775/Discrete-flux-and-velocity-fields-of-probability

All bibliographic links are references to established methods, not validation of IDOS.
