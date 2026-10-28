# Intelligence Dynamics Architecture (IDOS) — Discovery Architecture v1.0

**An open, executable reference design for revising the conditions of discovery.**

## Purpose

Discovery is not restricted to searching for answers within a pre-existing reference frame. Deliberate interventions in **relation trajectories** may alter interaction histories, expose previously unrepresented differences, and create conditions in which new observational units, distinctions, or reference-frame candidates can arise. When warranted, the *conditions that generate those possibilities* can themselves be deliberately intervened upon and revised.

This is a **design proposal**, not an established causal discovery method. It does not claim that changing a relationship necessarily produces a novel frame, or that an observed sequence proves causation.

## The two layers of intervention

**Layer 1 — Relation-trajectory intervention:** Intervene in how heterogeneous updating units are connected and how their relationships develop over time. Possible, non-exhaustive axes: partners, roles/authority, information exchange, timing/sequence, boundaries, and interaction-based evaluation. The object's *history* matters, not merely its current configuration.

**Layer 2 — Discovery-generation-condition intervention:** When differences and failed/partial observations warrant it, intervene in the conditions under which observational units, distinctions and frame candidates can emerge: observational units, distinction rules, measurement configurations, interaction-generating arrangements, frame-proposal rules, and the preservation of unresolved interpretations. This second layer can recursively alter subsequent Layer 1 design. Neither layer guarantees discovery.

### Minimal recursive protocol

1. **Anchor:** identify a registered IDOS relation trajectory, updating units, and baseline reference frame; preserve their distinct identities.
2. **Design:** specify a contrast (before/after), intention, comparison condition, potential losses, constraints, and authority references.
3. **Intervene:** distinguish proposed, authorized, performed, cancelled; do not mistake a statement for a real-world action.
4. **Detect and hold:** record reported/observed/unknown differences and competing explanations; Difference is not automatically Residual.
5. **Propose:** optionally suggest a new reference frame without claiming that it has been created, adopted or validated.
6. **Recontact:** distinguish supporting, insufficient and non-supporting evidence; retain what a new frame obscures.
7. **Revise conditions:** if warranted, deliberately alter Layer 1 and/or Layer 2 generation conditions; allow maintenance, pause, branching and abandonment.

The numbered presentation is explanatory; it is not a mandatory, irreversible sequence.

## Why not merely change perspective?

Changing perspective modifies the observer's account of a phenomenon. Intervening in a relation trajectory **can change the observed system's relational conditions**, its history of interaction, and subsequent possibilities for joint updating. It may consequently make previously unavailable observational distinctions possible, but this result must be separately established. An apparent frame shift arising from a change in evaluation language alone is **not** evidence that a relation was changed. Conversely, a changed relationship does not by itself prove that an entirely new frame emerged.

## Alignment with IDOS Reference

- **Reference v1.1:** UpdatingUnit, dynamic Boundary, Trajectory, Difference versus Residual, domain-specific Holding, revisable ReferenceFrame/Measurement, Reality recontact, Reopening, and Future Updateability are the conceptual/operational baseline.
- **Reference v1.2:** registered relation trajectories (RelationDynamics), reference-frame proposal (FrameGenesis), and evidence-grounded social connection registry (SocialConnectionRegistry) are used by the adapter (`idos_bridge.py`).
- The adapter checks that referenced trajectories and frames exist; it **does not modify** either frozen Reference file. These modules must remain separate from `src/idos_reference_v1_1.py` and `src/idos_reference_v1_2.py`.
- The second layer is represented by `generation_conditions.py`. Application produces a **traceable condition-revision record**, not automatic frame adoption or a guaranteed change to the external world.

## Files

| File | Role |
|---|---|
| `discovery_architecture.py` | Minimal discovery cycle and evidence-linked trace |
| `intervention_design.py` | First-layer relation intervention design, authorization references and interpretation losses |
| `generation_conditions.py` | Second-layer changes to discovery generation conditions |
| `idos_bridge.py` | Direct adapter to IDOS Reference v1.2 objects |
| `example.py` | Hypothetical trace example (no empirical claims) |
| `test_*.py` | Executable constraints and integration tests |

## Installation and tests

Requires Python 3.10+ and the repository's `src/idos_reference_v1_2.py`. Run from the root of the [IDOS repository](https://github.com/atsushikubo-idos/intelligence-dynamics-architecture):

```bash
PYTHONPATH=src:implementation/discovery_architecture python -m unittest discover -s implementation/discovery_architecture -p 'test_*.py' -v
PYTHONPATH=src:implementation/discovery_architecture python implementation/discovery_architecture/example.py
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH='src;implementation/discovery_architecture'
python -m unittest discover -s implementation/discovery_architecture -p 'test_*.py' -v
python implementation/discovery_architecture/example.py
```

## Interpretive and ethical boundaries

- Planned ≠ performed; a cited artifact ≠ verified external evidence; authorization reference ≠ proof of legitimate consent.
- Recorded interaction ≠ established causal impact; temporal ordering ≠ causation.
- Updating unit ≠ Agency ≠ Subject ≠ Sovereignty; Coupling ≠ Enactment.
- Difference ≠ Residual; unobserved ≠ observed; new words ≠ a new reference frame.
- Relation-specific trajectory ≠ a sum of participants' trajectories.
- Proposed frame ≠ accepted frame; recontact ≠ validation.
- Preserving future capacity to update is as important as any immediate discovery; intervention may reduce that capacity.
- Interventions in humans or institutions require appropriate consent, oversight, reversibility and real-world checks **outside this software**.
- The six intervention axes are replaceable operational categories, not a claim of an exhaustive ontology or a transcription of all 183 original diagrams.

## Status and intended reuse

Version 1.0 fixes a *minimal, inspectable architectural reference* for a potential general-purpose discovery protocol (analogous in accessibility, **not** equivalent in operation, to PDCA). It is **not** an empirical demonstration of novel discoveries or a fully automated intervention engine. Keep primary source diagrams and the `preservation/` archive as the source of record; future implementations can extend this design without erasing differences or retroactively changing v1.0.

**License:** Intended for distribution under Apache-2.0, consistent with the repository's software license; confirm repository licensing before publication.


## Executable Discovery Engine (v0.4)

The Discovery Architecture does not guarantee the discovery of the unknown. It provides an executable architecture for engaging with unknown possibilities through four connected operations:

1. Generate possibility candidates without specifying their content in advance.
2. Update observation targets and evaluation methods according to the proposed reference frame.
3. Reconfigure intervention conditions and executable operations.
4. Feed intervention outcomes back into the next generation cycle.

The engine preserves previous reference frames, unresolved differences, and conditions for future reconsideration.

The current implementation supports simulation-based execution and an optional AI candidate-generation interface. Actual AI-generated discovery remains unverified.

See [emergent_engine/README_v04.md](emergent_engine/README_v04.md) for implementation details and execution instructions.
  
