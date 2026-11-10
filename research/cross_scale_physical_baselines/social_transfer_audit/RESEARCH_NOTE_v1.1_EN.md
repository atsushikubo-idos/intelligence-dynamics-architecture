# Cross-Scale Sequence History Discovery Audit v1.1

## Question
Can a model infer a predictive pattern from *anonymous ordered event records* without being handed the previously explicit `verified_transfer_event` flag? Does that pattern remain useful when the outcome mechanism changes?

## Scientific scope
This is a **synthetic predictive benchmark**, not a simulation of quantum bonding or a validated model of social relations. It builds on the social-transfer audit v0.9/v1.0; it does not alter IDOS MASTER_MAP, 12CDP, CFV/MU, or the Social Connection Architecture. No physical energy conservation is mapped to consent, trust or authorization.

## Reproducible protocol
- Generator: 6 anonymous tokens, episode length 5–10, with an experimenter-planted ordered event-pair mechanism. Outcomes are Bernoulli with success probabilities 0.90 versus 0.10 depending on whether that ordered pair occurs. The true pair is never passed to any model. Random seeds and parameters are fixed in code.
- Split: first 3,600 episodes train; next 1,200 validation; final 1,200 held-out test. Independent episodes, no within-episode time leakage. The selected model is refitted to train+validation after selection.
- Selection: evaluate all 30 directed ordered token pairs on validation Brier score, choose the minimum. These candidate features are designed beforehand; the system is not learning arbitrary new concepts.
- Comparators: no event information, last event, bag of observed tokens, a sparse histogram of all pair indicators, and **standard L2-regularized logistic regression** on the same full set of ordered pair indicators. The sparse histogram is not a strong baseline because of combinatorial sparsity; the logistic regression is the fairer competing general learner.
- Mechanism shift: 2,400 new independently generated episodes, where the planted ordered pair's conditional success probability changes to 0.52; the alternate condition remains 0.10. Fixed predictors are tested without updating. A separate prequential run predicts each outcome *before* using the newly observed outcome to recalibrate conditional rates, using a rolling window of 250 and a minimum 40 observations.

## Measured results (Brier loss; lower is better)

| Predictor | Held-out normal regime | Changed regime, fixed |
|---|---:|---:|
| Current-only | 0.242848 | 0.277573 |
| Last token | 0.219877 | 0.280259 |
| Unordered bag | 0.194483 | 0.278515 |
| All ordered pairs (sparse exact histogram) | 0.217706 | 0.275973 |
| Standard regularized logistic regression over ordered pairs | 0.095508 | 0.254768 |
| Validation-selected ordered pair | 0.085989 | 0.282428 |

The discovered pair was `(b, e)` (matching the generator's planted pair); **30** candidates evaluated. With *sequential recalibration* of the selected feature, changed-regime prequential Brier loss was **0.194132**, versus **0.282428** when held fixed. This is not a fair causal comparison between all learners because adaptation is performed for one predictor; it illustrates one mechanism for detecting outdated probability calibration, not demonstrated superiority over adaptive standard models.

## Interpretation
The test supports the narrow claim that a prediction-relevant ordered event feature can be selected without prelabeling its semantic role, within a fixed hand-engineered feature dictionary. It does not show causal discovery, emergence of new observation primitives, learning of consent, or generalization to real relations. The meaning of the tokens is not identifiable from the outcomes alone. The change is **outcome reliability**, not a demonstrated autonomous frame creation.

## Limitations and falsifiability
- The synthetic event-order signal is planted and cannot establish an IDOS-specific law.
- The 30 candidate sequence patterns and the expected future event are chosen by the researcher.
- Baseline logistics also learns from the same data with high accuracy; there is no claim of IDOS prediction superiority.
- Shifted performance requires retraining/calibration with revealed outcomes. No unsupervised drift detection is implemented.
- Full raw history access for competing learners is feasible; claims of necessary unique IDOS provenance storage are not supported.
- Next: learn latent state from raw, variable-duration multimodal event sequences using standard HMM / predictive-state methods, test true out-of-family shifts, and monitor consent/refusal without treating them as physics.

## Reproduction
From repository root:

```bash
python research/cross_scale_physical_baselines/social_transfer_audit/sequence_latent_discovery_v11.py
python -m unittest discover -s research/cross_scale_physical_baselines/social_transfer_audit -p 'test_sequence_latent_discovery_v11.py'
```

Python standard library only. Tested with Python 3.11; runtime depends on host.
