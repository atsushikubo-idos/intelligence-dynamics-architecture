# Enterprise Trajectory Management × IDOS Reference v1.1

This is an **experimental, conservative bridge** from the IDOS ver.83 enterprise event ledger to the existing `src/idos_reference_v1_1.py` classes. It does **not** change the canonical IDOS reference source.

## What is mapped

- Enterprise observations → `RealityContact` and trajectory provenance.
- Explicit enterprise `Difference` → `Difference`, **not** automatically `Residual`.
- Explicit enterprise `Residual` → `Residual` with a source trace; source classification is preserved, not independently verified.
- Enterprise `Holding` → `UpdatingUnit.hold()` only for an explicitly classified residual.
- Linear reference-frame revision → `ReferenceFrame.revise()` and `UpdatingUnit.update(L3)`.
- Relation revisions and governance actions → provenance events, **not** automatic Coupling, Agency or causal claims.
- Candidate future trajectories → possibility-space action descriptions; not forecasts.
- Explicit second-order recontact/reopening → optional `complete_reopening_after_recontact()` requiring a caller-supplied `FutureUpdateabilityAssessment` and `ReopeningAction`.

## Deliberately not claimed

- A textual `Reopening` event does not complete the minimum IDOS recontact/reopen loop.
- A governance `pause` does not itself imply a core `ReopeningAction`.
- Relational revisions are **not** equivalent to a verified coupling process.
- The enterprise ledger and core ontology are **not** semantically identical.
- No empirical validation, predictive performance, or improvement over baseline event logging is established.
- Only a linear chain of enterprise reference-frame revisions is supported; branches are rejected rather than silently flattened.

## Run

From the repository root:

```bash
python -m unittest discover -s implementation/enterprise_trajectory_management -p 'test_*.py' -v
```

No external dependencies. Python 3.10+.

## Source alignment

Reviewed against the repository archive's `src/idos_reference_v1_1.py` and the existing enterprise v0.1 prototype. This is a **software compatibility and conceptual consistency check**, not an independent scientific validation.
