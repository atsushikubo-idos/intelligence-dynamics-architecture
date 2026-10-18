# INTEGRITY_FIX_NOTES_v0.1 — Minimal research-integrity fix to the v1.1 reference code

Status: proposal on branch `integrity/minimal-research-fix`. Not merged. Not pushed.
**Unchanged by this fix:** `architecture/MASTER_MAP_v1.1.md`, `theory/DYNAMICS_MODEL.md`, the frozen
`src/idos_reference_v1_1.py`, and `validation/architecture_tests/ARCHITECTURE_INVARIANT_AUDIT_v0.1.md`
(byte-identical to `main`).

## 1. Scope

Two goals only.

1. Make the reproduction status of the recorded “34 passed / 0 failed” audit result unmistakable →
   [AUDIT_REPRODUCTION_STATUS_v0.1.md](AUDIT_REPRODUCTION_STATUS_v0.1.md), linked from `README.md` and `DOCUMENT_INDEX.md`.
2. Stop the reference code from presenting unverified judgments as determinate results →
   `src/idos_reference_v1_1_research_safe.py` (a derived copy; the frozen file is not edited).

| File | Role |
|---|---|
| `src/idos_reference_v1_1_research_safe.py` | recommended variant of the reference code |
| `src/idos_reference_v1_1_proposed.py` | Phase 2 artifact, kept for history; includes the withdrawn P4 rule; **do not use as the recommended variant** |
| `tests/test_integrity_fix.py` | tests for the three behaviours below (43 tests) |
| `tests/test_phase2_regression.py` | Phase 2 tests, **unedited** (37 tests) |
| `tests/results/integrity/` | saved results, per-test outcomes, generated `SUMMARY.md`, code diffs |

Neither test file is a reconstruction of the original 34-test suite, which is not in the repository.

## 2. Behaviour of the research-safe variant

### A. Cross-unit comparison — `CommonDynamicsProtocol.compare(a, b, *, shared_measure=None)`

| Situation | Output |
|---|---|
| no non-blank `shared_measure` | `comparability="not_established"`; `residual_difference=None`; `measurement_version_difference=None` |
| `shared_measure` declared by caller | `comparability="declared_unverified"`; both differences returned; the declared measure is echoed. The code does **not** verify the declaration. |
| any case | `same_frame_name` is reported as a literal fact and is **never** used as evidence of comparability |

Not gated (literal comparisons, no subtraction): `same_phase`, `both_holding`, `future_updateability_equal`
(the last is marked `fu_comparison_basis: evaluator_judgment_labels_only`).

### B. Future Updateability — evaluator judgment vs. measurement

Basis: Measurement protocol v0.3 §5.6 (FU is a latent capacity, never an O/P/I/U score; `not_estimable` without a
perturbation/re-test; never invent a numeric score); Purpose and Use v0.2 §11 / Operational Protocol v0.2 §10 (status
labels ↑ → ↓ ? with six assessment questions and no aggregation rule).

- `FutureUpdateabilityAssessment` is an **evaluator judgment record**: derived fields `record_type="evaluator_judgment"`,
  `measurement_status`, `review_flags`. Callers cannot set them (`init=False`).
- `measurement_status` is `not_estimable` unless at least one non-blank id is given in the new input
  `claimed_perturbation_evidence_ids`, in which case it is `latent_not_validated`. The code never emits an estimated,
  validated, measured or numeric value, and does not verify the claim.
- **Phase 2 P4 (forced rejection of `FU=INCREASED` without a recontact route) is not adopted.** Presence or absence of a
  route does not alter, confirm or deny a status.
- CDP `describe()`/`translate()` expose `latest_fu_record_type` and `latest_fu_measurement_status`; reopening provenance
  now reads “evaluator FU judgment=… (measurement_status=…)”.
- `architecture_manifest()["non_equivalences"]` gains three entries (evaluator FU judgment ≠ measured FU; declared level ≠
  verified level; frame-name equality ≠ comparability).

### C. Update-level consistency — flags only

`check_update_level_consistency(level, frame_replaced=…, possibility_space_replaced=…)`, applied inside `update()`.
Basis: `DYNAMICS_MODEL.md` §8. Flags are stored in `UpdateEvent.level_flags` and as `level_mismatch` provenance events.
The update is still applied and the declared level is never changed.

