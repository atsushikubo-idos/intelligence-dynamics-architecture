# CASE_SAMPLING_PROTOCOL_v0.2
## Domain-Stratified Prospective Case Sampling Protocol for IDOS

**Protocol Version:** 0.2  
**Date:** 2026-10-02  
**Status:** PROSPECTIVE — applies beginning with CASE-P003  
**Previous Protocol:** CASE_SAMPLING_PROTOCOL_v0.1  
**Baseline Architecture at Adoption:** MASTER_MAP_v1.0 — FROZEN

---

## 0. Purpose

This protocol defines how prospective empirical cases are selected for stress-testing IDOS.

Its purpose is not to create a statistically representative sample of all real-world systems.

Its narrower purpose is to reduce avoidable case-selection bias while ensuring that IDOS is challenged across materially different domains rather than repeatedly tested on cases from one favored area.

The governing principle is:

**Random selection does not imply an unbiased candidate pool.**

Therefore:

**Selection randomness** and **candidate-pool construction** must be treated as separate methodological problems.

---

## 1. Reason for Revision from v0.1

CASE-P001 and CASE-P002 were both prospectively selected under `CASE_SAMPLING_PROTOCOL_v0.1`.

CASE-P001 explicitly recorded the limitation that its eligible candidate pool had been constructed through AI-assisted web search and therefore could contain candidate-pool bias even though the final draw was pseudorandom.

CASE-P002 was then selected mechanically from the same frozen pool and was also an AI-related case.

The appearance of two AI-related cases does not invalidate either case.

However, it exposes a design issue:

**A mechanically random draw can still reproduce domain bias if the frozen candidate pool is itself domain-skewed.**

Accordingly, v0.2 changes the sampling design prospectively.

It does not revise, invalidate, relabel, or retrospectively resample CASE-P001 or CASE-P002.

---

## 2. Cohort Boundary

```yaml
v0.1_cohort:
  cases:
    - CASE-P001
    - CASE-P002
  status: frozen

v0.2_cohort:
  first_case: CASE-P003
  status: prospective
```

CASE-P001 and CASE-P002 remain valid prospective cases under the protocol that governed their selection.

---

## 3. Core Sampling Principle

Beginning with CASE-P003, case selection uses **domain-stratified prospective sampling**.

The sequence is:

**Define domains → construct candidate pools → freeze pools → compute deterministic ordering → analyze selected cases**

No IDOS mapping is permitted before candidate-pool freeze.

---

## 4. Frozen Domain Strata

The following six domain strata are fixed for the first v0.2 cycle.

### D1 — Individual Human / Behavioral
Examples: learning, skill acquisition, decision revision, perceptual adaptation, behavioral change, expert judgment.  
AI involvement is not required and should not define the case.

### D2 — Human–AI / Artificial Intelligence
Examples: Human–AI collaboration, AI-assisted work, multi-agent artificial systems, AI-mediated decisions, AI-tool adoption.

### D3 — Organization / Institution
Examples: organizational restructuring, institutional learning, operational change, coordination failure, governance redesign, process adaptation.

### D4 — Social / Collective System
Examples: collective coordination, public-system adaptation, community response, distributed social behavior, multi-actor collective change.

### D5 — Biological / Ecological System
Examples: adaptation, regulatory change, ecological response, biological coordination, recovery dynamics, population-level change.

### D6 — Physical / Engineering / Infrastructure System
Examples: engineering control, infrastructure recovery, physical-system adaptation, fault response, system reconfiguration, reliability and failure recovery.

---

## 5. Domain Assignment Rule

Each candidate must be assigned to exactly one primary stratum before pool freeze.

If a case spans several domains, assign it to the stratum corresponding to the **primary unit and process studied in the source evidence**, not the domain that makes the case more attractive for IDOS.

If two strata remain equally defensible, exclude the candidate from the first v0.2 pool rather than assign it opportunistically.

---

## 6. Candidate-Pool Size

