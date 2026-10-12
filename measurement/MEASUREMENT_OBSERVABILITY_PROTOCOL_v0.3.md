# IDOS Measurement & Observability Protocol v0.3

**Status:** Proposed operational specification / NOT empirically validated  
**Date:** 2026-10-12  
**Architecture baseline:** `MASTER_MAP_v1.1` (FROZEN; unchanged)  
**Normative predecessor:** `MEASUREMENT_OBSERVABILITY_PROTOCOL_v0.2` (FROZEN; unchanged)  
**Evidence of prior work:** `MEASUREMENT_VALIDATION_RECORD_v0.2` and `MEASUREMENT_VALIDATION_RECORD_v0.2_INTEGRATED`  
**Scope:** Reproducible evidence-based description and attempted measurement; not a new theory or a claim of universal applicability.

> **Publication status (2026-10-12): DRAFT — proposed measurement specification; NOT empirically validated.**  
> **Scope:** Human, AI and organizational dynamics as potential measurement targets; cross-domain reliability and applicability not demonstrated.  
> **Architecture:** `MASTER_MAP_v1.1` remains frozen. This document does not introduce a new theory.  
> **Code:** No separate `IDOS_IMPLEMENTATION_SPEC_v0.1.md` is assumed or required.

## Quick overview / 概要

**日本語：** IDOSが対象とする「知性の動態」を、観測記録から第三者が追跡・判定できるようにするための暫定測定仕様。証拠を先に登録し、観測可能性（O/P/I/U）、主体と境界、参照系、12CDP、変化の軌跡を順に記述する。Residual・Holding・Updating Unitは未確立の操作的定義であり、Future Updateabilityは直接的な数値スコアにしない。

**English:** An evidence-first, provisional procedure to trace the dynamics of intelligence without presuming every IDOS construct is observable. It specifies minimum evidence records, observability decisions, unit/boundary and reference-system tracking, non-mandatory 12CDP tracing, and trajectory reporting. Operational definitions and comparative value remain unvalidated.

**What is completed:** A written v0.3 specification; author-created synthetic structural checks; a 16-item synthetic coder package; agreement-calculation software QA; and a field-pilot kit. Those are engineering preparation, **not** independent empirical validation.

**What remains untested:** Independent coder reliability on primary evidence; discriminant/construct validity of Residual and Holding; identification of distinct joint Updating Units; predictive or cross-domain validity; and added decision value against strong conventional methods. One prior SWE-bench single-trace feasibility analysis was closed without demonstrating incremental value.

**Release principle:** Publish this single document as a public DRAFT, without publishing pilot answer keys, participant data, or a claim of scientific validation.

---

## 0. Version boundary and audit

This is a proposed *implementation overlay* on v0.2. All six v0.2 rules and its ordered pipeline remain authoritative. This file does **not** change the frozen architecture, does not declare any latent construct validated, and does not turn the 12CDP coordinates into mandatory stages.

Already specified in v0.2: evidence-first pipeline, O/P/I/U, six epistemic constraints, candidate updating units and boundaries, observer/reference separation, non-sequential 12CDP, `T(U,B,Δt)`, re-observation, latent Future Updateability, and eight output categories. Already proposed (but not tested) in the integrated record: mismatch instrumentation, temporal treatment of unresolved difference, interaction-history ablation, measurement-system revisions, and multiple perturbations. Do **not** present these existing proposals as v0.3 discoveries.

New in this version: machine-readable minimal records; evidence linking and missingness semantics; operational coding rules and rejection gates; trace and continuity formats; coder agreement/adjudication; acceptance tests; comparison design.

**Source review and dependency boundary (2026-10-12):** The public repository contains `MASTER_MAP_v1.1.md`, `IDOS_OPERATIONAL_PROTOCOL_v0.2.md`, and `src/idos_reference_v1_1.py`. The repository root listing does not show an `IDOS_IMPLEMENTATION_SPEC_v0.1.md`; no such document is assumed to have been created. This specification is self-contained as a measurement *record and decision procedure*, but not a claim that existing Python code implements it. `IDOS_OPERATIONAL_PROTOCOL_v0.2.md` concerns broader operation and does not substitute for this measurement-specific schema. Future compatibility testing against `src/idos_reference_v1_1.py` is an implementation task, not a prerequisite document.

