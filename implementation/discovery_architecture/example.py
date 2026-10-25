"""Hypothetical M&A example. Does not imply actual discovery or causal proof."""
from discovery_architecture import DiscoveryCycle, EvidenceStatus, ReviewStatus

cycle = DiscoveryCycle("What remains invisible in integration?", "relation-trajectory-id", "frame-v1")
intervention = cycle.intervene("Change information-sharing order with consent", evidence_ids=("sim-log-1",), performed=True)
diff = cycle.difference("New asymmetry in decision access was reported", after=intervention,
                        evidence_ids=("sim-observation-1",), status=EvidenceStatus.OBSERVED)
proposal = cycle.propose_frame("frame-candidate-2", "Distinguish decision access from formal authority", based_on=diff)
review = cycle.recontact(proposal, "Preliminary check is inconclusive", evidence_ids=("independent-test-1",),
                         judgment=ReviewStatus.INSUFFICIENT)
revision = cycle.revise_conditions("Try a second relation sequence under the same observation criteria", based_on=review)
for record in cycle.trace(revision.id):
    print(record.kind, "|", record.statement)
print("Candidate review:", cycle.reviews[proposal.id].value)
