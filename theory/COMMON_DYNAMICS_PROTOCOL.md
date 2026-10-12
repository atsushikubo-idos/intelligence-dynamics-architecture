# Intelligence Dynamics Architecture

## Common Dynamics Protocol — CDP v1.0

**A Provisional Protocol for Dynamic Interoperability among Heterogeneous Updating Units**

## 1. Status of This Document

The Common Dynamics Protocol (CDP) is a provisional component of Intelligence Dynamics Architecture (IDOS).

It should be read together with:

* `CANONICAL_v1.0.md`
* `DYNAMICS_MODEL.md`
* `GLOSSARY.md`

CDP is not presented as:

* a universal internal architecture of intelligence,
* a universal ontology,
* a programming standard,
* a communication protocol in the conventional networking sense,
* or a scientifically validated representation of all intelligent systems.

Its purpose is narrower:

**CDP explores whether heterogeneous Updating Units can describe, compare, translate, and coordinate aspects of their dynamics without requiring their internal representations to become identical.**

Its central orientation is:

**Dynamic Interoperability without Representational Unification.**

Unless otherwise stated, CDP should be treated as:

**[P] Provisional**

## 2. Why a Common Dynamics Protocol?

Humans, AI systems, robots, organizations, institutions, and other Updating Units may differ radically in:

* internal representation,
* embodiment,
* architecture,
* memory,
* timescale,
* language,
* objectives,
* values,
* sensory access,
* Reference Frames,
* and available Possibility Spaces.

A common internal representation may therefore be impossible, undesirable, or unnecessary.

CDP asks a different question:

**Can heterogeneous systems remain internally different while making aspects of their updating dynamics mutually observable?**

The proposal is not to standardize what each system is internally.

It is to explore whether some aspects of:

* Reality Contact,
* Difference,
* Residual,
* Holding,
* Update,
* Trajectory,
* Boundary,
* Reference Frame,
* Possibility Space,
* Coupling,
* and transition

can be described at a sufficiently abstract level to support interoperability.

## 3. Core Principle

CDP separates:

**Internal Representation**

from:

**Dynamic Description**

Two Updating Units do not need identical internal states to describe that:

* something unexpected occurred,
* an existing model failed,
* uncertainty remains unresolved,
* a Reference Frame changed,
* a Boundary shifted,
* a Trajectory branched,
* or a previous possibility became unavailable.

Conceptually:

**Internal System A → CDP Description A**

**Internal System B → CDP Description B**

The CDP layer then attempts to support:

**Description → Translation → Comparison → Coordination**

without requiring:

**Internal System A = Internal System B**

## 4. CDP Is Not the Dynamics It Describes

A critical distinction is:

**Coupling ≠ CDP**

and more generally:

**Dynamics ≠ Description of Dynamics**

Coupling may occur whether or not CDP exists.

Residual may occur whether or not CDP records it.

Trajectories may transform whether or not they are represented through a protocol.

CDP is therefore not the cause of intelligence dynamics.

It is a candidate layer for making selected dynamics:

* observable,
* describable,
* exchangeable,
* comparable,
* and potentially governable.

## 5. Minimal CDP Record

A minimal CDP record may provisionally contain:

**CDPRecord**

* UpdatingUnit
* Time
* RealityContact
* Observation
* Difference
* Residual
* HoldingState
* Update
* TrajectoryReference
* ReferenceFrame
* Boundary
* PossibilitySpace
* Action
* Outcome
* Provenance
* EpistemicStatus

Not every system must populate every field.

Missing information is itself meaningful.

CDP should allow:

* unknown,
* unavailable,
* private,
* incommensurable,
* unresolved,
* or not-applicable

states rather than forcing false precision.

## 6. Updating Unit

Every CDP description requires a provisional answer to:

**What is being observed as the Updating Unit?**

This does not mean that the Updating Unit is permanently fixed.

A record may identify:

**UpdatingUnit**

* id
* type
* current_boundary
* parent_unit
* component_units
* temporal_scope
* confidence

Examples might include:

* a human,
* an AI system,
* a Human–AI configuration,
* a team,
* an organization,
* or another dynamically enacted unit.

However:

**Physical Entity ≠ Updating Unit**

and:

**Updating Unit identity may itself change.**

CDP must therefore allow Updating Units to:

* emerge,
* merge,
* split,
* become nested,
* dissolve,
* or be reidentified.

## 7. Reality Contact

A CDP record should distinguish between an internal representation and the event or condition through which renewed Reality contact occurred.

Possible dimensions include:

**RealityContact**

* source
* mode
* environment
* event
* intervention
* observed_consequence
* uncertainty

Examples of modes may include:

* direct observation,
* experiment,
* action consequence,
* external feedback,
* sensor input,
* institutional response,
* human interaction,
* environmental change.

CDP does not assume that Reality itself is fully encoded.

It records the mode of contact.

**Representation of Reality Contact ≠ Reality itself**

## 8. Difference and Residual

CDP distinguishes:

**Difference ≠ Residual**

A Difference records an observed mismatch, change, distinction, or deviation.

A Residual records the part that remains insufficiently absorbed by the currently operative structure.

A provisional description may include:

**Difference**

* description
* magnitude
* context
* confidence

**Residual**

* description
* related_difference
* precision
* salience
* persistence
* unresolved_aspects

Numerical fields are optional.

Structural or qualitative descriptions are legitimate.

## 9. Holding

CDP should allow unresolved Residual to remain unresolved.

A provisional description may include:

**Holding**

* active
* held_residuals
* reason
* duration
* competing_interpretations
* unresolved_constraints

The protocol should not require every Residual to be immediately classified as:

* solved,
* error,
* noise,
* or failure.

This is important because premature classification may erase information relevant to later transformation.

**Unresolved does not mean irrelevant.**

## 10. Update

CDP describes what changed after interaction with Residual, Reality, or other Updating Units.

A provisional description may include:

**Update**

* level
* changed_state
* changed_parameters
* changed_reference_frame
* changed_boundary
* changed_possibility_space
* reversibility
* confidence

The provisional Update levels are:

* **L1 — Local Absorption**
* **L2 — Parameter Update**
* **L3 — Frame Transformation**
* **L4 — Frame Traversal**
* **L5 — Possibility-Space Transformation / Generation**

These levels are not rankings of intelligence.

## 11. Reference Frame

CDP should make the operative Reference Frame explicit when possible.

A provisional description may include:

**ReferenceFrame**

* id
* assumptions
* distinctions
* categories
* scale
* relations
* interpretive_constraints
* provenance

The objective is not to fully encode every internal worldview.

It is to expose enough of the operative frame to understand why something became:

* visible,
* meaningful,
* anomalous,
* residual,
* or actionable.

A Reference Frame may change during interaction.

Therefore, both may be recorded:

**ReferenceFrame_before → ReferenceFrame_after**

## 12. Boundary

Because Updating Units are not assumed to be permanently fixed, CDP must allow their boundaries to change.

A provisional description may include:

**Boundary**

* included_processes
* excluded_processes
* external_dependencies
* permeability
* temporal_scope
* provenance

A Boundary transition may be represented as:

**Boundary_before → Boundary_after**

together with:

**Transition_reason**

This becomes especially important in:

* Human–AI collaboration,
* multi-agent systems,
* organizations,
* physical AI,
* distributed decision systems,
* and institutional networks.

## 13. Possibility Space

CDP distinguishes Reference Frame from Possibility Space.

**Reference Frame structures interpretation.**

**Possibility Space structures what may become available as an alternative.**

A provisional description may include:

**PossibilitySpace**

* available_actions
* available_frames
* available_relations
* available_trajectories
* excluded_or_unavailable_options
* generative_constraints

Changes may be recorded as:

**PossibilitySpace_before → PossibilitySpace_after**

CDP does not assume that the full Possibility Space is observable.

The description may remain partial.

## 14. Trajectory

CDP treats individual events as parts of histories.

A Trajectory reference may include:

**Trajectory**

* id
* prior_events
* update_history
* frame_history
* boundary_history
* coupling_history
* provenance
* current_phase

