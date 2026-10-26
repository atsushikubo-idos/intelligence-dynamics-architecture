"""AI execution governance extension: no tool calls; external enforcement required.

Inputs are assertions from trusted integrations, NOT independently verified facts.
This module never detects emergence, authenticates tokens, or changes IDOS frames.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Tuple
from governance import CoexistenceGovernor, Proposal, Decision

class GateStatus(str, Enum):
    ELIGIBLE = 'eligible_for_external_enforcement'
    REVIEW = 'human_review_required'
    DENY = 'deny'
    PAUSED = 'paused'

@dataclass(frozen=True)
class ExecutionClaim:
    proposal_id: str
    actor_id: str
    action: str
    resource: str
    expires_at_utc: datetime
    authenticated: bool = False   # must come from external trusted verifier
    scoped: bool = False          # verified action/resource/actor scope
    verifier_ref: str = ''

@dataclass(frozen=True)
class CollectiveSignal:
    proposal_id: str
    kind: str  # unexpected_coordination, correlated_failure, escalation, other
    evidence_refs: Tuple[str, ...]
    unresolved: bool = True

@dataclass(frozen=True)
class GateResult:
    status: GateStatus
    reasons: Tuple[str, ...]

class AIExecutionGate:
    """Fast conservative decision layer paired with v0.2 human review.

    This is a policy demonstration, not a secure enforcement point. Enforcement
    must occur OUTSIDE the AI model, and caller-provided attestations must be
    checked by independent authenticators and tool/resource permission systems.
    """
    def __init__(self, governor: CoexistenceGovernor):
        self.governor = governor
        self.signals: list[CollectiveSignal] = []
        self.policy_version = 1
        self.policy_history: list[dict] = []
        self.locked = False

    def report_collective_signal(self, signal: CollectiveSignal):
        if not signal.evidence_refs:
            raise ValueError('evidence reference required')
        self.signals.append(signal)
        self.governor._record('collective_signal', proposal_id=signal.proposal_id,
                              kind=signal.kind, evidence_refs=list(signal.evidence_refs))

    def gate(self, proposal: Proposal, claim: ExecutionClaim, *,
             approvals: Tuple[str, ...] = (), cdp_ready: bool = False,
             external_invariants_ok: bool = False) -> GateResult:
        """CDP readiness is supplied by a separate adapter, never asserted by this gate."""
        if claim.proposal_id != proposal.proposal_id or claim.actor_id != proposal.proposer_id or claim.action != proposal.action:
            return GateResult(GateStatus.DENY, ('Capability/proposal mismatch',))
        if self.governor.paused or self.locked:
            return GateResult(GateStatus.PAUSED, ('Emergency or governance pause',))
        if (not claim.authenticated or not claim.scoped or not claim.verifier_ref
                or not claim.resource or claim.expires_at_utc.tzinfo is None
                or claim.expires_at_utc <= datetime.now(timezone.utc)):
            return GateResult(GateStatus.DENY, ('Missing, expired, or unverified execution capability',))
        if not external_invariants_ok:
            return GateResult(GateStatus.DENY, ('External non-bypassable safety checks not attested',))
        pending = [s for s in self.signals if s.proposal_id == proposal.proposal_id and s.unresolved]
        if pending:
            return GateResult(GateStatus.REVIEW, ('Unresolved collective risk signal',))
        outcome = self.governor.assess(proposal, approvals=approvals)
        if outcome.decision == Decision.PAUSE:
            return GateResult(GateStatus.PAUSED, outcome.reasons)
        if outcome.decision == Decision.BLOCK:
            return GateResult(GateStatus.DENY, outcome.reasons)
        if outcome.decision != Decision.ALLOW:
            return GateResult(GateStatus.REVIEW, outcome.reasons)
        kinds = {self.governor.actors[x].kind for x in (proposal.proposer_id,) + proposal.affected_actor_ids}
        if len(kinds) > 1 and not cdp_ready:
            return GateResult(GateStatus.REVIEW, ('Heterogeneous CDP description is unavailable',))
        self.governor._record('execution_eligible', proposal_id=proposal.proposal_id,
                              verifier_ref=claim.verifier_ref, policy_version=self.policy_version)
        return GateResult(GateStatus.ELIGIBLE, ('Pass to external enforcement; not execution authorization itself',))

    def propose_policy_revision(self, *, reason: str, reviewers: Tuple[str, ...], evidence_refs: Tuple[str, ...]):
        """Slow loop: record a revision REQUEST only; no automatic policy rewrite."""
        authorized = {a for a in reviewers if a in self.governor.actors and self.governor.actors[a].kind in ('human','organization')}
        if len(authorized) < 2 or not reason.strip() or not evidence_refs:
            raise PermissionError('Two distinct configured human/organizational reviewers and evidence required')
        self.policy_history.append(dict(version=self.policy_version, reason=reason,
                                        reviewers=sorted(authorized), evidence_refs=list(evidence_refs),
                                        status='review_requested_not_applied'))
        self.governor._record('policy_review_requested', version=self.policy_version, reviewers=sorted(authorized))

    def lock_for_incident(self, reason: str):
        if not reason.strip():
            raise ValueError('reason required')
        self.locked = True
        self.governor._record('gate_locked', reason=reason)

    def release_lock(self, *, reviewers: Tuple[str, ...], evidence_refs: Tuple[str, ...]):
        authorized = {a for a in reviewers if a in self.governor.actors and self.governor.actors[a].kind in ('human','organization')}
        if len(authorized) < 2 or not evidence_refs:
            raise PermissionError('Two distinct reviewers and evidence required')
        self.locked = False
        self.governor._record('gate_lock_released', reviewers=sorted(authorized), evidence_refs=list(evidence_refs))
