"""IDOS Discovery Architecture v1.0: second-order intervention.

A discovery condition is a provisional, revisable arrangement of what can be
noticed and distinguished; not Reality itself. This layer changes the
conditions of exploration, NOT the observed evidence or the reference core.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
from discovery_architecture import DiscoveryCycle, Record

class ConditionAxis(str, Enum):
    OBSERVATIONAL_UNIT = "observational_unit"
    DISTINCTION_RULE = "distinction_rule"
    MEASUREMENT = "measurement"
    INTERACTION_GENERATION = "interaction_generation"
    FRAME_PROPOSAL_RULE = "frame_proposal_rule"
    RETENTION_AND_HOLDING = "retention_and_holding"
    OTHER = "other"

class ConditionState(str, Enum):
    PROPOSED = "proposed"
    AUTHORIZED = "authorized"
    APPLIED = "applied"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class GenerationConditionChange:
    axis: ConditionAxis
    before: str
    after: str
    rationale: str
    intended_observation: str
    possible_blind_spots: tuple[str, ...]
    comparison_condition: str
    authorization_refs: tuple[str, ...] = ()
    id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        if any(not x.strip() for x in (self.before, self.after, self.rationale,
                                        self.intended_observation, self.comparison_condition)):
            raise ValueError("Describe previous and proposed conditions, rationale and comparison")
        if self.before == self.after:
            raise ValueError("A change must be specified")

@dataclass(frozen=True)
class ConditionApplication:
    change_id: str
    state: ConditionState
    evidence_refs: tuple[str, ...] = ()
    authorization_refs: tuple[str, ...] = ()
    note: str = ""

    def __post_init__(self):
        if self.state == ConditionState.APPLIED and (not self.evidence_refs or not self.authorization_refs):
            raise ValueError("Applied requires evidence and authorization references")

class DiscoveryConditions:
    """Track deliberate revision of conditions that may make new observations possible.

    This is NOT automatic reference frame genesis and makes NO causal claims.
    """
    def __init__(self, cycle: DiscoveryCycle):
        self.cycle = cycle
        self.proposals: dict[str, GenerationConditionChange] = {}
        self.applications: dict[str, ConditionApplication] = {}
        self.records: dict[str, Record] = {}

    def propose(self, change: GenerationConditionChange, *, based_on: Record) -> str:
        if based_on.id not in {r.id for r in self.cycle.records}:
            raise ValueError("The motivating record must belong to this discovery cycle")
        if based_on.kind not in {"difference", "recontact", "discovery_conditions_revision"}:
            raise ValueError("Condition change needs a traceable difference, recontact or previous revision")
        self.proposals[change.id] = change
        return change.id

    def apply(self, application: ConditionApplication, *, based_on: Record) -> Record | None:
        change = self.proposals.get(application.change_id)
        if change is None:
            raise ValueError("Unknown condition change")
        if based_on.id not in {r.id for r in self.cycle.records}:
            raise ValueError("Untraceable source")
        if application.state == ConditionState.APPLIED:
            if not change.authorization_refs or not set(application.authorization_refs).intersection(change.authorization_refs):
                raise ValueError("Recorded authorization does not match proposal")
            if based_on.kind not in {"difference", "recontact", "discovery_conditions_revision"}:
                raise ValueError("Condition update needs a qualifying prior record")
            result = self.cycle.revise_conditions(
                f"APPLIED generation condition [{change.axis.value}]: {change.before} -> {change.after}; "
                f"intent={change.intended_observation}; possible_blind_spots={change.possible_blind_spots}; "
                f"comparison={change.comparison_condition}; evidence={application.evidence_refs}; "
                f"proposal={change.id}", based_on=based_on)
            self.records[change.id] = result
        else:
            result = None
        self.applications[change.id] = application
        return result