```yaml
number_of_strata: 6
eligible_candidates_per_stratum: 4
total_frozen_candidates: 24
```

Each stratum must contain exactly four eligible candidates before any CASE-P003 selection calculation is performed.

---

## 7. Candidate Eligibility Criteria

A candidate is eligible only if all of the following are satisfied before selection.

### E1 — Real-world or empirical event
The case must concern an observed empirical process. Purely hypothetical and theory-only examples are excluded.

### E2 — Evidence accessibility
At least one sufficiently detailed primary or near-primary source must be publicly accessible or archived for the research record.

### E3 — Reconstructable temporal structure
The evidence must permit a minimal theory-neutral reconstruction with:
- an initial condition or baseline;
- an event, intervention, disturbance, or changing condition;
- at least one subsequent observable state or outcome.

### E4 — Outcome independence
Eligibility must not depend on whether the case supports, contradicts, enriches, or appears especially compatible with IDOS.

### E5 — Non-duplication
The candidate must not merely duplicate another included underlying case.

### E6 — Evidence before interpretation
No Master Map mapping, IDOS terminology assignment, Red Team judgment, or architecture-fit assessment may be used in deciding eligibility.

---

## 8. Exclusion Criteria

Exclude a candidate before freeze if:
- evidence is too sparse for theory-neutral reconstruction;
- the underlying event cannot be identified clearly;
- only tertiary commentary is available;
- the case duplicates another candidate;
- domain assignment cannot be made without discretionary interpretation;
- the candidate was introduced specifically because it appeared unusually favorable or damaging to IDOS.

Exclusion reasons must be recorded.

---

## 9. Candidate Discovery Procedure

Candidate discovery is not assumed to be unbiased.

For every nominated candidate, record:

```yaml
candidate_id:
stratum:
case_name:
primary_source:
source_type:
discovery_method:
search_query_or_route:
date_discovered:
eligibility_status:
exclusion_reason_if_any:
IDOS_analysis_before_freeze: NO
```

AI-assisted search may be used, but AI-generated ranking or recommendation must not itself determine final selection.

---

## 10. Search Diversity Rule

When reasonably possible, the four eligible candidates within one stratum should not all come from the same discovery route.

Candidate discovery should seek diversity across source families such as:
- empirical research;
- official or institutional reports;
- public datasets or experimental records;
- incident or investigation reports.

This reduces one source of bias but does not create population representativeness.

---

## 11. Candidate-Pool Freeze

Before selecting CASE-P003, archive a complete `V0_2_CANDIDATE_POOL_FREEZE` record containing all 24 candidates.

After freeze:
- candidate names cannot be changed;
- strata cannot be changed;
- candidates cannot be added because they look useful;
- candidates cannot be removed because they look unhelpful;
- known outcomes cannot alter selection priority.

Any post-freeze eligibility failure must remain visible in the audit trail.

---

## 12. Deterministic Selection Method

v0.2 uses deterministic SHA-256 ordering.

### Fixed seed
```text
2026100202
```

### Stratum ordering
For each stratum `Dk`, compute:

```text
SHA256("2026100202|STRATUM|Dk")
```

Sort the six strata by hexadecimal hash value in ascending order.

### Candidate ordering within each stratum
For each candidate, compute:

```text
SHA256("2026100202|Dk|candidate_id")
```

Sort candidates within that stratum by hexadecimal hash value in ascending order.

The first-ranked candidate is used on the first pass through that stratum, the second-ranked candidate on the second pass, and so on.

This method is deterministic, auditable, and implementation-independent.

---

## 13. Balanced Cycle Rule

Every stratum must contribute one selected case before any stratum contributes a second case.

Thus, the first six v0.2 cases form Cycle 1:
- one case from D1;
- one case from D2;
- one case from D3;
- one case from D4;
- one case from D5;
- one case from D6.

The actual order is determined mechanically by the frozen SHA-256 stratum ordering.

