# CASE-P005 — Deepwater Horizon Process-Safety Failure
## IDOS Prospective Cross-Domain Validation Case

**Case ID:** CASE-P005  
**Domain / Stratum:** D6 — Physical / Engineering / Infrastructure System  
**Selected Candidate:** D6-03 — Deepwater Horizon Process-Safety Failure  
**Selection Method:** Deterministic SHA-256 ordering  
**Seed:** `2026100202`  
**Cycle:** CASE_SAMPLING_PROTOCOL_v0.2 — Cycle 1  
**Cycle Position:** 3 of 6  
**Master Map Baseline:** `MASTER_MAP_v1.0` — FROZEN  
**IDOS Analysis Status at Selection:** NOT STARTED  
**Primary Source Family:** U.S. Chemical Safety Board (CSB), Macondo Blowout and Explosion Investigation  
**Purpose:** Prospective, cross-domain stress test of IDOS concepts and architecture using a complex physical/engineering failure case.

---

# 0. Case Selection Record

The frozen candidate ordering for D6 was:

1. D6-03 — Deepwater Horizon Process-Safety Failure — `05fcb5a0...`
2. D6-04 — I-35W Bridge Collapse — `0ea79d3f...`
3. D6-01 — 2021 Winter Storm Uri Grid Failure — `53e2889e...`
4. D6-02 — August 2003 Northeast Blackout — `5898bea4...`

Therefore:

$$
\boxed{
\text{CASE-P005 = Deepwater Horizon Process-Safety Failure}
}
$$

---

# 1. Stage A — Theory-Neutral Reconstruction

## A1. Empirical setting

On April 20, 2010, the Deepwater Horizon drilling rig was conducting temporary-abandonment operations at the Macondo well in the Gulf of Mexico. During this process, well control was lost, hydrocarbons entered the rig, explosions and fire occurred, eleven workers were killed, and the rig later sank.

At this stage, the case is not described using IDOS terms such as Residual, Holding, Update, or System Update.

The minimum theory-neutral structure is:

$$
\boxed{
\text{Operational well system}
\rightarrow
\text{Temporary-abandonment operations}
}
$$

## A2. Pre-incident system

The relevant system included at least:

- Macondo well;
- Deepwater Horizon rig;
- drilling mud / seawater system;
- cement barrier;
- blowout preventer (BOP);
- drilling crew;
- BP personnel;
- Transocean personnel;
- operating procedures;
- monitoring instruments;
- management systems.

The case is therefore treated as a **complex engineering system**, not as a single-component mechanical failure.

$$
\boxed{
\text{Physical equipment}
+
\text{Human operation}
+
\text{Procedures}
+
\text{Management system}
}
$$

## A3. Immediate operational context

A critical step in temporary abandonment was the negative pressure test.

Official investigation found that the test lacked clear written procedures, success criteria, and safe operating limits. The temporary-abandonment plan was also changed multiple times during the week before the accident, without clear evidence of adequate formal management-of-change or hazard assessment.

Theory-neutrally:

$$
\text{Operational Plan}
\rightarrow
\text{Repeated Changes}
$$

and:

$$
\text{Pressure Test}
\rightarrow
\text{Interpretation}
\rightarrow
\text{Operational Decision}
$$

## A4. Critical test interpretation

A central empirical fact is that the pressure-test result was not interpreted in a way that matched the actual well condition.

The test was treated as indicating adequate well integrity, but the hydrocarbon zone was not actually securely isolated.

Therefore:

$$
\boxed{
\text{Measured Signals}
\rightarrow
\text{Operational Interpretation}
}
$$

did not match:

$$
\boxed{
\text{Actual Well Condition}
}
$$

At this stage, the mismatch is not yet called an IDOS `Difference` or `Residual`.

## A5. Subsequent operation

Following the interpretation that the well was secure, abandonment operations continued. Drilling mud was displaced by seawater, reducing hydrostatic pressure.

The physical sequence became:

$$
\text{Hydrocarbon influx}
\rightarrow
\text{Loss of well control}
$$

The accident was investigated as involving multiple direct and contributing causes and multiple barrier failures.

## A6. Escalation

The physical escalation can be represented as:

$$
\boxed{
\text{Well Control Loss}
\rightarrow
\text{Hydrocarbon Release}
\rightarrow
\text{Emergency Barrier Failure}
\rightarrow
\text{Explosion / Fire}
}
$$

The BOP failed to seal the well. Post-incident engineering analysis identified drillpipe buckling and off-center positioning as important elements of the failure mechanism.

## A7. Observable consequences

Observed consequences included:

- 11 fatalities;
- injuries;
- major fire;
- rig loss;
- rig sinking;
- prolonged oil release.

Thus:

$$
\boxed{
\text{Pre-incident operational state}
\neq
\text{Post-incident physical state}
}
$$

## A8. Not a single-failure case

The official investigations addressed interacting technical, operational, procedural, and organizational conditions, including:

- cement barrier;
- pressure-test interpretation;
- operating procedure;
- management of change;
- hazard assessment;
- crew response;
- BOP;
- safety-critical equipment management.

Therefore:

$$
\boxed{
\text{Accident}
\neq
\text{Single Component Failure}
}
$$

and more cautiously:

$$
\boxed{
\text{Multiple interacting technical, operational, and organizational conditions}
\rightarrow
\text{Catastrophic outcome}
}
$$