## 1. Definitions of record status

**Observability:** `O`=direct evidence covers the specified target claim; `P`=direct evidence covers only an explicit portion; `I`=only an evidence-linked but defeasible inference supports the claim; `U`=the available dataset does not allow the claim to be identified. These labels express *observability given a claim and evidence boundary*, not existence, truth, strength of causality, or statistical confidence. `O` does not mean a claim is true if its source is inaccurate.

**Separate finding:** `present_candidate`, `not_detected`, `contradicted`, `indeterminate`, `not_applicable`. A directly documented *absence* is not necessarily U; code the direct evidence and `not_detected`/`contradicted` as appropriate. **Do not map missing to negative.**

**Coding decision:** `assigned`, `deferred`, `disputed`, `not_applicable`. A deferred judgment has no forced O/P/I/U label if prerequisites for defining the claim are missing. If the claim is well-defined but its evidence is lacking, record `U` plus the reason. Distinguish `not_collected`, `not_available`, `redacted`, `not_recorded`, `out_of_window`, `not_applicable`, `unknown`.

**Evidence type:** `direct`, `proxy`, `inference` is a property of a *link between an item and a claim*, not an intrinsic property of an entire document. A transcript directly witnesses utterances but does not directly witness an internal mental state.

## 2. Minimal data package and constraints

A package is a set of UTF-8 tabular or JSON records; the canonical textual representation can be JSON Lines, one object per row, or equivalent relational tables. Each record has immutable `id`, `schema_version`, `created_at`, `source_id`, and optional `supersedes_id`. Records may be appended or superseded but never silently rewritten. All event times use ISO 8601 with timezone or explicitly documented unknown timezone; distinguish `event_time` from `recorded_at` and `coding_time`. Relative order may substitute for unavailable timestamps, labeled `sequence_only`.

**Package header — required:** `case_id`, `protocol_version`, `architecture_version`, `analysis_question`, `evidence_cutoff`, `observation_window_start/end` (nullable with reason), `analyst_id`, `coding_guide_version`, `data_access_constraints`, `sampling_rule`, `baseline_method_id` (nullable), `code_commit_or_tool_version` (nullable), `file_manifest` (name, checksum, access limitations). No sensitive content needs to be public; restricted source locators and stable redacted excerpts are allowed, with stated reproducibility constraints.

**Evidence Register — required per item:** `evidence_id`, `case_id`, `source_locator` (or restricted-reference token), `source_kind`, `content_locator` (page/line/event range or hash), `event_time_or_order`, `time_quality`, `actor_ids` (possibly empty), `collection_method`, `collector_or_origin`, `authenticity_status`, `missingness_status`, `raw_vs_transformed`, `transformation_steps`, `version_or_hash`, `observation_scope`. Optional: `raw_payload_pointer`, `privacy_class`, `instrument_id`, `sampling_weight`, `data_quality_notes`. If source, time, or actors are unavailable, populate explicit unknown values and reasons rather than invent them. Every ID referenced downstream must resolve to an evidence item or an explicit inaccessible-source marker.

**Entity/Unit record — required for every proposed U:** `candidate_unit_id`, `components`, `unit_kind` (human/AI/organization/relation/other), `inclusion_rule`, `exclusion_rule`, `boundary_id`, `boundary_valid_from/to`, `boundary_basis_evidence_ids`, `alternative_boundary_ids`, `state_variables_observable`, `independence_assumptions`. A *candidate* unit is not a confirmed emergent Updating Unit.

**Reference record — required for every assessed claim:** `reference_id`, `observer_id`, `owner_id`, `target`, `criteria_or_frame`, `instrument_id`, `instrument_version`, `boundary_id`, `valid_from/to`, `evidence_ids`, `unknown_fields`. Do not merge different observers' criteria; changed criteria require a new version and linked change evidence.

