"""Executable exploratory Discovery loop, deterministic sandbox adapter.
Not a claim of AI creativity or real-world causal identification.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Protocol
import json, hashlib
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery_architecture import DiscoveryCycle, EvidenceStatus, ReviewStatus
from reference_transition import FrameSnapshot, review_transition, Decision

@dataclass(frozen=True)
class Frame:
    name: str
    observables: tuple[str, ...]
    constraints: tuple[str, ...]

@dataclass(frozen=True)
class Possibility:
    label: str
    evidence: str
    observable: str
    proposed_action: str

@dataclass
class World:
    wealth: float = 50.0
    energy: float = 4.0
    output: float = 6.0
    capacity: float = 9.0
    history: list[dict] = field(default_factory=list)

    def measure(self) -> dict[str,float]:
        return {'wealth':self.wealth, 'energy':self.energy, 'output':self.output, 'capacity':self.capacity}

    def apply(self, action: str) -> dict:
        before=self.measure()
        if action == 'subsidize':
            self.wealth += 2
            self.output += 0.5
        elif action == 'expand_energy':
            self.energy += 2
            self.wealth -= 1
        elif action == 'boost_output':
            self.output += 2
            self.energy -= 0.75
        elif action == 'inspect':
            pass
        else:
            raise ValueError('Action not supported in sandbox')
        self.output=min(self.output, self.capacity, self.energy * 1.5)
        after=self.measure()
        event={'action': action, 'before':before, 'after':after}
        self.history.append(event)
        return event

class Generator(Protocol):
    def propose(self, frame: Frame, observation: dict[str,float], residual: dict[str,float]) -> Possibility | None: ...

class ResidualGenerator:
    """Generates a candidate from a measured discrepancy; no hardcoded new-frame answer in task prompt."""
    def propose(self, frame, observation, residual):
        if residual.get('unexplained_output_gap',0) > 1 and 'energy' not in frame.observables:
            return Possibility('capacity_without_throughput', 'output gap under current scoring', 'energy', 'expand_energy')
        if residual.get('unused_capacity',0)>1 and 'capacity' not in frame.observables:
            return Possibility('unused_capacity', 'unused productive capacity measured', 'capacity', 'boost_output')
        return None

class InterventionPlanner:
    def choose(self, frame: Frame, world: World, candidate: Possibility | None) -> str:
        if candidate and candidate.observable in frame.observables:
            return candidate.proposed_action
        if 'energy' in frame.observables and world.energy * 1.5 < world.capacity:
            return 'expand_energy'
        if 'capacity' in frame.observables and world.output < world.capacity:
            return 'boost_output'
        return 'subsidize'

def digest(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]

class Engine:
    def __init__(self, generator: Generator | None = None):
        self.generator=generator or ResidualGenerator()
        self.planner=InterventionPlanner()
        self.world=World()
        self.frame=Frame('F0', ('wealth','output'), ('no_external_actions',))
        self.cycle=DiscoveryCycle('What limits future prosperity?', 'economy-rel-1', self.frame.name)
        self.events=[]
        self.pending=None

    def residuals(self, observed):
        return {'unexplained_output_gap':max(0,observed['capacity']-observed['output']),
                'unused_capacity':max(0,observed['capacity']-observed['output'])}

    def step(self, *, authorize: bool=False):
        before=self.world.measure()
        residual=self.residuals(before)
        candidate=self.generator.propose(self.frame,before,residual)
        frame_before=self.frame
        review=None
        if candidate and candidate.observable not in self.frame.observables:
            proposed=Frame('F'+str(len([x for x in self.events if x.get('adopted')])+1),
                           self.frame.observables+(candidate.observable,), self.frame.constraints)
            review=review_transition(
                FrameSnapshot(self.frame.name,frozenset(self.frame.observables),frozenset({'baseline-'+self.frame.name})),
                FrameSnapshot(proposed.name,frozenset(proposed.observables),frozenset({'candidate-'+digest(asdict(candidate))})),
                independent_evidence=frozenset({'sandbox-check-'+digest(before)}),
                authorization_id='sandbox-approval' if authorize else None)
            self.pending=(proposed,candidate,review)
            if review.decision is Decision.AUTHORIZED:
                self.frame=proposed
        action=self.planner.choose(self.frame,self.world,candidate)
        performed=self.cycle.intervene(action,evidence_ids=('sandbox-execution-'+str(len(self.events)),),performed=True)
        outcome=self.world.apply(action)
        difference=self.cycle.difference('World values changed after sandbox action '+action,
            after=performed,evidence_ids=('sandbox-outcome-'+digest(outcome),),status=EvidenceStatus.OBSERVED)
        if candidate:
            self.cycle.propose_frame(self.pending[0].name, candidate.evidence,based_on=difference)
        event={'iteration':len(self.events),'frame_before':frame_before.name,'frame_after':self.frame.name,
               'observed_before':before,'residual':residual,'possibility':asdict(candidate) if candidate else None,
               'transition_review':review.decision.value if review else None,
               'adopted':frame_before.name!=self.frame.name,'action':action,'outcome':outcome,
               'record_ids':[performed.id,difference.id],
               'evidence_scope':'sandbox_observation_not_external_corroboration'}
        self.events.append(event)
        return event

    def run(self, cycles=3, authorize=False):
        return [self.step(authorize=authorize) for _ in range(cycles)]

if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--cycles',type=int,default=3)
    parser.add_argument('--authorize-sandbox', action='store_true')
    parser.add_argument('--output',default='run.json')
    args=parser.parse_args()
    engine=Engine()
    result=engine.run(args.cycles,args.authorize_sandbox)
    Path(args.output).write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print(json.dumps([{'iteration':r['iteration'],'frame':r['frame_after'],'candidate':r['possibility']['label'] if r['possibility'] else None,'decision':r['transition_review'],'action':r['action']} for r in result],ensure_ascii=False,indent=2))
