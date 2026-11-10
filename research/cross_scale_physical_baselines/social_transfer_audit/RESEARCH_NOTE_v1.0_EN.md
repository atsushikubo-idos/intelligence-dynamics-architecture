# IDOS Cross-Scale History Discovery Audit v1.0

## Scope
This follows the **synthetic** v0.9 connection-mechanism experiment. It tests whether a learner can discover which **already observed** event-history features predict persistence after a mediator departs. It does not infer meaningful consent or discover latent human intentions, and **does not derive** social laws from quantum chemistry.

## Experimental design

- Artificial episodes represent A/B relationships that are connected at the current time. Candidate inputs are current connection, an event recording a previously verified and authorized protocol transfer, mediator-use event, direct-protocol event, disruption event, correlated noisy marker, and unrelated random event.
- The simulated subsequent intervention is **identical** for all episodes: mediation and direct protocol become unavailable; A/B retain consent. The stipulated v0.9 rule then makes persistence depend on a previously certified transfer.
- Importantly, the training algorithm is **not told which feature matters**. It searches 42 subsets (current connection plus up to three event-history features) using internally group-held-out Brier loss plus a predeclared complexity penalty.
- Episodes are split by disjoint artificial groups: 1,680 for development and 720 reserved for final evaluation. Model selection occurs only on the development split.
- Hold-out baselines include current connection only, an all-observed-features histogram, noisy marker, a transfer-feature oracle, **and a standard one-split decision tree/stump independently selected from all available features**. The latter tests whether IDOS-like selection has any advantage over a basic established learning method.
- A separate counterfactual changes transfer reliability from 1.0 to 0.55 without informing the models. This is an environmental rule change, not an observed real-world regime change. Results are deterministic with fixed random seeds.

## Reproduced results

From `results_v10.json`:

| Model | Held-out Brier score (lower is better) | Shifted rule Brier |
|---|---:|---:|
| Current connection only | 0.1875000 | 0.1527778 |
| Selected history | 0.0000022 | 0.1342252 |
| All observed features, unsmoothed complexity beyond basic priors | 0.0007582 | 0.1256616 |
| Noisy marker | 0.1330759 | 0.1455781 |
| Oracle selected history | 0.0000022 | 0.1342252 |
| Standard decision stump | 0.0000022 | 0.1342252 |

The selected subset is `connection_now` and `verified_transfer_event`. The independent standard decision stump finds that **same history event**, with the **same held-out score**. There is **no IDOS-specific predictive advantage**. The slight full-history histogram disadvantage reflects data sparsity, not an informational disadvantage of full history. The tiny nonzero score for deterministic labels is due to deliberately applied probability smoothing.

## Critical limitations

1. **Ground-truth leakage through engineered observables:** While the correct feature is not explicitly passed to feature selection, the observation `verified_transfer_event` is itself a deliberately constructed, perfectly predictive certificate. This is much easier than identifying latent causal structure from unstructured historical records.
2. **Artificial labels:** The outcome is specified directly by the simulator's rules. This is a test of recovery of a known mechanism from data, not scientific validation of that mechanism.
3. **Finite candidate set:** The learner can only select features prepared by the designer; it does not invent a new reference frame or learn event semantics.
4. **Shift sensitivity:** Changing the rule breaks calibration. Neither an IDOS architecture nor an autonomous reference-frame update was tested.
5. **No claim of causality:** Predictive feature importance is not causal identification. A valid causality test requires interventions, confounding analysis and new data.
6. **No scientific uniqueness:** The decision-stump baseline matches the selected-history predictor.

## Next falsifiable experiment

Remove the explicit transfer certificate from the observations. Supply only noisy, time-stamped sequences (consent declarations, observed verification interactions, authorization changes, protocol reuse). Learn a latent predictive state with predeclared temporal baselines (last-k event model, regularized logistic regression, hidden-state model), then evaluate on unseen mediators and rule-change sequences. Compare **out-of-sample calibration, next-step prediction and adaptation cost**, while preserving refusals and unresolved differences. Avoid choosing feature definitions using test-set outcomes.

## Reproduce

Python 3.10+, standard library only. Run:

```bash
python -m unittest -v test_history_discovery_v10.py
python history_discovery_v10.py > results_v10.json
```

Place these four v1.0 files in `research/cross_scale_physical_baselines/social_transfer_audit/`. Existing v0.9 files are unchanged. No repository-root additions.