**Claim record — required:** `claim_id`, `construct`, `claim_text`, `claim_scope`, `unit_id`, `boundary_id`, `reference_id`, `time_interval`, `evidence_links` (each: `evidence_id`, `direct|proxy|inference`, `support|contradict|context`, `precise_locator`), `observability` (`O|P|I|U|null`), `finding`, `decision_status`, `rule_ids_applied`, `alternatives`, `missing_requirements`, `coder_id`, `adjudication_id` (nullable), `rationale`. `null` observability is permitted only for deferred/not-applicable claims, never as an unmarked omission.

**Event/transition record:** `event_id`, `event_time_or_order`, `actors`, `input_refs`, `output_refs`, `pre_state_ref`, `post_state_ref`, `transition_evidence_refs`, `criterion_version_refs`, `component_relation_refs`, `causal_status` (`observed_sequence|hypothesized_link|experimentally_tested`), `uncertainties`. Without transition evidence, record change of state only.

## 3. Execution procedure (mandatory order)

1. **Predefine scope:** Write question, observation window, sampling, candidate targets, and data access limitations before searching for positive IDOS constructs. Preserve later amendments with timestamps.
2. **Freeze evidence boundary:** Register raw evidence and its versions/hashes; record exclusion reasons and missing sources. Do not pre-label raw evidence with CDP terms.
3. **Preliminary observability inventory:** For every planned claim, record available evidence, holes, and provisional O/P/I/U or `deferred`; this is revisable with an audit trail.
4. **Candidate units and boundaries:** List plausible competing units and evidence-constrained system boundaries. Do not select the boundary because it makes a preferred finding appear.
5. **Reference systems:** Register each observer, criterion, instrument, and their changes separately. Distinguish altered measured outcome from altered measurement procedure.
6. **Construct coding:** Create claim-specific evidence links for applicable 12CDP coordinates, with explicit missing/competing/collapsed/nonlinear processes. Never complete a 12-element sequence by narrative necessity.
7. **Trajectory reconstruction:** State `T(U,B,Δt)`, identify state observations versus transition evidence, and record unresolved provenance gaps and branching.
8. **Optional perturbation/re-observation:** Register baseline, perturbation nature, exposure, adaptation opportunity, re-test differences, and observed response. Avoid relabeling success as Future Updateability.
9. **Blind independent recoding (when feasible):** Second coder receives a frozen evidence package and coding guide; record disagreements before discussion.
10. **Issue output package:** Eight v0.2 outputs plus claim ledger, coding disagreement log, manifest and validation report. Record negative and not-observable results without deletion.

## 4. General decision gates

- `O` only when the *whole narrowly defined observable claim* is directly supported by traceable evidence, with relevant unit, boundary, timeframe, and reference identified. An observed act does not directly reveal an unobserved internal motive.
- `P` only when one or more specified claim components have direct evidence, while other indispensable components remain unobserved. Explicitly enumerate observed and missing components.
- `I` only when no direct evidence of the target relation is available but explicit evidence and an alternative-explanation test support a plausible interpretation. Link premises; include competing explanation. The mere existence of a theory does not qualify.
- `U` when a defined target cannot be identified from the bounded evidence. If evidence is contradictory, preserve both and use `disputed` finding rather than confidently forcing `O`.
- `deferred` when the claim cannot even be evaluated because a prerequisite (time window, reference, unit, operational distinction) is undefined; log `missing_requirements` and planned remedy.
- Observability may differ by granularity: e.g. `O` for a posted comment, `I` for internal uncertainty, `U` for a lasting reference-frame change. Do not pool these into one O.
- When counterevidence exists, record it before deciding. An `O` claim can be `contradicted` by directly observed counterevidence: observability does not imply confirmation.

## 5. Provisional construct codebook (measurement hypotheses, not ontology)

For each coordinate, assess only the precisely framed target. The following are candidate observable signatures, **not sufficient universal criteria**.

