# Architecture note — two-level intervention and recursive discovery

## Core claim (provisional)

An observer may change a *description* without changing the relational process being described. IDOS Discovery Architecture distinguishes that act from an intervention in the **history-bearing relationship among updating units**. A relation intervention changes the conditions of interaction, which may or may not cause new differences to be registered. A further intervention can change the *generating conditions* used to identify observational units, preserve differences, or propose reference frames. Both are revisable and neither guarantees discovery.

## Layer boundaries

| Layer | Object of deliberate change | Inferred automatically? | Recorded by |
|---|---|---|---|
| Relation trajectory | Partners, responsibilities, access, interaction order, boundary | No | `RelationInterventionSpec`, `InterventionStudy`, Reference `RelationDynamics` adapter |
| Discovery generation conditions | Observational-unit rule, distinctions, measurement, frame-proposal criteria, Holding strategy | No | `GenerationConditionChange`, `DiscoveryConditions` |
| Observation and interpretation | Differences, counter-readings, losses, candidate frames | No | `DiscoveryCycle` and the adapter |
| Reality recontact | Follow-up evidence and provisional review | No causal proof | `DiscoveryCycle.recontact` |

## Scope, NOT a new theory of discovery

This is an **architecture of possible operations**, not a statement that all scientific discovery follows a universal sequence. Existing practices (e.g. experiment design, participatory research, organizational change) may overlap. Novelty relative to those practices has not been established. The distinguishing *design intent* here is to preserve relation-specific histories and enable second-order revision of the conditions that make observational categories possible while retaining traceable, partial IDOS connections.

## Minimal example

In a fictional post-merger integration study, the researcher modifies meeting order (Layer 1) while keeping available documents constant. Observers record a disputed mismatch concerning decision rights. Rather than automatically declaring a new frame, they preserve incompatible interpretations. Later they may change the unit of observation from each organization to an actual joint decision process (Layer 2). A new category is proposed and independently checked against further situations. No link in the sequence is assumed causal without an independent evidentiary argument.

## Boundaries on implementation

The Python classes are **records and adapters**, not controllers for people, organizations or AI agents. Use provider-specific control layers and independently verified permissions for real interventions. The registry and provenance links establish referential integrity and traceability, not truth. Version 1.0 is deliberately small so extensions need not conform to one fixed discovery ontology.
