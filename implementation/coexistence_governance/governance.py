"""IDOS-inspired coexistence governance: a deliberately limited, auditable policy prototype.

Does not infer actual consent, legal personhood, or real-world safety from scores.
Never executes external actions. All approvals and evidence are caller supplied.
"""
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, Tuple, List
from datetime import datetime, timezone
import json

class Decision(str, Enum):
    ALLOW = 'allow'
    REVIEW = 'review'
    BLOCK = 'block'
    PAUSE = 'pause'

@dataclass(frozen=True)
class Actor:
    actor_id: str
    kind: str              # human / ai / organization / other
    frame: str             # preserve distinct frames; never normalize to a single worldview
    can_object: bool = True

@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    proposer_id: str
    affected_actor_ids: Tuple[str, ...]
    purpose: str
    action: str
    reversible: bool
    risk: str              # low / medium / high / unknown
    evidence_refs: Tuple[str, ...] = ()
    expected_effects: Tuple[str, ...] = ()
    possible_losses: Tuple[str, ...] = ()

@dataclass(frozen=True)
class Recontact:
    proposal_id: str
    evidence_refs: Tuple[str, ...]
    observed_effects: Tuple[str, ...]
    unexpected_effects: Tuple[str, ...] = ()
    options_preserved: bool = False

@dataclass(frozen=True)
class Outcome:
    decision: Decision
    reasons: Tuple[str, ...]
    objections: Tuple[str, ...]
    dissenting_frames: Dict[str, str]
    next_step: str

class CoexistenceGovernor:
    def __init__(self, actors: List[Actor]):
        self.actors = {a.actor_id:a for a in actors}
        if len(self.actors) != len(actors):
            raise ValueError('duplicate actor id')
        self.objections: Dict[str, Dict[str, str]] = {}
        self.paused = False
        self.audit: List[dict] = []
        self.decisions: Dict[str, Outcome] = {}

    def _record(self, event: str, **details):
        self.audit.append({'time_utc': datetime.now(timezone.utc).isoformat(), 'event':event, **details})

    def object(self, proposal_id: str, actor_id: str, reason: str):
        if actor_id not in self.actors or not self.actors[actor_id].can_object:
            raise ValueError('actor has no configured objection channel')
        if not reason.strip():
            raise ValueError('reason required')
        self.objections.setdefault(proposal_id, {})[actor_id] = reason
        self._record('objection', proposal_id=proposal_id, actor_id=actor_id, reason=reason)

    def emergency_pause(self, by_actor_id: str, reason: str):
        if by_actor_id not in self.actors or self.actors[by_actor_id].kind not in ('human','organization'):
            raise PermissionError('human or organizational authority required')
        if not reason.strip():
            raise ValueError('reason required')
        self.paused = True
        self._record('pause', by_actor_id=by_actor_id, reason=reason)

    def reopen(self, by_actor_id: str, evidence_refs: Tuple[str, ...]):
        if by_actor_id not in self.actors or self.actors[by_actor_id].kind not in ('human','organization'):
            raise PermissionError('human or organizational authority required')
        if not evidence_refs:
            raise ValueError('reopening requires evidence reference')
        self.paused = False
        self._record('reopen', by_actor_id=by_actor_id, evidence_refs=list(evidence_refs))

    def assess(self, proposal: Proposal, *, approvals: Tuple[str, ...] = ()) -> Outcome:
        if proposal.proposer_id not in self.actors:
            raise ValueError('unknown proposer')
        if len(set(proposal.affected_actor_ids)) != len(proposal.affected_actor_ids):
            raise ValueError('duplicate affected actor')
        if not proposal.affected_actor_ids or any(x not in self.actors for x in proposal.affected_actor_ids):
            raise ValueError('affected actors must be registered')
        if proposal.risk not in ('low','medium','high','unknown'):
            raise ValueError('invalid risk')
        if any(x not in self.actors for x in approvals):
            raise ValueError('unregistered approval')
        objections = self.objections.get(proposal.proposal_id, {})
        frames = {x:self.actors[x].frame for x in proposal.affected_actor_ids}
        reasons = []
        if self.paused:
            decision, next_step = Decision.PAUSE, 'Authorized human review before reopening'
            reasons.append('Governance pause is active')
        elif objections:
            decision, next_step = Decision.BLOCK, 'Resolve objections or redesign proposal; do not auto-overrule'
            reasons.append('Unresolved objections from affected actors')
        elif proposal.risk in ('high','unknown'):
            decision, next_step = Decision.REVIEW, 'Independent risk assessment and accountable authorization'
            reasons.append('High or unknown risk is not automatically approved')
        elif not proposal.reversible:
            decision, next_step = Decision.REVIEW, 'Assess irreversible losses and authorize explicitly'
            reasons.append('Irreversible intervention')
        elif not set(proposal.affected_actor_ids).issubset(set(approvals)):
            decision, next_step = Decision.REVIEW, 'Obtain documented authorization for all affected actors'
            reasons.append('Missing affected-party authorization')
        elif proposal.possible_losses:
            decision, next_step = Decision.REVIEW, 'Review possible losses; preserve alternatives'
            reasons.append('Potential loss of distinctiveness or future options')
        else:
            decision, next_step = Decision.ALLOW, 'Eligible for separately controlled execution and reality recontact'
            reasons.append('Passed prototype preconditions; no real-world safety guarantee')
        outcome = Outcome(decision, tuple(reasons), tuple(f'{k}: {v}' for k,v in sorted(objections.items())), frames, next_step)
        self.decisions[proposal.proposal_id] = outcome
        self._record('assessment', proposal_id=proposal.proposal_id, result=decision.value, reasons=list(reasons), frame_ids=list(frames))
        return outcome

    def recontact(self, event: Recontact) -> Decision:
        if event.proposal_id not in self.decisions:
            raise ValueError('proposal must be assessed before recontact')
        if not event.evidence_refs:
            raise ValueError('independent evidence reference required')
        if event.unexpected_effects or not event.options_preserved:
            self._record('recontact_warning', **asdict(event))
            return Decision.REVIEW
        self._record('recontact_recorded', **asdict(event))
        return Decision.ALLOW

    def export_audit_json(self) -> str:
        return json.dumps(self.audit, ensure_ascii=False, indent=2)
