"""IDOS Connection Boundary Audit v0.2 (T5/T6): controlled baselines and observables.

No real human/AI cognition, consent authentication, semantic verification, or
causal mutual learning is claimed. Existing v0.1 boundary calculation reused.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from typing import Iterable
from connection_boundary_audit import World, boundary, make_world


@dataclass(frozen=True)
class Challenge:
    challenger: str
    respondent: str
    claim: str
    reference_frame: str
    evidence_ids: tuple[str, ...]
    required_evidence: tuple[str, ...]


@dataclass(frozen=True)
class Response:
    respondent: str
    evidence_ids: tuple[str, ...]
    disclosed_ids: tuple[str, ...]
    acknowledgment: bool
    challenged_meaning_resolved: bool  # externally asserted, not inferred


def verification_opportunity(challenge: Challenge, response: Response,
                             public_evidence: Iterable[str]) -> dict:
    """Auditable opportunity to check a claim; NOT actual truth/understanding."""
    public = set(public_evidence)
    supplied = set(response.evidence_ids) & set(response.disclosed_ids) & public
    complete = (response.respondent == challenge.respondent and response.acknowledgment
                and set(challenge.required_evidence).issubset(supplied))
    return {
        'challenge_addressed': complete,
        'missing_public_evidence': sorted(set(challenge.required_evidence)-supplied),
        'semantic_equivalence_verified': False,
        'declared_interpretation_resolved': response.challenged_meaning_resolved if complete else False,
    }


@dataclass(frozen=True)
class UpdateOpportunity:
    actor: str
    before_frame: str
    candidate_frame: str
    offered: bool
    allowed_to_decline: bool
    choice: str  # adopt, hold, reject
    trace_id: str


def mutual_update_opportunity(offered: tuple[UpdateOpportunity, ...],
                              actors: tuple[str, ...]) -> dict:
    """Operational proxy: separate, permissioned, traceable paths for each actor.

    No requirement that both actually adopt, and no learning is implied.
    """
    relevant = {a:[x for x in offered if x.actor == a] for a in actors}
    by_actor = {a: (len(paths)==1 and paths[0].offered and paths[0].allowed_to_decline
                    and paths[0].choice in {'adopt','hold','reject'} and bool(paths[0].trace_id)
                    and bool(paths[0].before_frame) and bool(paths[0].candidate_frame))
                for a,paths in relevant.items()}
    return {'opportunity_for_each_actor': by_actor,
            'bilateral_paths_preserved': len(actors)>1 and all(by_actor.values()),
            'substantive_mutual_learning_proven': False}


@dataclass(frozen=True)
class AuditRecord:
    tick: int
    observation: tuple[str, ...]
    actor: str
    event_type: str
    value: str
    shared: bool
    provenance: str


def reopen_history(records: tuple[AuditRecord, ...], tick: int,
                   requested: tuple[str, ...]) -> dict:
    """Historic *authorized* evidence only; no hindsight or private disclosure."""
    found={r.event_type:r.value for r in records if r.tick==tick and r.shared
           and r.provenance and r.event_type in requested}
    return {'historic_tick':tick, 'available':found,
            'missing': sorted(set(requested)-set(found)),
            'invented_observations': False}


def independent_full_information_baseline(worlds: tuple[World,...], domain: str,
                                          actors: tuple[str,...], obs:tuple[str,...],
                                          actions:tuple[str,...]) -> tuple[str,tuple[str,...]]:
    """Reference from FULL world histories, independently of boundary() algorithm."""
    relevant=[w for w in worlds if w.observation==obs]
    if not relevant: raise ValueError('No matching world')
    allowed_per_world=[]
    for w in relevant:
        per_world=[action for action in actions
                   if all(action in w.local_ok.get(domain,{}).get(actor,frozenset()) for actor in actors)]
        allowed_per_world.append(set(per_world))
    common=set(actions)
    for accepted in allowed_per_world: common.intersection_update(accepted)
    if common: return 'GUARANTEED',tuple(a for a in actions if a in common)
    if any(allowed_per_world): return 'POSSIBLE_NOT_GUARANTEED',()
    return 'IMPOSSIBLE',()


def recency_only_baseline(worlds:tuple[World,...],domain:str,actors:tuple[str,...],
                          obs:tuple[str,...],actions:tuple[str,...]):
    """Intentionally WEAK comparison, chooses latest matching world; may be wrong."""
    matches=[w for w in worlds if w.observation==obs]
    if not matches: raise ValueError('No matching world')
    return independent_full_information_baseline((matches[-1],),domain,actors,obs,actions)


def comparison_scenarios():
    actors=('human','ai')
    actions=('plan_a','plan_b')
    scenarios={
      'ambiguous_conflict':(
       make_world('w_a',('same',),{'human':{'plan_a'},'ai':{'plan_a'}}),
       make_world('w_b',('same',),{'human':{'plan_b'},'ai':{'plan_b'}})),
      'jointly_robust':(
       make_world('w_a',('same',),{'human':{'plan_a'},'ai':{'plan_a'}}),
       make_world('w_b',('same',),{'human':{'plan_a','plan_b'},'ai':{'plan_a'}})),
      'total_conflict':(
       make_world('w_a',('same',),{'human':{'plan_a'},'ai':{'plan_b'}}),
       make_world('w_b',('same',),{'human':{'plan_b'},'ai':{'plan_a'}})),
      'explicit_refusal':(
       make_world('w_a',('same',),{'human':set(),'ai':{'plan_a'}}),),
    }
    rows=[]
    for name,worlds in scenarios.items():
        robust=boundary(worlds,'decision',actors,('same',),actions)
        full=independent_full_information_baseline(worlds,'decision',actors,('same',),actions)
        lossy=recency_only_baseline(worlds,'decision',actors,('same',),actions)
        rows.append({'scenario':name,'idos_status':robust.status,
                     'full_history_status':full[0],'full_history_equal':(robust.status,robust.guaranteed_actions)==full,
                     'recency_only_status':lossy[0],'lossy_disagrees':robust.status!=lossy[0]})
    return rows


def run_results():
    c=Challenge('human','ai','policy is safe','human_frame',('public:1',),('public:1',))
    ok=verification_opportunity(c,Response('ai',('public:1',),('public:1',),True,False),('public:1',))
    withheld=verification_opportunity(c,Response('ai',('private:1',),('private:1',),True,True),('public:1',))
    paths=(UpdateOpportunity('human','frame_h','candidate',True,True,'reject','evt_h'),
           UpdateOpportunity('ai','frame_a','candidate',True,True,'adopt','evt_ai'))
    mu=mutual_update_opportunity(paths,('human','ai'))
    history=(AuditRecord(0,('initial',),'human','reason','dissent',True,'human:test'),
             AuditRecord(0,('initial',),'human','private_reason','secret',False,'human:private'),
             AuditRecord(1,('later',),'ai','reason','new evidence',True,'ai:test'))
    return {'scope':'synthetic software proxies; not demonstrated semantic CFV or actual MU',
            'T5':comparison_scenarios(),
            'T6':{'public_challenge':ok,'private_only_challenge':withheld,
                  'independent_paths':mu,
                  'historic_reopening':reopen_history(history,0,('reason','private_reason','future'))},
            'limitations':['Full-history baseline matches IDOS on all controlled cases.',
                           'A lossy baseline can fail due to missing history, not architecture identity.',
                           'Challenges and policy paths are caller-attested; no real learning or authentication.']}

if __name__=='__main__':
    import json
    print(json.dumps(run_results(),indent=2,ensure_ascii=False))
