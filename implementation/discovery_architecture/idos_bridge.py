"""Explicit IDOS adapter for Discovery Architecture v0.1.

Uses the *actual* v1.2 runtime objects, which preserve v1.1 core semantics.
Both Reference files remain unchanged. Proposed frames are never silently adopted;
evidence links are interpretations, not proof of causation.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from discovery_architecture import DiscoveryCycle, Record, EvidenceStatus, ReviewStatus
from idos_reference_v1_2 import (
    SocialConnectionRegistry, SourceGrounding, RealityContact, ProvenanceEvent,
    Difference, FrameGenesis, RelationChange, DynamicInteractionGraph,
    LinkKind, FrameGenesisStatus,
)

@dataclass
class IDOSDiscoveryBridge:
    registry: SocialConnectionRegistry
    coupling_id: str
    baseline_frame_id: str
    question: str

    def __post_init__(self):
        relation = self.registry.relations.get(self.coupling_id)
        if relation is None:
            raise ValueError('Real registered RelationDynamics required')
        if self.baseline_frame_id not in self.registry.frames:
            raise ValueError('Real registered baseline ReferenceFrame required')
        self.relation = relation
        self.cycle = DiscoveryCycle(self.question, relation.trajectory.id,
                                    self.baseline_frame_id)
        self.graph = DynamicInteractionGraph(self.registry)
        self._changes: dict[str, RelationChange] = {}
        self._geneses: dict[str, FrameGenesis] = {}

    def intervene(self, operation: str, *, performed: bool = False,
                  evidence_ids: tuple[str, ...] = ()) -> Record:
        record = self.cycle.intervene(operation, performed=performed,
                                      evidence_ids=evidence_ids)
        if performed:
            self.relation.trajectory.provenance.append(ProvenanceEvent(
                'discovery_intervention_reported', operation,
                [record.id, *evidence_ids, self.coupling_id]))
        return record

    def difference(self, description: str, *, after: Record,
                   evidence_ids: tuple[str, ...],
                   observer: str, status: EvidenceStatus = EvidenceStatus.REPORTED) -> Record:
        record = self.cycle.difference(description, after=after,
                                       evidence_ids=evidence_ids, status=status)
        grounding = SourceGrounding(evidence_ids, observer,
            'Difference reported after intervention; causal origin is unproven')
        change = self.relation.record(description, grounding,
                                      relation_only_changes=(description,))
        self._changes[record.id] = change
        self.graph.record_relation_change(self.coupling_id, change.id)
        # This is a represented Difference, not automatically a Residual.
        self.relation.trajectory.provenance.append(ProvenanceEvent(
            'discovery_difference', description, [record.id, change.id]))
        return record

    def propose_frame(self, candidate_name: str, reason: str, *,
                      based_on: Record, observer: str) -> tuple[Record, FrameGenesis]:
        change = self._changes.get(based_on.id)
        if change is None:
            raise ValueError('Frame proposal must originate in this relation’s recorded difference')
        genesis = self.registry.propose_frame((self.baseline_frame_id,), candidate_name,
            SourceGrounding(change.evidence.source_refs, observer,
                            f'Proposed frame from relation difference: {reason}'))
        proposal = self.cycle.propose_frame(genesis.id, reason, based_on=based_on)
        self._geneses[proposal.id] = genesis
        return proposal, genesis

    def recontact(self, proposal: Record, finding: str, *,
                  evidence_ids: tuple[str, ...], observer: str,
                  judgment: ReviewStatus) -> Record:
        if proposal.id not in self._geneses:
            raise ValueError('Unrecognized frame proposal')
        contact = RealityContact(source=observer, observation=finding, mode='recontact')
        result = self.cycle.recontact(proposal, finding, evidence_ids=evidence_ids,
                                      judgment=judgment)
        self.relation.trajectory.provenance.append(ProvenanceEvent(
            'discovery_recontact', finding, [contact.id, result.id, *evidence_ids]))
        # Recontact and positive review do not adopt a frame or prove causality.
        return result

    def revise_conditions(self, change: str, *, based_on: Record) -> Record:
        result = self.cycle.revise_conditions(change, based_on=based_on)
        self.relation.trajectory.provenance.append(ProvenanceEvent(
            'discovery_conditions_revised', change, [result.id, based_on.id]))
        return result
