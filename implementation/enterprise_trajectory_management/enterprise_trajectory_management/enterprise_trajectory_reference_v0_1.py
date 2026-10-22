"""IDOS ver.83 Enterprise Trajectory Management: experimental reference model.

Event-sourced descriptive architecture, NOT an optimizer or validated predictor.
No external dependencies. Python >=3.10.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime, timezone
import json

PROCESSES = ('Reality','Difference','Representation','Residual','Holding','Update',
             'Possibility Space','Trajectory','Limit','Enactment','Reality Prime','Reopening')

@dataclass(frozen=True)
class Evidence:
    id: str
    source: str
    description: str
    observed_at: str

@dataclass(frozen=True)
class Event:
    id: str
    sequence: int
    process: str
    subject: str
    description: str
    evidence_ids: tuple[str, ...] = ()
    reference_frame: Optional[str] = None
    relation_ids: tuple[str, ...] = ()
    explicit_residual: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ReferenceFrameRevision:
    id: str
    previous_id: Optional[str]
    name: str
    assumptions: tuple[str, ...]
    criteria: tuple[str, ...]
    rationale: str
    evidence_ids: tuple[str, ...] = ()

@dataclass(frozen=True)
class RelationRevision:
    id: str
    parties: tuple[str, ...]
    kind: str
    description: str
    previous_id: Optional[str] = None
    evidence_ids: tuple[str, ...] = ()

@dataclass(frozen=True)
class FutureTrajectory:
    id: str
    name: str
    assumptions: tuple[str, ...]
    possibilities: tuple[str, ...]
    constraints: tuple[str, ...]
    status: str = 'candidate'
    # No probability or ranking is inferred from a candidate description.

@dataclass(frozen=True)
class GovernanceDecision:
    id: str
    actor: str
    action: str  # select, intervene, pause, revise, reopen
    rationale: str
    evidence_ids: tuple[str, ...] = ()
    trajectory_id: Optional[str] = None
    reversible: Optional[bool] = None

class EnterpriseTrajectoryModel:
    """Trace changes in state, relationships, reference frames and governance."""
    def __init__(self, label: str):
        self.label = label
        self.evidence: dict[str, Evidence] = {}
        self.events: list[Event] = []
        self.frames: dict[str, ReferenceFrameRevision] = {}
        self.relations: dict[str, RelationRevision] = {}
        self.futures: dict[str, FutureTrajectory] = {}
        self.decisions: list[GovernanceDecision] = []
        self.holdings: dict[str, str] = {}  # unresolved event id -> reason
        self._ids: set[str] = set()

    def _unique(self, key: str):
        if not key or key in self._ids:
            raise ValueError(f'Invalid or duplicate id: {key!r}')
        self._ids.add(key)

    def _evidence(self, ids):
        unknown = set(ids) - self.evidence.keys()
        if unknown:
            raise ValueError(f'Unknown evidence: {sorted(unknown)}')

    def add_evidence(self, item: Evidence):
        self._unique(item.id)
        self.evidence[item.id] = item

    def add_frame(self, item: ReferenceFrameRevision):
        self._evidence(item.evidence_ids)
        if item.previous_id is not None and item.previous_id not in self.frames:
            raise ValueError('Reference frame predecessor not found')
        self._unique(item.id)
        self.frames[item.id] = item

    def add_relation(self, item: RelationRevision):
        self._evidence(item.evidence_ids)
        if len(item.parties) < 2:
            raise ValueError('Relation must have at least two parties')
        if item.previous_id is not None and item.previous_id not in self.relations:
            raise ValueError('Relation predecessor not found')
        self._unique(item.id)
        self.relations[item.id] = item

    def add_future(self, item: FutureTrajectory):
        self._unique(item.id)
        self.futures[item.id] = item

    def observe(self, event: Event):
        if event.process not in PROCESSES:
            raise ValueError(f'Unknown process: {event.process}')
        if event.sequence != len(self.events) + 1:
            raise ValueError('Events must be recorded in contiguous sequence')
        self._evidence(event.evidence_ids)
        if event.reference_frame and event.reference_frame not in self.frames:
            raise ValueError('Unknown reference frame')
        if set(event.relation_ids) - self.relations.keys():
            raise ValueError('Unknown relation')
        if event.process == 'Residual' and not event.explicit_residual:
            raise ValueError('Residual requires explicit classification')
        self._unique(event.id)
        self.events.append(event)

    def hold(self, residual_event_id: str, reason: str):
        event = next((e for e in self.events if e.id == residual_event_id), None)
        if not event or event.process != 'Residual' or not event.explicit_residual:
            raise ValueError('Holding requires an explicitly classified residual')
        if not reason.strip():
            raise ValueError('Holding requires a reason')
        self.holdings[residual_event_id] = reason

    def decide(self, item: GovernanceDecision):
        self._evidence(item.evidence_ids)
        if item.action not in {'select','intervene','pause','revise','reopen'}:
            raise ValueError('Unknown governance action')
        if item.trajectory_id and item.trajectory_id not in self.futures:
            raise ValueError('Unknown trajectory')
        self._unique(item.id)
        self.decisions.append(item)

    def report(self) -> dict[str, Any]:
        """Descriptive report only: no inferred causality, score, or prediction."""
        return {'model':'IDOS ver.83 enterprise trajectory reference v0.1',
                'label':self.label,
                'processes':list(PROCESSES),
                'evidence':[asdict(x) for x in self.evidence.values()],
                'events':[asdict(x) for x in self.events],
                'reference_frames':[asdict(x) for x in self.frames.values()],
                'relations':[asdict(x) for x in self.relations.values()],
                'candidate_trajectories':[asdict(x) for x in self.futures.values()],
                'holdings':dict(self.holdings),
                'governance':[asdict(x) for x in self.decisions],
                'limitations':['synthetic demonstration only',
                               'no empirical validation',
                               'no causal inference or automatic optimization',
                               'no automatic residual classification']}

def synthetic_demo() -> EnterpriseTrajectoryModel:
    m = EnterpriseTrajectoryModel('Synthetic enterprise transition')
    m.add_evidence(Evidence('ev1','synthetic board note','Resource constraint emerged','2026-01-01'))
    m.add_frame(ReferenceFrameRevision('rf1',None,'Current business','existing market',('cash','delivery'), 'Initial criteria'))
    m.add_relation(RelationRevision('rel1',('management','operations'),'coordination','Initial division of responsibility'))
    m.observe(Event('obs1',1,'Reality','enterprise','Current operating condition',('ev1',),'rf1',('rel1',)))
    m.observe(Event('diff1',2,'Difference','enterprise','Plan and observed resources differ',('ev1',),'rf1'))
    m.observe(Event('res1',3,'Residual','enterprise','Unresolved coordination constraint',('ev1',),'rf1',explicit_residual=True))
    m.hold('res1','Evidence insufficient to resolve without operational review')
    m.add_frame(ReferenceFrameRevision('rf2','rf1','Resilience-oriented',('uncertainty matters',),('cash','reversibility'),'Criteria revised after recontact',('ev1',)))
    m.add_relation(RelationRevision('rel2',('management','operations'),'shared-review','Joint weekly review','rel1',('ev1',)))
    m.add_future(FutureTrajectory('pathA','Maintain current scope',('stable demand',),('incremental change',),('cash limit',)))
    m.add_future(FutureTrajectory('pathB','Stage transition',('review capacity',),('phased investment',),('reversibility',)))
    m.decide(GovernanceDecision('gov1','management','pause','Further evidence required',('ev1',),'pathB',True))
    m.observe(Event('update1',4,'Update','enterprise','Frame and relationship revised',('ev1',),'rf2',('rel2',)))
    m.observe(Event('reopen1',5,'Reopening','enterprise','Decision review scheduled',('ev1',),'rf2',('rel2',)))
    return m

if __name__ == '__main__':
    print(json.dumps(synthetic_demo().report(), ensure_ascii=False, indent=2))
