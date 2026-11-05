# IDOS Inverse Observability — Integrated Research Pilot

**Status: Experimental numerical diagnostic adapter. Not a validated latent-structure discovery engine.**  
**Date:** 2026-11-05  
**Architecture compatibility:** The frozen IDOS `MASTER_MAP v1.1` and `Reference v1.1` are not modified.

## Purpose

This repository component investigates whether observational trajectories support (a) comparing pre-specified latent-structure hypotheses, (b) finding useful *already recorded* observations, and (c) detecting when a fixed model family is inadequate. It connects selected numerical experiments from v0.6 (event-log analysis), v0.7 (observation design), and v0.8 (model-family adequacy checking) into a single **synthetic-data pilot**.

It does **not** demonstrate recovery of previously unknown causal mechanisms, automatic generation of latent variables, autonomous reference-frame revision, or the unique validity of 12PDM.

## What the integrated pipeline actually does

1. Simulates 360 business-process cases with time-stamped review and completion events.
2. Constructs features available **at the first review**, without using subsequent outcomes as input features.
3. Splits cases chronologically: 216 for training, 72 for calibration/model selection, and 72 held out for evaluation.
4. Compares a baseline predictor with candidate ridge-regression models using one additional feature each; selects a model on the calibration set.
5. Fits approximate observation-likelihood parameters using training records, for a **short/long completion-time outcome**, not causal hypotheses.
6. Ranks *existing* observation fields by estimated information gain, subject to the pilot's design assumptions.
7. Checks held-out residuals against a restrictive, pre-specified Gaussian family and repeats the check after a **synthetic 72-hour delay** applied only to test-case completion events.

## Reproducible synthetic results

| Evaluation condition | Selected predictive feature | Selected observation | Reduction in log-duration MAE vs baseline | Adequacy check |
|---|---|---|---:|---|
| Unmodified synthetic cases | Handoff | `handoff_at_review` | 39.09% | Not rejected (Monte Carlo p = 0.633333) |
| Test-case completions delayed by 72 hours | Handoff | `handoff_at_review` | 1.42% | Model family rejected (Monte Carlo p = 0.000333) |

The percentage is a **relative reduction in predictive error on log-transformed duration**. It is **not** an improvement in real-world workflow speed, and the rejection does not identify the cause of model failure.

## Reproduce

Use Python 3.10+ from inside the `inverse_observability/` directory:

```bash
python -m pip install -r requirements.txt
python pipeline.py
python -m unittest -v
```

`pipeline.py` regenerates `results.json`. The package includes its required Python dependency modules under `dependencies/`; it does not require separate installation of earlier research artifacts. The integrated pilot originally passed 10 automated tests; rerun tests in your own environment before relying on it.

## Interpretation and IDOS boundaries

- **12PDM** is an observation/description protocol, **not** a mandatory sequence, twelve numerical indicators, or twelve sensors. Earlier notes may also use the name **12CDP**.
- Statistical regression residuals are **not identical** to the IDOS concept of `Residual`.
- Waiting time in an event log is **not automatically** an IDOS `Holding` state.
- Improved predictive fit is **not** evidence of maintained `Future Updateability`.
- A detected model mismatch may result from noise, misspecification, reference-frame drift, selection bias, or an omitted variable; it is **not** proof of a previously unknown structure.
- Observations are **proposals for investigation**, not authorized instructions to intervene in real organizations.
- The reference context is held at `case_review_v1`; comparing to `review_v2` would require a documented measurement bridge.
- Discovery Architecture remains responsible for concept-level proposal and reference-frame iteration. This module is an independent **numerical diagnostic adapter** rather than a replacement for Discovery Architecture.

## Remaining validation gates

Before making claims beyond this pilot: obtain appropriately licensed/authorized real process-event data; apply leakage-safe chronological validation; use likelihoods appropriate to each variable type; check temporal dependence and residual-distribution assumptions; compare against conventional regression, process mining, change-point detection, and active experiment design; link optional 12PDM descriptions to primary evidence; and evaluate the *realized* value of newly collected observations instead of selecting fields already present in a log.

## Documentation

- [Detailed research methodology and results](RESEARCH_NOTES.md)
- [Integrated v0.1–v0.8 audit](INTEGRATION_AUDIT.md)
- [Reproducible output](results.json)

For compatibility with an earlier GitHub upload, `README_JA.md` and `INTEGRATION_AUDIT_JA.md` are retained as English-language pointers. No Python algorithms or saved numeric outputs were changed in this documentation-only update.

**Suggested commit:** `Translate inverse observability documentation to English`