Cases 7–12 under v0.2 form Cycle 2 using the second-ranked candidate within each stratum.

---

## 14. No Outcome-Based Rebalancing

Once the pool and ordering are frozen:
- an AI case cannot be skipped because earlier cases were AI-heavy;
- a biological case cannot be promoted because previous cases fit IDOS too well;
- a negative case cannot be replaced by a more interpretable case;
- a weak selected case cannot disappear silently.

Balance is achieved by protocol, not discretionary correction after results are seen.

---

## 15. Selected Case with Post-Freeze Evidence Failure

If a selected case later proves unusable because of a factual or evidence-access issue not reasonably knowable at freeze time, record:

```yaml
selection_status: SELECTED
analysis_status: EXCLUDED_AFTER_SELECTION
reason: <explicit reason>
```

Then proceed to the next candidate in the same frozen stratum order.

The failed draw remains part of the provenance record.

---

## 16. Theory-Neutral Stage A Requirement

Every selected case begins with Stage A.

Stage A must not presuppose IDOS-specific causal conclusions such as:
- Difference;
- Residual;
- Holding;
- Selection;
- Update;
- Reference Frame;
- Boundary;
- Possibility Space;
- Trajectory;
- Updating Unit;
- CDP;
- Relational Update;
- System Update.

Stage A is frozen before Stage B begins.

---

## 17. Existing-Theory Baseline

Before claiming IDOS-specific explanatory value, each case must be tested against simpler or established alternatives where applicable.

Examples include:
- measurement theory;
- control theory;
- cognitive science;
- organizational theory;
- Human–Computer Interaction;
- distributed cognition;
- systems engineering;
- ecology;
- learning theory;
- network theory;
- institutional analysis.

The applicable alternatives depend on the selected domain.

**Existing explanation first; IDOS incremental value second.**

---

## 18. Observability Discipline

Every IDOS mapping must distinguish:

```text
O — Observed
I — Inferred
U — Unobservable
N — Not tested / not required
```

A concept may not be promoted merely because it creates a coherent narrative.

Unobservable is an acceptable result.

---

## 19. Removal and Red-Team Requirement

For each selected case, actively test whether IDOS concepts can be removed without losing explanatory precision.

Core question:

> Can the case be described, measured, or explained equally well without this IDOS distinction?

A concept that repeatedly fails this test across independent domains becomes a candidate for demotion or removal.

A concept that repeatedly resists removal across independent domains gains empirical retain pressure.

---

## 20. Difference–Update Trace Priority

CASE-P002 exposed a specific empirical gap:

**Detected Difference does not imply Demonstrable Update.**

Accordingly, when the source permits, record separately:
1. externally detectable discrepancy or change;
2. recognition or non-recognition;
3. response or non-response;
4. transformation;
5. continuity or identity across transformation;
6. Reality Recontact;
7. subsequent observable Difference.

This is a measurement priority, not an eligibility requirement.

---

## 21. Architecture Baseline Rule

Every selected case is evaluated against the architecture frozen at selection.

For CASE-P003:

```yaml
Master_Map_Baseline: MASTER_MAP_v1.0
Status: FROZEN
```

If the Master Map is revised later, prior case analyses remain tied to their original baseline.

They are not rewritten retrospectively.

---

## 22. Anti-Overfitting Rule

No Master Map concept should be revised solely to improve fit with one selected case.

Case-level tensions must first be recorded as:
- contradiction;
- redundancy;
- unobservability;
- measurement gap;
- definition gap;
- alternative explanation;
- removal pressure.

Architecture revision should occur only when:
- an architectural-level contradiction is sufficiently strong; or
- a repeated pattern survives across heterogeneous prospective cases; or
- a full v0.2 cross-domain cycle reveals systematic failure or redundancy.

---

## 23. Cross-Domain Cycle Review

