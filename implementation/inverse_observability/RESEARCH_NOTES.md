# IDOS Inverse Observability — End-to-End Synthetic Pilot: Research Notes

**Study date:** 2026-11-05  
**Scope:** Existing IDOS source ZIP provided in the conversation and previously developed v0.6, v0.7, and v0.8 research prototypes.

## Executive finding

An internally consistent, same-evidence-source pipeline ran on **360 synthetic business-process cases**. This demonstrates that candidate fitting, observation selection, and fixed-family adequacy checking can be chained together under specified assumptions. It does **not** establish 12PDM-specific empirical capability, causal-structure discovery, the creation of new latent variables, or effectiveness in real organizations.

### Supported and unsupported claims

**Supported for this pilot:** Using a pre-specified feature and model space, separate training/calibration/test periods chronologically; (i) select a predictive model on calibration data, (ii) estimate observation-ranking parameters from training data, and (iii) test a fixed residual-model family on held-out cases.

**Not supported:** Discovery of new physical or organizational internal structures; causal analysis of a real firm; direct quantitative measurement of all 12PDM descriptions; automatic reference-frame construction; operational performance gains; or generalization to real organizational records.

## Synthetic data and protocol

- The generator is `synthesize(360, seed=71)` from the bundled v0.6 `eventlog_validation.py` module.
- `make_cases()` reconstructs the event-level cases. Features are restricted to information available **by the first `REVIEW` event**; the target is elapsed time from that review until case completion.
- Cases are ordered by start timestamp and split into **216 training / 72 calibration / 72 final test** cases.
- Baseline predictor: pre-review elapsed time. Candidate ridge-regression models each add one feature: handoff, rework, or work-in-progress. Standardization is fitted on training data; candidate selection uses calibration MAE alone, not test outcomes.
- For v0.7, approximate Gaussian likelihood means and variances are **estimated from training data**. Here the competing outcome classes are **short vs long post-review duration**, not the causal hypotheses “handoff problem,” “workload problem,” and “missing-document problem.” Modeling a binary observation with Gaussian likelihood is a coarse approximation.
- For v0.8, a residual standard deviation is estimated on calibration data. The final residual vector is checked against a **pre-specified two-component family** with means 0 or +2 standard deviations. The test relies on strong assumptions of independent, identically distributed Gaussian residuals and a shared mean shift across the batch; those assumptions remain untested for real logs.
- Stress condition: add **72 hours to the completion events of held-out cases only**. This is an artificial data perturbation, not a naturally occurring latent change.

## Results

Details are stored in `results.json`.

| Condition | Selected model | v0.7 selected field | Held-out reduction in log-duration MAE | v0.8 result |
|---|---|---|---:|---|
| Normal synthetic observations | `handoff` | `handoff_at_review` | 39.09% | `compatible_not_proven` (p = 0.633333) |
| Completion shifted by +72 h in test only | `handoff` | `handoff_at_review` | 1.42% | `family_rejected` (p = 0.000333) |

MAE means mean absolute error on **log-transformed completion time**. A 39% reduction is **not** a 39% reduction in real processing time.

## Compatibility with IDOS

- Frozen `MASTER_MAP v1.1` and `Reference v1.1` remain unchanged.
- 12PDM is a protocol for observation and description, not a one-to-one correspondence with numerical regression features.
- Predictive residual ≠ the IDOS `Residual`; observed waiting time ≠ `Holding`; predictive improvement ≠ `Future Updateability`.
- Observations are tagged with context `case_review_v1`. A transition to `review_v2` requires explicit measurement compatibility/bridging; no autonomous frame change is implemented.
- An observation recommendation is only a **proposal**. In this pilot, the suggested variable is **already recorded**, so the pilot does not demonstrate a new observational capability.
- Keep the adapter separate from Discovery Architecture, which already implements concept-level candidate generation and intervention proposals.

## Next evidence gates

1. Obtain real process-event records with appropriate access authorization and provenance, and check event IDs, timestamps, observation availability, and reference-frame comparability.
2. Use a leakage-safe (including outcome-maturity-aware/purged where appropriate) chronological split.
3. Use Bernoulli likelihood for binary variables; test predicted information gain against actual improvement (for example, in Brier score). Do **not** call an experiment successful unless an initially absent observation was collected and evaluated.
4. Test v0.8's independence/normality assumptions; consider blocked or time-aware resampling if temporal dependence is present.
5. Add optional evidence-linked 12PDM annotations and examine agreement across observers.
6. Compare against standard regression, process mining, and active-learning/experiment-design baselines on the same split.
7. Do not label model inadequacy as discovery: require new candidate generation, new primary evidence, and independent corroboration.

## Reproduce

From `inverse_observability/`:

```bash
python -m pip install -r requirements.txt
python pipeline.py
python -m unittest -v
```

The dependency copies under `dependencies/v0_6/`, `dependencies/v0_7/`, and `dependencies/v0_8/` are bundled for reproducibility. They do not alter the historical versions.
