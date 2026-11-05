# IDOS Inverse Observability — Integrated Research Pilot

**Status:** Experimental numerical diagnostic adapter; **not** a validated discovery engine.

This package consolidates the end-to-end pilot and its required v0.6 / v0.7 / v0.8 source dependencies, plus an integrated audit. The original IDOS architecture and its frozen MASTER_MAP v1.1 remain unchanged.

## Scope

- Synthetic business-event logs only (360 simulated cases).
- Chronological train/calibration/test split.
- Candidate feature and predictive-model selection.
- Data-fitted next-observation ranking (for observed outcomes, **not causal hypotheses**).
- Open-set adequacy check under restrictive independent Gaussian residual assumptions.
- No new sensor acquisition, autonomous frame change, latent causal mechanism discovery, or validated 12PDM-specific effectiveness.

## Reproduce

From this directory, with Python 3.10+:

```bash
python -m pip install -r requirements.txt
python pipeline.py
python -m unittest -v
```

Running `pipeline.py` regenerates `results.json` in the current folder. For detailed Japanese instructions and methodological limitations, see [README_JA.md](README_JA.md); for the audit, see [INTEGRATION_AUDIT_JA.md](INTEGRATION_AUDIT_JA.md).

## Upload to GitHub

Place the enclosed **`inverse_observability/`** directory under `implementation/` in the existing `intelligence-dynamics-architecture` repository. Do not upload the ZIP itself as a code file.

Suggested commit: `Add inverse observability integrated research pilot and audit`
