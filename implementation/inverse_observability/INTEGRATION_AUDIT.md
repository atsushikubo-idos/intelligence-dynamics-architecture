# IDOS Inverse Observability v0.1–v0.8 — Integrated Audit

**Audit date:** 2026-11-05  
**Evidence reviewed:** The uploaded `intelligence-dynamics-architecture-main (18)(1).zip`, plus the separately produced v0.1–v0.8 local artifacts. **This was not an audit of the latest live GitHub commit.**

## Overall judgment

**Retain as independent exploratory and verification research. Do not promote it to the frozen MASTER_MAP or externally claim that it is an engine that discovers unknown structures.**

Ninety-two out of ninety-two automated tests passed across the eight independent versions (7, 9, 18, 12, 8, 9, 14, and 15 tests respectively). Passing those tests establishes defined implementation behavior under test conditions, **not** independent theoretical validation, 12PDM validity, or an end-to-end empirical result.

## 1. Definition audit: 12PDM / 12CDP

- Section 9 of `architecture/MASTER_MAP_v1.1.md` places **12PDM** under **Dynamic Observation / Description Protocol**, not as a required Core constituent.
- The historical sequence is: **Reality → Difference → Representation → Residual → Holding → Update → Possibility Space → Trajectory → Limit → Enactment → Reality′ → Reopening**.
- `measurement/MEASUREMENT_OBSERVABILITY_PROTOCOL_v0.3.md` also uses the earlier **12CDP** label and requires evidence-first observation, O/P/I/U observability classifications, and reference-frame, boundary, measurement, and provenance records.
- Do **not** treat the sequence as mandatory order, twelve independent sensors, or twelve numerical scores. Statistical residual ≠ IDOS `Residual`; observed waiting time ≠ `Holding`; a lower prediction error ≠ `Future Updateability`.
- `CommonDynamicsProtocol` / `CDPDescription` in `src/idos_reference_v1_1.py` should **not** automatically be identified with the historical 12CDP entries; the acronym can refer to a different abstraction.

## 2. Verified functions and limitations by research version

| Version | Implemented check | Data | Not demonstrated |
|---|---|---|---|
| v0.1 | Observability rank for known A/C matrices | Synthetic 2D system | Unknown dynamics or latent-variable existence |
| v0.2 | Finite-horizon distinguishability of two specified models | Synthetic, noise-free | Arbitrary model discovery or causal identification |
| v0.3 | Second-difference elimination of unknown initial level/drift; noisy decisions | Synthetic, known noise scale | General latent-state recovery |
| v0.4 | Selection among lag candidates 0–3 using residual structure | Synthetic event data | Rule discovery outside the candidate class |
| v0.5 | Held-out macro time-series comparison (AR(4) vs selected lagged covariate) | Real macro series | Hidden variables, 12PDM validity, causation |
| v0.6 | Business event-log CSV analyzer and time-based split | Synthetic event log | Generalization to real organizational logs |
| v0.7 | Expected information gain and selection for supplied hypotheses | Synthetic likelihoods | Unknown-hypothesis discovery or real-data likelihood calibration |
| v0.8 | Model-family adequacy testing and comparison stops | Synthetic Gaussian settings | Root-cause attribution or reference-frame creation |

Reproduction at audit time used `python -m unittest discover -p 'test*.py' -q` separately in each version folder, yielding the counts shown above. Do not interpret those separate tests as a single integrated-system validation.

## 3. Overlap with the existing IDOS source

- `implementation/discovery_architecture/discovery_architecture.py` (`DiscoveryCycle`) already records differences, proposes reference-frame candidates, and supports recontact/condition revision.
- `implementation/discovery_architecture/intervention_design.py` addresses intervention specifications and execution records.
- `implementation/discovery_architecture/emergent_engine/engine.py` contains `ResidualGenerator`, `InterventionPlanner`, and `Engine`; concept-level candidate generation is not new to this adapter.
- `src/idos_reference_v1_1.py` contains `ReferenceFrame`, `MeasurementSystem`, `Trajectory`, and `ProvenanceEvent`.
- The proposed **narrow additional numerical role** is observability, hypothesis discrimination, information-theoretic observation ranking, and open-set/model-family audits. Direct source-level integration with Reference v1.1 and Discovery Architecture was **not** verified.

### Pre-integration gap

