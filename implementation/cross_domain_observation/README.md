# IDOS — Cross-Domain Trajectory Observation (Experimental v0.5)

## Research thesis / 研究の中心命題

**新しいのは、これまで重要だと知られていなかった要素を発見することではなく、重要だと分かっていながら十分に扱えなかった複雑な変化を、共通の構造のもとで継続的に捉えようとする点にある。**

The proposed contribution is not the discovery of previously unknown important factors. It is an attempt to continuously observe complex changes already recognized as important but difficult to handle adequately, within a shared structure **without erasing domain-specific differences**.

## What this demonstrates

- A shared **descriptive event schema** for three synthetic domains: M&A, hiring, and clinical trajectories.
- Recorded expectations, commitments, observations, unresolved questions, review dates, and explicitly recorded changes.
- A conservative software bridge to the existing `src/idos_reference_v1_1.py` (unchanged).
- A comparison with a lossless chronological event log; **no new information or superiority is claimed**.

## What this does NOT demonstrate

Scientific construct validity, causal inference, prediction, clinical efficacy, hiring fairness, better decisions, equivalent domain meanings, or measured Future Updateability. A ledger label `residual` or `holding` is **not** automatically a reference-architecture `Residual` or `HoldingState`. A recorded reference-frame change is mapped by convention, not verified as a real-world transformation.

All examples are synthetic. `restricted` items are excluded from ordinary reports, but this is **not a security or access-control system**. `consented` items may appear in output. Never place real personal, clinical, or client records in a public repository.

## Files

- `idos_ver84_application_v0_2.py` — existing event-ledger adapter, locally extended to allow the synthetic clinical domain.
- `synthetic_clinical_v0_5.py` — fictional clinical example.
- `idos_reference_bridge_v0_3.py` — bridge to the existing `src/idos_reference_v1_1.py`.
- `three_domain_experiment_v0_5.py` — three-domain demonstration and lossless-log baseline.
- `test_*.py` — automated tests.

## Run

Place this folder at `implementation/cross_domain_observation/` **inside the existing repository**. Keep the existing `src/idos_reference_v1_1.py` and `implementation/trajectory_observation/` as they are. From the new folder run:

```bash
python -m unittest discover -p 'test_*.py' -v
python three_domain_experiment_v0_5.py
```

The second command creates `three_domain_results_v0_5.json` in the working directory. This generated JSON is optional for publication; do not include real data. Python standard library only.

## Relationship to existing work

This is a **separate experimental extension**, not a replacement for `implementation/trajectory_observation/` or a revision to the frozen MASTER_MAP v1.1. The version label v0.5 refers to this experiment, not a new validated IDOS theory version. It reuses the current event-ledger adapter in a working copy without modifying the original GitHub folder.

## Status

Synthetic proof of software interoperability and structural coverage only. No independent evaluation or deployment. Further validation is deliberately left for future work.
