# AUDIT_REPRODUCTION_STATUS_v0.1 — Correction notice for the recorded “34 passed / 0 failed” audit result

```
REPRODUCTION_STATUS: NOT_REPRODUCED
Subject record:      validation/architecture_tests/ARCHITECTURE_INVARIANT_AUDIT_v0.1.md  (unchanged; see §6)
Checked on:          2026-10-18, fresh clone, main @ 672bbf6
Re-checked:          2026-10-18 after `git fetch --all --prune`: no new refs; origin/main still 672bbf6; no test_idos* file in any ref
```

## 1. What this notice is

`ARCHITECTURE_INVARIANT_AUDIT_v0.1.md` (added in commit `be73f4e`, 2026-10-07) reports the result
**“34 passed / 0 xfailed / 0 failed”** for a suite named `test_idos_invariants.py` run against
`src/idos_reference_v1_1.py`.

That figure is **preserved here as the value reported at the time**. It is **not deleted or edited**.
This notice only states what can and cannot be verified from the repository today.

**Readers should treat the 34/34 figure as an unverified historical report, not as evidence.**

## 2. Reproduction status

The original suite **cannot be re-run from the current repository**, because it is not in the repository.

| Check | Result |
|---|---|
| `test_idos_invariants.py` in the working tree of `main` | not found |
| Any file named `test_idos*` ever added, in any ref (`git log --all --diff-filter=A`; refs: local `main`; `origin/main`, `origin/backup-before-reorganization-20261012`, `origin/fix-markdown-math-display-20261012`, `origin/reorganize-repository-20261012`; tag `v1.0.0`) | not found |
| Any other repository file containing the string `test_idos_invariants` | only the audit record itself |
| History of `src/idos_reference_v1_1.py` | one commit (`a625495`, 2026-10-07); not modified afterwards |

Also unexplained: the record lists **25** initial checks (its §3) but reports **34** results; how the 34 relate to
the 25 cannot be determined from the repository.

## 3. Statements in the record that the committed code does not satisfy

Verified by executing the committed `src/idos_reference_v1_1.py`
(see `tests/test_phase2_regression.py`, results in `tests/results/original.txt`: `FutureUpdateabilityConsistency.test_increased_without_recontact_route_is_rejected`, `EvidenceChecks.test_unknown_evidence_id_is_rejected`, `CycleEventOrder.*`, and the expected failure `OpenSpecDecisions.test_SPEC_X2_*`; each fails or is an expected failure on the committed code).

| Statement in the record | Observed in committed code |
|---|---|
| §6: `FU=INCREASED` with no recontact route is rejected (“the implementation was tightened”) | accepted without error |
| §7: comparative FU statuses require a comparison basis | no such field exists on `FutureUpdateabilityAssessment` |
| §5: reopening evidence must be traceable; non-traceable ids rejected | arbitrary ids accepted |
| §4: reopening without recontact does not complete the Minimum IDOS cycle | demo flag `minimum_idos_cycle_complete` is `bool(reopening_history)`, true with zero recontact events |

## 4. The Phase 2 tests are a different suite

`tests/test_phase2_regression.py` (**37 tests**, written 2026-10-18) and the later
`tests/test_integrity_fix.py` are **new tests**. They are **not** a reconstruction, replacement or
re-run of the 34-test suite. Their counts must not be added to, compared with, or substituted for the
reported 34. They test selected behaviours of the reference code and make no claim about what the original suite covered.

## 5. What this notice does and does not show

- It does **not** show that the suite never existed, or that the 34/34 result was false. The suite and a
  tightened implementation may exist uncommitted or elsewhere.
- It does **not** assess whether the architectural claims of IDOS are true; the audit record itself says 34/34 is not empirical validation.
- It shows that the reported result **cannot be independently verified from this repository**, and that the
  committed code differs from the code the record describes (§3).

## 6. Integrity of the original record

`ARCHITECTURE_INVARIANT_AUDIT_v0.1.md` is left **byte-for-byte unchanged** by this correction. The notice is
placed in this separate file and linked from `README.md` and `DOCUMENT_INDEX.md`. A banner inside the original
file would be more visible but would alter a preserved record; that choice is left to the maintainer.

## 7. How to close this

1. Commit the suite and the implementation version that produced 34/34, and state the commit hash; **or**
2. amend the audit record (preferably as a dated addendum) to say the result is unreproduced; **or**
3. rebuild the suite and report it as a new, separately named result.

Until one of these is done, the status above stands.
