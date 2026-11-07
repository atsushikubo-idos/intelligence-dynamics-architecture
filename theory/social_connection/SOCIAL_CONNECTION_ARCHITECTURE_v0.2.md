# IDOS Social Connection Architecture v0.2 — Theory Integration and Selective Audit

**Positioning:** This is an architecture audit of an experimental social-connection integration. It does **not** replace MASTER_MAP v1.1, the 12CDP framework, or the 13 equations.

**Implementation:** [`implementation/social_connection_architecture/`](../../implementation/social_connection_architecture/)

**Research status:** Emergence in real social systems, self-updating capabilities, and meaningful CFV/MU have **not** been empirically demonstrated. MASTER_MAP v1.1 remains unchanged.

**Date:** November 7, 2026.

## 1. Integration principle

The central objective is to build a **social-connection architecture** in which heterogeneous intelligences interact while preserving their distinct reference frames, boundaries, and decision rights. Their interactions may give rise to relational distributions and new reference-frame possibilities, potentially supporting the self-renewal of what can be explored.

The integration does **not** indiscriminately combine all prior experiments. It selects capabilities needed by the shared social-connection protocol, preserves the original v0.1 implementation, and adds the v0.2 extension. The established definitions in MASTER_MAP v1.1, 12CDP, and the 13 equations are not revised.

## 2. Research findings selectively integrated

| Prior work | Finding retained | Concrete implementation in v0.2 | Qualification |
|---|---|---|---|
| Minimal Pilot v0.1–v0.2 | Minimal representation and equivalence depend on the observation frame | `capture_frame` / `check_equivalence` | Does not automatically compute optimal distributional compression |
| Minimal Pilot v0.3–v0.4 | Preserve provenance and original observations; reopen differences under past frames | `audit_observations` / `reopen_frame` | Cannot reconstruct variables that were never provided in the past |
| Minimal Pilot v0.5–v0.6 | Connect records from heterogeneous actors through a shared interface | Inherited `Actor` / `Evidence` / `snapshot` | Does not establish equivalence of actors' native meanings |
| Minimal Pilot v0.7–v1.0 | Distinguish candidate relational representations from their evaluation and adoption | Evaluation history added to `explore` / `evaluate_candidate` | Autonomous symbol emergence and invention of new operators are not integrated |
| Minimal Pilot v1.1–v1.2 | Distribution over methods differs from actors' adoption choices; relational and hypothesis distributions also differ | Separate `record_relational_state` and `hypothesis_weights`; `present_options` | Current relational distribution is a narrow empirical proxy based on recorded choices |
| Minimal Pilot v1.3 | CFV and MU are distinct capabilities | Retained and tested v0.1 `cfv_review` / `update_actor` | Checking a shared value is not proof of truth or meaningful understanding |
| Minimal Pilot v1.4 | Observation frames may originate externally; presentation may steer decisions | `ExternalOffer` / `present_options` | Behavioral influence of presentation is recorded as a risk, not measured |
| Inverse Audit v0.1–v0.2 | Do not collapse inverse inference into a single answer | Inherited `hypothesis_weights`; keep distinct distributions separate | Weights use illustrative likelihoods, not calibrated inference |
| Inverse Audit v0.3 | Residuals can motivate verification questions | `formulate_question`; permission-gated external evidence | Question structure remains human-designed |
| Minimum-Structure Audit v0.1–v0.2 | Do not assume an explicit relational variable is always necessary | No mandatory relational entity imposed on all actor states | Necessity of an independent relational process remains unproven |
| MASTER_MAP v1.1 and 13 equations | Future updateability, provenance, reality contact, and nonidentity | Retained v0.1 12CDP-shaped snapshots plus explicit histories and limitations | No claim of complete or formally certified 12CDP compliance |

## 3. Deliberately excluded from the core

- **XOR/AND formula-search engines, PID, MCTS, and standalone active learners:** not established as indispensable to the social-connection architecture.
- **Speedup ratios measured on synthetic datasets:** comparable gains are available from standard aggregation and caching; they are not claimed as unique contributions of this integration.
- **Automatic optimization of a distribution over reference-frame generation methods:** preliminary components exist in earlier pilots, but calibration and the linkage to actor-specific meanings remain unverified. v0.2 retains a candidate set and auditable illustrative hypothesis weights instead.
- **Autonomous invention of unknown meanings or entirely new questions:** previous code relies on pre-existing rules or externally supplied information.
- **Claims that CFV and MU are necessary and sufficient for new frame generation:** there is insufficient evidence.

## 4. Important boundaries and failure behavior

1. Private observations are excluded from shared computation, externally visible snapshots, and archival reopening. **This prototype is not a production-grade authorization or privacy-security system.**
2. If attributed shared observations with the same label conflict, the system neither silently overwrites nor averages them; it excludes that variable from the relevant shared derivation.
3. If a compressed representation from an earlier frame is insufficient for a new question, equivalence fails explicitly and the system may revisit authorized historical records.
4. A variable first observed at a later time must never be backfilled as if it had been measured earlier.
5. Externally offered observations are incorporated only when the provider allows sharing and all required participating actors approve.
6. Presenting a distribution never forces adoption. Presentation style and its potential steering effects are logged.
7. Candidate evaluations are stored by observation time; new evaluations do not overwrite the historical record.
8. Constructing an inquiry from residuals must not be misrepresented as invention of an entirely new concept.

## 5. Current integration status

**Implemented within one code path:** recording heterogeneous actor observations and permissions; preserving differences; presenting options without enforced choices; checking attributed statements; maintaining multiple explanatory candidates; reopening archived frames; obtaining authorized external evidence; and retaining time-indexed histories.

**Not demonstrated:** emergence of relational distributions in actual societies or intelligence interactions; autonomous self-renewal of reference-frame and exploration spaces; calibrated distributions over generation methods; real Human–AI–Organization field validation; CFV under extreme capability asymmetry; meaningful two-way MU; or a unique advantage over strong established methods.

**Next engineering priority:** Rather than adding another isolated predictive or search algorithm, define interfaces for independently operating actors, authorization boundaries, event contracts, and observable CFV/MU tests in a real social setting.

## 6. Relationship to the existing IDOS architecture

MASTER_MAP v1.1 remains the frozen architectural baseline. The 12CDP vocabulary provides a descriptive interface for realities, differences, representations, residuals, trajectories, updates, enactment, and reopening. The 13 equations remain mathematical tools rather than a claim of a complete universal dynamical theory.

**IDOS does not prescribe a single optimal choice to every actor.** It provides possible reference frames, evidence, unresolved differences, and provenance; each actor retains the right to adopt, defer, or reject within its legitimate authority.

This document describes an **experimental interface integration**, not proof of general emergence or autonomous social self-renewal.
