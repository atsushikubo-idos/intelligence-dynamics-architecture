# IDOS Reference v1.1 × Value Recognition (experimental adapter)

This experimental adapter connects the standalone `value_recognition.py` prototype to the canonical IDOS Reference v1.1 located at `../../src/idos_reference_v1_1.py`, without modifying the reference architecture.

The adapter records how previously observed events can be reassessed when reference frames and valuation criteria change. This is an experimental implementation, not a validated method for discovering unknown values.

## What is reused
- `UpdatingUnit`, `ReferenceFrame.revise()`, `UpdatingUnit.update()`, `UpdateLevel.L3`, and `ProvenanceEvent` from IDOS Reference v1.1.
- `Observation`, `ReferenceFrame` (application-level valuation criteria), `Evaluation`, and `Trajectory` from the standalone prototype.

## What is new
- Explicit links between IDOS frame IDs and application-level valuation-frame IDs.
- Trace events for preserving an observation, evaluating it, and reevaluating the *same observation* under a revised frame.
- Separation of an **unassessed value candidate** from IDOS `Residual` and `HoldingState`: lack of valuation data does **not** imply a detected mismatch or a Residual.

## Run
Place the uploaded reference file, renamed to `idos_reference_v1_1.py`, and the previous prototype's `value_recognition.py` on `PYTHONPATH`, alongside this directory, then run `python example.py`. A packaged copy of both dependencies is included for convenience.

## Limits
- Scores and features in the demonstration are hypothetical and depend on externally provided valuation criteria.
- Reevaluation is not discovery of intrinsic value, not causal inference, and not empirical validation.
- This extension does not by itself complete the Minimum IDOS cycle (Recontact and Reopen remain separate obligations).
- Frame IDs and application-level observations are traced but not persisted in a durable database.
