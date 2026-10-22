# IDOS ver.83 — Enterprise Trajectory Reference v0.1

An **experimental, descriptive** Python reference for the enterprise trajectory management diagram. This is an *application-layer prototype*, not a replacement for `src/idos_reference_v1_1.py` and not a complete implementation of the diagram.

## Represented elements

- 12 process labels, preserving the diagram's order (descriptive event classification, not a fully executable 12-stage process engine)
- Observations and evidence provenance
- Explicit Difference / Residual distinction and Holding
- Reference-frame revisions, with predecessor links
- Changes in relations among agents, organizations and systems
- Alternative future trajectories as **candidates**, not forecasts
- Human governance decisions including pause and reopen

The broader 4-part architecture (Dynamics, Observability, Relational Dynamics, Second-Order Updateability) is reflected selectively, not formally verified. Trajectory curvature, stagnation, branching, lock-in, future updateability scores and causal coupling are **not computed**.

## Run

```bash
cd implementation/enterprise_trajectory_management
python enterprise_trajectory_reference_v0_1.py
python -m unittest -v test_enterprise_trajectory_reference_v0_1.py
```

No third-party dependencies. All demonstration content is synthetic. No automated enterprise advice, prediction, or scientifically validated measurement is provided. Do not publish private enterprise data without access controls and consent.

## Relationship to existing IDOS reference

`../../src/idos_reference_v1_1.py` is the primary theoretical reference implementation. This module intentionally stands alone to avoid modifying that source. Future work could build a carefully tested adapter mapping events to the core `UpdatingUnit`, `RealityContact`, `ReferenceFrame`, and `ReopeningDecision` objects without silently reclassifying differences as residuals.
