"""Finite-world connection-boundary audit for IDOS Social Connection v0.3.

This is a narrow FORMAL TEST HARNESS, not a new social engine. It supplies
observable decision bounds; it does not measure actual understanding, CFV, or MU.
All actors/worlds are synthetic, and worlds are enumerated rather than inferred.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from collections import Counter
from typing import Mapping, Hashable


@dataclass(frozen=True)
class World:
    """Hidden world and permitted actions for each domain and actor.

    local_ok[domain][actor] is the action set actor accepts in this world;
    no actor must adopt a proposal. Forbid/decline is independent of observability.
    """
    key: str
    observation: tuple[Hashable, ...]
    local_ok: Mapping[str, Mapping[str, frozenset[str]]]


@dataclass(frozen=True)
class Boundary:
    possible_worlds: tuple[str, ...]
    guaranteed_actions: tuple[str, ...]
    supported_worlds: Mapping[str, tuple[str, ...]]
    status: str
    reason: str


def boundary(worlds: tuple[World, ...], domain: str, actors: tuple[str, ...],
             observation: tuple[Hashable, ...], action_universe: tuple[str, ...]) -> Boundary:
    """Compute robust connectability in one domain from observable history.

    GUARANTEED iff some same action is permitted by ALL actors in ALL worlds
    consistent with the observation. POSSIBLE_NOT_GUARANTEED iff some action
    works in at least one world only. IMPOSSIBLE iff no action works in any
    consistent world. No probability, psychology, or actual consent is inferred.
    """
    if not worlds or not actors or not action_universe:
        raise ValueError('Worlds, actors and actions are required')
    matching=tuple(w for w in worlds if w.observation == observation)
    if not matching:
        raise ValueError('No world consistent with this observation')
    support={a:[] for a in action_universe}
    for w in matching:
        for a in action_universe:
            if all(a in w.local_ok.get(domain, {}).get(i, frozenset()) for i in actors):
                support[a].append(w.key)
    guarantee=tuple(a for a in action_universe if len(support[a])==len(matching))
    some=any(support.values())
    status='GUARANTEED' if guarantee else ('POSSIBLE_NOT_GUARANTEED' if some else 'IMPOSSIBLE')
    reason={'GUARANTEED':'A jointly permitted action exists in every observationally possible world.',
            'POSSIBLE_NOT_GUARANTEED':'Some worlds permit a joint action, but none works in all possible worlds.',
            'IMPOSSIBLE':'No jointly permitted action exists in any observationally possible world.'}[status]
    return Boundary(tuple(w.key for w in matching), guarantee,
                    {k:tuple(v) for k,v in support.items()},status,reason)


def classify_domains(worlds: tuple[World,...], domains: tuple[str,...],
                     actors: tuple[str,...], observation: tuple[Hashable,...],
                     actions: tuple[str,...]):
    """Three-valued coverage classification is a declared PROXY, not universal social ontology.

    CONNECTED: every domain robustly connectable; LIMITED: some, but not all;
    DISCONNECTED: no domain robustly connectable. Each domain keeps a richer
    GUARANTEED/POSSIBLE_NOT_GUARANTEED/IMPOSSIBLE status separately.
    """
    out={d:boundary(worlds,d,actors,observation,actions) for d in domains}
    count=sum(x.status=='GUARANTEED' for x in out.values())
    return ('CONNECTED' if count==len(domains) else 'LIMITED' if count else 'DISCONNECTED'),out


def observational_impossibility_witness(worlds:tuple[World,...],domain:str,
                                        actors:tuple[str,...],obs:tuple[Hashable,...],
                                        actions:tuple[str,...]):
    """Find two indistinguishable worlds with disjoint joint-allowed actions.

    This is a SUFFICIENT witness for failure of a deterministic guarantee;
    absence of a pairwise witness does not imply existence of a common action.
    """
    matched=[w for w in worlds if w.observation==obs]
    for i,x in enumerate(matched):
        x_ok={a for a in actions if all(a in x.local_ok.get(domain,{}).get(actor,frozenset()) for actor in actors)}
        for y in matched[i+1:]:
            y_ok={a for a in actions if all(a in y.local_ok.get(domain,{}).get(actor,frozenset()) for actor in actors)}
            if x_ok and y_ok and not x_ok.intersection(y_ok):
                return (x.key,y.key)
    return None


def make_world(key, obs, choices, domain='decision'):
    return World(key,tuple(obs),{domain:{a:frozenset(vals) for a,vals in choices.items()}})


def temporal_example():
    """Time changes the OBSERVATION and permitted actions; not a learning claim."""
    actors=('A','B'); actions=('left','right')
    initial=(make_world('hidden-left',('unknown',),{'A':{'left'},'B':{'left'}}),
             make_world('hidden-right',('unknown',),{'A':{'right'},'B':{'right'}}))
    informed=(make_world('hidden-left',('observed-left',),{'A':{'left'},'B':{'left'}}),
              make_world('hidden-right',('observed-right',),{'A':{'right'},'B':{'right'}}))
    withdrawn=(make_world('hidden-left',('observed-left',),{'A':{'left'},'B':set()}),)
    return [
        ('t0_ambiguous',boundary(initial,'decision',actors,('unknown',),actions)),
        ('t1_new_observation',boundary(informed,'decision',actors,('observed-left',),actions)),
        ('t2_refusal',boundary(withdrawn,'decision',actors,('observed-left',),actions)),
        ('t3_consent_restored',boundary(informed,'decision',actors,('observed-left',),actions)),
    ]


def triadic_counterexample():
    """X,Y,Z each marginal fair; pair marginals match under XOR and independence.

    Different 3-way parity laws show pairwise DISTRIBUTIONS do not identify
    the joint distribution. Access to a full individual JOINT HISTORY does.
    """
    xor=tuple((x,y,x^y) for x,y in product((0,1),repeat=2))
    independent=tuple(product((0,1),repeat=3))
    # Multiplicities represent equal probability mass in each model.
    def pair_dist(rows,i,j):
        return {pair:n/len(rows) for pair,n in Counter((r[i],r[j]) for r in rows).items()}
    pairwise_equal=all(pair_dist(xor,i,j)==pair_dist(independent,i,j)
                       for i,j in ((0,1),(0,2),(1,2)))
    parity_xor=sum(x^y^z==0 for x,y,z in xor)/len(xor)
    parity_ind=sum(x^y^z==0 for x,y,z in independent)/len(independent)
    return {'pairwise_marginals_equal':pairwise_equal,
            'xor_even_parity_rate':parity_xor,
            'independent_even_parity_rate':parity_ind,
            'full_joint_distinguishes':Counter(xor)!=Counter(independent)}


def two_vs_three_example():
    """Third actor can permit/block; not evidence that 3 actors are necessary."""
    actors2=('A','B'); actors3=('A','B','C'); actions=('a','b')
    w=make_world('w',('same',),{'A':{'a'},'B':{'a'},'C':{'b'}})
    two=boundary((w,),'decision',actors2,('same',),actions)
    three=boundary((w,),'decision',actors3,('same',),actions)
    w2=make_world('w2',('same',),{'A':{'a'},'B':{'a'},'C':{'a'}})
    return {'two':two.status,'three_with_conflict':three.status,
            'three_with_permission':boundary((w2,),'decision',actors3,('same',),actions).status}


def audit_results():
    steps=temporal_example()
    return {
        'scope':'Finite synthetic worlds; necessary/sufficient results are relative to explicit assumptions.',
        'temporal':[{ 'stage':label,'status':res.status,'guaranteed_actions':res.guaranteed_actions,
                      'possible_worlds':res.possible_worlds} for label,res in steps],
        'three_actor':two_vs_three_example(),
        'triadic_distribution':triadic_counterexample(),
        'novelty_claim':'None. Strong full-history baselines contain the same joint information.'
    }


if __name__=='__main__':
    import json
    print(json.dumps(audit_results(),indent=2,ensure_ascii=False))