## A9. Earlier signals and prior incidents

Before Macondo, related well-control incidents and lessons existed within organizational history.

A prior Transocean incident had produced an Operations Advisory, and Deepwater Horizon itself had experienced a well-kick event roughly one month before the accident.

Thus:

$$
\text{Earlier Incident}
\rightarrow
\text{Recorded Information}
$$

existed, but:

$$
\text{Recorded Information}
\rightarrow
\text{Effective Operational Change}
$$

was not clearly established.

## A10. Measurement issue

Official investigation also criticized the emphasis on personal-safety indicators relative to process-safety indicators.

Thus:

$$
\boxed{
\text{What was measured}
}
$$

was not identical to:

$$
\boxed{
\text{What catastrophic risk was developing}
}
$$

The theory-neutral statement is:

> The safety indicators in use did not capture all dimensions of major-accident risk.

## A11. Minimal temporal reconstruction

$$
\boxed{
\text{Exploratory well completed}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Temporary abandonment preparation}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Pressure testing}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Test interpretation}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Continuation of abandonment operations}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Hydrocarbon influx}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Loss of well control}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Emergency barrier failure}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Explosion, fire, sinking, spill}
}
$$

## A12. Observable vs inferred

Relatively direct evidence includes:

- operating plans;
- pressure measurements;
- equipment configuration;
- operational actions;
- hydrocarbon influx;
- fire / explosion;
- BOP physical state;
- fatalities / injuries;
- sinking;
- oil release.

Reconstructed or inferred elements include:

- what operators internally believed;
- why specific test results were accepted;
- precise influence of management systems on individual decisions;
- exact causal contribution among interacting barriers;
- counterfactual outcomes under alternative actions.

Therefore:

$$
\boxed{
\text{Physical Evidence}
\neq
\text{Complete Reconstruction of Human / Organizational State}
}
$$

---

# Stage A-1 Freeze Statement

> **CASE-P005 concerns a complex offshore drilling system in which temporary-abandonment operations proceeded after pressure-test results were interpreted as indicating adequate well integrity. Subsequent operations were followed by hydrocarbon influx, loss of well control, failure of multiple preventive and emergency barriers, explosion and fire, loss of life, rig loss, and a prolonged oil release. Official investigations identify interacting technical, operational, procedural, and management-system conditions rather than a single isolated failure. Earlier well-control events and safety information also existed before the accident, but effective transfer into preventive operational change was incomplete.**

日本語：

> **CASE-P005は、Macondo油井のtemporary abandonment作業において、油井健全性を確認する圧力試験が安全側に解釈され、その後の作業継続中に炭化水素流入、well controlの喪失、複数の予防・緊急barrierの機能不全、爆発・火災、人的被害、リグ喪失、長期間の油流出へ至った複合工学システム事故である。公式調査はこれを単一故障ではなく、技術・操作・手続・management systemが相互作用した事故として扱っている。また事故以前にもwell-control関連の情報や類似事象が存在していたが、それが十分な予防的運用変更へ転換されたとは確認できない。**

---

# 2. Stage A-2 — Evidence / Barrier / Causal Boundary Reconstruction

## Evidence classes

### E1 — Real-time observable evidence

Examples:

- drillpipe pressure;
- kill-line pressure;
- mud flow;
- pit volume;
- pump behavior;
- equipment configuration;
- negative-pressure-test readings.

Key distinction:

$$
\boxed{
\text{Available}
\neq
\text{Recognized}
}
$$

### E2 — Pre-existing organizational knowledge

Prior well-control incidents and recorded lessons existed before Macondo.

Key distinction:

$$
\boxed{
\text{Knowledge existed}
\neq
\text{Knowledge reached the relevant operation}
}
$$

### E3 — Procedural / design evidence

Examples:

- absence of clear test procedure;
- absence of explicit success criteria;
- repeated plan changes;
- weak formal management-of-change documentation.

### E4 — Post-incident reconstructed evidence

Examples:

- recovered BOP evidence;
- engineering simulation;
- pressure-data reconstruction;
- witness testimony;
- component testing.

Key distinction:

$$
\boxed{
\text{Known after accident}
\not\Rightarrow
\text{Knowable by operators before accident}
}
$$

## Barrier reconstruction

A useful theory-neutral barrier structure is:

$$
\boxed{
\text{Formation Isolation}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Integrity Verification}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Operational Detection / Response}
}
$$

$$
\downarrow
$$

$$
\boxed{
\text{Emergency Containment}
}
$$

The accident is better represented as interacting and sequential barrier degradation than as a single-failure event.

## Causal boundary

Three levels are distinguished.

### C1 — Immediate physical causation

$$
\text{Hydrocarbon influx}
\rightarrow
\text{Loss of well control}
\rightarrow
\text{Release}
\rightarrow
\text{Ignition}
\rightarrow
\text{Explosion / Fire}
$$

### C2 — Operational causation

$$
\text{Test}
\rightarrow
\text{Interpretation}
\rightarrow
\text{Decision}
\rightarrow
\text{Mud displacement}
\rightarrow
\text{Loss of hydrostatic control}
$$

### C3 — Organizational / system conditions

Includes:

- procedures;
- training;
- management of change;
- incident learning;
- safety metrics;
- barrier management.

