"""IDOS Discovery v0.2: deliberate relation-trajectory intervention design.

This module models WHAT is intentionally changed, HOW it is compared, and
WHAT cannot be inferred. It does not intervene in real human/AI systems.
The six axes are an optional working vocabulary, not an exhaustive ontology.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4
from discovery_architecture import DiscoveryCycle, Record, EvidenceStatus, ReviewStatus


class InterventionAxis(str, Enum):
    PARTNERS = "partners"             # who is connected or disconnected
    ROLES_AUTHORITY = "roles_authority" # who can propose, decide, veto, withdraw
    INFORMATION = "information"       # asymmetry, delay, access, memory
    TIMING_SEQUENCE = "timing_sequence" # timing, ordering, frequency, reversibility
    BOUNDARY = "boundary"             # inside/outside, permeability
    EVALUATION = "evaluation"         # what counts as success/observable


class ExecutionState(str, Enum):
    PROPOSED = "proposed"
    AUTHORIZED = "authorized"
    PERFORMED = "performed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class RelationInterventionSpec:
    axis: InterventionAxis
    relation_trajectory_id: str
    baseline_frame_id: str
    before: str
    after: str
    intent: str
    observation_target: str
    comparison_condition: str
    possible_losses: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    authorization_refs: tuple[str, ...] = ()
    reversibility: Optional[bool] = None
    id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        fields = (self.relation_trajectory_id, self.baseline_frame_id,
                  self.before, self.after, self.intent,
                  self.observation_target, self.comparison_condition)
        if any(not x.strip() for x in fields):
            raise ValueError("Specification requires trajectory, frame, contrast, intent and comparison")
        if self.before == self.after:
            raise ValueError("No change specified between before and after")


@dataclass(frozen=True)
class ExecutionReceipt:
    specification_id: str
    state: ExecutionState
    evidence_refs: tuple[str, ...] = ()
    authorization_refs: tuple[str, ...] = ()
    notes: str = ""

    def __post_init__(self):
        if self.state == ExecutionState.PERFORMED:
            if not self.evidence_refs:
                raise ValueError("Performed requires evidence refs")
            if not self.authorization_refs:
                raise ValueError("Performed requires authorization refs; legitimacy is externally verified")


@dataclass(frozen=True)
class Interpretation:
    difference_record_id: str
    baseline_explanation: str
    proposed_new_distinction: str
    explanation_lost: str
    competing_interpretations: tuple[str, ...] = ()

    def __post_init__(self):
        if not all((self.difference_record_id, self.baseline_explanation,
                    self.proposed_new_distinction, self.explanation_lost)):
            raise ValueError("Distinction, baseline and losses must be explicit")


class InterventionStudy:
    """Extension around a DiscoveryCycle, not a replacement for IDOS objects."""
    def __init__(self, cycle: DiscoveryCycle):
        self.cycle = cycle
        self.specifications: dict[str, RelationInterventionSpec] = {}
        self.receipts: dict[str, ExecutionReceipt] = {}
        self.performed_records: dict[str, Record] = {}
        self.interpretations: dict[str, Interpretation] = {}

    def design(self, spec: RelationInterventionSpec) -> Record:
        if (spec.relation_trajectory_id != self.cycle.relation_trajectory_id
                or spec.baseline_frame_id != self.cycle.baseline_frame_id):
            raise ValueError("Intervention must target this cycle's relation and frame")
        self.specifications[spec.id] = spec
        return self.cycle.intervene(
            f"PLAN [{spec.axis.value}] {spec.before} => {spec.after}; "
            f"intent={spec.intent}; observe={spec.observation_target}; "
            f"comparison={spec.comparison_condition}; "
            f"losses={spec.possible_losses}; constraints={spec.constraints}",
            performed=False)

    def record_execution(self, receipt: ExecutionReceipt) -> Optional[Record]:
        spec = self.specifications.get(receipt.specification_id)
        if spec is None:
            raise ValueError("Unknown intervention specification")
        if receipt.state == ExecutionState.PERFORMED:
            if not spec.authorization_refs:
                raise ValueError("Explicit prior authorization refs required in specification")
            if not set(receipt.authorization_refs).intersection(spec.authorization_refs):
                raise ValueError("Authorization refs inconsistent with specification")
            record = self.cycle.intervene(
                f"PERFORMED [{spec.axis.value}] {spec.before} => {spec.after}; "
                f"spec={spec.id}; {receipt.notes}",
                performed=True, evidence_ids=receipt.evidence_refs)
            self.performed_records[spec.id] = record
        else:
            record = None
        self.receipts[spec.id] = receipt
        return record

    def observe(self, spec_id: str, description: str, evidence_refs: tuple[str, ...],
                status: EvidenceStatus = EvidenceStatus.REPORTED) -> Record:
        after = self.performed_records.get(spec_id)
        if after is None:
            raise ValueError("Observation requires recorded performed intervention")
        return self.cycle.difference(description, after=after,
                                     evidence_ids=evidence_refs, status=status)

    def interpret(self, interpretation: Interpretation) -> None:
        ids = {r.id for r in self.cycle.records if r.kind == "difference"}
        if interpretation.difference_record_id not in ids:
            raise ValueError("Interpretation must refer to a difference in this cycle")
        self.interpretations[interpretation.difference_record_id] = interpretation

    def propose_from(self, difference: Record, frame_id: str, reason: str) -> Record:
        if difference.id not in self.interpretations:
            raise ValueError("Record interpretation and losses before proposing new frame")
        return self.cycle.propose_frame(frame_id, reason, based_on=difference)
