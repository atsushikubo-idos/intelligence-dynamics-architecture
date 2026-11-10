"""Auditable predictive-state discovery from OBSERVATIONS, not latent states.

Synthetic six-state Markov chain replicates v0.2's block transitions (self contained).
The provenance-like signal is simulated noisy observable metadata, NOT actual IDOS provenance.
All fitted predictions are learned only from observations and training outcomes.
Standard library only. No claim of IDOS advantage or physical atomistic dynamics.
"""
from __future__ import annotations
from collections import defaultdict, Counter
from itertools import product
import json, math, random

BLOCKS=('A','B','Y')
TRANS={'A':(.05,.05,.90),'B':(.05,.85,.10),'Y':(.25,.25,.50)}

def simulate(n, seed=10, tag_accuracy=.80, flip=False):
    rng=random.Random(seed); block='A'; observations=[]; latent=[]
    for _ in range(n):
        macro='Y' if block=='Y' else 'X'
        if block=='Y': tag='N'
        else:
            canonical='a' if block=='A' else 'b'
            tag=canonical if rng.random()<tag_accuracy else ('b' if canonical=='a' else 'a')
            if flip:tag='b' if tag=='a' else 'a'
        observations.append((macro,tag)); latent.append(block)
        block=rng.choices(BLOCKS,weights=TRANS[block],k=1)[0]
    return observations,latent

def samples(obs, include_tag=True, use_history=True):
    """Predict next macro using information observable at time t and earlier."""
    output=[]
    for t in range(1,len(obs)-1):
        macro,tag=obs[t]; past_macro,past_tag=obs[t-1]
        key=(macro,)
        if include_tag:key+=(tag,)
        if use_history:key+=(past_macro,)
        if include_tag and use_history:key+=(past_tag,)
        output.append((key,int(obs[t+1][0]=='Y')))
    return output

def fit_counts(rows):
    counts=defaultdict(lambda:[0,0])
    for key,y in rows:counts[key][y]+=1
    return dict(counts)

def prob(count,alpha=1.0):return (count[1]+alpha)/(sum(count)+2*alpha)

def predict_model(counts, key, fallback):return prob(counts.get(key, fallback))

def evaluate(rows, predictor):
    score=sum((predictor(key)-y)**2 for key,y in rows)/len(rows)
    logloss=-sum(y*math.log(max(1e-12,predictor(key)))+(1-y)*math.log(max(1e-12,1-predictor(key))) for key,y in rows)/len(rows)
    return {'n':len(rows),'brier':round(score,7),'log_loss_nats':round(logloss,7)}

def count_model(train, valid, test):
    counts=fit_counts(train); total=[sum(c[0] for c in counts.values()),sum(c[1] for c in counts.values())]
    pr=lambda key:predict_model(counts,key,total)
    return {'train_contexts':len(counts),'validation':evaluate(valid,pr),'test':evaluate(test,pr)},pr

def cluster_counts(counts, radius):
    """Predictive response merging: one-step Bernoulli forecasts from observations.
    Greedy deterministic clusters; model selection is by an independent validation slice.
    This is a simple established clustering baseline, not epsilon-machine inference.
    """
    groups=[]
    for key, count in sorted(counts.items(),key=lambda kv:(prob(kv[1]),kv[0])):
        value=prob(count)
        if groups and abs(value-groups[-1]['center'])<=radius:
            groups[-1]['keys'].append(key);groups[-1]['counts'][0]+=count[0];groups[-1]['counts'][1]+=count[1]
            groups[-1]['center']=prob(groups[-1]['counts'])
        else:groups.append({'keys':[key],'counts':count.copy(),'center':value})
    lookup={key:group_idx for group_idx,g in enumerate(groups) for key in g['keys']}
    return groups,lookup

