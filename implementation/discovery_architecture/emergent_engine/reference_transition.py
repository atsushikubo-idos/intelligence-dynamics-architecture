"""Conservative evaluation-frame transition plan for IDOS.

This module NEVER adopts a frame. Evidence independence and authorization are
externally asserted; IDs are trace links, not cryptographic verification.
"""
from dataclasses import dataclass
from enum import Enum

class Decision(str, Enum):
    HOLD = 'holding'
    REJECT = 'rejected'
    READY = 'ready_for_human_authorization'
    AUTHORIZED = 'authorized_for_controlled_transition'

@dataclass(frozen=True)
class FrameSnapshot:
    frame_id: str
    distinctions: frozenset[str]
    evidence_ids: frozenset[str]

@dataclass(frozen=True)
class TransitionReview:
    source: str
    target: str
    decision: Decision
    retained: frozenset[str]
    gained: frozenset[str]
    lost: frozenset[str]
    unresolved: frozenset[str]
    rationale: str
    authorization_id: str | None = None

def review_transition(old: FrameSnapshot, new: FrameSnapshot, *,
                      unresolved: frozenset[str] = frozenset(),
                      independent_evidence: frozenset[str] = frozenset(),
                      explicit_rejection: bool = False,
                      authorization_id: str | None = None) -> TransitionReview:
    if not old.frame_id or not new.frame_id or old.frame_id == new.frame_id:
        raise ValueError('Distinct nonempty frame IDs required')
    if not old.evidence_ids or not new.evidence_ids:
        raise ValueError('Each frame needs traceable evidence references')
    retained = old.distinctions & new.distinctions
    gained = new.distinctions - old.distinctions
    lost = old.distinctions - new.distinctions
    if explicit_rejection:
        status, reason = Decision.REJECT, 'Candidate explicitly rejected'
    elif unresolved or lost:
        status, reason = Decision.HOLD, 'Unresolved evidence or lost distinctions require holding'
    elif not independent_evidence or not independent_evidence.isdisjoint(old.evidence_ids | new.evidence_ids):
        status, reason = Decision.HOLD, 'Independent corroboration missing or overlapping'
    elif authorization_id and authorization_id.strip():
        status, reason = Decision.AUTHORIZED, 'Externally asserted authorization; no core frame mutation'
    else:
        status, reason = Decision.READY, 'Candidate supported; authorization required'
    return TransitionReview(old.frame_id, new.frame_id, status, retained, gained, lost,
                            unresolved, reason, authorization_id if status is Decision.AUTHORIZED else None)