| Coordinate | Direct target if instrumented | Proxy / usual gap | Reject shortcut |
|---|---|---|---|
| Reality | Dated external event, task environment, instrument reading | Reports about unmeasured reality | Claiming complete access to Reality |
| Difference | Two identified comparands and recorded discrepancy at a stated frame | Outcome deviation without specified comparator | Equating every difference with Residual |
| Representation | Recorded model, statement, belief report, policy, schema or artifact version | Behavior allegedly implying a representation | Inferring an internal representation from output alone |
| Residual | Documented incompatibility *relative to the operative representation/frame* plus trace of non-absorption at the relevant decision point | Prompt revision, error report, dissatisfaction | Treating objective mismatch as experienced Residual |
| Holding | Same unresolved issue explicitly retained and made available for later treatment across documented time/events | Elapsed time, postponed decision, stored file | Treating passive delay or memory as active Holding |
| Update | Difference-linked state/rule/structure/relationship transition with trace | Before/after performance | Treating arbitrary change as update |
| Possibility Space | Documented admissible option set / generation rules and revisions | Number of proposed ideas | Inferring all latent alternatives |
| Trajectory | Dated or sequenced states for fixed or explicitly versioned U/B plus changes/persistence | Snapshots with missing transitions | Claiming process solely from longitudinal states |
| Limit | Recorded constraint or observed boundary of admissible action | Failure score as presumed intrinsic limit | Assuming single failure identifies limit |
| Enactment | Observable implemented action with actor and setting | Planned action only | Equating intention with enacted action |
| Reality′ | Subsequent environmental observation with temporal/provenance link | Self-reported success alone | Presuming action generated observed result |
| Reopening | Recorded reconsideration after prior provisional closure and new difference/input | One edit or routine retry | Inferring structural reopening from any revision |

`Trajectory` in the table is also separately assembled in Stage 7; its appearance in 12CDP does not create duplicate independent evidence.

### 5.1 Residual: candidate coding test

Record separately `(a)` expected/represented state, `(b)` observed/claimed state, `(c)` specified frame/criterion, `(d)` registered mismatch, `(e)` evidence that current frame did not assimilate it at that decision moment, and `(f)` later treatment. Objective discrepancy is directly observable when `(a)-(d)` are recorded. **Candidate Residual** is `O` only for an expressly *operational, public/recorded non-absorption* claim when `(e)` is directly documented; it does not imply direct access to internal experience. Use `P` for directly recorded detection lacking documented non-absorption; `I` for inferred unresolved incompatibility from subsequent acts; `U` when the relevant representation or frame is unobserved. Do not require a specific next behavior as evidence of existence; next behavior is recorded separately. Rival codes: prediction error, contradiction, uncertainty, dissatisfaction. The coding guide must say what Residual adds beyond each rival; when inseparable, flag `construct_non_discriminable`.

### 5.2 Holding: candidate coding test

Require a stable `issue_id`, dated detection of an unresolved issue, an identifiable *retention mechanism or explicit instruction*, and a later trace showing the issue remains revisitable or was revisited without a fabricated closure. `O` is limited to **recorded issue retention across episodes**, not unobservable cognitive Holding. `P` if explicit retention exists but later continuity is not observed; `I` if delay plus subsequent discussion only suggests retention; `U` if neither retention nor issue lineage is captured. Rival codes: working memory, queueing, deferral, indecision, active information search. If a simple queue model fully explains the trace, no unique Holding claim is warranted. An unobserved gap does not establish temporal Holding.

### 5.3 Updating Unit and dynamic boundary

Enumerate component and relational candidates before coding. Document: individual states, shared context/history, coupled decisions, joint state transition, evidence for persistent relational dependence, and alternative models (human learning alone, AI context cache, external shared memory, coordination). Use `candidate_unit` until evidence supports a specified relational transition. For any asserted relational effect, compare observed behavior to a preregistered contrast if available (history reset, partner swap, AI swap, independent components, shared-memory removal). Without such contrasts, typically `I` for a proposed *distinct* relational Updating Unit even when interaction is O. Never infer ontological emergence from one ablation. Boundary changes require explicit pre/post inclusion criteria and change trace; changed software version or org chart alone is not automatically a changed functional boundary.

