# AUDIT_REPRODUCTION_STATUS_v0.1 — Reproducibility status of `ARCHITECTURE_INVARIANT_AUDIT_v0.1`

Checked: 2026-10-18, against a fresh clone (HEAD `672bbf6`, branch `main`).

## Status: **再現未確認 (not reproduced)**

`ARCHITECTURE_INVARIANT_AUDIT_v0.1.md` records **"34 passed / 0 xfailed / 0 failed"** for the suite
`test_idos_invariants.py` against `src/idos_reference_v1_1.py`. This result could **not** be
reproduced, and it is not treated as passed here.

## What was checked

| Check | Result |
|---|---|
| `test_idos_invariants.py` present in the working tree of `main` | not found |
| Any file named `test_idos*` ever added, in any ref (`git log --all --diff-filter=A`; refs: local `main`; `origin/main`, `origin/backup-before-reorganization-20261012`, `origin/fix-markdown-math-display-20261012`, `origin/reorganize-repository-20261012`; tag `v1.0.0`) | not found |
| Any other file in the repository containing the string `test_idos_invariants` | only the audit record itself |
| History of `src/idos_reference_v1_1.py` | one commit (`a625495`, 2026-10-07); never modified afterwards |
| Executing the committed code against the audit record's claims | see below |

## Claims in the audit record that the committed code does not satisfy (verified by execution)

| Audit record statement | Observed in committed `idos_reference_v1_1.py` |
|---|---|
| §6: `FU=INCREASED` with no recontact route is rejected ("the implementation was tightened") | accepted without error |
| §7: comparative FU statuses require a comparison basis | `FutureUpdateabilityAssessment` has no such field |
| §5: reopening evidence must be traceable; non-traceable ids rejected | arbitrary ids accepted |
| §4: reopening without recontact does not complete the Minimum IDOS cycle | demo flag `minimum_idos_cycle_complete` is `bool(reopening_history)`, true with zero recontact events |

## What this does and does not show

- It does **not** show the suite never existed or that the 34/34 result was false. A tightened
  implementation and the suite may exist uncommitted, or on another machine.
- It shows that the stated result **cannot be independently verified from the repository**, and that
  the committed code differs from the code the record describes.

## How to close this

1. Commit the suite and the implementation version that produced 34/34 (state which commit/hash), **or**
2. amend the audit record to say the result is unreproduced and describe the committed code, **or**
3. rebuild the suite (`tests/test_phase2_regression.py` covers a subset only: 37 tests, not a
   reconstruction of the 34).