But:

$$
\boxed{
\text{Organizational condition}
\neq
\text{Direct physical cause}
}
$$

## Hindsight boundary

$$
\boxed{
\text{Evidence}_{investigator}
\neq
\text{Evidence}_{operator,t}
}
$$

The information set available after the accident must not be projected backward onto the real-time operator.

## Counterfactual boundary

$$
\boxed{
\text{Observed history}
\neq
\text{Counterfactual history}
}
$$

Claims such as “the accident would have been prevented if…” remain counterfactual.

---

# Stage A-2 Freeze Statement

> **CASE-P005 contains multiple empirically distinguishable evidence layers. Some information relevant to well integrity and well-control risk was available in real time to operators; additional knowledge existed elsewhere in organizational records and prior incidents; and further mechanisms, particularly aspects of BOP failure and the full causal sequence, became reconstructable only after the accident through physical examination, engineering analysis, testimony, and data integration. The accident should therefore not be reconstructed from a single hindsight information set. Its barrier structure is more defensibly represented as a sequence of interacting physical, verification, operational, and emergency-containment barriers embedded within broader procedural and management conditions.**

日本語：

> **CASE-P005には、経験的に区別可能な複数の証拠層が存在する。油井健全性やwell-control riskに関する一部の情報は事故進行中に現場で観測可能であり、別の知識は過去事故や組織内部の記録として事故前から存在していた。一方、BOPの詳細な故障機構や完全な因果連鎖の一部は、事故後の物理検査、工学分析、証言、データ統合によって初めて再構成された。したがって、事故を単一の「後知恵の情報集合」から再構成してはならない。事故のbarrier構造は、物理barrier、verification barrier、operational detection/response、emergency containmentが、より広い手続・management system条件の中で相互作用しながら劣化したものとして表現するのが妥当である。**

---

# 3. Stage B — IDOS Blind Mapping

The frozen evidence is mapped to IDOS concepts without changing the theory-neutral reconstruction.

Status categories:

- **Direct**
- **Supported Inference**
- **Unobservable**
- **Not Established**

## Blind Mapping Matrix

| IDOS concept | P005 mapping | Status |
|---|---|---|
| Reality | Actual well / physical system | **Direct** |
| Difference | Pressure / expected-state discrepancy | **Supported–Direct** |
| Representation | Well interpreted as sufficiently secure | **Supported Inference** |
| Residual | Unresolved discrepancy after interpretation | **Supported candidate** |
| Holding | Difference kept open without closure | **Not Established** |
| Selection | Continue abandonment operations | **Direct outcome / mechanism unobservable** |
| Transformation | Operational state changed | **Direct** |
| Update | Difference-driven adaptive transformation | **Not Established** |
| History | Earlier incidents / records | **Direct** |
| Provenance use | Prior history influencing later operation | **Incomplete / weak** |
| Measurement | Safety/test measurement configuration | **Supported** |
| Reference Frame | Operator interpretive frame | **Inferred** |
| Possibility Space | Available alternatives | **Partially inferable** |
| Trajectory | Accident progression | **Directly reconstructable** |
| Limit | Independent IDOS process | **Not Established** |
| Enactment | Operational actions affecting Reality | **Direct** |
| Reality Recontact | Subsequent physical feedback | **Direct** |
| Reopening | Independent process | **Not Established** |
| Cross-unit Update | Knowledge propagation across organizations | **Supported problem** |
| System Update | Organization-wide effective learning | **Not demonstrated** |

A key result is that the full provisional 12PDM does **not** map cleanly or uniformly.

The stronger structure is:

$$
\boxed{
\text{Reality}
\rightarrow
\text{Measurement / Observation}
\rightarrow
\text{Difference}
\rightarrow
\text{Selective Response}
\rightarrow
\text{Enactment}
\rightarrow
\text{Reality Recontact}
\rightarrow
\text{New Difference}
}
$$

with History / Provenance and cross-unit propagation as lateral structures.

---

# Stage B Freeze Statement

> **Blind mapping of CASE-P005 to IDOS does not support a claim that all elements of the provisional 12PDM are independently observable in the case. Reality contact, measurement, Difference, operational Representation, selection outcomes, enactment, subsequent Reality recontact, and historical/provenance structures can be mapped with relatively strong empirical support. Residual is supportable only as a candidate unresolved discrepancy; Holding, full Possibility-Space dynamics, Limit, and an independent Reopening process cannot be established directly from the available evidence. Cross-unit knowledge propagation and the distinction between local learning and System Update emerge as particularly strong architectural features of the case.**

日本語：

> **CASE-P005をIDOSへblind mappingした結果、provisional 12PDMの全要素が独立して観測できるとは支持されなかった。一方、Reality contact、Measurement、Difference、operational Representation、Selectionの結果、Enactment、その後のReality Recontact、およびHistory / Provenanceについては比較的強い経験的対応が確認できる。Residualは未解消の不一致として候補化できるが、Holding、完全なPossibility-Space dynamics、Limit、独立したReopening processについては現在の証拠から直接確立できない。また、組織間・単位間における知識伝播と、局所的学習とSystem Updateの非同一性が、このケースにおける特に強いarchitecture-level構造として現れた。**

---

# 4. Stage C — Alternative Explanation / Rival Framework Test