### 5.4 Reference-frame / measurement evolution

Track `F_t/F_t+1` and `M_t/M_t+1` as independently versioned artifacts. Direct change may be observed in criteria, measurement code/configuration, evidence weights, scoring rules, accepted data types or instrument calibration with dated provenance. Different outcomes under an unchanged instrument ≠ instrument change. Role changes ≠ frame change without corresponding criterion evidence. Causality between the observed change and later decisions requires separate transition evidence.

### 5.5 Trajectory

A trajectory record must identify `unit_id`, `boundary_id/version`, `time_basis`, `start/end`, ordered `state_refs`, `transition_refs`, `persisting_properties`, `changed_properties`, `branches`, `identity_assumptions`, and `provenance_gaps`. Present **state trajectory** independently of **process trace**. When unit identity/boundary changed, either open a new segment with documented continuity assumptions or record identity as undecidable. Do not merge task-level and organizational timescales.

### 5.6 Future Updateability and related relations

Retain Future Updateability as a **latent capacity, not an O/P/I/U outcome score**. The observable claims are individual perturbations, opportunities to respond, measurement/rule/boundary transitions, and responses under renewed uncertainty. Each `AR_i` has pre-state, specific perturbation, exposure, adaptation opportunity, response trace, outcome, and confounders. A second perturbation should have an explicitly distinct uncertainty source. At most report `evidence_relevant_to_FU`, with alternative explanations (practice, memorization, resilience, transfer, robustness). If no perturbation or re-test exists, `FU_evaluation = not_estimable`. If present, status remains `latent_not_validated`; never set `FU=O` or invent a numeric score.

CFV and MU in relational cases: register which actor could inspect or reproduce whose claims, and which side's criteria/actions demonstrably changed after the other's contribution. Agreement is not CFV; communication is not MU. Both retain alternative explanations and independent claim records. Do not treat desirable governance outcomes as descriptive observations.

## 6. Output package specification

Emit a directory or single logical bundle containing:

1. `manifest` — versions, sampling, hashes, access/ethics limitations and exclusions.
2. `evidence_register` — source records uncolored by IDOS labels.
3. `observability_matrix` — one row per construct-specific claim with O/P/I/U or deferred and evidence links.
4. `unit_boundary_record` — all candidates, rejected/alternate boundaries and change times.
5. `reference_system_record` — observer/owner/instrument/frame versions.
6. `process_trace` — non-obligatory 12CDP coordinates with evidence, ordering and absences.
7. `trajectory_record` — `T(U,B,Δt)` with state/transition/provenance splits.
8. `limitations` — all inaccessible/missing evidence, non-discriminability, observer bias and scope.
9. `adaptive_response_record` — optional perturbation sequence, with no FU score.
10. `coding_log` — individual coder decisions, contradictions, amendments, adjudication.
11. `comparison_record` — optional rival method results and incremental value.

All findings must resolve through `claim_id → evidence_link → evidence_id → source_locator/version`, or be marked inaccessible. Counts are descriptive only; do not convert them into an IDOS intelligence score.

## 7. Independent coding and reliability

Freeze evidence and codebook **before** independent coding. Coders separately label a fixed sample or entire case; compare both observability label and finding, with `deferred` as distinct. Record exact match rate plus a full confusion matrix; for sufficient sample size optionally calculate nominal Krippendorff alpha (or an agreed kappa variant), with missingness and prevalence reported. No universal pass threshold is asserted. Distinguish agreement on obvious observables from agreement on Residual/Holding/Updating Unit. Adjudicate *after* preserving the original independent records. If disagreement stems from ambiguous operational criteria, amend the next guide version; do not retroactively relabel the holdout without preserving history.

## 8. Comparator protocol

Provide rival analysts identical evidence boundary, available time, and question, without IDOS terminology. Use a strong baseline (event-log/process-mining analysis, qualitative process tracing or ordinary organizational/agent audit as appropriate), not a deliberately weak control. Predeclare the decision task and assess: verifiable claim coverage, false positives, unsupported inference, missed documented events, coding agreement, analyst time/cost, and any decision-relevant new finding. Blind reviewers to analysis condition where feasible. If IDOS adds no justified, actionable information or imposes undue burden, record a null/negative result. Do not infer causal superiority from post-hoc narrative comparisons.

