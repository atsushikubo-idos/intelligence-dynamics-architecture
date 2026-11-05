"""IDOS Inverse Observability v0.8: open-set predictive adequacy audit.

Hypotheses and Gaussian observation likelihoods are explicitly ASSUMED.
Tests assess adequacy of a pre-registered closed family; they cannot discover a new cause.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import log
from typing import Sequence
import json
import numpy as np

@dataclass(frozen=True)
class HypothesisFamily:
    names: tuple[str,...]
    means: tuple[float,...]
    sigma: float
    frame: str
    provenance: str
    def __post_init__(self):
        if len(self.names)<2 or len(self.means)!=len(self.names) or len(set(self.names))!=len(self.names):
            raise ValueError('Must define >=2 distinct hypotheses and aligned means')
        if not self.frame or not self.provenance or self.sigma<=0 or not np.isfinite(self.sigma):
            raise ValueError('Frame, provenance, positive noise required')
        if not np.isfinite(np.array(self.means)).all():
            raise ValueError('Hypothesis means must be finite')

@dataclass(frozen=True)
class EvidenceBatch:
    values: tuple[float,...]
    frame: str
    provenance: str
    phase: str = 'evaluation'
    def __post_init__(self):
        if len(self.values)<6 or not np.isfinite(np.asarray(self.values,dtype=float)).all():
            raise ValueError('At least six finite measurements required')
        if not self.frame or not self.provenance:
            raise ValueError('Frame and provenance required')
        if self.phase!='evaluation':
            raise ValueError('Evaluation batch must not be training/calibration data')


def _min_sse(values:np.ndarray, means:np.ndarray, sigma:float):
    residuals=(values[None,:]-means[:,None])/sigma
    ss=np.sum(residuals**2,axis=1)
    return float(np.min(ss)),int(np.argmin(ss))


def _critical_null(family:HypothesisFamily,n:int,mc:int,seed:int,alpha:float):
    """Simulate one H per entire batch: NOT one H per measurement."""
    rng=np.random.default_rng(seed)
    means=np.asarray(family.means,dtype=float)
    draws=rng.integers(0,len(means),size=mc)
    obs=rng.normal(means[draws,None], family.sigma, size=(mc,n))
    sse=np.min(np.sum(((obs[:,None,:]-means[None,:,None])/family.sigma)**2,axis=2),axis=1)
    return np.sort(sse)


def audit(family:HypothesisFamily, batch:EvidenceBatch, *, alpha:float=0.05,
          mc:int=10000, seed:int=101):
    """Pre-registered minimal-SSE predictive adequacy test with MC null calibration.

    'compatible' means not rejected by THIS particular finite-sample test.
    'family_rejected' means none of the specified models fit under assumed likelihood.
    Statistical audit alone cannot distinguish new mechanism from noise shift.
    """
    if family.frame!=batch.frame:
        return {'status':'blocked_reference_frame', 'reason':'unverified_measurement_bridge',
                'family_frame':family.frame,'evidence_frame':batch.frame,
                'provenance':batch.provenance}
    if not 0<alpha<.5 or mc<999: raise ValueError('Invalid alpha or Monte Carlo budget')
    vals=np.asarray(batch.values,dtype=float)
    means=np.asarray(family.means,dtype=float)
    score,k=_min_sse(vals,means,family.sigma)
    null=_critical_null(family,len(vals),mc,seed,alpha)
    # Randomization p-value: conservative +1 correction.
    p=(int(np.count_nonzero(null>=score))+1)/(mc+1)
    residual=(vals-means[k])
    standardized_mean=float(np.mean(residual)/family.sigma)
    standardized_sd=float(np.std(residual,ddof=1)/family.sigma)
    # Descriptive diagnostics; no causal interpretation or calibrated subtype inference.
    hints=[]
    if abs(standardized_mean) > 2.5/np.sqrt(len(vals)):
        hints.append('systematic_shift_or_wrong_mean')
    if standardized_sd>1.5:
        hints.append('variance_shift_or_dependency_or_outliers')
    if standardized_sd<.5:
        hints.append('variance_overestimated_or_dependency')
    return {'status':'family_rejected' if p<=alpha else 'compatible_not_proven',
            'best_fitting_hypothesis':family.names[k],
            'min_standardized_sse':round(score,5),'monte_carlo_p':round(p,6),
            'alpha':alpha,'n':len(vals),'mc':mc,'reference_frame':batch.frame,
            'model_provenance':family.provenance,'evidence_provenance':batch.provenance,
            'standardized_residual_mean':round(standardized_mean,5),
            'standardized_residual_sd':round(standardized_sd,5),
            'diagnostic_hints':hints,
            'epistemic_limits':[
                'Rejection does not establish a new cause or new reference frame',
                'Noise changes, dependence, contamination, wrong parameters can also produce rejection',
                'Compatibility is not proof that any hypothesis is true',
                'Independent measurement noise and pre-specified Gaussian likelihoods assumed'
            ]}


def propose_next_step(result:dict):
    """Audit routing only; never updates a reference frame automatically."""
    if result['status']=='blocked_reference_frame':
        return {'action':'request_measurement_bridge','update_reference_frame':False,
                'reason':'Existing observations not comparable under approved bridge'}
    if result['status']=='compatible_not_proven':
        return {'action':'continue_external_validation','update_reference_frame':False,
                'reason':'No evidence to reject family, not evidence of causal truth'}
    return {'action':'review_model_and_measurement','update_reference_frame':False,
            'candidate_checks':['recalibrate_noise','audit_measurement_drift','inspect_temporal_dependence',
                                'record_unexplained_residual','consider_alternative_hypotheses',
                                'design_new_observation_subject_to_permission'],
            'reason':'Open-set alert; no automatic attribution to unknown structure'}


def demonstration(seed=20261105):
    family=HypothesisFamily(('handoff','workload','missing_information'),
                            (0.,2.,4.),1.,'review_v1',
                            'assumed Gaussian means, not learned from actual process data')
    rng=np.random.default_rng(seed)
    cases={
        'in_family':rng.normal(2,1,48),
        'unlisted_shift':rng.normal(7,1,48),
        'noise_inflation':rng.normal(2,3,48),
    }
    results={}
    for key,values in cases.items():
        ev=EvidenceBatch(tuple(float(v) for v in values),'review_v1',
                         f'SYNTHETIC generator: {key}, seed={seed}')
        outcome=audit(family,ev,seed=seed+17,mc=10000)
        results[key]={'audit':outcome,'next_step':propose_next_step(outcome)}
    blocked=audit(family,EvidenceBatch(tuple(float(v) for v in cases['in_family']),
                                             'review_v2','synthetic unbridged measurement'),seed=seed+17)
    results['unbridged_frame']={'audit':blocked,'next_step':propose_next_step(blocked)}
    return {'scope':'SYNTHETIC, external validity not established',
            'family':{'names':family.names,'means':family.means,'sigma':family.sigma,
                      'frame':family.frame},'results':results}

if __name__=='__main__':
    from pathlib import Path
    p=Path(__file__).with_name('synthetic_results.json')
    p.write_text(json.dumps(demonstration(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Wrote',p)
