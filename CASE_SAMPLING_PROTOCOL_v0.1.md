# IDOS Case Sampling Protocol v0.1

**Status:** FROZEN FOR PROSPECTIVE CASE SELECTION  
**Version:** 0.1  
**Date:** 2026-10-02  
**Applies to:** Prospective empirical and architectural case testing of IDOS  
**Architecture Baseline:** IDOS Master Map v1.0 — FROZEN

## 1. Purpose

This protocol defines how cases are selected for prospective testing of the Intelligence Dynamics Architecture / IDOS.

Its primary purpose is to reduce:

- confirmation bias,
- cherry-picking,
- domain-selection bias,
- source-selection bias,
- retrospective case fitting,
- and replacement of cases that produce unfavorable results.

The governing principle is:

> Cases should not be selected because they appear likely to support, illustrate, or challenge IDOS.

Case selection and IDOS analysis must remain procedurally separated.

The required sequence is:

Candidate Pool  
→ Eligibility Assessment  
→ Sampling  
→ Case Selection  
→ IDOS Analysis  
→ Result Preservation

not:

Interesting IDOS-compatible case  
→ Selection  
→ Analysis

A case showing no incremental value from IDOS is a valid result.

A case that contradicts IDOS is also a valid result.

## 2. Research Principle

The purpose of prospective case testing is not to demonstrate that IDOS can explain every case.

The purpose is to determine:

1. which IDOS distinctions are actually necessary;
2. which distinctions can be operationalized;
3. which are redundant with existing theories;
4. which fail under real-world evidence;
5. whether IDOS provides incremental explanatory, observational, measurement, or implementation value;
6. whether repeated failures reveal an architectural problem.

The sampling process must therefore allow IDOS to fail.

## 3. Prospective Application Boundary

This protocol applies prospectively only to cases selected after the freeze of CASE_SAMPLING_PROTOCOL_v0.1.

Cases analyzed before this protocol was frozen must not be retrospectively classified as having been selected under this protocol.

In particular:

**Case G-001 — Recursive AI R&D Governance Red Team**

was selected and analyzed before CASE_SAMPLING_PROTOCOL_v0.1 was established.

Case G-001 is therefore classified as:

**Exploratory Pre-Protocol Case**

It may be retained as part of the IDOS research trajectory and used for methodological learning, but it must not be counted as evidence from prospective randomized or protocol-governed case selection.

The first case selected after this protocol is frozen will constitute:

**Prospective Case 001 under CASE_SAMPLING_PROTOCOL_v0.1**

This distinction must be preserved in future cross-case analysis.

## 4. Observation Window

For the initial prospective case pool:

**Observation Window: 2025-01-01 through 2026-10-02**

This window is frozen for the initial sampling round.

Future sampling rounds may use different observation windows, but changes must be documented prospectively and must not retroactively alter the original candidate pool.

## 5. Unit of Sampling

The sampling unit is a documented real-world case or event sequence.

A case should contain sufficient evidence to reconstruct at least part of:

Event  
→ Response  
→ Change / No Change  
→ Subsequent Consequence

The sampling unit is NOT:

- a theory,
- an opinion,
- a hypothetical scenario,
- a general trend without identifiable events,
- or a case constructed specifically to illustrate IDOS.

## 6. Inclusion Criteria

A case is eligible when all of the following conditions are satisfied.

### I1 — Multiple Distinguishable Entities or Systems

At least two distinguishable entities, actors, organizations, technical systems, institutions, or other systems are involved.

These entities do not need to correspond to IDOS Updating Units at the sampling stage.

### I2 — Observable Change or Response

The case contains at least one documented:

- change,
- response,
- failure,
- adaptation,
- intervention,
- decision,
- transition,
- or non-response with observable consequences.

### I3 — Evidence Availability

Sufficient public evidence exists to reconstruct at least part of the event sequence.

### I4 — Temporal Structure

The case contains enough temporal information to distinguish at least:

