"""Connect frame transition reviews to real IDOS v1.2 frame genesis and relation history.

A proposal is not an adopted frame; this adapter intentionally cannot adopt.
"""
from dataclasses import dataclass, field
from idos_reference_v1_2 import FrameGenesisStatus, ProvenanceEvent
from reference_transition import FrameSnapshot, TransitionReview, review_transition

@dataclass
class TransitionBridge:
    discovery_bridge: object
    reviews: list[TransitionReview] = field(default_factory=list)

    def evaluate(self, genesis_id: str, *, old_distinctions: frozenset[str],
                 new_distinctions: frozenset[str], old_evidence: frozenset[str],
                 new_evidence: frozenset[str], independent_evidence: frozenset[str] = frozenset(),
                 unresolved: frozenset[str] = frozenset(), explicit_rejection: bool = False,
                 authorization_id: str | None = None) -> TransitionReview:
        registry = self.discovery_bridge.registry
        genesis = registry.geneses.get(genesis_id)
        if genesis is None or genesis_id not in {g.id for g in self.discovery_bridge._geneses.values()}:
            raise ValueError('Genesis must be proposed by this discovery bridge')
        if genesis.status != FrameGenesisStatus.PROPOSED:
            raise ValueError('Only pending genesis proposals can be reviewed')
        baseline = self.discovery_bridge.baseline_frame_id
        if baseline not in genesis.origin_frame_ids or baseline not in registry.frames:
            raise ValueError('Genesis does not originate from the baseline frame')
        result = review_transition(
            FrameSnapshot(baseline, old_distinctions, old_evidence),
            FrameSnapshot(genesis.id, new_distinctions, new_evidence),
            unresolved=unresolved, independent_evidence=independent_evidence,
            explicit_rejection=explicit_rejection, authorization_id=authorization_id)
        self.reviews.append(result)
        self.discovery_bridge.relation.trajectory.provenance.append(ProvenanceEvent(
            'reference_transition_review', result.decision.value,
            [genesis.id, baseline, *sorted(old_evidence | new_evidence | independent_evidence)]))
        return result