def train_predictive_clusters(train, valid, test):
    counts=fit_counts(train)
    total=[sum(c[0] for c in counts.values()),sum(c[1] for c in counts.values())]
    choices=[]
    for radius in (0,.015,.03,.06,.1,.2,.4,1.0):
        groups,lookup=cluster_counts(counts,radius)
        def pr(key):return prob(groups[lookup[key]]['counts']) if key in lookup else prob(total)
        metric=evaluate(valid,pr)
        choices.append((metric['brier'],len(groups),radius,groups,lookup))
    # tie: prefer simpler partition
    score,k,radius,groups,lookup=min(choices,key=lambda q:(q[0],q[1]))
    def predict(key):return prob(groups[lookup[key]]['counts']) if key in lookup else prob(total)
    frequencies=Counter(key for key,_ in train)
    group_mass=Counter({i:sum(frequencies[k] for k in g['keys']) for i,g in enumerate(groups)})
    N=sum(group_mass.values())
    entropy=-sum((v/N)*math.log2(v/N) for v in group_mass.values())
    return {'selected_radius':radius,'discovered_predictive_classes':k,
            'full_observed_contexts':len(counts), 'observed_class_entropy_bits':round(entropy,5),
            'validation':evaluate(valid,predict),'test':evaluate(test,predict),
            'candidate_validation':[{ 'radius':r,'classes':k,'brier':round(s,7)} for s,k,r,_,_ in choices]},predict

def online_test(rows, initial_rows, window=600):
    """Prequential expanding test: predict BEFORE each test outcome is added.
    Adaptation uses observable rows including targets from previous test times.
    """
    recent=list(initial_rows[-window:]); preds=[]
    for key,y in rows:
        c=fit_counts(recent); total=[sum(x[0] for x in c.values()),sum(x[1] for x in c.values())]
        p=predict_model(c,key,total)
        preds.append((p,y));recent.append((key,y));recent=recent[-window:]
    return {'n':len(preds),'brier':round(sum((p-y)**2 for p,y in preds)/len(preds),7),
            'log_loss_nats':round(-sum(y*math.log(max(p,1e-12))+(1-y)*math.log(max(1-p,1e-12)) for p,y in preds)/len(preds),7),
            'window':window}

def run(seed=2026, ntrain=16000, nvalid=5000, ntest=7000):
    obs_train,latent_train=simulate(ntrain,seed)
    obs_valid,_=simulate(nvalid,seed+1)
    obs_test,_=simulate(ntest,seed+2)
    # Out-of-distribution shift: instrument calibration meaning of a/b reversed.
    obs_shift,_=simulate(ntest,seed+3,flip=True)
    result={'study':'observational predictive state discovery under train/test split',
            'synthetic':True,'oracle_partition_used_for_training':False,
            'generator_known_to_experimenter':True,
            'train_test_split':'independent random-seed trajectories (not random adjacent rows)',
            'shift':'observation tag a/b inverted; latent dynamics unchanged',
            'models':{}}
    designs=[('macro_current',False,False),('macro_history',False,True),('macro_tag_current',True,False),('macro_tag_history',True,True)]
    for name,tags,hist in designs:
        train=samples(obs_train,tags,hist);valid=samples(obs_valid,tags,hist)
        test=samples(obs_test,tags,hist);shift=samples(obs_shift,tags,hist)
        model,pr=count_model(train,valid,test)
        model['shift_test']=evaluate(shift,pr)
        result['models'][name]=model
    train=samples(obs_train);valid=samples(obs_valid);test=samples(obs_test);shift=samples(obs_shift)
    learned,pr=train_predictive_clusters(train,valid,test)
    learned['shift_test']=evaluate(shift,pr)
    result['models']['learned_predictive_groups']=learned
    result['models']['adaptive_full_observed_context']={
        'shift_test_prequential':online_test(shift,train,window=600),
        'in_distribution_prequential':online_test(test,train,window=600)}
    # oracle has hidden ground truth: upper-bound reference only, never a fair baseline.
    block_y={'A':.90,'B':.10,'Y':.50}
    result['oracle_hidden_state_reference']={'one_step_brier':round(sum((block_y[b]-int(obs_train[t+1][0]=='Y'))**2 for t,b in enumerate(latent_train[:-1]))/(len(latent_train)-1),7),
        'warning':'uses hidden state and known rates, not directly comparable to observational learners'}
    result['limitations']=['Observed provenance-like tag is synthetically generated with pre-specified informativeness.',
       'Discovered groups are grouped forecast frequencies, not new explanatory/causal reference frames.',
       'Only one-step binary event forecasting; no CFV/MU, refusal or consent evaluation.',
       'Shift changes sensor semantics rather than social institutions or physical chemistry.',
       'Adaptive full-context model is a standard prequential baseline; no IDOS algorithm has been implemented.',
       'No claim of physical, molecular or societal validation.']
    return result

if __name__=='__main__':print(json.dumps(run(),indent=2))