Rival frameworks considered:

- Swiss Cheese Model;
- STAMP / CAST;
- High Reliability Organization (HRO);
- Resilience Engineering / Safety-II;
- Normal Accident Theory;
- organizational learning and information-flow perspectives.

## Core result

P005 does not require IDOS for domain-level accident explanation.

Barrier failure, control failure, process-model mismatch, weak-signal handling, management structure, and organizational learning can already be described by established theories.

Therefore:

$$
\boxed{
\text{P005 Accident Causation}
\not\Rightarrow
\text{Need for IDOS}
}
$$

The strongest remaining candidate for IDOS is at a different level:

$$
\boxed{
\text{Difference}_i
\rightarrow
\text{Update}_i
\rightarrow
\text{Difference}_j
\rightarrow
\text{Update}_j
\rightarrow
\text{Relational/System Update}
}
$$

That is, IDOS may function as a **general update architecture**, not as a replacement accident theory.

---

# Stage C Freeze Statement

> **Rival-framework analysis does not support treating IDOS as necessary for explaining the Deepwater Horizon accident itself. Barrier-based models and the Swiss Cheese Model can explain interacting layers of defense failure; STAMP/CAST can account for feedback, control, process-model mismatch, organizational structure, and unsafe control actions; and HRO and resilience perspectives can address weak-signal recognition, reluctance to simplify, communication, organizational learning, and adaptive capacity. Accordingly, these phenomena should not be treated as distinctive explanatory achievements of IDOS. The remaining candidate contribution of IDOS lies at a different level: a general architecture for tracing how Difference is generated, represented, propagated across heterogeneous Updating Units, selectively transformed or not transformed, incorporated into relations and Measurement Systems, and ultimately converted—or not converted—into System Update. This architecture-level contribution remains a hypothesis requiring further comparative testing.**

日本語：

> **競合理論との比較の結果、Deepwater Horizon事故そのものを説明するためにIDOSが必要であるとは支持されなかった。Barrier modelやSwiss Cheese Modelは複数防御層の失敗を説明でき、STAMP/CASTはfeedback、control、process-model mismatch、組織構造、unsafe control actionを扱える。またHROやResilience Engineeringはweak signalの認識、単純化への抵抗、communication、organizational learning、adaptive capacityを説明できる。したがって、これらをIDOS固有の説明成果として扱うべきではない。一方、IDOSに残る候補的価値は別の抽象度にある。すなわち、Differenceが生成され、表象され、異種Updating Unit間を伝播し、選択的にTransformationされるかされないか、RelationやMeasurement Systemへ組み込まれ、最終的にSystem Updateへ変換されるか否かを横断的に記述する一般的update architectureである。このarchitecture-levelの差分は現時点では仮説であり、さらなる比較検証を必要とする。**

---

# 5. Stage D — IDOS Added-Value / Necessity Test

The removal test asks:

$$
\boxed{
\text{Remove IDOS: what becomes impossible to describe?}
}
$$

## Main results

Most individual IDOS process concepts are not necessary for explaining P005.

| IDOS element | Remove and still explain P005? | Added value |
|---|---:|---:|
| Difference | Yes | Low |
| Residual | Yes | Low |
| Holding | Yes | Low |
| Selection | Yes | Low–Medium |
| Transformation | Yes | Low |
| Reality Recontact | Mostly | Medium |
| History / Provenance | Yes | Medium |
| Reference Frame | Yes | Low–Medium |
| Measurement System | Yes | Medium |
| Possibility Space | Yes | Low |
| Trajectory | Yes | Low |
| Limit | Yes | Very low |
| Reopening | Yes | Very low |
| Cross-unit Update | Yes, but coarser | **High candidate** |
| Relational Update | Yes, but coarser | **Medium–High** |
| System Update | Yes, but coarser | **High candidate** |
| Heterogeneous Interoperability | Not tested | Unknown |

The most important remaining question is:

$$
\boxed{
\text{How does locally generated knowledge become System Update?}
}
$$

---

# Stage D Freeze Statement

> **The IDOS removal test shows that most individual process concepts are not necessary to explain CASE-P005. Difference, Residual, Holding, Selection, Reference Frame, Possibility Space, Limit, and Reopening can largely be replaced by established concepts from safety engineering, organizational theory, or ordinary causal description without losing the core accident explanation. The strongest candidate added value of IDOS appears at a higher architectural level: distinguishing local Update from relational and System Update, tracing Update-to-Difference propagation across multiple Updating Units, treating History/Provenance and Measurement Systems as components of future update capacity, and maintaining Reality Recontact as a recurrent condition rather than terminating analysis at internal decision or transformation. Even these features are not yet established as theoretically unique; their current value is primarily integrative and descriptive.**

---

# 6. Stage E — Failure / Falsification Pressure Test

P005 cannot falsify IDOS as a whole. Falsification pressure must be separated across:

1. mechanism;
2. process model;
3. architecture.

## Failure criteria