After the first six v0.2 cases, conduct a Cycle 1 review comparing:
- constructs repeatedly retained;
- constructs repeatedly removable;
- constructs repeatedly unobservable;
- domain-specific constructs;
- architecture-level contradictions;
- measurement bottlenecks;
- cases explainable without IDOS;
- cases where IDOS appears to add incremental structure.

This is the earliest planned point for systematic domain-balanced reassessment, absent a decisive contradiction.

---

## 24. What v0.2 Does Not Claim

This protocol does not claim:
- statistical representativeness;
- unbiased candidate discovery;
- random sampling from a known population;
- proof of IDOS generality;
- proof that the six strata exhaust Reality;
- proof that equal weighting is theoretically optimal.

It addresses a narrower problem:

**preventing one discovery domain, especially AI-related cases, from dominating the prospective stress-test sequence merely because it is overrepresented in the candidate pool.**

---

## 25. Known Limitations

### L1 — Candidate-discovery bias remains
Stratification reduces domain imbalance but does not make discovery random.

### L2 — Domain definitions are researcher-defined
The six strata are methodological partitions, not ontological claims.

### L3 — Equal weighting is pragmatic
One case per domain per cycle is a stress-testing design, not an estimate of prevalence.

### L4 — Evidence-rich cases remain favored
Accessible documentation affects eligibility.

### L5 — Cross-domain cases may be excluded
This is temporarily accepted to reduce discretionary assignment.

### L6 — Search engines and AI tools influence discovery
The discovery log exposes but does not eliminate this limitation.

---

## 26. Audit Record Required Before CASE-P003

Before selecting CASE-P003, archive:

```yaml
protocol: CASE_SAMPLING_PROTOCOL_v0.2
protocol_status: FROZEN_FOR_P003_SELECTION
seed: 2026100202
hash: SHA-256

strata:
  - D1_Individual_Human_Behavioral
  - D2_Human_AI_Artificial
  - D3_Organization_Institution
  - D4_Social_Collective
  - D5_Biological_Ecological
  - D6_Physical_Engineering_Infrastructure

candidates_per_stratum: 4
total_candidates: 24
candidate_pool: FROZEN
IDOS_mapping_before_freeze: PROHIBITED
first_case_under_protocol: CASE-P003
```

Only after this record exists should deterministic ordering be calculated.

---

## 27. Compact Protocol

```text
1. Freeze six domains.
2. Identify four eligible cases per domain.
3. Record discovery and eligibility provenance.
4. Freeze all 24 candidates.
5. Apply SHA-256 ordering using seed 2026100202.
6. Select one case from each domain before repeating a domain.
7. Perform Stage A without IDOS interpretation.
8. Apply existing-theory baseline.
9. Map IDOS with O / I / U / N discipline.
10. Run removal and Red Team tests.
11. Preserve negative and null results.
12. Do not repair the architecture case-by-case.
13. Review architecture after one six-domain cycle unless a decisive contradiction occurs earlier.
```

---

## 28. Protocol Principle

**Random Selection ≠ Unbiased Candidate Pool**

Therefore:

**Domain Balance → Candidate-Pool Freeze → Mechanical Selection → Prospective Stress Test**

The purpose is not to guarantee that IDOS survives heterogeneous cases.

The purpose is to make it increasingly difficult for IDOS to survive merely because the research repeatedly selects the kinds of cases from which the architecture was developed.

---

## 29. Final Status

```yaml
CASE_SAMPLING_PROTOCOL_v0.2:
  status: PROSPECTIVE
  adopted: 2026-10-02
  applies_from: CASE-P003
  supersedes_for_future_cases: CASE_SAMPLING_PROTOCOL_v0.1
  retroactive_effect_on_P001_P002: NONE
  domain_stratification: ENABLED
  candidate_pool_freeze_required: YES
  deterministic_selection: SHA-256
  selection_seed: 2026100202
  first_cross_domain_review_after: 6_v0.2_cases
```

Any future revision must be prospective, versioned, justified, and must not alter the historical selection status of cases already drawn.
