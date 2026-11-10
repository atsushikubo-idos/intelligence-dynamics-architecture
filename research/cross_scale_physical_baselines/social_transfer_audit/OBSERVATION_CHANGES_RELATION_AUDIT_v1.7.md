# IDOS Cross-Scale Audit v1.7 — Observation Changes the Relationship

## Status
Executable synthetic baseline, not a validated model of social behavior or IDOS-specific scientific advantage. 14 unit tests passed on 2026-11-11. All stochastic results arise from *assumed* kernels and seeded simulations, not measured causal effects.

## Research question
Can an observation policy maximize evidence while simultaneously degrading the relationship whose dynamics it is trying to understand? Can an explicitly risk-aware policy preserve the relationship better under otherwise identical prior information?

## Known generative process
- Two latent hypotheses, `A` and `B`, equally likely initially.
- Three actions: passive, gentle probe, strong probe. The positive-observation probabilities under A/B are (.58/.42), (.76/.24), (.93/.07).
- Conditional relationship dissolution risks per action are 0, .025, .23. Costs are 0, .01, .015 respectively. These are *stipulated*, not inferred.
- Consent is a hard feasibility constraint for either active probe. Refusal forces passive observation.
- Each episode begins with the relationship intact; at most three sequential decisions are made. A diagnostic observation is registered first, and then the relation may dissolve. No later probes follow dissolution. Bayesian posterior is updated from the diagnostic outcome. Dissolution itself has no additional diagnostic value because the hazard is assumed hypothesis-independent.
- The belief threshold .95 terminates additional observation. Equal prior, known observation kernels and hazard model.

## Methods
Information gain is `H(C) - E[H(C|Y,d)]`. The information-only policy maximizes that one-step quantity. The risk-aware policy maximizes `IG - 2.7 * dissolution_risk - cost`. The passive baseline never probes. This is a one-step, myopic planner, **not** a complete POMDP or a learned adaptive intervention model.

Reproduce with Python 3.10+ (stdlib only):

```bash
cd research/cross_scale_physical_baselines/social_transfer_audit
python -m unittest -v test_observation_changes_relation_v17.py
python observation_changes_relation_v17.py
```

## Results (10,000 seeded simulated episodes, 20261111)
| Policy | Brier error | Relationship survives | Mean observations | First action |
|---|---:|---:|---:|---|
| Passive | 0.233011 | 1.0000 | 3.0000 | passive |
| Information-only | 0.029655 | 0.5657 | 1.8432 | strong_probe |
| Risk-aware | 0.119895 | 0.9434 | 2.9310 | gentle_probe |

All policies obeyed explicit refusal in the implemented test; their forced action was passive. The policies use the same prior and observation kernels, but different utility objectives; outcome streams are independently seeded and therefore not exactly paired by random draw.

## Interpretation and falsifiability
This synthetic example demonstrates a *tradeoff induced by model assumptions*: a highly informative act can degrade future relationship survival. A conventional Bayesian planner with the identical risk objective reproduces the same choices. It offers no claim of novel Bayesian information theory or IDOS prediction advantage.

Stress tests and empirical work would need (1) inferred, uncertain, context-specific intervention hazards, (2) effects of interventions on future observation kernels and agents' reference frames, (3) delayed consent and autonomy constraints, (4) multi-actor decision records and provenance, (5) repeated environment shifts and independent validation.

## Relationship to the preceding physical and social audits
The quantum chemistry baseline is a physics computation; the current social intervention model is an analogy **only at the level of formation, maintenance, dynamics and environmental coupling**. Energies, conservation laws, chemical bonds and consent must not be equated. Earlier physical finite-bath experiments did not yield a social law or prove the new policy.

## Established fields
Dual control, active sensing, experimental design, and causal interventions already analyze information-action tradeoffs. For example:
- La et al. (2016), *Dual Control and Information Gain in Controlling Uncertain Processes*, IFAC-PapersOnLine, DOI: 10.1016/j.ifacol.2016.07.230.
- La et al. (2017), *Dual Control and Online Optimal Experimental Design*, SIAM J. Scientific Computing, DOI: 10.1137/16M1069936.
- Steyvers et al. (2003), *Inferring causal networks from observations and interventions*, Cognitive Science, DOI: 10.1207/s15516709cog2703_6.
