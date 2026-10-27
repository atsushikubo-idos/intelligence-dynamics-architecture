# IDOS Reference Transition — integration candidate v0.6

## Objective
An architecture for proposing, validating, adopting, and revisiting evaluation reference frames while preserving prior distinctions and unresolved differences. This is not an anomaly detector.

## Scope
These modules extend the existing `implementation/discovery_architecture/` code and require the repository's `src/idos_reference_v1_2.py`, `idos_bridge.py`, `discovery_architecture.py`, and `generation_conditions.py`. Do not replace existing files without reviewing changes.

## End-to-end integration
`test_full_transition_cycle.py` exercises actual IDOS objects: intervention and difference, frame genesis, transition review, authorized registry adoption, ledger recording, dual-frame reassessment, independent recontact, and an explicitly authorized next-observation condition revision. The active agent frame is deliberately not switched.

## Run
From `implementation/discovery_architecture/`:

```bash
PYTHONPATH=../../src:. python -m unittest discover -p 'test_*.py' -q
```

Observed locally: 83 tests passing, including inherited tests re-run in the integration subclass (not 83 unique scenarios).

## Evidence limitations
Synthetic, caller-supplied observations; provenance references and authorization IDs are not externally authenticated. The fixed-frame comparator only demonstrates category coverage by construction. This does not prove autonomous discovery, safety, or superiority in real-world environments. Ledger hash linkage detects simple edits but does not provide tamper-proof storage or atomic persistence with in-memory frame adoption.

## Next release gate
Run real event traces and a non-trivial baseline under the same evidence; independently audit blind spots, losses, authorization, and recovery after interrupted adoption.
