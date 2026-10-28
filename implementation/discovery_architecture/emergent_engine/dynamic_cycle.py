"""IDOS experimental dynamic measurement/authorization/intervention loop.

Sandbox-only; no proof of semantic novelty or causal identification.
A proposal is declarative data, never executed as Python.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib, json
from typing import Protocol
from engine import World
from reference_transition import FrameSnapshot, review_transition, Decision

# A deliberately bounded sensor registry. A new metric can be configured without new Python
# from the model; novel sensors must be separately implemented and approved.
SENSORS = {
 'wealth': lambda s: s['wealth'],
 'output': lambda s: s['output'],
 'energy': lambda s: s['energy'],
 'capacity': lambda s: s['capacity'],
 'unmet_capacity': lambda s: max(0.,s['capacity']-s['output']),
 'energy_ceiling_gap': lambda s: max(0.,s['capacity']-s['energy']*1.5),
 'output_per_energy': lambda s: s['output']/s['energy'] if s['energy']>0 else None,
}
ACTIONS = {'inspect','subsidize','expand_energy','boost_output'}

@dataclass(frozen=True)
class FrameSpec:
    id: str
    metric: str
    maximize: bool
    # admissible actions are an explicit frame *policy*, but are intersected with
    # unchanged sandbox authorization; switching frame never increases authority.
    admissible: tuple[str,...]

@dataclass(frozen=True)
class Candidate:
    idea: str
    metric: str
    maximize: bool
    proposed_action: str
    rationale: str

class ProposalSource(Protocol):
    def propose(self, *, history: list[dict], frame: FrameSpec, visible_observations: dict) -> Candidate | None: ...

class ReplaySource:
    """Test fixtures are scripted, not AI discoveries."""
    def __init__(self, candidates): self.candidates=iter(candidates)
    def propose(self, **kwargs): return next(self.candidates,None)

class DynamicCycle:
    def __init__(self, generator: ProposalSource, *, initial_world: World|None=None):
        self.world=initial_world or World()
        self.frame=FrameSpec('F0','wealth',True,('subsidize','inspect'))
        self.generator=generator
        self.history=[]
        self.authorized_actions={'inspect','subsidize','expand_energy','boost_output'}
        self.frames={self.frame.id:self.frame}
    def measure(self,frame,raw): return SENSORS[frame.metric](raw)
    def _eligible(self, frame,raw):
        # Conditions are evaluated against the current world at every cycle.
        possible=[]
        for a in frame.admissible:
            if a not in self.authorized_actions: continue
            if a=='boost_output' and (raw['energy']<0.75 or raw['output']>=raw['capacity']): continue
            if a=='expand_energy' and raw['wealth']<1: continue
            possible.append(a)
        return possible
    def step(self, *, approve_frame=False):
        before=self.world.measure()
        previous=self.frame
        previous_score=self.measure(previous,before)
        candidate=self.generator.propose(history=list(self.history),frame=previous,visible_observations={
            'current_measure':previous.metric,'current_value':previous_score,'past_events':len(self.history)})
        review_status='no_candidate'; rejected=None
        if candidate is not None:
            if (not isinstance(candidate,Candidate) or candidate.metric not in SENSORS
                    or candidate.proposed_action not in ACTIONS or len(candidate.idea)>200
                    or len(candidate.rationale)>500):
                review_status='rejected'; rejected='unsupported_or_invalid_candidate'
            else:
                next_frame=FrameSpec('F'+str(len(self.frames)),candidate.metric,candidate.maximize,
                                     (candidate.proposed_action,'inspect'))
                # Same raw world, two different readouts; no claim either is better.
                # Demonstrated independent *instrumented* metric, not independent research evidence.
                assessment=review_transition(
                    FrameSnapshot(previous.id,frozenset((previous.metric,)),frozenset(('trace:'+previous.id,))),
                    FrameSnapshot(next_frame.id,frozenset((previous.metric,next_frame.metric)),frozenset(('proposal:'+next_frame.id,))),
                    independent_evidence=frozenset(('simulation-sensor-registry',)),
                    authorization_id='local_sandbox_operator' if approve_frame else None)
                review_status=assessment.decision.value
                if assessment.decision is Decision.AUTHORIZED:
                    self.frame=next_frame
                    self.frames[next_frame.id]=next_frame
        eligible=self._eligible(self.frame,before)
        # The model cannot execute its own actions. Only whitelisted operations are available.
        action=eligible[0] if eligible else 'inspect'
        outcome=self.world.apply(action)
        after=self.world.measure()
        event={
            'cycle':len(self.history)+1,'frame_before':previous.id,'frame_after':self.frame.id,
            'metric_before':previous.metric,'metric_after':self.frame.metric,
            'score_before_on_old_frame':previous_score,
            'score_before_on_new_frame':self.measure(self.frame,before),
            'score_after_on_old_frame':self.measure(previous,after),
            'score_after_on_new_frame':self.measure(self.frame,after),
            'candidate':asdict(candidate) if isinstance(candidate,Candidate) else None,
            'review_status':review_status,'rejection':rejected,
            'eligible_interventions_before':self._eligible(previous,before),
            'eligible_interventions_after_frame_change':eligible,
            'action':action,'world_before':before,'world_after':after,
            'source_type':'provided_generator_not_verified_ai',
        }
        event['record_hash']=hashlib.sha256(json.dumps(event,sort_keys=True).encode()).hexdigest()
        self.history.append(event)
        return event
    def run(self,n=3,approve_frame=False):
        if not 1<=n<=20: raise ValueError('cycles must be 1..20')
        return [self.step(approve_frame=approve_frame) for _ in range(n)]

if __name__=='__main__':
    candidates=[Candidate('Energy is a binding physical bottleneck','energy_ceiling_gap',False,'expand_energy','Observe missed output due to energy limit'),Candidate('Measure underused production capacity','unmet_capacity',False,'boost_output','An alternative distinction'),None]
    run=DynamicCycle(ReplaySource(candidates)).run(3,approve_frame=True)
    print(json.dumps(run,ensure_ascii=False,indent=2))
