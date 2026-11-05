"""IDOS v0.7 — conditional experiment/observation design for pre-registered hypotheses.

No causal identification from correlations; all predictions are explicit assumptions.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from math import exp, log, pi, sqrt
from typing import Sequence
import json
import numpy as np

@dataclass(frozen=True)
class Candidate:
    name: str
    description: str
    # H0, H1, H2 represent suspected causes: handoff friction, workload, missing information.
    means: tuple[float, ...]
    sigma: float
    cost: float
    risk: float
    reference_frame: str = 'review_v1'
    ethical_permission: bool = True
    observational_only: bool = True
    provenance: str = 'hypothetical expert-specified model'

    def __post_init__(self):
        if self.sigma <= 0 or self.cost < 0 or not 0 <= self.risk <= 1:
            raise ValueError('Invalid sigma/cost/risk')
        if not self.reference_frame or not self.provenance:
            raise ValueError('Reference frame and provenance required')


def _check(prior: Sequence[float], candidates: Sequence[Candidate]):
    p = np.array(prior, dtype=float)
    if len(p) < 2 or np.any(p < 0) or not np.isfinite(p).all() or not np.isclose(p.sum(), 1.0):
        raise ValueError('Prior must be a normalized nonnegative distribution over >=2 hypotheses')
    for c in candidates:
        if len(c.means) != len(p) or not np.isfinite(c.means).all():
            raise ValueError('Candidate predictions must align with hypotheses')
    return p


def posterior(prior: Sequence[float], c: Candidate, observation: float):
    p = _check(prior, [c]); m=np.asarray(c.means)
    logp=np.log(np.maximum(p, 1e-300)) - .5*((observation-m)/c.sigma)**2
    logp[p==0] = -np.inf
    logp-=np.max(logp)
    weights=np.exp(logp)
    return (weights/weights.sum()).tolist()


def entropy(p):
    a=np.asarray(p,dtype=float)
    return float(-np.sum(a[a>0]*np.log2(a[a>0])))


def information_gain(prior: Sequence[float], c: Candidate, grid_points: int=4001):
    """Numerical expected reduction in hypothesis entropy, in bits.
    Integrates predictive Gaussian mixture over finite grid (mean +/- 8 sigma).
    """
    p=_check(prior,[c]); m=np.asarray(c.means)
    lo=float(m.min()-8*c.sigma); hi=float(m.max()+8*c.sigma)
    xs=np.linspace(lo,hi,grid_points)
    dens=np.exp(-.5*((xs[:,None]-m[None,:])/c.sigma)**2)/(sqrt(2*pi)*c.sigma)
    weighted=dens*p[None,:]; mix=weighted.sum(axis=1)
    post=weighted/np.maximum(mix[:,None],1e-300)
    ent=-np.sum(np.where(post>0,post*np.log2(np.maximum(post,1e-300)),0),axis=1)
    avg=float(np.trapezoid(ent*mix,xs)/np.trapezoid(mix,xs))
    return max(0., entropy(p)-avg)


def rank_candidates(prior:Sequence[float], candidates:Sequence[Candidate], *, max_risk:float=.25,
                    max_cost:float=10, allowed_frame:str='review_v1', cost_weight:float=.03):
    _check(prior,candidates)
    items=[]
    for c in candidates:
        restrictions=[]
        if not c.ethical_permission: restrictions.append('no_permission')
        if c.risk > max_risk: restrictions.append('risk_exceeded')
        if c.cost > max_cost: restrictions.append('cost_exceeded')
        if c.reference_frame != allowed_frame: restrictions.append('reference_frame_mismatch')
        ig=information_gain(prior,c)
        reasons=[]
        if ig < 1e-5: reasons.append('observationally_equivalent_for_this_candidate')
        score=ig-cost_weight*c.cost
        items.append({'candidate':c.name, 'information_gain_bits':round(ig,6),
            'cost':c.cost,'risk':c.risk,'score':round(score,6),
            'status':'excluded' if restrictions else ('uninformative' if ig < 1e-5 else 'eligible'),
            'reasons':restrictions+reasons,'provenance':c.provenance,
            'observation_only':c.observational_only})
    items.sort(key=lambda it:(it['status']!='eligible',-it['score'],it['candidate']))
    qualified=[r for r in items if r['status']=='eligible' and r['score']>0]
    selected=max(qualified,key=lambda it:it['score'])['candidate'] if qualified else None
    return {'selected':selected,'hypothesis_entropy_bits':round(entropy(prior),6), 'ranking':items,
           'warning':'Predicted information gain depends on specified hypotheses, likelihoods and priors; not evidence of causal truth.'}


def synthetic_candidates():
    return [
        Candidate('repeat_current_log','Same incomplete process log', (0,0,0),1,0.1,.0),
        Candidate('capture_handoff_reason','Record precise handoff reason', (2.4,0.1,0.0),1,1.5,.06),
        Candidate('capture_queue_snapshot','Record review-time backlog by role',(0.0,2.0,0.1),1,1.2,.05),
        Candidate('capture_missing_documents','Record missing-document flags',(0.0,0.2,2.1),1,1.0,.04),
        Candidate('force_staff_rotation','Intervene by forcing staff rotation',(3,0,0),.55,4,.8,ethical_permission=False,observational_only=False),
        Candidate('new_frame_without_bridge','Change scoring reference frame',(4,0,0),1,.5,.01,reference_frame='review_v2'),
    ]


def simulate(seed=20261105,n=600):
    """Independent hypothetical sampling to audit selection and posterior accuracy.
    No empirical human/organizational data are represented.
    """
    rng=np.random.default_rng(seed)
    prior=[1/3]*3; candidates=synthetic_candidates()
    ranked=rank_candidates(prior,candidates)
    selected=next(c for c in candidates if c.name==ranked['selected'])
    true=rng.integers(0,3,size=n)
    observed=rng.normal(np.array(selected.means)[true],selected.sigma)
    p=np.asarray([posterior(prior,selected,float(y)) for y in observed])
    guesses=p.argmax(axis=1)
    return {'setup':{'scenario':'SYNTHETIC ONLY','hypotheses':['handoff_friction','workload','missing_information'],
                     'prior':prior, 'true_state_generation':'uniform draws per independent synthetic case',
                     'observation_generation':'Gaussian assumed likelihoods, not learned from data'},
            'selection':ranked,'validation':{'n':n,'accuracy':round(float(np.mean(guesses==true)),4),
                    'mean_posterior_true':round(float(np.mean(p[np.arange(n),true])),4),
                    'selected':selected.name,'post_observation_illustration':posterior(prior,selected,2.1)}}

if __name__=='__main__':
    from pathlib import Path
    out=Path(__file__).with_name('synthetic_results.json')
    out.write_text(json.dumps(simulate(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Results:',out)
