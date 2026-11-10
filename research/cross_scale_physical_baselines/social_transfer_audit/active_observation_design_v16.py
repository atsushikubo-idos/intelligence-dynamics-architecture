"""Synthetic active observation design, v1.6. Standard library only.

A/B are observationally equivalent passively, as in v1.5. Candidate probes are
specified by the experimenter; the algorithm chooses among them. This is
Bayesian experimental design, not an IDOS-specific causal discovery algorithm.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import log2, log, exp
from typing import Optional
import random
import json

@dataclass(frozen=True)
class Probe:
    key: str
    p_a: float
    p_b: float
    cost: float
    burden: float
    owner: str
    purpose: str

PROBES = (
    Probe('high_information', .85, .15, 3.0, 3.0, 'A', 'direct_diagnostic'),
    Probe('low_cost', .72, .28, 1.0, .45, 'B', 'limited_diagnostic'),
    Probe('low_burden', .62, .38, .50, .10, 'C', 'minimal_diagnostic'),
    Probe('uninformative', .45, .45, .20, .05, 'C', 'negative_control'),
)

def entropy(p: float) -> float:
    return -sum(v*log2(v) for v in (p, 1-p) if v>0)

def info_gain(prior_a: float, probe: Probe) -> float:
    p1 = prior_a*probe.p_a + (1-prior_a)*probe.p_b
    if p1 in (0,1): return 0.
    post1 = prior_a*probe.p_a/p1
    post0 = prior_a*(1-probe.p_a)/(1-p1)
    return max(0., entropy(prior_a)-p1*entropy(post1)-(1-p1)*entropy(post0))

def bayes_update(prior_a: float, probe: Probe, outcome: int) -> float:
    if outcome not in (0,1): raise ValueError(outcome)
    pa = probe.p_a if outcome else 1-probe.p_a
    pb = probe.p_b if outcome else 1-probe.p_b
    denom = prior_a*pa+(1-prior_a)*pb
    return prior_a*pa/denom if denom else prior_a

def choose_probe(prior_a: float, candidates: tuple[Probe,...], permissions: dict[str,bool],
                 budget: float, burden_limit: float, policy: str='constrained',
                 lambda_cost: float=.09, lambda_burden: float=.03) -> Optional[Probe]:
    if policy not in ('constrained','information_only','standard_bayesian_design'):
        raise ValueError(policy)
    valid = [p for p in candidates if permissions.get(p.owner,False) and p.cost <= budget+1e-12
             and p.burden <= burden_limit+1e-12]
    if not valid: return None
    if policy == 'information_only':
        return max(valid, key=lambda p:(info_gain(prior_a,p),-p.cost,p.key))
    if policy == 'standard_bayesian_design':
        # Exact standard decision-theoretic comparator; same utility and abstention as constrained.
        scored = [(info_gain(prior_a,p)-lambda_cost*p.cost-lambda_burden*p.burden,p) for p in valid]
        best = max(scored,key=lambda pair:(pair[0],-pair[1].cost,pair[1].key))
        return best[1] if best[0]>0 else None
    scored = [(info_gain(prior_a,p)-lambda_cost*p.cost-lambda_burden*p.burden,p) for p in valid]
    best = max(scored,key=lambda pair:(pair[0],-pair[1].cost,pair[1].key))
    return best[1] if best[0]>0 else None

def run_trial(cause: str, seed: int, policy: str, permissions: dict[str,bool],
              budget: float=6., max_steps: int=8, burden_limit: float=3.5,
              candidates: tuple[Probe,...]=PROBES, confidence: float=.95,
              lambda_cost: float=.09,lambda_burden: float=.03) -> dict:
    if cause not in ('A','B'): raise ValueError(cause)
    rng=random.Random(seed)
    p=.5; events=[]; remaining=budget
    for _ in range(max_steps):
        if p >= confidence or p <= 1-confidence: break
        probe=choose_probe(p,candidates,permissions,remaining,burden_limit,policy,lambda_cost,lambda_burden)
        if probe is None: break
        outcome = int(rng.random() < (probe.p_a if cause=='A' else probe.p_b))
        prev=p; p=bayes_update(p,probe,outcome)
        remaining -= probe.cost
        events.append({'probe':probe.key,'owner':probe.owner,'outcome':outcome,
                       'prior_a':round(prev,8),'posterior_a':round(p,8),
                       'cost':probe.cost,'information_gain':round(info_gain(prev,probe),8)})
    label = 'A' if p>=confidence else 'B' if p<=1-confidence else 'undetermined'
    return {'actual':cause,'decision':label,'posterior_a':p,'count':len(events),
            'cost':round(budget-remaining,8),'events':events,
            'reason': 'posterior_threshold' if label!='undetermined' else 'insufficient_permitted_evidence_or_budget'}

def evaluate(reps: int=300,seed: int=20261111) -> dict:
    scenarios={
        'all_permitted':{'A':True,'B':True,'C':True},
        'direct_probe_refused':{'A':False,'B':True,'C':True},
        'only_minimal_probe':{'A':False,'B':False,'C':True},
        'all_refused':{'A':False,'B':False,'C':False},
    }
    out={}
    for scenario,permissions in scenarios.items():
        out[scenario]={}
        for policy in ('information_only','standard_bayesian_design','constrained'):
            trials=[]
            for cause in ('A','B'):
                for k in range(reps):
                    # Pair seeds across policies for reproducibility, not strict CRN across different probes.
                    trials.append(run_trial(cause,seed+100000*(cause=='B')+k,policy,permissions))
            total=len(trials)
            out[scenario][policy]={
                'n':total,
                'accuracy_without_abstentions':(sum(t['decision']==t['actual'] for t in trials)/sum(t['decision']!='undetermined' for t in trials)) if any(t['decision']!='undetermined' for t in trials) else None,
                'coverage':sum(t['decision']!='undetermined' for t in trials)/total,
                'wrong_decision_rate':sum(t['decision'] not in ('undetermined',t['actual']) for t in trials)/total,
                'mean_cost':sum(t['cost'] for t in trials)/total,
                'mean_probes':sum(t['count'] for t in trials)/total,
                'permission_violations':sum(not permissions.get(e['owner'],False) for t in trials for e in t['events']),
                'probe_counts':{p.key:sum(e['probe']==p.key for t in trials for e in t['events']) for p in PROBES}
            }
    # A and B have identical passive law; equal prior means mutual information 0.
    return {'config':{'reps_per_cause':reps,'seed':seed,'budget':6.,'max_steps':8,
                      'confidence':.95,'burden_limit':3.5,'lambda_cost':.09,'lambda_burden':.03,
                      'prior_a':.5,'passive_p_a':.45,'passive_p_b':.45,
                      'note':'Candidate probe likelihoods are known to the algorithm; no causal identification beyond stipulated A/B world.'},
            'candidate_probes':[vars(p) for p in PROBES],
            'initial_information_gain_bits':{p.key:info_gain(.5,p) for p in PROBES},
            'passive_information_gain_bits':0.0,
            'results':out,
            'limitations':['Synthetic Bernoulli environment; true probe responses supplied by researcher.',
                           'Consent represented by a Boolean gate, not a measurement of real autonomy.',
                           'Same posterior-based baseline with same utility has identical selection decisions.',
                           'The experiment does not discover new probes or identify unknown causes.',
                           'No field evidence; no IDOS-specific predictive advantage established.']}

if __name__=='__main__':
    print(json.dumps(evaluate(),indent=2,ensure_ascii=False))
