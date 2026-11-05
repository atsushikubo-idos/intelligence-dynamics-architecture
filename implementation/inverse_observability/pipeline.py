"""Pilot connecting v0.6 event evidence, data-fitted v0.7 observation likelihoods,
and v0.8 family adequacy. SYNTHETIC experiment; classification is not cause identification.
No intervention execution; no automatic reference-frame update.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
for directory in ('dependencies/v0_6','dependencies/v0_7','dependencies/v0_8'):
    sys.path.insert(0,str(ROOT/directory))
from eventlog_validation import synthesize,make_cases,read_csv,_fit_predict
from observation_design import Candidate,rank_candidates,posterior
from open_set_audit import HypothesisFamily,EvidenceBatch,audit,propose_next_step

FEATURES=['pre_review_hours','queue_at_review','handoff_at_review','pre_review_rework']

def _train_predict(train, test, names):
    return np.asarray(_fit_predict(train,test,names))

def _split(cases):
    if len(cases)<90:raise ValueError('>=90 complete cases required')
    n=len(cases);a=int(.6*n);b=int(.8*n)
    return cases[:a],cases[a:b],cases[b:]

def _mae(y,yp):return float(np.mean(np.abs(y-yp)))

def _fit_observation_likelihoods(train,feature_names):
    """Data-fitted P(feature | high/low future duration), strictly train-only.
    Gaussian approximation used for binary features as a simplifying working model.
    """
    y=np.log1p([c['duration_hours'] for c in train])
    threshold=float(np.median(y))
    classes=y>threshold
    prior=[float(np.mean(~classes)), float(np.mean(classes))]
    options=[]
    for name in feature_names:
        x=np.array([float(c[name]) for c in train]);m=[]
        for k in (False,True):
            values=x[classes==k]
            m.append(float(np.mean(values)))
        # pooled class-within variance; floor prevents false high confidence for binary fields
        sigma=max(float(np.sqrt(np.mean((x-np.where(classes,m[1],m[0]))**2))),.30)
        options.append(Candidate(name,name,tuple(m),sigma,1.0,0.0,
                   reference_frame='case_review_v1', provenance='fitted on training subset only; Gaussian working approximation'))
    return threshold,prior,options

def run(events, *, seed=20261105, shifted=False):
    cases,meta=make_cases(events)
    train,calib,test=_split(cases)
    baseline=['pre_review_hours']
    # Fixed candidate list and baseline; fit on training; compare on calibration; choose once.
    candidates={'baseline':baseline,'handoff':baseline+['handoff_at_review'],
                'rework':baseline+['pre_review_rework'], 'queue':baseline+['queue_at_review']}
    yc=np.log1p([c['duration_hours'] for c in calib]); yt=np.log1p([c['duration_hours'] for c in test])
    calib_mae={k:_mae(yc,_train_predict(train,calib,v)) for k,v in candidates.items()}
    chosen=min(calib_mae,key=calib_mae.get)
    pred_test=_train_predict(train,test,candidates[chosen]); pred_base=_train_predict(train,test,baseline)
    # v0.7 likelihoods fitted to observed 2-class outcome, not causal hypotheses.
    threshold,prior,opts=_fit_observation_likelihoods(train,FEATURES)
    ranking=rank_candidates(prior,opts,allowed_frame='case_review_v1',cost_weight=.0)
    best=ranking['selected']; selected=next(c for c in opts if c.name==best)
    post=[posterior(prior,selected,float(c[best]))[1] for c in test]
    actual=yt>threshold
    pred_class=np.array(post)>.5
    # Brier score, using base-rate as null baseline.
    brier=float(np.mean((np.array(post)-actual)**2))
    brier_null=float(np.mean((prior[1]-actual)**2))
    # v0.8: compute residual noise ONLY using calibration (not test).
    calib_resid=yc-_train_predict(train,calib,candidates[chosen])
    noise=max(float(np.std(calib_resid,ddof=1)),.05)
    # pre-defined family of stable residual offset and +2 calibrated std offset;
    # audit is a *diagnostic* under iid Gaussian assumption, not a causal test.
    fam=HypothesisFamily(('stable_residual','positive_shift'),(0.,2*noise),noise,
         'case_review_v1','training-fitted predictive model; calibration-only noise estimate')
    test_resid=yt-pred_test
    report=audit(fam,EvidenceBatch(tuple(map(float,test_resid)),'case_review_v1',
         'SYNTHETIC held-out event log, test only'),mc=2999,seed=seed+20)
    return {'scope':'SYNTHETIC ONLY; same-source train/calibration/test; no causal inference',
      'n':{'train':len(train),'calibration':len(calib),'test':len(test)},
      'metadata':meta,'time_boundaries':{'calibration_first_start':calib[0]['start'].isoformat(),'test_first_start':test[0]['start'].isoformat()},
      'model_selection':{'calibration_mae':calib_mae,'chosen':chosen,'selection_data':'calibration only'},
      'held_out_predictive':{'baseline_log_mae':_mae(yt,pred_base), 'chosen_log_mae':_mae(yt,pred_test),
         'relative_mae_change_pct':float(100*(_mae(yt,pred_base)-_mae(yt,pred_test))/_mae(yt,pred_base))},
      'observation_design':{'hypotheses':'observed low vs high future duration; NOT causal explanations',
         'training_threshold_log_duration':threshold,'training_class_prior':prior,
         'selected_observation':best,'ranking':ranking['ranking'],'heldout_brier':brier,
         'heldout_prior_brier':brier_null,'heldout_classification_accuracy':float(np.mean(pred_class==actual)),
         'warning':'Candidate features are already in the log; real new observation was not collected. Gaussian approximation especially limited for binary features.'},
      'family_audit':{'calibration_noise_sigma':noise,'result':report,'next':propose_next_step(report),
         'warning':'v0.8 assumes independent Gaussian residuals and one shared mean per batch; not validated for operational events.'},
      'reference_frame':{'id':'case_review_v1','bridge_to_new_frame':False,'12PDM_labels':'not automatically assigned'},
      'limitations':['no empirical organizational data','no genuinely new sensor acquired','all candidate features observed before first review',
        'no causal latent structure identification','no automated discovery frame transition']}

def main():
    base=synthesize(360,seed=71)
    stable=run(base)
    # Shifting held-out outcomes only after chronological split; model fitted on unchanged histories.
    # Uses fixed positive +72h on held-out cases, without changing case features.
    cases,meta=make_cases(base)
    boundary=cases[int(.8*len(cases))]['start']
    altered=[]
    for ev in base:
        ev=ev.copy()
        if ev['activity'] in {'APPROVE','REJECT'} and ev['case_id'] in {c['case_id'] for c in cases if c['start']>=boundary}:
            from datetime import timedelta
            ev['timestamp']=ev['timestamp']+timedelta(hours=72)
        altered.append(ev)
    drift=run(altered)
    payload={'stable':stable,'shifted_holdout':drift,'shift_note':'Synthetic shift: +72h on test-period terminal events only.'}
    output=Path(__file__).with_name('results.json')
    output.write_text(json.dumps(payload,indent=2,ensure_ascii=False,default=str)+'\n',encoding='utf-8')
    return payload

if __name__=='__main__':
    x=main()
    for key in ('stable','shifted_holdout'):
        y=x[key]; print(key,'n',y['n'],'selected',y['model_selection']['chosen'],'nextobs',y['observation_design']['selected_observation'],
           'MAEchange',round(y['held_out_predictive']['relative_mae_change_pct'],2),
           'brier',round(y['observation_design']['heldout_brier'],3),
           'audit',y['family_audit']['result']['status'],'p',y['family_audit']['result'].get('monte_carlo_p'))