| IDOS claim | Failure / weakening condition |
|---|---|
| Difference ≠ Update | Difference-to-Update is effectively automatic and no distinction is needed |
| Residual independent status | Difference and Residual cannot be reproducibly distinguished |
| Holding independent status | Cannot be distinguished from delay / selection / uncertainty management and adds no value |
| Selection mechanism | Same explanation/prediction is possible without independent Selection variable |
| Reality Recontact | Meaningful Update/Validation can systematically close without recontact |
| Cross-unit Update | Multi-unit change is fully captured by simple communication/copy |
| Relational Update | Relation state reduces without loss to component states |
| System Update | System change reduces to the sum of component changes |
| Reference Frame | Simpler information/model variables fully substitute |
| Reflexive Measurement | Treating Measurement System as a state adds no value |
| 12PDM | Repeated cases fail to identify the proposed processes |
| IDOS architecture | Existing architecture gives equal or greater coverage with lower complexity |

## Critical anti-falsification rule

IDOS must not become compatible with every possible observation.

Statements such as:

- “if Difference was not observed, it was hidden”;
- “if Update did not occur, Holding must have occurred”;
- “if Holding was absent, Residual must have been erased”

would destroy empirical content.

Therefore:

$$
\boxed{
\text{Observed}
\neq
\text{Inferred}
\neq
\text{Unobservable}
}
$$

must remain enforced.

---

# Stage E Freeze Statement

> **CASE-P005 does not falsify the minimal IDOS architecture, but it places substantial falsification pressure on several provisional process concepts. Residual, Holding, Limit, Reopening, and parts of the 12PDM are not independently required or directly observable in this case and should not be protected by post-hoc reinterpretation. The minimal distinctions between Difference and Update, transformation and Reality recontact, local and System Update, and the possibility of cross-unit propagation remain viable but are not uniquely confirmed. Architecture-level falsification would require stronger evidence: for example, showing that heterogeneous systems cannot be meaningfully described through a common update grammar, that relational/system-level dynamics reduce without loss to component-level dynamics, or that an existing architecture provides equal or greater descriptive, measurement, and implementation coverage with lower conceptual complexity.**

---

# 7. Stage F — Incremental Explanatory Value Test

The comparison target is:

$$
\boxed{
\text{Existing Framework + IDOS}
>
\text{Existing Framework Alone}?
}
$$

## Result

IDOS does not materially improve domain-level causal explanation.

The candidate gain is primarily **cross-unit / system-level descriptive integration**.

| Target | Existing framework alone | + IDOS | Incremental value |
|---|---|---|---|
| Physical accident causation | Strong | Strong | **Low** |
| Barrier analysis | Strong | Strong | **Low** |
| Signal / model mismatch | Strong | Strong | **Low** |
| Weak-signal handling | Strong | Strong | **Very Low** |
| Organizational learning | Strong | Strong | **Low–Medium** |
| Cross-unit failure localization | Medium | More explicit | **Medium–High** |
| Local vs System Update | Medium | Explicit hierarchy | **High candidate** |
| Relational change | Medium | Explicit | **Medium–High** |
| Measurement-system update | Medium | Explicit / reflexive | **Medium** |
| Frame / Boundary / Measurement coupling | Fragmented | Integrated | **Medium candidate** |
| Cross-scale common grammar | Fragmented | Intended core | **Not tested here** |
| Predictive improvement | — | — | **Not demonstrated** |
| Intervention improvement | — | — | **Not demonstrated** |

A useful decomposition of incremental value is:

$$
\boxed{
IEV=\{D,P,I,C\}
}
$$

where:

- \(D\): Descriptive gain;
- \(P\): Predictive gain;
- \(I\): Intervention gain;
- \(C\): Compression / Integration gain.

For P005:

- \(D\): Medium;
- \(P\): Not tested;
- \(I\): Not tested;
- \(C\): Medium candidate.

---

# Stage F Freeze Statement

> **The incremental-value test does not show that IDOS improves the domain-level causal explanation of CASE-P005. Existing safety and organizational frameworks already provide strong accounts of barrier failure, feedback and process-model mismatch, weak-signal handling, organizational learning, and control structure. The principal candidate incremental value of IDOS is instead descriptive and integrative: it provides an explicit grammar for tracing where locally generated Difference fails to propagate into another Updating Unit, where local change fails to become relational change, and where local learning fails to become System Update. It also makes Measurement Systems, Relations, and Reality Recontact explicit parts of the update architecture. However, no predictive gain, intervention gain, or cross-domain generalization has yet been demonstrated. IDOS should therefore not be treated as replacing domain theories in CASE-P005, but as a candidate meta-level architecture whose incremental value remains to be empirically tested.**

---

# 8. Stage G — Cross-Case Transfer Test

P005 was compared against prior prospective cases:

- CASE-P003 — Michigan ICU Keystone Infection-Reduction Intervention;
- CASE-P004 — Generative AI / Professional Writing.

## Repeated cross-case pattern

Across healthcare intervention, Human-AI professional work, and engineering failure:

$$
\boxed{
\text{Evidence at level }L_k
\not\Rightarrow
\text{Evidence at level }L_{k+1}
}
$$

Examples:

- P003: Outcome improvement does not establish System Update.
- P004: Performance improvement does not establish Human / Relational / System Update.
- P005: Local learning does not establish System Update.

A recurring architecture-level distinction is therefore:

$$
\boxed{
\text{Difference}
\not\Rightarrow
\text{Update}
}
$$

and:

$$
\boxed{
\text{Internal Change}
\not\Rightarrow
\text{Validated System Update}
}
$$

Reality Recontact also remained useful across the three cases.

## Repeated weakening