At the time of this audit, v0.6 output had **not** supplied fitted likelihoods to v0.7; v0.8's model family and noise were also specified separately. Hence the separate versions did not demonstrate a single v0.6 → v0.7 → v0.8 evidence-driven pipeline. The accompanying **later synthetic integrated pilot** addresses this gap in a limited same-source demonstration; see [RESEARCH_NOTES.md](RESEARCH_NOTES.md), but that does not establish real-world effectiveness.

## 4. Principal research weaknesses (priority order)

1. **No authorized primary organizational evidence:** No complete real-case set with case identifiers, time-stamped actions/outcomes, reference/measurement versions and provenance. The original BPI2012 event log was not obtained in this work.
2. **Earlier components were separately calibrated:** v0.7 likelihoods and v0.8 noise in their initial versions were stipulated rather than jointly learned. The later synthetic pilot only partially closes this gap.
3. **Insufficient comparative baselines:** Need comparisons with state-space/HMM methods, process mining, change-point detection, active learning, and optimal experimental design on matched samples.
4. **Identifiability is not proof of real-world structure:** Equivalent models, confounders, selection effects, leakage, and observer effects are not adequately excluded.
5. **IDOS-specific outcome undefined:** Specify measurable gains in identifying distinctions, retaining loss across frame changes, provenance completeness, and future re-updateability.
6. **Reality contact:** Link each purported 12PDM observation to primary evidence and distinguish observed data, inferred claims, competing interpretations, and missing records.

## 5. Proposed minimal interface (design only, not implemented)

`EvidenceRecord → ObservationContext → CandidateSet → TestReport → ObservationProposal → RecontactRecord`

| Component | Suggested fields / function |
|---|---|
| `EvidenceRecord` | `evidence_id`, `source`, `timestamp`, observed/inferred flag, `case_id`, `actor_id`, usage authorization |
| `ObservationContext` | `updating_unit_id`, `boundary_version`, `reference_frame_version`, `measurement_version`, `observer_id`, `time_basis`, `provenance_ids` |
| `CandidateSet` | Fixed candidate family, fitted model version, candidate origins and exclusion reasons |
| `TestReport` | Training/evaluation distinction, out-of-sample results, ambiguous/rejected/incomparable outcomes, baseline comparison |
| `ObservationProposal` | Expected information gain, cost, authority, reversibility, privacy impact, rejection reasons; **never an automatic intervention command** |
| `RecontactRecord` | Whether observation/intervention occurred, new primary evidence, cross-frame bridge, negative evidence, unresolved discrepancies |

The interface does **not** require numerical values for all twelve PDM elements. Optional 12PDM descriptions should have explicit primary-evidence references. No frozen-Core changes. Any call analogous to Discovery's `propose_frame` requires review and authorization.

## 6. Gates for the next empirical study

- Preregister the question, event definitions, observation window, missingness policy, unit of analysis, and endpoints.
- Obtain at least one appropriately authorized primary event log; otherwise do not claim external validity.
- Fit candidates, likelihoods, and noise properties using the same historical evidence, with strictly untouched later or independent evaluation data.
- Include no-extra-observation, standard process-mining, change-point, and conventional active-experiment baselines.
- Compare *predicted* information gain with *realized* gain from newly collected evidence.
- Preserve old-frame information and its losses when proposing a new reference frame.
- Retain unresolved cases and negative findings rather than forcing adoption of a candidate.

A possible IDOS-specific benefit would need independent evidence of either (a) distinguishing actual relationships missed by matched baselines, or (b) better maintaining evidence, information loss, provenance, and re-updateability across reference-frame changes. **Neither criterion has yet been met.**

## 7. Decision

- **Preservation:** Keep v0.1–v0.8 as unchanged research history; archive their findings through a consolidated README and audit, rather than re-copying every historical source.
- **Architecture:** Keep inverse-problem numerics as an independent experimental adapter callable by Discovery, not absorbed into frozen Core.
- **Next work:** Prioritize licensed real-log acquisition, evidence mapping, common data specifications, and matched baseline tests rather than incrementing the version number.
- **Permissible public claim:** “Implemented and independently tested restricted observability, candidate comparison, observation ranking, and model-family inadequacy checks.”
- **Impermissible claim:** “Analytically discovered unknown structures from 12PDM.”