## 9. Machine-checkable integrity tests

A minimal implementation must reject or flag:

- duplicate IDs, dangling evidence references or source changes without provenance;
- missing mandatory keys without explicit missingness reason;
- timestamp order inconsistencies or timezones silently omitted;
- an O/P label whose claim has no linked direct evidence;
- an I label with no premises or rival interpretation;
- any `FU` numeric score or direct observability coding for latent capacity;
- any candidate Updating Unit based on interaction count alone;
- a trajectory without U, B or Δt;
- a transition process asserted from pre/post snapshots alone;
- coding changes that overwrite the original coder's decision;
- forced completion of twelve CDP stages.

A validator checks **record consistency, not scientific truth**. Passing structural validation says nothing about whether a candidate measure has construct validity.

## 10. Worked micro-example (synthetic, illustrative only)

At 09:00 an AI gives a wrong answer; at 09:02 a human documents a mismatch with the published rule; at 09:04 the human records "unresolved — revisit after checking"; at 09:30 the same issue ID is reopened after source verification; at 09:35 the team changes its review checklist. With dated logs, *wrong output* and *documented detection* can be O; narrowly defined *recorded unresolved-issue retention* may be O. An internal felt Residual remains I/U without evidence; a checklist version change may be O while its causal role remains I; formation of a new Human–AI Updating Unit is not established. Future Updateability is not estimable without renewed perturbations/re-test. This example demonstrates coding separation, not IDOS efficacy.

## 11. Self-audit and unresolved problems

**Still not established:** construct validity/discriminant validity of Residual and Holding; necessary/sufficient Updating Unit criterion; stable trajectory identity across changing boundaries; source representativeness; human/AI/organization equivalence; causal attribution to an update; optimal inter-rater agreement; latent Future Updateability prediction; comparative value over strong alternatives. Candidate coding tests may collapse into preexisting concepts and should be removable without changing MASTER_MAP v1.1.

**Risks:** surface-log bias; unrecorded human deliberation; private AI states; selective event retention; translation loss; hindsight choice of U/B; measurement-system drift; normative contamination; correlation/causation confusion; accessibility and privacy constraints. Every case must report which risks prevent the strongest possible interpretation.

**Specification acceptance criteria:** (a) an external analyst can populate a record package without redefining the architecture, (b) every decision traces to evidence or transparent absence, (c) direct observation and inference cannot be silently merged, (d) disagreeing coders can preserve disagreements, (e) known measurement gaps stay open, (f) at least one strong rival can be evaluated on matched evidence. **Meeting these criteria is specification readiness, not empirical validation.**

## 12. Proposed next verification (not reported as completed)

1. Compare this self-contained measurement record specification directly with `src/idos_reference_v1_1.py` and `IDOS_OPERATIONAL_PROTOCOL_v0.2.md`; record field-level compatibility and gaps without assuming a separate implementation-specification file.
2. Have two independent coders use one pre-existing trace under a frozen codebook; preserve both judgments.
3. Run all integrity tests on intentionally malformed datasets as well as one small valid dataset.
4. Conduct at least one prospective perturbation/re-test and strong-baseline comparator before claiming empirical measurement utility.
5. Revise candidate definitions only with versioned evidence and negative findings intact.

**Change policy:** v0.2 and MASTER_MAP v1.1 remain frozen. This v0.3 is a candidate measurement procedure subject to testing, reduction and rejection.

## 13. Third-party execution worksheet (minimum example)

Before measurement begins, an external analyst shall complete the following worksheet. Use explicit `unknown`/`not_collected` values rather than guessing. All field labels in this worksheet refer to the formal records in Section 2.