Across P003–P005:

- Holding as an independent mandatory stage: weak;
- Residual as independently measurable construct: weak;
- Limit as necessary process: weak;
- full 12PDM as universal empirical sequence: weak;
- predictive gain: not demonstrated.

## Emerging measurement target

A provisional research hypothesis emerged:

$$
\boxed{
\text{Future Updateability}
}
$$

meaning:

> The capacity of a Unit, Relation, or System to detect and selectively respond to subsequent Difference independently of current outcome improvement.

This is **not** yet a canonical IDOS construct.

---

# Stage G Freeze Statement

> **Cross-case transfer across CASE-P003, CASE-P004, and CASE-P005 shows that the principal residual structure identified in P005 is not confined to accident analysis. Across healthcare intervention, Human–AI professional work, and complex engineering failure, observable improvement or local change does not by itself establish Updating-Unit, Relational, or System Update. Evidence at one observational level does not automatically constitute evidence at the next level. Difference remains distinguishable from Update, and Reality Recontact remains a recurrently useful architectural distinction. In contrast, Holding, independently measurable Residual, and the necessity of the full 12PDM receive repeated weakening pressure across the three cases. Cross-unit propagation and Relational/System Update remain promising but incompletely operationalized. A new cross-case measurement target therefore emerges: Future Updateability—the capacity of a Unit, Relation, or System to detect and selectively respond to subsequent Difference independently of current outcome improvement. This is a research hypothesis, not yet a canonical IDOS construct.**

---

# 9. Stage H — Cross-Case Counterexample Test

The Stage G pattern was deliberately challenged.

## Counterexamples

### CE1 — Outcome Improvement may equal System Update

If the relevant system consists of a single Updating Unit and the observed outcome change is the system change itself, then:

$$
\text{Local Update}
=
\text{System Update}
$$

may be valid.

Therefore the stronger claim:

$$
\text{Outcome Improvement}
\neq
\text{System Update}
$$

is replaced by:

$$
\boxed{
\text{Outcome Improvement}
\not\Rightarrow
\text{System Update}
}
$$

### CE2 — Cross-unit propagation may be unnecessary

Single-unit systems or centrally controlled star-topology systems may not require:

$$
Update_i
\rightarrow
Difference_j
\rightarrow
Update_j
$$

### CE3 — Relation may be reducible

If:

$$
Relation_{ij}
=
f(State_i,State_j)
$$

with no loss of relevant information, an independent Relational Update construct may be unnecessary.

### CE4 — Future Updateability may be irrelevant

One-shot tasks, terminating systems, or very stable environments may not require future updateability as a measurement target.

### CE5 — Difference may not be required for every change

Exploration, random mutation, or internally generated transformation may challenge a universal:

$$
Difference
\rightarrow
Update
$$

claim unless Difference has independent identification criteria.

### CE6 — Reality Recontact requires operational boundaries

If Reality is defined too broadly as “anything constraining the system,” Reality Recontact becomes non-falsifiable.

---

# Stage H Freeze Statement

> **Cross-case counterexample testing weakens several universal formulations that appeared to emerge from CASE-P003–P005. Outcome Improvement is not necessarily distinct from System Update; rather, outcome evidence does not by itself entail System Update. Local and System Update may coincide when the local Updating Unit is itself the entire relevant system. Cross-unit propagation is therefore not a universal requirement but becomes analytically relevant when multiple semi-autonomous Updating Units exist. Likewise, Relational Update is useful only where relational state contributes information not reducible to component states. Future Updateability should be treated as a conditional measurement target for systems expected to continue encountering and responding to future Difference, not as an intrinsically desirable or universally relevant property. Reality Recontact remains a viable minimal architectural candidate, but its empirical use requires a domain-specific operational definition of what counts as Reality and Recontact. These counterexamples shift IDOS away from universal process claims and toward a conditional architecture whose distinctions become necessary under identifiable structural conditions.**

---

# 10. Stage I — Conditionality / Scope Boundary Test

The revised form is:

$$
\boxed{
\text{If structural condition }C\text{ holds, concept }X\text{ becomes useful / necessary.}
}
$$

## Conditional architecture matrix

| IDOS distinction | Becomes useful / necessary when... |
|---|---|
| Difference | non-identity materially affects subsequent response |
| Selection | multiple responses to Difference are possible |
| Holding | unresolved Difference must remain available across time |
| Residual | unresolved structure remains after attempted processing / translation |
| Reality Recontact | internal transformation can be wrong about an external or constraining reality |
| History / Provenance | path dependence affects current or future update |
| Updating Unit | update attribution depends on scale or boundary |
| Dynamic Boundary | the relevant system boundary changes |
| Cross-unit Update | multiple semi-autonomous Units exist |
| Relational Update | relation state is not reducible to component states |
| System Update | system change is not reducible to the sum of component changes |
| Measurement System | observability materially depends on measurement configuration |
| Reflexive Measurement | the Measurement System itself changes |
| Reference Frame | interpretive structure materially changes observations / Differences / actions |
| Possibility Space | Update changes future reachability |
| Future Updateability | continued adaptation to future Difference is part of the task |
| Heterogeneous Interoperability | materially different Units must coordinate without representational unification |
| CDP | heterogeneous representations need a common operational interface |

## P005 scope result

### Strongly applicable