Before  
→ Event / Interaction  
→ After

### I5 — Independent Eligibility

The case must remain eligible without reference to IDOS terminology.

A case must NOT be included merely because it appears to contain:

- Difference,
- Residual,
- Holding,
- Update,
- Frame change,
- Boundary change,
- Translation Residual,
- Cross-Unit Update,
- or other IDOS concepts.

Eligibility must be determined before IDOS mapping.

## 7. Exclusion Criteria

A candidate case is excluded when one or more of the following conditions apply.

### E1 — Purely Hypothetical

The case is a thought experiment, fictional scenario, forecast, or purely hypothetical future event.

### E2 — Insufficient Evidence

Available evidence is insufficient to reconstruct a meaningful event sequence.

### E3 — Commentary-Only Evidence

The case is supported only by retrospective commentary, interpretation, or secondary discussion without adequate underlying evidence.

### E4 — Duplicate Event

The candidate substantially duplicates another case already representing the same underlying event.

### E5 — IDOS-Driven Selection

The case entered the candidate pool specifically because it appeared favorable, unfavorable, interesting, or illustrative for IDOS.

### E6 — Irreconstructable Sequence

Relevant events cannot be ordered sufficiently to support analysis.

All exclusions must be recorded with an explicit exclusion reason.

Excluded cases must not silently disappear from the candidate pool.

## 8. Source Strata

The candidate pool should be constructed from multiple source classes to reduce source-selection bias.

The initial source strata are:

### A — Academic Research

- peer-reviewed research,
- conference papers,
- preprints,
- documented experimental studies.

### B — Government / Regulatory / Standards Sources

- government reports,
- regulator documents,
- public investigations,
- standards bodies,
- official technical assessments.

### C — Corporate Technical / Incident Sources

- technical reports,
- system cards,
- incident reports,
- engineering reports,
- evaluation reports,
- postmortems.

### D — Independent Investigation / Audit Sources

- independent audits,
- external investigations,
- documented incident databases,
- third-party technical assessments.

### E — Documented Real-World Human / Organizational Cases

Cases involving observable interactions among:

- humans,
- AI systems,
- organizations,
- institutions,
- or other socio-technical systems,

provided that the evidence requirements above are satisfied.

No source stratum is assumed to be inherently superior.

Evidence quality must be evaluated separately from source category.

## 9. Candidate Pool Construction

The candidate pool must be created before IDOS analysis begins.

For each candidate, record only neutral metadata required for sampling.

Recommended fields:

Case ID  
Title / Neutral Event Description  
Date  
Source Type  
Primary Source  
Secondary Source, if applicable  
Evidence Availability  
Inclusion Criteria Status  
Exclusion Criteria Status  
Eligibility Decision  
Exclusion Reason, if applicable

Do NOT record during candidate-pool construction:

- whether the case supports IDOS;
- which IDOS concepts appear relevant;
- whether IDOS is expected to perform well;
- whether the case is theoretically interesting;
- expected novelty;
- expected explanatory value.

The candidate pool is a sampling instrument, not an IDOS interpretation document.

## 10. Eligibility Assessment

Eligibility must be determined using only the Inclusion and Exclusion Criteria defined in this protocol.

The eligibility question is:

> Is there sufficient documented evidence to analyze this real-world multi-entity event sequence?

The eligibility question is NOT:

> Is this a good case for IDOS?

Eligible cases proceed to sampling.

Ineligible cases remain recorded with their exclusion reasons.

## 11. Sampling Procedure

After eligibility assessment:

1. Assign each eligible case a stable sequential Case Pool ID.
2. Freeze the eligible candidate list.
3. Record the total number of eligible cases.
4. Define the sampling method before selection.
5. Record the randomization procedure.
6. Record the random seed where applicable.
7. Execute the selection mechanically.
8. Record the selected Case Pool ID.
9. Preserve the selection record before IDOS analysis begins.

