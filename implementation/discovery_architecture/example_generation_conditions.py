"""Minimal illustration of second-order intervention; no real-world change."""
from discovery_architecture import DiscoveryCycle, EvidenceStatus
from generation_conditions import (
    ConditionAxis, GenerationConditionIntervention, GenerationConditionRegistry,
)

cycle = DiscoveryCycle("What differences become observable?", "relation-trajectory-id", "frame-id")
performed = cycle.intervene("Change interaction order", performed=True, evidence_ids=("example-execution",))
difference = cycle.difference("An unexpected distinction was reported", after=performed,
                              evidence_ids=("example-observation",), status=EvidenceStatus.REPORTED)
conditions = GenerationConditionRegistry(cycle)
proposal_id = conditions.propose(GenerationConditionIntervention(
    axis=ConditionAxis.OBSERVATION_BOUNDARY,
    before="Only participant A is observed",
    after="The interaction between A and B is also observed",
    rationale="Test whether relational history changes available distinctions",
    possible_closures=("Old single-actor metrics may lose comparability",),
))
revision = conditions.enact(
    proposal_id, based_on=difference,
    authorization_refs=("example-approval",),
    execution_evidence_refs=("example-revision-log",),
)
for event in cycle.trace(revision.id):
    print(event.kind, event.statement)
