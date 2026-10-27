"""Reassess a registered transition under both historical and adopted frames.

No claim of semantic equivalence: the caller supplies observations for each frame.
An old-only distinction is preserved as a difference, not automatically erased.
"""
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json


class ReassessmentStatus(str, Enum):
    COMPATIBLE = 'compatible'
    HOLDING = 'holding'
    REGRESSION = 'regression'


@dataclass(frozen=True)
class FrameObservation:
    frame_id: str
    distinctions: frozenset[str]
    evidence_ids: frozenset[str]
    observed_at: str


@dataclass(frozen=True)
class Reassessment:
    old_frame_id: str
    new_frame_id: str
    transition_digest: str
    status: ReassessmentStatus
    retained: frozenset[str]
    old_only: frozenset[str]
    new_only: frozenset[str]
    unresolved: frozenset[str]
    evidence_ids: frozenset[str]

    def as_dict(self):
        return {'event': 'post_transition_reassessment', 'old_frame_id': self.old_frame_id,
                'new_frame_id': self.new_frame_id, 'transition_digest': self.transition_digest,
                'status': self.status.value, 'retained': sorted(self.retained),
                'old_only': sorted(self.old_only), 'new_only': sorted(self.new_only),
                'unresolved': sorted(self.unresolved), 'evidence_ids': sorted(self.evidence_ids)}


def reassess(ledger, old: FrameObservation, new: FrameObservation, *,
             unresolved: frozenset[str] = frozenset(), record: bool = False) -> Reassessment:
    """Compare fresh observations; persist only when explicitly requested.

    Regression means old-only distinctions exist, not that the new frame is unsafe.
    Holding means evidence cannot support a complete comparison.
    """
    history = ledger.read()  # also verifies hash chain
    adopted = [r for r in history if r['payload'].get('event') == 'adopted'
               and r['payload'].get('old_frame_id') == old.frame_id
               and r['payload'].get('new_frame_id') == new.frame_id]
    if len(adopted) != 1:
        raise ValueError('Exactly one matching recorded adoption required')
    anchor = adopted[0]
    if not old.observed_at or not new.observed_at:
        raise ValueError('Observation timestamps required')
    retained = old.distinctions & new.distinctions
    old_only = old.distinctions - new.distinctions
    new_only = new.distinctions - old.distinctions
    if (not old.evidence_ids or not new.evidence_ids
            or not old.evidence_ids.isdisjoint(new.evidence_ids)):
        status = ReassessmentStatus.HOLDING
    elif unresolved:
        status = ReassessmentStatus.HOLDING
    elif old_only:
        status = ReassessmentStatus.REGRESSION
    else:
        status = ReassessmentStatus.COMPATIBLE
    result = Reassessment(old.frame_id, new.frame_id, anchor['digest'], status,
                          retained, old_only, new_only, unresolved,
                          old.evidence_ids | new.evidence_ids)
    if record:
        ledger.append(result.as_dict())
    return result