Where appropriate, stratified random sampling may be used to reduce concentration in a single source class or domain.

Any stratification scheme must be defined before seeing IDOS analysis results.

## 12. No Replacement Rule

Once a case has been validly selected, it must not be replaced because it is:

- inconvenient,
- difficult,
- uninteresting,
- poorly aligned with IDOS,
- better explained by another theory,
- unfavorable to IDOS,
- or likely to produce a negative result.

A selected case may only be removed if a previously undetected violation of the frozen eligibility criteria is identified.

Any such removal must be documented.

The replacement procedure, if required, must follow the same frozen sampling method.

## 13. Analysis Freeze

IDOS analysis begins only after the selected case has been recorded.

At the beginning of each case analysis, record:

Sampling Protocol:  
CASE_SAMPLING_PROTOCOL_v0.1

Selection Method:  
[record method]

Random Seed:  
[record seed if applicable]

Case Pool ID:  
[record ID]

Master Map Baseline:  
MASTER_MAP_v1.0 — FROZEN

Selection Date:  
[record date]

No IDOS interpretation should influence case selection.

## 14. Evidence Order

Where possible, case reconstruction should proceed in the following order:

1. primary or near-primary evidence;
2. contemporaneous technical or institutional records;
3. independent investigation;
4. secondary analysis;
5. IDOS interpretation.

IDOS terminology should not be used to construct the initial factual chronology.

The first reconstruction should be as theory-neutral as reasonably possible.

This is intended to reduce retrospective fitting.

## 15. Required Analysis Sequence

Each selected case should proceed through the following sequence.

### Stage A — Theory-Neutral Reconstruction

Describe:

- what happened,
- who or what was involved,
- temporal sequence,
- observable changes,
- observable non-changes,
- interventions,
- and consequences.

Do not begin with IDOS terminology.

### Stage B — Existing-Theory Comparison

Identify whether established theories or frameworks already provide sufficient explanation.

Where existing theory is sufficient, record that explicitly.

### Stage C — IDOS Mapping

Only after Stages A and B, map the case to the frozen Master Map.

Potentially relevant IDOS structures may then be examined.

### Stage D — Red Team

Attempt to falsify or reduce the IDOS interpretation.

Ask:

- Is the IDOS mapping circular?
- Is a simpler explanation sufficient?
- Is an IDOS concept unnecessary?
- Is the distinction observable?
- Is the distinction measurable?
- Does the case contradict the architecture?
- Is IDOS merely renaming an existing concept?

### Stage E — Incremental Value Assessment

Determine whether IDOS adds anything beyond existing descriptions.

Possible outcomes include:

- additional distinction,
- additional observability,
- additional measurement structure,
- additional causal organization,
- additional implementation value,
- no incremental value,
- contradiction.

### Stage F — Residual Preservation

Any unresolved discrepancy must be preserved as a Residual.

Do not reinterpret a negative result merely to protect IDOS.

## 16. Valid Result Categories

The following are all valid research outcomes.

### R1 — Incremental Value Observed

IDOS provides a distinguishable additional contribution.

### R2 — Redundant

Existing theories adequately capture the relevant structure.

Incremental Value_IDOS ≈ 0

### R3 — Partially Useful

Some IDOS distinctions are useful while others are unnecessary.

### R4 — Measurement Failure

The proposed distinction cannot currently be measured or operationalized.

### R5 — Application Failure

The case cannot be adequately represented using the current IDOS application model.

### R6 — Architectural Contradiction

The case directly conflicts with a frozen architectural commitment.

### R7 — Indeterminate

Available evidence does not support a reliable conclusion.

No result category is preferred in advance.

## 17. Negative Result Rule

Negative results must be retained.

Examples include:

Existing Theory = Sufficient

Incremental Value_IDOS ≈ 0

Measurement Hypothesis = Not Supported

IDOS Mapping = Unnecessary

Architecture = Contradicted

