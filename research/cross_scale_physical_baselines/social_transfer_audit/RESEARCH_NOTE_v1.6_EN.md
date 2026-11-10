# Cross-Scale v1.6 — Permission-Constrained Active Observation Audit

## Status
Synthetic, reproducible baseline experiment. It is **not** an empirical study of human or AI autonomy, proof of an IDOS-specific advantage, or a method for automatically inventing new diagnostic operations.

## Relation to v1.5
The previous identifiability audit demonstrated two stipulated causes, A and B, that have an identical passive observation law: Bernoulli(0.45), while a specified diagnostic probe can separate their likelihoods. Here the *candidate* diagnostic operations are known in advance, and a Bayesian selector chooses which permissible operation to run next.

## Formal problem
Let the posterior on two stipulated causes be q=P(A|history). For diagnostic operation d with Bernoulli likelihoods p(y|A,d), p(y|B,d), use:

    IG(d|q) = H(q) - sum_y P(y|q,d) H(P(A|y,d,q))

with Shannon entropy H. An admissible operation requires explicit permission from its owner, acceptable per-operation burden, and adequate remaining total budget. The research policy maximizes:

    U(d|q) = IG(d|q) - lambda_cost * cost(d) - lambda_burden * burden(d)

and abstains from running a probe if all admissible utilities are <= 0. After an outcome, Bayes' rule updates q. Attribution A/B is reported only if posterior >= 0.95 / <= 0.05; otherwise `undetermined` is returned. No assumption is made that the nominal posterior threshold guarantees a frequentist error rate.

## Candidate observations

| Candidate | P(positive|A) | P(positive|B) | Cost | Burden | Owner |
|---|---:|---:|---:|---:|---|
| high_information | 0.85 | 0.15 | 3.00 | 3.00 | A |
| low_cost | 0.72 | 0.28 | 1.00 | 0.45 | B |
| low_burden | 0.62 | 0.38 | 0.50 | 0.10 | C |
| uninformative | 0.45 | 0.45 | 0.20 | 0.05 | C |

These likelihoods, costs, and permissions are **artificial design choices**. Budget=6, max 8 operations, burden cap=3.5, lambda_cost=0.09, lambda_burden=0.03, seed=20261111. 300 synthetic trials per cause per policy and permissions scenario. The reference baseline `standard_bayesian_design` has exactly the same objective, filters, and abstention criteria as the `constrained` policy: identical outcomes are expected.

## Results from reproducible run

| Permissions | Policy | Decision coverage | Accuracy conditional on decision | Wrong decisions / all trials | Mean cost |
|---|---|---:|---:|---:|---:|
| all | information only | 0.760 | 0.963 | 0.028 | 6.000 |
| all | cost/burden constrained | 0.000 | n/a | 0.000 | 3.093 |
| direct high-information probe denied | information only | 0.493 | 0.983 | 0.008 | 5.463 |
| direct high-information probe denied | constrained | 0.000 | n/a | 0.000 | 3.093 |
| only minimal probe permitted | information only | 0.032 | 1.000 | 0.000 | 3.984 |
| only minimal probe permitted | constrained | 0.000 | n/a | 0.000 | 0.000 |
| all declined | either | 0.000 | n/a | 0.000 | 0.000 |

The information-only and cost-sensitive policies optimize **different objectives**, so greater coverage by one is not an IDOS performance advantage. In this setup the cost-sensitive objective sometimes terminates before attaining the confidence threshold. `standard_bayesian_design` matches `constrained` exactly in all four permission scenarios. Permission violations: zero. All results are finite Monte Carlo estimates under known synthetic likelihoods.

## IDOS correspondence, not equivalence
- **Reference Frame / Observability**: observational equivalence of A/B persists without additional data; the available actions determine which distinctions become observable.
- **Boundary**: consent, rights, and burden represented as hard admissibility conditions; a Boolean flag is not an adequate model of actual consent.
- **Provenance**: each action records owner, choice, outcome, prior, posterior and cost.
- **Reality Contact**: observations are used to update, not to declare cause from unsupported passive measurements.
- **Future Updateability**: untested. Future research must examine invalid probe likelihoods, changed permissions and unmodeled third causes.
- **CFV/MU**: not operationally evaluated.

## Critical limitations
1. All candidate observations and likelihoods were specified by the experimenter. The algorithm selects a probe; it **does not discover or invent** a new probe.
2. Actions do not change the latent causes, environmental dynamics, or consent. A real social intervention could change the very system being measured.
3. Only two causes are assumed; the system cannot recognize an unmodeled third cause.
4. Results rely on exact model likelihoods and do not include calibration error, missing reports, adversarial signals, delayed feedback, or real stakeholders.
5. A classic Bayesian design baseline produces the same decisions when given the same objective and constraints. No distinctive IDOS prediction is demonstrated.
6. No chemical kinetics or quantum simulation is performed in v1.6. Its relationship to the physical-chemistry track is methodological (dynamics, observability, constrained interventions), not a derivation from chemical laws.

## Reproduce

```bash
cd research/cross_scale_physical_baselines/social_transfer_audit
python active_observation_design_v16.py > /tmp/idos_v16_results.json
python -m unittest -v test_active_observation_design_v16.py
```

No external Python dependencies. The stored `results_v16.json` is generated with the default seed. Existing v0.9–v1.5 files are untouched.