| Declared | Recorded by `update()` | Flag |
|---|---|---|
| L1 or L2 | frame replaced | `definition_conflict` (magnitude not assessed — see SD-12) |
| L3 | no frame replaced | `definition_conflict` |
| L5 | no Possibility Space replaced | `definition_conflict` |
| not L5 | Possibility Space replaced | `convention_dependent` (documents do not say whether a multi-structure update is labelled by its deepest level) |
| L4 | — | never checked (traversal between existing frames is not distinguishable in this record) |
| any | Boundary or Measurement changed | never mapped to a level (not related to L1–L5 in `DYNAMICS_MODEL.md` §8) |

Update depth may be scale- and observer-dependent (`KNOWN_LIMITATIONS.md` §6); there is **no** automatic level assignment.

## 3. Phase 2 test expectations that differ on the research-safe variant

The Phase 2 test file was **not edited**: it records Phase 2 as executed. Running it against the research-safe variant
ends with exactly these deviations and no others (31 pass / 1 fail / 3 xfail / 2 unexpected_success):

| Phase 2 test | proposed | research_safe | Reason | Superseded by |
|---|---|---|---|---|
| `FutureUpdateabilityConsistency.test_increased_without_recontact_route_is_rejected` | pass | **fail** | P4 withdrawn: no MASTER_MAP v1.1 rule requires a route; protocol v0.3 §5.6 treats FU as latent, not scored | `FUJudgmentRecord.test_increased_without_route_is_accepted_not_rejected` |
| `OpenSpecDecisions.test_SPEC1_…` | xfail | unexpected_success | the variant now flags level/structure conflicts | `UpdateLevelConsistency.*` |
| `OpenSpecDecisions.test_SPEC3_…` | xfail | unexpected_success | comparison is gated on a declared shared measure | `FrameComparisonGate.*` |

`unexpected_success` here means a previously open decision is now partly addressed, **not** that it is settled.

## 4. Changes made while reviewing the first draft

- **Hardening:** `claimed_perturbation_evidence_ids=[""]`, `["  "]` or `[None]` previously moved `measurement_status` to
  `latent_not_validated`. Blank or non-string entries are now ignored (tests: `GapGuards.*`).
- **Added tests (`GapGuards`, 6):** derived FU fields cannot be injected (guarded against a vacuous pass); blank claims;
  `translate()` carries the FU nature; no numeric value in `compare()` output without a shared measure; L5 with a
  frame-only replacement is flagged.
- **Dangling references fixed:** this notes file (cited by the module docstring) did not exist; the correction notice
  cited `audit_repro.py`, which is not in the repository.
- `PHASE2_SPEC_DECISIONS_v0.1.md` annotated (P4 withdrawn; SD-1 and SD-8 partly addressed); nothing deleted.

## 5. Provenance of this change set

The first draft of `idos_reference_v1_1_research_safe.py`, `tests/test_integrity_fix.py`, `tests/summarize_results.py`,
the `README.md` / `DOCUMENT_INDEX.md` notices, a rewrite of `AUDIT_REPRODUCTION_STATUS_v0.1.md` and a first set of
saved results were found uncommitted in the working tree (file times 2026-10-18 18:03–18:06 JST, earlier than the message
requesting this fix). The author could not be established. Before adoption they were read in full, **every suite was
re-run** (outcomes identical test-by-test to the stored results), and the changes listed in §4 were made. The saved
results in `tests/results/integrity/` are from the re-run, not from the first draft.

## 6. New open decisions (continuing `PHASE2_SPEC_DECISIONS_v0.1.md`)

| ID | Decision needed |
|---|---|
| SD-12 | L1/L2 with a recorded frame replacement is labelled `definition_conflict`, but the definitions exclude only a *material* / *substantial* change, which the code cannot assess. The flag means “a replacement is recorded”, not “the change was material”. Alternative: a softer label for this case only. |
| SD-13 | `claimed_perturbation_evidence_ids` are not checked for traceability (perturbation records may live outside trajectory provenance). A non-blank string suffices for `latent_not_validated`. |
| SD-14 | `INCREASED` with no recontact route carries a **non-binding** `review_flags` note. This was not requested and encodes no rule; remove the flag generation if any route-based signalling is unwanted. |
| SD-15 | `shared_measure` is a free-text string, not tied to the two units, their frames or a coding rubric; `incomparable` cannot be asserted explicitly (only `not_established` is produced). |
| SD-16 | Literal cross-unit comparisons (`same_phase`, `both_holding`, `future_updateability_equal`) are still returned ungated. |

Carried over unchanged: SD-2, SD-3, SD-4, SD-5, SD-6 (route/FU consistency stays open), SD-7, SD-9, SD-10, SD-11.

## 7. What this does not establish

No test result here validates IDOS scientifically or shows the original 34-test result. The tests and the variant were
reviewed by the same agent that adopted them; independent review is recommended.
