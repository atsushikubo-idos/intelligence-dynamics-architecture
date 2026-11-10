# IDOS Cross-Scale Audit v1.5 — Observational Equivalence and Permitted Diagnostics

**Status:** synthetic, reproducible methodological audit; **not** an established law of social interaction and **not** proof of IDOS-specific predictive superiority.

## Research question

Can a system detect that a previously useful connection-maintenance rule has changed, refrain from attributing an observationally indistinguishable cause, and specify a permitted diagnostic observation that can distinguish competing mechanisms?

## Model and proof of passive non-identifiability

At times `t<200`, all mechanisms emit independent Bernoulli observations with `p=0.80`. From `t>=200`, both hypothetical causes `A` and `B` emit **exactly the same** passive Bernoulli observation law with `p=0.45`. For every possible passive observation sequence `y`,

`P(y | A) = P(y | B)`.

Consequently the total-variation distance between their passive observational distributions is **zero**, and their passive log-likelihood ratio is **zero for every sequence**. No classifier relying exclusively on this observation channel can distinguish A versus B better than the prior-optimal guess, regardless of the amount of passive data. The principled passive output in this audit is `undetermined`.

This is an identifiability counterexample, not a statement that real world causes can never be distinguished.

## Change detection (separate question)

Two baseline detectors use *only* the passive channel: (1) a Page-style one-sided likelihood-ratio CUSUM using specified, known pre/post rates (oracle-informed baseline), (2) a rolling average crossing a fixed heuristic threshold. Both can detect a distribution change, but neither can identify A versus B. Thresholds were adjusted during exploratory development on the same synthetic simulator; the resulting error rates are **descriptive, not independently calibrated estimates**.

## Permitted diagnostic observations

Starting at t=240, a fixed, scheduled diagnostic probe is hypothetically available every three steps. Outcomes follow Bernoulli(0.80) if cause A, and Bernoulli(0.15) if cause B; the schedule is not outcome-selected. Sequential log Bayes factors choose A or B after posterior probability crosses 0.95 under equal priors and the **assumption that the cause is either A or B**. If permission is absent, diagnostic observations are unavailable, or evidence remains insufficient, the operational wrapper outputs `undetermined` and records the reason. No automated real-world intervention is performed.

The diagnostic response model is intentionally supplied by the experimenter; the system did **not** discover the probe type or its causal effects from raw data. The 0.95 nominal posterior is conditional on model correctness and is not a frequentist guarantee, especially with optional stopping and model misspecification.

## Reproduction

From this directory:

```bash
python identifiability_probe_audit_v15.py > results_v15.json
python -m unittest -v test_identifiability_probe_audit_v15.py
```

Python standard library only. The deterministic seed and full parameters are in `results_v15.json`.

## Results (200 independently generated sequences per condition)

See `results_v15.json` for all statistics. A and B produce exactly equal passive likelihood for every observation, but both exhibit a detectable change relative to the no-shift baseline. With synthetic diagnostic probes, conditional mechanism attribution is usually correct. The 'none' condition has no A-vs-B ground truth; probe attribution alone is invalid there, underscoring the need for a reliable change gate and a null hypothesis. Detection metrics include prechange alarms and require separate accounting.

## Scientific interpretation and IDOS boundaries

- **Reference frame / observability:** distinguish what a measurement channel can identify from what it cannot.
- **Provenance:** preserve whether a conclusion came from passive observations or a permitted diagnostic probe.
- **Autonomy / refusal:** if the probe cannot be carried out with required consent and authorization, output `undetermined`, not a forced causal claim.
- **Reality Contact:** revise conclusions with observation; record probe assumptions and error rates.
- **Future Updateability:** distinguish detecting a change, identifying its cause, and choosing a new representation; only the first two are partly covered in this toy model.

There is no validated quantitative map from a quantum-chemical environmental bath or energy dissipation to social intervention or consent. There is no experimental claim of causality in people, AI systems, or organizations. The result is consistent with standard statistical identification, active experiment design, and sequential testing.

## Next steps

1. Independently calibrate false alarms and test priors/sensor noise misspecification.
2. Compare active probe strategies at matched permission, cost, and information budgets.
3. Allow competing causes beyond A/B and demonstrate honest abstention under model mismatch.
4. Replace synthetic outcomes with consented, observable real-world interaction data and compare to existing active learning/change-detection baselines.
