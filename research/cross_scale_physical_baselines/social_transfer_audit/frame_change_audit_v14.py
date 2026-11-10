"""IDOS v1.4: prequential frame-change detection and diagnostic limits.

Synthetic data based on v1.3; independent validation calibrates alert thresholds.
Event observations and outcomes are separated to avoid leakage. Not causal identification.
Requires the previously archived multiframe_relation_audit_v13.py.
"""
from __future__ import annotations
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss
from multiframe_relation_audit_v13 import generate, select_pairs, observed_current

SEED = 20261111
WINDOW = 100

def shift_data(d, regime, seed=25):
    """Construct fresh post-change observations and/or outcomes, never modifying input."""
    rng = np.random.default_rng(seed)
    d = {k: v.copy() if hasattr(v, 'copy') else v for k, v in d.items()}
    if regime == 'none':
        return d
    if regime == 'observer_A':
        # Change interpretation of A's reporting symbols only, *after* outcomes.
        # Observational shift, not a change in the true relation mechanism.
        a = d['events'][:, 0, :]
        d['events'][:,0,:] = np.where(a == 1,5, np.where(a == 5,1,a))
    elif regime in ('relation','environment'):
        # Same event streams, changed outcome mechanisms.
        eligible = d['eligible'].astype(bool)
        if regime == 'relation':
            transferred_exit = d['latent_transfer'].astype(bool) & (d['exit'] == 1)
            p = np.where(eligible & transferred_exit,.48,np.where(eligible,.94,.03))
        else:
            p = np.where(eligible,.69,.03)
        d['y'] = rng.binomial(1,p)
    else:
        raise ValueError(regime)
    return d

def blocks(x, size=WINDOW):
    return np.asarray(x[:len(x)//size*size]).reshape(-1,size).mean(axis=1)

def relation_features(d, selected):
    """Equivalent to v1.3 features, computing only selected pair indicators."""
    obs=d['events']
    def ordered_batch(agent_i, symbol_i, agent_j, symbol_j):
        aa=(obs[:,agent_i,:] == symbol_i)
        bb=(obs[:,agent_j,:] == symbol_j)
        ia=np.argmax(aa,axis=1)
        ib=obs.shape[2]-1-np.argmax(bb[:,::-1],axis=1)
        return (aa.any(axis=1) & bb.any(axis=1) & (ia<ib)).astype(int)
    ia,ib=selected
    ab=ordered_batch(0,ia//6,1,ia%6)
    bc=ordered_batch(1,ib//6,2,ib%6)
    transfer=ab*bc*d['permissions'][:,2]
    return np.column_stack([observed_current(d),d['permissions'][:,2],ab,bc,transfer,transfer*d['exit']])

def fit_model(train, selected):
    clf = LogisticRegression(max_iter=800, C=30)
    clf.fit(relation_features(train,selected),train['y'])
    return clf

def evaluate_run(clf, selected, d, threshold, window=WINDOW):
    x = relation_features(d,selected)
    pred = np.clip(clf.predict_proba(x)[:,1],1e-5,1-1e-5)
    losses = (pred-d['y'])**2
    loss_blocks = blocks(losses,window)
    alerts=np.flatnonzero(loss_blocks>threshold)
    return {'brier': float(np.mean(losses)),
            'first_alert_observations':int((alerts[0]+1)*window) if len(alerts) else None,
            'alerted_blocks':int(len(alerts)),
            'total_blocks':int(len(loss_blocks))},pred

def diagnostics(train, d, selected, p):
    """Observable signatures, not ground-truth regime labels."""
    # Change in A's symbol frequencies (a 1↔5 exchange is unidentifiable here).
    fa=np.bincount(d['events'][:,0,:].ravel(), minlength=6)/d['events'][:,0,:].size
    ft=np.bincount(train['events'][:,0,:].ravel(),minlength=6)/train['events'][:,0,:].size
    exit_ = (d['exit']==1) & (d['permissions'][:,0]==1) & (d['permissions'][:,1]==1) & (d['revoked']==0)
    stay_ = (d['exit']==0) & (d['permissions'][:,0]==1) & (d['permissions'][:,1]==1) & (d['revoked']==0)
    def residual(mask):
        return float(np.mean(d['y'][mask]-p[mask])) if mask.any() else None
    return {'A_symbol_total_variation':float(.5*np.abs(fa-ft).sum()),
            'residual_exit_permitted':residual(exit_),
            'residual_stay_permitted':residual(stay_),
            'mean_residual':float(np.mean(d['y']-p))}

def adapt_and_score(train, d, selected, warmup=300):
    """Fixed-model and recency-refit *both* predict on the same untouched future subset.
    Past observed outcomes from the warmup are usable; future outcomes are not.
    """
    old=fit_model(train,selected)
    new=fit_model({k:v[:warmup] for k,v in d.items()}, selected)
    future={k:v[warmup:] for k,v in d.items()}
    x=relation_features(future,selected)
    y=future['y']
    return {'fixed_brier':float(brier_score_loss(y,old.predict_proba(x)[:,1])),
            'recent_refit_brier':float(brier_score_loss(y,new.predict_proba(x)[:,1])),
            'observed_refit_labels':warmup,'future_labels_used_to_refit':0}

def run():
    train=generate(4200,111)
    valid=generate(2000,222)
    selected=select_pairs(train)
    fitted=fit_model(train,selected)
    vp=fitted.predict_proba(relation_features(valid,selected))[:,1]
    calibration=blocks((vp-valid['y'])**2)
    # Multiple windows: empirical 99th-percentile baseline, no nominal alpha guarantee.
    threshold=float(np.quantile(calibration,.99))
    regimes={}
    for i,name in enumerate(('none','observer_A','relation','environment')):
        d=shift_data(generate(2400,301+i),name,1001+i)
        metric,p=evaluate_run(fitted,selected,d,threshold)
        metric['signatures']=diagnostics(train,d,selected,p)
        metric['adaptation']=adapt_and_score(train,d,selected)
        regimes[name]=metric
    return {'version':'1.4','seed':SEED,'source':'v1.3 synthetic generator',
            'selected_pairs':{'A_to_B':list(divmod(selected[0],6)),'B_to_C':list(divmod(selected[1],6))},
            'calibration_windows':len(calibration),'detection_threshold':threshold,
            'window':WINDOW,'regimes':regimes,
            'qualification':'Mechanisms and shift timing were controlled by experimenter. Observable diagnostic signatures are not a causal identification algorithm. Refit uses 300 post-change labeled cases; fixed and refit evaluated on same future cases.'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