| Step | Analyst records | Failure/deferral trigger |
|---|---|---|
| A | `case_id`, question, observation window, evidence cutoff, sampling rule | No defined target/question → stop and scope the case |
| B | Evidence register with immutable source locators and available timestamps/order | No accessible evidence → register gap; do not invent process trace |
| C | Provisional claim list and observability inventory | Ambiguous claim → `deferred`; defined but unidentifiable claim → `U` |
| D | Candidate units, inclusions/exclusions, boundaries and competing candidates | Boundary chosen only after result → flag post-hoc choice |
| E | Independent observer/reference records, versions and criteria | Unknown observer/instrument → record missingness; downgrade claims needing it |
| F | Claim-by-claim 12CDP coding with direct/proxy/inferred links | Insufficient evidence → `I/U` as warranted; never fill missing steps |
| G | `T(U,B,Δt)` segments separating state and transition evidence | Only two snapshots → state difference, not observed Update process |
| H | If available, perturbation, adaptation opportunity and re-test | Without prospective renewed uncertainty → FU not estimable |
| I | Two separate coder records and disagreement register | One coder only → reliability not evaluated |
| J | Export records, manifest, limitations, comparison plan | Broken source links → package fails structural validation |

**Required output status header** for every case: `structural_validation = pass|fail|not_run`; `independent_recode = completed|not_done`; `construct_validity = not_established|under_test` (never automatically `established`); `comparison_test = completed|not_done`; `fu_status = not_estimable|latent_not_validated`. These are **v0.3 record conventions**, not scientific classifications proven by the existing cases.

### Operational distinction: schema completeness vs scientific agreement

- **Ready for pilot coding:** Section 2 records can be populated, all links resolve, and each claim follows a documented decision gate.
- **Reliability tested:** independent coders apply the same frozen evidence/codebook, with disagreements retained and summarized.
- **Construct validity tested:** evidence differentiates the construct from pre-registered alternatives, preferably under discriminating observations/interventions.
- **General use supported:** multiple domains/observers replicate acceptable reliability and validity; no such achievement is claimed here.

### Existing reference material and provenance

- Frozen architecture: `MASTER_MAP_v1.1.md`.
- Frozen measurement baseline: `MEASUREMENT_OBSERVABILITY_PROTOCOL_v0.2.md`.
- Completed cases and candidate prospective designs: `MEASUREMENT_VALIDATION_RECORD_v0.2.md` and `MEASUREMENT_VALIDATION_RECORD_v0.2_INTEGRATED.md`.
- Related operating protocol: `IDOS_OPERATIONAL_PROTOCOL_v0.2.md`.
- Existing Python architectural reference: `src/idos_reference_v1_1.py`.
- **Not an existing dependency:** `IDOS_IMPLEMENTATION_SPEC_v0.1.md`. No document with this filename is required or asserted to exist.


## 14. Status of subsequent preparation (non-validation note; 2026-10-12)

After drafting v0.3, preliminary QA and experiment-preparation work was performed. A small author-generated synthetic set was used for input and agreement-script checks, with successful arithmetic checks in deliberately identical or altered artificial codings. Such percentages are **not independent-coder agreement**. A field-pilot kit was revised to reduce prompting of expected mismatch; **no participants were enrolled and no primary data were collected** in these preparatory steps.

The prior SWE-bench `django__django-15499` single-trace exercise was an engineering feasibility check, not a random representative selection. Its final audit did not establish Residual, Holding, updating-rule change, Future Updateability, or incremental value relative to conventional trace analysis. Avoid repeating that closed case without genuinely new evidence.

**Next empirical gate:** consented, prospectively recorded primary interactions with timestamps, pre-outcome expectations, independently traceable evidence, independent coding, and a strong conventional comparator. If the constructs cannot be discriminated from simpler alternatives, report null results rather than force an IDOS-positive judgment.

**Internal consistency note:** The main specification permits `disputed` and `not_applicable` as general decision statuses; the frozen 16-item synthetic coder trial intentionally accepts only `assigned` and `deferred`. These vocabularies apply to different levels and must not be silently interchanged.

**This document is the only recommended public Measurement v0.3 Markdown for this publication step.** Ancillary checks and kits remain working materials, not separate evidence of validation.
