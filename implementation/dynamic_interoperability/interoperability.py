"""Difference-preserving interoperability: an application of IDOS CDP, not a replacement.

Claims below are declared by participants / reviewers. They are NOT automatically
semantic truth or detected tacit knowledge. All exchanged content is local data.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
from uuid import uuid4

class Disposition(str, Enum):
    PRESERVED = "preserved"       # reviewer verified an invariant survived
    ALTERED = "altered"           # reviewer identified transformation
    OMITTED = "omitted"           # reviewer identified absence
    UNRESOLVED = "unresolved"     # no adequate determination
    CONTESTED = "contested"       # incompatible interpretations remain

@dataclass(frozen=True)
class Claim:
    id: str
    text: str
    origin: str
    frame: str

@dataclass(frozen=True)
class Assessment:
    claim_id: str
    disposition: Disposition
    evidence: str = ""
    assessor: str = ""
    translated_text: Optional[str] = None

@dataclass(frozen=True)
class Exchange:
    id: str
    round: int
    source_id: str
    target_id: str
    source_frame: str
    target_frame: str
    source_trajectory: str
    target_trajectory: str
    original: tuple[Claim, ...]
    translated: str
    assessments: tuple[Assessment, ...]
    cdp_quality: str
    cdp_residual: str
    declared_by: str
    previous_exchange_id: Optional[str] = None

@dataclass
class Ledger:
    exchanges: list[Exchange] = field(default_factory=list)

    def record(self, *, round: int, source_id: str, target_id: str,
               source_frame: str, target_frame: str,
               source_trajectory: str, target_trajectory: str,
               original: list[Claim], translated: str,
               assessments: list[Assessment], cdp_quality: str,
               cdp_residual: str, declared_by: str,
               previous_exchange_id: Optional[str] = None) -> Exchange:
        if round < 1 or source_id == target_id or not translated.strip():
            raise ValueError("Round, distinct participants and nonempty translation required")
        if not original or len({c.id for c in original}) != len(original):
            raise ValueError("Provide distinct original claims")
        ids = {c.id for c in original}
        if len({a.claim_id for a in assessments}) != len(assessments):
            raise ValueError("At most one assessment per claim per exchange")
        if any(a.claim_id not in ids for a in assessments):
            raise ValueError("Assessments must reference source claims")
        if any(a.disposition in (Disposition.PRESERVED, Disposition.ALTERED, Disposition.OMITTED)
               and (not a.evidence.strip() or not a.assessor.strip()) for a in assessments):
            raise ValueError("Determinate assessments require evidence and assessor")
        if previous_exchange_id and not any(e.id == previous_exchange_id for e in self.exchanges):
            raise ValueError("Previous exchange must exist")
        # Missing assessment stays unresolved; never infer preservation from silence.
        known = {a.claim_id for a in assessments}
        completed = assessments + [Assessment(c.id, Disposition.UNRESOLVED) for c in original if c.id not in known]
        result = Exchange(str(uuid4()), round, source_id, target_id, source_frame,
                          target_frame, source_trajectory, target_trajectory,
                          tuple(original), translated, tuple(completed), cdp_quality,
                          cdp_residual, declared_by, previous_exchange_id)
        self.exchanges.append(result)
        return result

    def open_issues(self) -> list[dict]:
        return [{"exchange_id": e.id, "claim_id": a.claim_id, "state": a.disposition.value,
                 "direction": f"{e.source_id}->{e.target_id}"}
                for e in self.exchanges for a in e.assessments
                if a.disposition != Disposition.PRESERVED]

    def snapshot(self) -> list[dict]:
        return [asdict(e) for e in self.exchanges]
