"""IDOS Discovery Architecture v0.1 — minimal, exploratory, not validated.

Relation intervention -> observed difference -> proposed frame -> reality recontact
-> revision of discovery conditions. Steps are records, not automatic causality.
Uses external IDs to point to IDOS Reference v1.2 trajectories/frames without
modifying v1.2 or reducing a relation trajectory to its participants' states.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from uuid import uuid4


def new_id() -> str:
    return uuid4().hex


class EvidenceStatus(str, Enum):
    OBSERVED = "observed"
    REPORTED = "reported"
    UNKNOWN = "unknown"


class ReviewStatus(str, Enum):
    SUPPORTED = "supported"
    INSUFFICIENT = "insufficient"
    NOT_SUPPORTED = "not_supported"


@dataclass(frozen=True)
class Record:
    kind: str
    statement: str
    source_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    status: EvidenceStatus = EvidenceStatus.REPORTED
    id: str = field(default_factory=new_id)


@dataclass
class DiscoveryCycle:
    """Minimal protocol. Neither new knowledge nor causal links are inferred."""
    question: str
    relation_trajectory_id: str
    baseline_frame_id: str
    records: list[Record] = field(default_factory=list)
    candidate_frame_ids: list[str] = field(default_factory=list)
    reviews: dict[str, ReviewStatus] = field(default_factory=dict)

    def _add(self, kind: str, statement: str, sources: tuple[str, ...],
             evidence: tuple[str, ...] = (),
             status: EvidenceStatus = EvidenceStatus.REPORTED) -> Record:
        if not statement.strip():
            raise ValueError("A descriptive statement is required")
        known = {r.id for r in self.records}
        if any(src not in known for src in sources):
            raise ValueError("Unknown source record: linkage must remain traceable")
        record = Record(kind, statement, sources, evidence, status)
        self.records.append(record)
        return record

    def intervene(self, operation: str, *, evidence_ids: tuple[str, ...] = (),
                  performed: bool = False) -> Record:
        """Planned and performed interventions are never equivalent."""
        if performed and not evidence_ids:
            raise ValueError("Performed intervention needs an evidence reference")
        return self._add("performed_intervention" if performed else "planned_intervention",
                         operation, (), evidence_ids)

    def difference(self, description: str, *, after: Record,
                   evidence_ids: tuple[str, ...] = (),
                   status: EvidenceStatus = EvidenceStatus.REPORTED) -> Record:
        if after.kind != "performed_intervention":
            raise ValueError("A post-intervention difference needs a performed intervention")
        if status is EvidenceStatus.OBSERVED and not evidence_ids:
            raise ValueError("Observed evidence needs a source reference")
        return self._add("difference", description, (after.id,), evidence_ids, status)

    def propose_frame(self, frame_id: str, reason: str, *, based_on: Record) -> Record:
        if based_on.kind != "difference":
            raise ValueError("Frame proposal must refer to a difference record")
        if not frame_id.strip():
            raise ValueError("Candidate frame ID required")
        proposal = self._add("frame_proposal", f"{frame_id}: {reason}", (based_on.id,))
        self.candidate_frame_ids.append(frame_id)
        return proposal

    def recontact(self, proposal: Record, finding: str, *, evidence_ids: tuple[str, ...],
                  judgment: ReviewStatus) -> Record:
        if proposal.kind != "frame_proposal" or proposal.id not in {r.id for r in self.records}:
            raise ValueError("Known frame proposal required")
        if not evidence_ids:
            raise ValueError("Reality recontact needs external evidence")
        rec = self._add("recontact", finding, (proposal.id,), evidence_ids,
                        EvidenceStatus.OBSERVED)
        self.reviews[proposal.id] = judgment
        return rec

    def revise_conditions(self, change: str, *, based_on: Record) -> Record:
        if based_on.kind not in {"difference", "recontact"}:
            raise ValueError("Revisions must link to a difference or a recontact")
        return self._add("discovery_conditions_revision", change, (based_on.id,))

    def trace(self, record_id: str) -> list[Record]:
        by_id = {r.id: r for r in self.records}
        if record_id not in by_id:
            raise ValueError("Unknown record")
        seen: set[str] = set()
        order: list[Record] = []
        def visit(identifier: str) -> None:
            if identifier in seen:
                return
            seen.add(identifier)
            for parent in by_id[identifier].source_ids:
                visit(parent)
            order.append(by_id[identifier])
        visit(record_id)
        return order
