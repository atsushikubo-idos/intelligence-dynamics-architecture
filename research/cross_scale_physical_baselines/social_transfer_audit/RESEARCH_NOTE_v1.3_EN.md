# Cross-Scale Multi-Frame Relational Predictivity Audit v1.3

## Scope and scientific status

This is an **artificial, falsifiable benchmark**, not evidence for real-world social mechanisms, physical/social law equivalence, or IDOS-specific predictive superiority. It extends the *research question* in v1.2, but is standalone code that does not import or modify preceding audits.

## Research question

Can a learner construct a compact cross-actor event-order representation from the differing observations of agents A, B and C, and does that representation predict the future maintenance of a mediated connection? What happens when the governing mechanism changes?

## Generative mechanism (harness only)

Three parties each emit six anonymous event symbols (six-token history); the learner receives raw event streams and current A/B permissions, C attestation, revocation and mediator-exit status. The private harness plants an A:1-before-B:4 and B:4-before-C:2 sequence. When the mediator exits, both cross-actor sequences and attestation permit a transferable connection; when it remains, permission permits mediated connection. Outcomes are Bernoulli observations: 0.94 success if eligible and 0.03 otherwise. In the shift regime, the successful transferred connection rate drops to 0.48. These are **invented model rules**, not empirical social findings.

## Learning and comparison

72 candidate directed cross-actor event-order predicates (36 A→B; 36 B→C) are evaluated using **training labels only**. The strongest predictive one from each group is selected. A logistic predictor uses those discovered relations together with the same current status variables. Four non-unique baselines compare current status only; all raw event tokens as one-hot logistic regression; all raw tokens as random forest; and a standard random forest given the same engineered relation features. The latter is a feature-parity baseline; matching performance counts *against* an IDOS-only advantage. The candidate order grammar is designed by the experimenter and is **not** discovered autonomously.

Train / validation / held-out test / shifted test: 4200 / 1400 / 1500 / 1500 episodes; independent deterministic seeds. Validation samples are generated but not used for model selection (reserved for extensions). All evaluations use Brier score (smaller is better), log loss, and thresholded accuracy. Explicit consent is a hard operational constraint, not a physical analog. Models do not issue actions; predicting probabilities is not equivalent to permission to connect.

## Reproduced observations

| Predictor | Normal held-out Brier | Changed-mechanism Brier |
|:--|--:|--:|
| Current status only | 0.10963 | 0.12457 |
| All raw events, logistic | 0.08309 | 0.12523 |
| All raw events, random forest | 0.05903 | 0.12188 |
| Learned relation feature, logistic | 0.04729 | 0.12467 |
| Same relation features, standard random forest | 0.04710 | 0.12875 |

The learned ordered pairs match the planted A:1→B:4 and B:4→C:2. The standard learner equipped with the same engineered features is indistinguishably competitive. On the shifted mechanism, relation-based predictors degrade. No one predicts that there is a universal gain from relational compression or that an adaptive update rule has been implemented.

The test harness verifies consent restrictions in **synthetic ground-truth eligibility**. The prediction models themselves do not enforce autonomy or refuse actions; future real systems require a separate hard-constraint policy. Likewise the input event streams are available to a centralized estimator: this experiment does not yet demonstrate decentralized privacy-preserving multi-agent learning.

## How to reproduce

Python 3.11+; dependencies `numpy` and `scikit-learn` (tested with NumPy 2.3.5 and scikit-learn 1.8.0). In this folder:

```sh
python multiframe_relation_audit_v13.py
python -m unittest -q test_multiframe_relation_audit_v13.py
```

Outputs are deterministic under listed seeds, but dependency/BLAS changes may affect floating-point metrics slightly. Results JSON is stored in `results_v13.json`.

## Relation to original physics/chemistry program

The models of H₂ electronic structure, FCI, nuclear trajectories and explicit finite baths in v0.4–v0.8 are **separate physical baselines**. This v1.3 benchmark tests a transferable methodological distinction—possible connection vs realized/persistent connection and the relevance of history—not a mathematical derivation of social behavior from quantum chemistry.

## Next falsifiable milestone

Predict and *detect* a change of regime online without access to a pre-labelled regime variable; compare fixed and adaptive models at equal feedback and computational budgets, include separate observations and explicit permission constraints, and report delay, false alarms, predictive loss, and preserved provenance.