However:

**Trajectory-centered, but not trajectory-fixed.**

CDP must allow Trajectories to:

* emerge,
* persist,
* couple,
* branch,
* transition,
* become dormant,
* dissolve,
* and re-emerge.

Therefore, Trajectory identity should not be represented only by a permanent identifier.

Historical continuity and identity are separate questions.

## 15. Provenance and Causal Continuity

CDP should preserve provenance where possible.

A provisional provenance record may include:

**Provenance**

* source
* prior_record
* transformation
* timestamp
* responsible_unit
* confidence
* missing_history

This supports:

**Non-fixed, but traceable.**

However:

**Provenance ≠ guaranteed causal continuity**

A historical link does not prove that two processes should be treated as the same Trajectory.

CDP may therefore separately describe:

**CausalContinuity**

* candidate_relation
* supporting_evidence
* conflicting_evidence
* confidence
* unresolved

No universal criterion for Trajectory identity is currently claimed.

## 16. Coupling

CDP may describe interaction among multiple Trajectories.

A provisional description may include:

**Coupling**

* participating_trajectories
* directionality
* mutual_constraint
* persistence
* asymmetry
* dependency
* observed_effects

Coupling may be:

* symmetric or asymmetric,
* temporary or persistent,
* weak or strong,
* beneficial or harmful,
* reversible or difficult to reverse.

CDP must not assume that stronger Coupling is always desirable.

## 17. Enactment

Some Couplings may contribute to the emergence of higher-order Updating Units.

Conceptually:

**Multiple Trajectories → Coupling → Enactment → Updating Unit**

CDP may record candidate Enactment without claiming that a universal criterion already exists.

A provisional description may include:

**EnactmentCandidate**

* participating_units
* persistence
* mutual_constraint
* shared_update_history
* boundary_formation
* candidate_agency
* confidence
* status

The status may remain:

**unresolved**

when it is unclear whether a higher-order Updating Unit has actually emerged.

## 18. Translation

Translation is central to CDP.

Suppose System A uses an internal representation:

**A_internal**

and System B uses:

**B_internal**

CDP does not require:

**A_internal = B_internal**

Instead:

**A_internal → CDP_A ↔ CDP_B ← B_internal**

Translation may be:

* complete,
* partial,
* approximate,
* asymmetric,
* lossy,
* contested,
* or impossible.

CDP must therefore record translation quality.

A candidate description includes:

**Translation**

* source_description
* target_description
* correspondence
* uncertainty
* information_loss
* unresolved_difference

## 19. Translation Residual

A failed or incomplete translation is not merely a protocol error.

It may itself produce a new Residual.

Conceptually:

**Description A → Translation Attempt → Description B → Remaining Difference → Translation Residual**

This is important because interoperability does not require perfect mutual understanding.

The remaining mismatch may reveal:

* incompatible Reference Frames,
* missing categories,
* different boundaries,
* different scales,
* different values,
* or genuinely incommensurable structures.

Therefore:

**Translation failure may be informative.**

## 20. Comparison

CDP may support comparison across heterogeneous Updating Units without requiring identical internal metrics.

Candidate comparison dimensions include:

* Residual persistence,
* Update depth,
* Holding duration,
* Frame stability,
* Boundary transition,
* Trajectory branching,
* Coupling structure,
* reversibility,
* and Reality re-contact.

Comparison should not imply that all systems can be reduced to one scalar score.

**Comparable ≠ Identical**

## 21. Coordination

Description and translation may support coordination.

Coordination may include:

* sharing unresolved Residual,
* exposing incompatible assumptions,
* negotiating boundaries,
* selecting interventions,
* coordinating Reality tests,
* maintaining alternative trajectories,
* or delaying irreversible action.

CDP does not prescribe one optimal coordination policy.

Its purpose is to make relevant dynamics more explicit.

## 22. Interoperability

Within CDP, Interoperability means the capacity of heterogeneous Updating Units to exchange useful descriptions of their dynamics despite internal differences.

This may include the ability to communicate:

**"I observed a Difference."**

**"My current frame cannot absorb it."**