- Difference;
- Selection;
- Reality Recontact;
- History / Provenance;
- Updating Unit;
- Cross-unit Update;
- System Update;
- Measurement System.

### Moderately applicable

- Relational Update;
- Reference Frame;
- Future Updateability.

### Weak / not established

- Holding;
- Residual;
- Dynamic Boundary;
- Reflexive Measurement;
- Possibility Space.

### Essentially not tested

- Heterogeneous Interoperability;
- CDP;
- Translation Residual;
- DO / CFV / MU.

## Scope boundary

IDOS has low added value in systems approximating:

$$
\boxed{
\text{Single Unit}
+
\text{Fixed Boundary}
+
\text{Stable Measurement}
+
\text{No independent relational state}
+
\text{One-shot task}
}
$$

Its potential value increases as the system contains:

$$
\boxed{
\text{Heterogeneity}
+
\text{Semi-autonomy}
+
\text{Relational dependence}
+
\text{Reflexive measurement}
+
\text{Continued adaptation}
}
$$

---

# Stage I Freeze Statement

> **The Conditionality / Scope Boundary Test indicates that IDOS should not be treated as a universal process model applied with equal necessity to all systems. Its distinctions become analytically useful under identifiable structural conditions. Difference matters when non-identity affects subsequent response; Selection when multiple responses are possible; Holding when unresolved Difference must persist over time; Cross-unit Update when multiple semi-autonomous Units exist; Relational Update when relational state is not reducible to component states; System Update when system-level change cannot be represented as the sum of local changes; and Future Updateability when continued adaptation to future Difference is part of the task. Heterogeneous Interoperability and CDP become relevant only when materially different Units must coordinate without representational unification. CASE-P005 satisfies several lower-regime conditions but does not strongly test the full heterogeneous-intelligence architecture. Its principal contribution is therefore to identify which IDOS distinctions already matter in present-day complex systems and which require higher-complexity future regimes for meaningful validation.**

---

# 11. Stage J — Final Synthesis / Architecture Impact Classification

Classification categories:

- **KEEP**
- **WEAKEN**
- **CONDITIONALIZE**
- **DEMOTE**
- **NOT TESTED**

## Final architecture-impact table

| IDOS element | P005 impact |
|---|---|
| Reality Contact | **KEEP** |
| Difference | **KEEP** |
| Representation | **KEEP** |
| Residual | **WEAKEN** |
| Holding | **CONDITIONALIZE + WEAKEN** |
| Selection distinction | **KEEP** |
| Selection mechanism \(\Gamma\) | **WEAKEN / NOT TESTED** |
| Transformation | **KEEP** |
| Stabilization | **WEAKEN** |
| Reality Recontact | **KEEP + operational conditionality** |
| History / Provenance | **KEEP** |
| Updating Unit | **KEEP** |
| Dynamic Boundary | **NOT TESTED** |
| Possibility Space | **CONDITIONALIZE / WEAKEN** |
| Trajectory | **KEEP** |
| Limit | **DEMOTE** |
| Enactment | **KEEP** |
| Reopening | **DEMOTE** |
| 12PDM as universal sequence | **WEAKEN** |
| Cross-unit Update | **CONDITIONALIZE** |
| Relational Update | **CONDITIONALIZE** |
| System Update | **CONDITIONALIZE — high value in multi-unit systems** |
| Measurement System | **KEEP** |
| Reflexive Measurement | **NOT TESTED** |
| Reference Frame | **CONDITIONALIZE** |
| Heterogeneous Interoperability | **NOT TESTED** |
| CDP | **NOT TESTED** |
| Translation Residual | **NOT TESTED** |
| DO / CFV / MU | **NOT TESTED** |
| Future Updateability | **CONDITIONALIZE — Research Hypothesis** |

---

# 12. Final P005 Result

The most compact result is:

$$
\boxed{
\text{P005 does not validate IDOS;}
\quad
\text{it reduces and conditions it.}
}
$$

The strongest surviving distinctions are:

$$
\boxed{
\text{Reality}
\neq
\text{Observation}
}
$$

$$
\boxed{
\text{Difference}
\not\Rightarrow
\text{Update}
}
$$

$$
\boxed{
\text{Transformation}
\rightarrow
\text{Reality Recontact}
}
$$

$$
\boxed{
\text{Evidence}_{L_k}
\not\Rightarrow
\text{Evidence}_{L_{k+1}}
}
$$

and, conditionally:

$$
\boxed{
\text{Local Update}
\not\Rightarrow
\text{System Update}
}
$$

In systems with multiple semi-autonomous Units, additional attention should be given to:

$$
\boxed{
\text{Cross-Unit Propagation}
}
$$

and:

$$
\boxed{
\text{Relational / System Update}
}
$$

---

# 13. Impact on MASTER_MAP_v1.0

## Immediate revision

$$
\boxed{
\text{NO CHANGE}
}
$$

P005 does not require an immediate revision of `MASTER_MAP_v1.0`.

The current Master Map already distinguishes:

- IDOS from 12PDM;
- architecture from mechanism;
- canonical from provisional;
- observed from inferred / unobservable;
- minimal General Update from detailed process models;
- local from relational / system-level change;
- theory from measurement;
- present architecture from future empirical revision.

Therefore P005 should be recorded as:

$$
\boxed{
\text{Accumulating Empirical Pressure}
}
$$

on provisional mechanisms, not as a trigger for immediate canonical change.

## 12PDM monitoring note

Across P003, P004, and P005, repeated weakening pressure has appeared around:

- independent Holding;
- independently measurable Residual;
- Limit;
- Reopening;
- universal necessity of the full 12PDM sequence.

A future revision trigger may be appropriate if additional prospective cases reproduce the same pattern.

---

# 14. Research Significance

The value of CASE-P005 is not that IDOS successfully “explained” Deepwater Horizon.

Most domain-level explanation was already available through established safety and organizational frameworks.

The stronger research result is that the validation procedure was able to:

1. reconstruct the case without IDOS;
2. separate real-time evidence from hindsight reconstruction;
3. map the case to IDOS without forcing full 12PDM fit;
4. return large portions of explanation to existing theories;
5. remove IDOS concepts and test what remained;
6. define falsification conditions;
7. evaluate incremental explanatory value;
8. compare the result with other domains;
9. actively search for counterexamples;
10. convert apparent universal claims into conditional architecture;
11. classify architecture impact without revising the frozen Master Map prematurely.

Therefore P005 functions primarily as:

$$
\boxed{
\text{Architecture Reduction}
+
\text{Scope Conditioning}
+
\text{Cross-Domain Stress Test}
}
$$

rather than as a validation case.

---

# 15. Final Freeze Statement

> **CASE-P005 should be classified as an architecture-reduction and scope-conditioning case rather than a validation case. It does not demonstrate superior domain-level causal explanation by IDOS and does not support treating the provisional 12PDM as a universal empirical sequence. Reality/Observation separation, Difference/Update separation, Reality Recontact, History/Provenance, Updating Unit, and Measurement-System sensitivity remain viable. Residual, Holding, Stabilization, Limit, Reopening, and several detailed process claims receive weakening or demotion pressure. Cross-unit, Relational, and System Update remain useful only under identifiable structural conditions, particularly in systems containing multiple semi-autonomous Units whose changes do not automatically propagate. Heterogeneous Interoperability, CDP, Translation Residual, dynamic Boundary change, reflexive Measurement, and related future-regime constructs remain largely untested by this case. No immediate revision of MASTER_MAP_v1.0 is required; the appropriate action is to preserve these results as accumulating empirical pressure on provisional mechanisms while continuing prospective cross-domain testing.**

日本語：

> **CASE-P005はIDOSのvalidation caseではなく、architecture reductionおよびscope conditioning caseとして位置づけるべきである。IDOSがdomain-levelな事故因果説明で既存理論を上回ることは示されず、provisional 12PDMを普遍的な経験的sequenceとして扱う根拠も得られなかった。一方、RealityとObservationの分離、DifferenceとUpdateの分離、Reality Recontact、History / Provenance、Updating Unit、Measurement Systemの重要性は維持された。Residual、Holding、Stabilization、Limit、Reopeningおよび複数の詳細process claimには弱化またはdemotion圧力がかかった。Cross-unit、Relational、System Updateは、複数のsemi-autonomous Unitが存在し、あるUnitの変化が他Unitへ自動伝播しないといった識別可能な構造条件のもとでのみ高い分析価値を持つ。Heterogeneous Interoperability、CDP、Translation Residual、Dynamic Boundary、Reflexive Measurement等のfuture-regime constructは本ケースではほぼ未検証である。MASTER_MAP_v1.0を直ちに変更する必要はなく、今回の結果はprovisional mechanismに対する累積的なempirical pressureとして保存し、prospectiveなcross-domain testingを継続するのが適切である。**

---

# 16. Primary Source Links

- U.S. Chemical Safety Board — Macondo Blowout and Explosion Investigation  
  https://www.csb.gov/macondo-blowout-and-explosion/

- CSB — Deepwater Horizon / Macondo final-report materials  
  https://www.csb.gov/

- Bureau of Safety and Environmental Enforcement — Deepwater Horizon Joint Investigation  
  https://www.bsee.gov/

---

# 17. Repository Note

Recommended status:

```yaml
case_id: CASE-P005
case_name: Deepwater Horizon Process-Safety Failure
sampling_protocol: CASE_SAMPLING_PROTOCOL_v0.2
master_map_baseline: MASTER_MAP_v1.0
analysis_mode: prospective
status: FROZEN
classification:
  - architecture_reduction
  - scope_conditioning
  - cross_domain_stress_test
master_map_revision_required: false
main_negative_pressure:
  - residual_independent_status
  - holding_as_universal_stage
  - stabilization_as_independent_stage
  - limit_as_independent_process
  - reopening_as_independent_process
  - full_12PDM_universal_sequence
main_retained_distinctions:
  - reality_vs_observation
  - difference_not_imply_update
  - reality_recontact
  - history_provenance
  - updating_unit
  - measurement_system
conditional_high_value:
  - cross_unit_update
  - relational_update
  - system_update
emerging_research_hypothesis:
  - future_updateability
future_regime_not_tested:
  - heterogeneous_interoperability
  - CDP
  - translation_residual
  - dynamic_boundary_change
  - reflexive_measurement
  - DO_CFV_MU
```

---

# 18. Suggested Commit Message

```text
Add CASE-P005 Deepwater Horizon architecture-reduction validation
```
