# IDOS Cross-Scale Frame-Change Detection Audit v1.4

**Status:** Reproducible synthetic benchmark, **not** empirical evidence of social or physical laws or IDOS-specific predictive superiority.

## Question

Can a predictor trained on three actors' anonymized event histories detect deterioration and, from its observable residual signatures, identify which kind of reference-frame or relation change might have occurred? Can a prediction model fitted to recently labeled observations recover accuracy after a change?

## Scientific lineage and boundary

The original physical-chemistry study (v0.4–v0.8) considered H₂ electron structure, nuclear motion, and energy exchange with an explicit oscillator environment. These calculations motivate a *methodological* separation between feasibility, realized process, and persistence. They **do not** imply an energy law for social ties. This audit studies a wholly synthetic social connection process based on `multiframe_relation_audit_v13.py`; it is **not** a new molecular simulation and does not inherit molecular validation.

## Experiment

- Independently generate training (4,200 cases), normal-only validation (2,000), and each of four evaluation regimes (2,400) using fixed random seeds.
- Find A→B and B→C event-order features on **training data only**, using the v1.3 feature-discovery procedure. Fit a standard logistic regression using current permission/context state and the learned relation indicators.
- Use a holdout set of **20 non-overlapping blocks of 100** observations to calibrate an empirical 99th-percentile mean squared probability error (Brier loss) threshold. This is **not** an analytically calibrated false-alarm level. Do not infer an overall false alarm rate from the four runs.
- Synthetic changes: (i) no change; (ii) exchange A's reporting symbols `1↔5` only after labels have been generated; (iii) change success probabilities for cases that depend on transferred capacity after C exits, from .94 to .48; (iv) change eligible baseline success from .94 to .69. Unchanged cases retain background success .03.
- Evaluate early blocks, residuals conditional on third-party exit/stay, and A's observed symbol distribution. **None** of these signatures proves why a change occurred; observationally equivalent causes may exist.
- Train a fresh logistic model using only the **first 300 labeled post-change cases**, and compare both fixed and refit models on the same **remaining 2,100 future cases**. Refit may perform better or worse; this is a supervised adaptation benchmark, not autonomous change-point-directed updating.

## Results (fixed seeds)

| Regime | Brier on 2,400 | First alert after observations | Alerts / 24 windows | Fixed Brier on future 2,100 | Refit Brier on same future |
|---|---:|---:|---:|---:|---:|
| None | 0.040293 | No alert | 0 | 0.042264 | 0.043174 |
| Observer A changed | 0.146401 | 100 | 24 | 0.147485 | 0.072585 |
| Relation mechanism changed | 0.119882 | 100 | 22 | 0.120099 | 0.083672 |
| Environment changed | 0.153784 | 100 | 24 | 0.151199 | 0.133007 |

One comparison run per regime. The empirical threshold was 0.0899169905; it is sample- and seed-dependent.

## Findings and limitations

1. Prediction-loss alarms can signal distribution changes even when current connection status looks similar. But changed loss **does not identify causes**.
2. Residuals stratified by third-party exit and permitted cases can produce distinguishable *hypotheses*: the relation mechanism shift primarily affected the exit stratum, whereas environment shift affected both. Observation relabeling also affects the estimated relation features; this should be checked using independent evidence of actor-level reporting changes.
3. All regime changes were **predefined by the experimenter**. The code does not infer regime labels, discover new observation variables, or prove robust real-world change attribution. It does not establish the theoretical identifiability of the three regime classes.
4. The standard logistic model is the actual learner; no proprietary or IDOS-only algorithm beats a matched baseline. An adaptive baseline receiving the same post-change labeled data should have comparable opportunity to recover.
5. Actor permission, revocation, unresolved differences, provenance, and CFV/MU remain governance/observation requirements outside the probability-estimation module; prediction alone cannot establish consent or grant authorization.
6. Environmental and relational interventions are intentionally synthetic, and the labels in every condition come from known simulator rules; **there is no real-world or causal validation**.

## Reproduction

Requires Python 3, NumPy, scikit-learn, and the prior v1.3 file `multiframe_relation_audit_v13.py` in the same directory.

```bash
python frame_change_audit_v14.py > results_v14.json
python -m unittest -q test_frame_change_audit_v14.py
```

The ZIP contains *only four new files*: this note, the v1.4 Python code, JSON report, and tests. The prior v1.3 module is **not** duplicated in the ZIP. Repository root remains unchanged.

## Next falsification experiment

Evaluate many independent seeds, including no-change series; report detection probability, detection delay, and false alarm rate with uncertainty intervals. Include *observationally equivalent* actor, relation, and environment interventions to test the fundamental limits of cause attribution. Hold out entire generative mechanisms, not just individual synthetic episodes. Benchmark matched standard CUSUM/Page–Hinkley/ADWIN detectors and rolling-refit models under identical information and compute budgets. Only after these checks should an operational reference-frame manager be proposed.
