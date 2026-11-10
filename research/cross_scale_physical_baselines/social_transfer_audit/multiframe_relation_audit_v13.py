"""IDOS synthetic multi-frame relational predictivity audit v1.3.

Synthetic 3-actor episodes; observational rather than causal evidence. Pairwise
patterns are discovered on training only. All comparison models get raw event
histories, permissions, and context when claimed 'full information'.
"""
from __future__ import annotations
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import brier_score_loss, log_loss

N_SYMBOLS=6
T=6


def ordered(a, symbol_a, b, symbol_b):
    ia=np.where(a == symbol_a)[0]; ib=np.where(b == symbol_b)[0]
    return bool(len(ia) and len(ib) and ia.min() < ib.max())


def generate(n=6000, seed=101, regime='base'):
    rng=np.random.default_rng(seed)
    # Each agent has a private stream; symbols are opaque, with NO semantic labels.
    obs=rng.integers(N_SYMBOLS,size=(n,3,T))
    for k in range(n):
        # Plant syntactically meaningful sequences, but also negative controls.
        if rng.random()<.52:
            p=rng.choice(T,size=3,replace=False)
            p.sort()
            obs[k,0,p[0]]=1
            obs[k,1,p[1]]=4
            obs[k,2,p[2]]=2
        if rng.random()<.20:
            p=rng.choice(T,size=2,replace=False); p.sort()
            obs[k,0,p[0]]=1;obs[k,1,p[1]]=4
    permissions=rng.binomial(1,[.88,.85,.90],size=(n,3))
    # A, B permission + provenance attestation from third actor
    revoked=rng.binomial(1,.12,size=n)
    context=rng.binomial(1,.5,size=n) # exit of third actor versus continued presence
    ab=np.array([ordered(x[0],1,x[1],4) for x in obs])
    bc=np.array([ordered(x[1],4,x[2],2) for x in obs])
    # Maintained if mediator stays OR verified transferable capacity exists.
    transferable=ab & bc & permissions[:,2].astype(bool)
    consent=permissions[:,0].astype(bool) & permissions[:,1].astype(bool) & ~revoked.astype(bool)
    eligibility=consent & ((context==0) | transferable)
    if regime=='base': p=np.where(eligibility,.94,.03)
    elif regime=='changed':
        # Mechanism change: attestation no longer guarantees transferred capacity.
        p=np.where(eligibility & (context==0),.94,np.where(eligibility & transferable,.48,.03))
    else: raise ValueError(regime)
    y=rng.binomial(1,p)
    return {'events':obs,'permissions':permissions,'revoked':revoked,'exit':context,'y':y,
            'latent_transfer':transferable.astype(int),'eligible':eligibility.astype(int)}


def observed_current(d):
    return np.column_stack([d['permissions'][:,:2],d['revoked'],d['exit']])


def raw_features(d):
    n=len(d['y'])
    return np.column_stack([d['events'].reshape(n,-1), d['permissions'],d['revoked'],d['exit']])


def pair_bank(d):
    obs=d['events']; n=len(obs)
    ab=np.zeros((n,36),dtype=int);bc=np.zeros_like(ab)
    for i in range(n):
        for a in range(6):
            for b in range(6):
                ab[i,a*6+b]=ordered(obs[i,0],a,obs[i,1],b)
                bc[i,a*6+b]=ordered(obs[i,1],a,obs[i,2],b)
    return ab,bc


def select_pairs(d):
    # The training data alone determines the pairwise features.
    # Examine cases where the mediator has exited and permissions allow joining.
    mask=(d['exit']==1) & (d['permissions'][:,0]==1) & (d['permissions'][:,1]==1) & (d['revoked']==0)
    ab,bc=pair_bank(d)
    y=d['y'][mask]
    def score(features):
        scores=[]
        for j in range(features.shape[1]):
            f=features[mask,j].astype(bool)
            if min(f.sum(),(~f).sum())<30: scores.append(-1)
            else: scores.append(abs(y[f].mean()-y[~f].mean()))
        return np.asarray(scores)
    ia=int(score(ab).argmax());ib=int(score(bc).argmax())
    return ia,ib


def relation_features(d, selected):
    ab,bc=pair_bank(d); ia,ib=selected
    transfer=(ab[:,ia] & bc[:,ib] & d['permissions'][:,2]).astype(int)
    return np.column_stack([observed_current(d),d['permissions'][:,2],ab[:,ia],bc[:,ib],transfer,
                            transfer*d['exit']])


def onehot_raw(train,test):
    enc=OneHotEncoder(handle_unknown='ignore',sparse_output=False)
    return enc.fit_transform(raw_features(train)),enc.transform(raw_features(test))


def evaluate(y,p):
    p=np.clip(p,1e-6,1-1e-6)
    return {'brier':float(brier_score_loss(y,p)), 'logloss':float(log_loss(y,p,labels=[0,1])),
            'accuracy':float(np.mean((p>=.5)==y))}


def fit_eval(train, test, selected):
    y=train['y']; res={}; predictions={}
    def add(name, tr, te, estimator):
        estimator.fit(tr,y)
        p=estimator.predict_proba(te)[:,1]
        res[name]=evaluate(test['y'],p)
        predictions[name]=p
    add('current_only',observed_current(train),observed_current(test),LogisticRegression(max_iter=500))
    tr,te=onehot_raw(train,test)
    add('all_raw_events_logistic',tr,te,LogisticRegression(max_iter=500))
    add('all_raw_events_random_forest',tr,te,RandomForestClassifier(n_estimators=160,min_samples_leaf=6,max_features=.65,random_state=23,n_jobs=-1))
    tr,te=relation_features(train,selected),relation_features(test,selected)
    add('learned_relation_features',tr,te,LogisticRegression(max_iter=500))
    # Fair comparator receives exactly the same engineered features; no IDOS advantage implied.
    add('standard_full_information_relation_baseline',tr,te,RandomForestClassifier(n_estimators=160,min_samples_leaf=6,random_state=23,n_jobs=-1))
    return res,predictions


def main():
    train=generate(4200,111);valid=generate(1400,222);test=generate(1500,333)
    shift=generate(1500,444,'changed')
    selected=select_pairs(train)
    # Do not tune after inspecting test. Validation is reserved for diagnostics only.
    metrics,p=fit_eval(train,test,selected)
    shifted,_=fit_eval(train,shift,selected)
    # An explicit rule audit: using a calibrated predictor alone cannot guarantee respect for permission.
    permissions_ok=(test['permissions'][:,0]==1)&(test['permissions'][:,1]==1)&(test['revoked']==0)
    violations={name:int(((q>=.5)&(~permissions_ok)).sum()) for name,q in p.items()}
    report={'version':'1.3','seed':[111,222,333,444],
            'sizes':{'train':len(train['y']),'validation':len(valid['y']),'test':len(test['y']),'shift_test':len(shift['y'])},
            'selected_pairs':{'A_to_B':[selected[0]//6,selected[0]%6], 'B_to_C':[selected[1]//6,selected[1]%6]},
            'normal':metrics,'changed_mechanism':shifted,'naive_action_permission_violations':violations,
            'true_private_generator_pairs':{'A_to_B':[1,4],'B_to_C':[4,2]},
            'caveat':'synthetic; pair features may be discovered but are supplied as candidate grammar; no novel causal identification; full-information model has all input signals'}
    return report


if __name__=='__main__':
    print(json.dumps(main(),indent=2,ensure_ascii=False))