**"The Residual remains unresolved."**

**"I am holding multiple interpretations."**

**"My Reference Frame changed."**

**"My Boundary changed."**

**"This interaction changed my future possibilities."**

**"Our translation remains incomplete."**

Such statements need not expose the entire internal representation.

This creates the possibility of:

**Dynamic Interoperability without Representational Unification.**

## 23. Values and Forced Alignment

CDP does not assume that heterogeneous Updating Units must possess identical values.

Nor does it assume that value differences are irrelevant.

Value differences may themselves become:

* explicit,
* contested,
* translated,
* partially coordinated,
* or sources of Residual.

CDP therefore explores interoperability:

**without requiring the unification of internal representations or forced value alignment.**

This does not imply:

* that alignment is unnecessary,
* that harmful values should be accepted,
* that governance is unnecessary,
* or that all value systems are equivalent.

It means only that interoperability should not be defined as complete value homogenization.

## 24. Privacy, Opacity, and Partial Disclosure

Interoperability should not require complete transparency.

A human, AI system, organization, or institution may be unable or unwilling to disclose its full internal state.

CDP should therefore support partial descriptions such as:

**Residual:** present
**Description:** private

**ReferenceFrameChange:** detected
**InternalRepresentation:** unavailable

**TranslationConfidence:** low
**Reason:** restricted information

This allows interoperability under bounded disclosure.

The governance implications remain open.

## 25. Multi-Scale Description

Updating Units may exist at different scales.

For example:

**Human → Human–AI Pair → Team → Organization → Institutional Network**

CDP should allow nested descriptions without assuming that one scale is always primary.

A Residual at one scale may not be a Residual at another.

A successful Update locally may create a larger Residual globally.

Therefore:

**Scale matters.**

Cross-scale dynamics are an important research problem.

## 26. Time and Update Velocity

Different Updating Units may operate on radically different timescales.

For example:

* biological learning,
* machine inference,
* organizational decision cycles,
* institutional reform,
* cultural change.

CDP should therefore record temporal scope where possible.

Candidate dimensions include:

**Time**

* event_time
* observation_window
* update_duration
* persistence_duration
* expected_recontact

Interoperability may fail not because systems cannot communicate, but because their update velocities differ.

This is especially relevant for Human–AI systems.

## 27. CDP and Intelligence Ecology

At larger scales, CDP may provide a descriptive layer for Intelligence Ecology.

Conceptually:

**Updating Units → Dynamic Descriptions → Translation → Interaction → Coupling → Co-evolution**

The objective is not centralized control of the entire ecology.

It is to improve observability of:

* who is changing,
* what is changing,
* which frames are changing,
* which boundaries are shifting,
* which possibilities are disappearing,
* which new possibilities are emerging,
* and which interactions are changing future trajectories.

## 28. CDP and Governance

Governance may use CDP descriptions to move beyond output-only monitoring.

Potential governance targets include:

* Output,
* State,
* Update,
* Trajectory,
* Reference Frame,
* Boundary,
* Coupling,
* Possibility Space,
* and higher-order Updating Units.

Questions may include:

**Which Trajectories are becoming irreversible?**

**Which Couplings are creating dependency?**

**Which Boundaries are shifting without accountability?**

**Which Possibility Spaces are disappearing?**

**Which Residuals are repeatedly suppressed?**

**Which Updating Units are losing Updateability?**

CDP does not itself answer these normative questions.

It may help make them observable.

## 29. CDP and Reality Re-contact

CDP descriptions must not become self-contained abstractions.

They remain representations.

Therefore:

**CDP Description ≠ Reality**

Descriptions should remain open to renewed Reality contact.

Conceptually:

**Reality → Dynamic Description → Translation / Coordination → Action → Consequence → Reality Re-contact → New Difference**

CDP itself may generate Residual and must remain updateable.

## 30. Minimal Interoperability Cycle

The minimal CDP interaction can be represented as:

**Updating Unit A → Dynamic Description A → Translation → Dynamic Description B → Updating Unit B → Response / Update → Reality Re-contact**

with possible feedback:

**Translation Residual → Holding → Revised Description → Revised Translation**

This process may occur in both directions.

## 31. Candidate CDP Functions

At the implementation level, CDP may eventually support functions such as:

**describe()**
**translate()**
**compare()**
**coordinate()**
**trace()**
**recontact()**

### describe()

Create a dynamic description without requiring full disclosure of internal state.

### translate()

Attempt correspondence between heterogeneous dynamic descriptions.

### compare()

Identify similarities and differences without assuming identity.

### coordinate()

Support interaction or joint action while preserving relevant differences.

### trace()

Maintain provenance and candidate continuity across transformations.

### recontact()

Return descriptions or decisions to Reality through observation, intervention, or consequence.

These functions are conceptual interfaces, not yet standardized APIs.

## 32. What CDP Does Not Solve

CDP v1.0 does not yet solve:

* universal Residual detection,
* semantic equivalence,
* Reference Frame identification,
* automatic value translation,
* universal Agency detection,
* Updating Unit identification,
* Trajectory identity,
* Causal Continuity,
* perfect cross-system translation,
* governance legitimacy,
* power asymmetry,
* privacy,
* deception,
* strategic manipulation,
* or enforcement.

It also does not prove that a universal Common Dynamics Protocol is possible.

That possibility itself is a research hypothesis.

## 33. Falsifiability and Failure Conditions

CDP should be revised, narrowed, or rejected if:

* heterogeneous systems cannot produce useful shared dynamic descriptions,
* translation destroys the information needed for meaningful coordination,
* the proposed common dimensions prove too observer-dependent,
* CDP adds no value beyond existing interoperability approaches,
* dynamic descriptions cannot be operationalized,
* or attempts at common description systematically create more distortion than insight.

Therefore:

**The protocol must be allowed to shrink.**

A useful CDP may ultimately contain fewer common dimensions than proposed here.

## 34. Minimal CDP v1.0 Schema

The following is a conceptual minimum rather than a final technical schema:

**CDPRecord**

* UpdatingUnit
* Time
* RealityContact
* Observation
* Difference
* Residual
* Holding
* Update
* Trajectory
* Boundary
* ReferenceFrame
* PossibilitySpace
* Coupling
* Action
* Outcome
* Provenance
* EpistemicStatus

Optional relational structures include:

* Translation
* CausalContinuity
* EnactmentCandidate
* PhaseSignature
* TransitionConfiguration

The schema is intentionally extensible.

## 35. Core CDP Principles

CDP v1.0 can be compressed into seven principles.

### 1. Difference without Isolation

Heterogeneous systems may remain different without becoming disconnected.

### 2. Connection without Unification

Interoperability does not require identical internal representation.

### 3. Update without Erasure

Transformation should not automatically destroy relevant history or alternative trajectories.

### 4. Partial Translation Is Legitimate

Incomplete correspondence is preferable to false equivalence.

### 5. Translation Residual Is Information

What cannot be translated may itself be dynamically important.

### 6. Description Must Return to Reality

Protocol-level agreement is not sufficient validation.

### 7. CDP Must Remain Updateable

The protocol itself is part of the architecture and is therefore subject to Residual, criticism, revision, and Reality re-contact.

# Closing

The Common Dynamics Protocol does not attempt to make heterogeneous intelligences the same.

It asks whether they can remain different while becoming sufficiently mutually observable to interact, coordinate, and co-evolve.

The central proposition is therefore not:

**Shared intelligence requires shared internal representation.**

It is:

**Heterogeneous intelligences may be able to interoperate through shared descriptions of change without sharing the same internal representation of the world.**

Whether this is possible across humans, AI systems, physical AI, organizations, and other Updating Units remains an open empirical and engineering question.

CDP v1.0 is a first attempt to make that question technically criticizable.

And, like every other component of IDOS:

**Nothing inside the protocol is assumed to be permanently fixed.**

**Everything remains answerable to Reality.**

**Common Dynamics Protocol v1.0 — September 2026**

*Provisional, heterogeneous by design, and open to implementation, criticism, reduction, and revision.*