A negative result must not be removed because it weakens the apparent explanatory scope of IDOS.

Negative results are part of the research trajectory.

## 18. Architecture Revision Rule

Master Map v1.0 remains frozen during prospective case testing.

A single difficult case does not automatically justify architectural revision.

The default response to a case-level failure is:

Case Failure  
→ Residual  
→ Measurement / Application Review  
→ Cross-Case Comparison

Architectural revision should only be considered when evidence indicates:

- direct architectural contradiction,
- repeated failure across independently selected cases,
- persistent redundancy,
- inability to represent an important recurring dynamic,
- or systematic failure of a core distinction.

The governing principle remains:

> Freeze the architecture, not every mechanism.

## 19. Cross-Case Review

After a predefined number of independently sampled cases, conduct a cross-case review.

The review should examine:

- recurring Residuals,
- recurring redundant concepts,
- repeated measurement failures,
- repeated explanatory gains,
- domain-specific effects,
- source-specific effects,
- and potential architectural contradictions.

The purpose of cross-case review is not to count how many cases IDOS "wins."

The purpose is to identify stable patterns of success and failure.

## 20. Provenance Requirements

The following must be preserved in the repository:

- Sampling Protocol version,
- candidate pool,
- eligibility decisions,
- exclusion reasons,
- frozen eligible pool,
- sampling method,
- random seed where applicable,
- selected Case Pool ID,
- evidence sources,
- theory-neutral reconstruction,
- existing-theory comparison,
- IDOS mapping,
- Red Team results,
- negative results,
- unresolved Residuals,
- and any later protocol revision.

Research provenance is part of the evidence.

## 21. Protocol Revision

This document is:

**FROZEN FOR PROSPECTIVE CASE SELECTION**

If the protocol itself proves inadequate, do not silently rewrite v0.1.

Create a new version:

CASE_SAMPLING_PROTOCOL_v0.2.md

The new version must record:

- what changed,
- why it changed,
- which prior cases used v0.1,
- and whether the change could affect comparability.

Cases already selected under v0.1 remain identified as v0.1 cases.

## 22. Separation of Functions

The research architecture should maintain the following separation:

MASTER_MAP_v1.0.md  
= What architecture is being tested

CASE_SAMPLING_PROTOCOL_v0.1.md  
= How cases are selected

Candidate Pool  
= What cases were eligible for selection

Case Research Records  
= What happened when selected cases were analyzed

Measurement Protocols  
= How specific constructs are operationalized

These functions should not be collapsed into a single document.

## 23. Core Anti-Bias Rule

The central anti-bias principle of this protocol is:

> Do not select cases to fit IDOS.  
> Select cases independently, then allow IDOS to succeed, fail, become redundant, or generate Residuals.

In compact form:

Sampling ⟂ Expected IDOS Result

Case Selection  
→ Evidence Reconstruction  
→ Existing Theory  
→ IDOS  
→ Red Team  
→ Result

not:

IDOS Expectation  
→ Case Selection

## 24. Research Position

This protocol does not guarantee unbiased research.

Randomization does not eliminate:

- evidence bias,
- publication bias,
- classification bias,
- measurement bias,
- interpretation bias,
- or model-assisted analysis bias.

Its purpose is narrower:

to make case-selection bias more visible, constrained, reproducible, and auditable.

Future protocols may address the remaining sources of bias separately.

## Final Principle

The objective is not to find cases that IDOS can explain.

The objective is to expose IDOS to cases it did not choose.

If the architecture survives, its credibility should increase.

If it fails, the failure should remain visible.

If existing theory is sufficient, IDOS should not claim additional value.

If repeated independently selected cases reveal the same architectural Residual, the architecture should be reconsidered.

The research process should therefore remain:

Reality  
→ Selection Independent of IDOS  
→ Evidence  
→ Comparison  
→ IDOS Application  
→ Red Team  
→ Residual  
→ Revision or Retention  
→ Reality Recontact
