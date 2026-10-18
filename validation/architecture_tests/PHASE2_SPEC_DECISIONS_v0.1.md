# PHASE2_SPEC_DECISIONS_v0.1 — Open specification decisions (未解決の仕様判断一覧)

Status: working record for review. **MASTER_MAP v1.1 is not modified by anything here.**
Scope: `src/idos_reference_v1_1.py` (frozen as committed) vs `src/idos_reference_v1_1_proposed.py` (proposed).
Tests: `tests/test_phase2_regression.py` (37 tests; results in `tests/results/`).

## Result summary (executed, same test file on both implementations)

| Implementation | pass | fail | error | xfail (open decision) | unexpected success |
|---|---:|---:|---:|---:|---:|
| `idos_reference_v1_1.py` (as committed) | 17 | 15 | 0 | 5 | 0 |
| `idos_reference_v1_1_proposed.py` | 32 | 0 | 0 | 5 | 0 |

Regressions (pass in original, not pass in proposed): **0**.
Caveat on the 15 failures in the original: 6 of them (`CycleEventOrder.*`) fail because the
method `cycle_event_order_satisfied()` does not exist there (API absence), not because of a
demonstrated behavioural bug; the behavioural issue itself (reopen with zero recontact sets the demo's
cycle flag to true) was shown separately by `audit_repro.py` case 2a.

Authorship caveat: the tests and the fixes were written by the same agent in the same session. They
encode one reading of the constraints and should be reviewed by someone who did not write them.

## What is implemented in the proposed file (and what it deliberately does NOT claim)

| # | Change | Does NOT establish |
|---|---|---|
| P1 | Holding stays active until every referenced residual is resolved; ids unknown to the unit are treated as still open; ignored ids are recorded in provenance | that "resolved" was correctly judged |
| P2 | `transition()` cannot leave DISSOLUTION; REEMERGENCE requires a predecessor | a complete allowed-transition matrix (SD-11) |
| P3 | `reopen()` rejects evidence ids absent from recorded provenance; provenance states "existence-checked only; semantic adequacy not assessed" | that evidence is relevant or sufficient (SD-5) |
| P4 | `FU=INCREASED` requires `reality_recontact_route_exists=True` | that this is a MASTER_MAP rule (it is an interpretation — SD-6) |
| P5 | `cycle_event_order_satisfied()` replaces the demo's `bool(reopening_history)`; demo key renamed; demo states theory assessment is not performed | that a Minimum IDOS cycle occurred in the theoretical sense (SD-2) |

## Open decisions

Each needs a human decision. Corresponding `xfail` tests exist where marked; an *unexpected success*
on them means the decision may have been resolved and the test should be revisited.

| ID | Decision needed | Why it is open (evidence) | Test |
|---|---|---|---|
| SD-1 | Declared update level (L1–L5) vs recorded structural change: reject, flag, or accept? | `DYNAMICS_MODEL.md` §8: L1 = no material change to operative frame, L3 = frame changes, L5 = space of frames/possibilities changes. `KNOWN_LIMITATIONS` §6: depth may be scale- and observer-dependent. Necessary-condition checks are implementable; automatic level assignment is not supported by any document. Observed: L1 with 4 replaced structures, and L5 with none, are both accepted. | `test_SPEC1_*` (xfail) |
| SD-2 | What counts as a completed Minimum IDOS cycle in code? | `IDOS_OPERATIONAL_PROTOCOL_v0.2` §14 requires six recorded items (Difference, Unresolved Residual, Updating Structure Change, Distribution Change, Reality Recontact, Next Updateability). Code only checks event order. Also open: whether the recontact must follow the *latest update* (chosen) or target the updated frame, or be cited in `evidence_ids`. | none (design) |
| SD-3 | Unregistered residuals: tolerate or reject? | `hold()` accepts any `Residual`, registered or not. Proposed behaviour is conservative (treated as open, recorded when ignored). Alternative: raise on unregistered ids in `hold()`/`resolve_residuals()`. | `HoldingResolution.*` (pass in proposed) |
| SD-4 | Representation of partial resolution | Chosen: keep one Holding active until all referenced residuals resolve. Alternatives: split the Holding, or shrink `residual_ids`. Also: `describe().active_holdings` counts holdings, not residuals. | `HoldingResolution.*` |
| SD-5 | Semantic validity of evidence | Existence is checked; relevance is not. Any provenance id passes (a unit's own initialisation event passes — documented by `test_existence_check_does_not_imply_semantic_validity`, which records a limitation, not an endorsement). Measurement protocol v0.3 §5.6 requires alternative explanations, and its §11 acceptance criteria require that disagreeing coders can preserve disagreements; code cannot judge either. Open: restrict evidence by event type or time order? | `EvidenceChecks.*` |
| SD-6 | Is the `FU=INCREASED` ⇒ recontact-route constraint valid? | **Not an explicit rule in MASTER_MAP v1.1** (§4.3.1 defines FU as second-order capacity to revise the update operator; no status values). Status values ↑ → ↓ ? and the six assessment questions (incl. "route back to Reality") are in Purpose and Use v0.2 §11 and Operational Protocol v0.2 §10, with **no aggregation rule**. Support for the constraint is interpretive: Q2 as worded in the code's `architecture_manifest()` ("update again without losing contact with Reality"; its wording in the canonical documents was not separately checked) and Protocol §14. **Tension with measurement v0.3 §5.6:** FU is a latent capacity, never an O/P/I/U score, `not_estimable` without renewed perturbation, "never invent a numeric score". The code's status enum is a protocol-level record; whether it may assert INCREASED/REDUCED in measurement contexts is undecided. Other possibly inconsistent combinations (e.g. INCREASED with `irreversible_dependency_increased=True`) are unconstrained. | `FutureUpdateabilityConsistency.*` |
| SD-7 | Comparative FU statuses need a comparison basis | The audit record (§7) says a basis field was added; the committed code has none. Adding it changes the dataclass signature and the demo. | `test_SPEC_X2_*` (xfail) |
| SD-8 | `compare()` across different Reference Frames | Subtracts raw residual counts and equates frames by name only, while `KNOWN_LIMITATIONS` §20 requires CDP to allow incommensurability. A comparability condition (shared declared measure) is undefined. | `test_SPEC3_*` (xfail) |
| SD-9 | `translate()` vs projection | Output is identical for any target except the echoed label; quality is a constant. Either implement loss accounting or rename to a projection. | `test_SPEC4_*` (xfail) |
| SD-10 | Holding review/expiry | `MASTER_MAP v1.1` §8.2 repositions Holding as a domain-specific mechanism, and `KNOWN_LIMITATIONS` §4 allows it to be narrowed or removed. Absence of expiry may be acceptable. | `test_SPEC6_*` (xfail) |
| SD-11 | Full phase-transition matrix | Only two guards were added. Other transitions (e.g. BIRTH→DISSOLUTION, ENACTMENT→BIRTH) are unconstrained and undefined in the documents read. | none |

## Not covered by this phase

- `MASTER_MAP_v1.1.md` and `DYNAMICS_MODEL.md` were read only at the passages cited above, not end to end.
- No empirical or scientific validation is implied by any test result.
