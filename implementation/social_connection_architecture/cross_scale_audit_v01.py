"""Synthetic structural-formation audit, not a new IDOS law.
Reuses the published Connection Boundary Audit v0.1 decision predicate.
"""
from __future__ import annotations
import json
from dataclasses import asdict, dataclass
from itertools import product
from connection_boundary_audit import World, boundary

ACTORS=('A','B')
ACTIONS=('left','right','mediated')

@dataclass(frozen=True)
class ScenarioResult:
    label:str
    status:str
    robust_actions:tuple[str,...]
    candidate_actions:tuple[str,...]
    topology:tuple[str,...]
    explanation:str


def worlds_for(*, signal:bool=False, mediated:bool=False, consent:bool=True, mediator:bool=True):
    """Two hidden worlds. The mediated action is available only if an explicit
    third-party protocol exists and all necessary consent is declared.
    Thus it is *not* automatically discovered by the boundary oracle.
    """
    out=[]
    for idx, action in enumerate(('left','right')):
        obs=(action,) if signal else ('opaque',)
        a={action}; b={action}
        if mediated and consent and mediator:
            a.add('mediated'); b.add('mediated')
        out.append(World(str(idx),obs,{'decision':{'A':frozenset(a),'B':frozenset(b)}}))
    return tuple(out)


def run_scenario(label, *, signal=False, mediated=False, consent=True, mediator=True):
    ws=worlds_for(signal=signal,mediated=mediated,consent=consent,mediator=mediator)
    obs=('left',) if signal else ('opaque',)
    actions=('left','right','mediated') if mediated and mediator else ('left','right')
    res=boundary(ws,'decision',ACTORS,obs,actions)
    topology=('A--B',) if not mediator else ('A--B','A--C','B--C')
    return ScenarioResult(label,res.status,res.guaranteed_actions,actions,topology,res.reason)


def compare():
    rows=(
        run_scenario('t0_private_ambiguous',mediator=False),
        run_scenario('t1_new_public_observation',signal=True,mediator=False),
        run_scenario('t1_proposed_mediator_but_no_protocol',mediator=True),
        run_scenario('t2_mediator_protocol_all_consent',mediated=True),
        run_scenario('t2_mediator_protocol_refused',mediated=True,consent=False),
        run_scenario('t2_protocol_without_mediator',mediated=True,mediator=False),
    )
    return tuple(asdict(r) for r in rows)


def complete_history_baseline(*, signal=False, mediated=False, consent=True, mediator=True):
    """A general-purpose exhaustive planner using the same worlds/observations,
    candidate universe and permissions, without invoking IDOS boundary()."""
    ws=worlds_for(signal=signal,mediated=mediated,consent=consent,mediator=mediator)
    obs=('left',) if signal else ('opaque',)
    actions=('left','right','mediated') if mediated and mediator else ('left','right')
    admissible=[]
    for action in actions:
        if all(action in w.local_ok['decision']['A'] and action in w.local_ok['decision']['B']
               for w in ws if w.observation==obs):
            admissible.append(action)
    return tuple(admissible)


def exhaustive_equivalence():
    # Exercise combinations of observation, protocol, mediator and consent.
    n=0
    for signal,mediated,consent,mediator in product((False,True),repeat=4):
        result=run_scenario('audit',signal=signal,mediated=mediated,consent=consent,mediator=mediator)
        baseline=complete_history_baseline(signal=signal,mediated=mediated,consent=consent,mediator=mediator)
        assert result.robust_actions==baseline
        n+=1
    return n

if __name__=='__main__':
    print(json.dumps({'scenarios':compare(),'same_information_baseline_cases':exhaustive_equivalence()},indent=2))
