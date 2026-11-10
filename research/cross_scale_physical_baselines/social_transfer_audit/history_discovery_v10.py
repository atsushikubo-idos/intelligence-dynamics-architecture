"""Data-driven history-selection audit for IDOS v1.0 (synthetic, standard library).

Labels are produced by the fixed v0.9 transition rule, but learner sees only
pre-outcome event observations. Training and evaluation episodes are disjoint.
Nothing here establishes empirical human/AI connection laws.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from collections import defaultdict
import json, random, math

FEATURES = ('connection_now','verified_transfer_event','mediator_used_event',
            'direct_protocol_event','prior_disruption_event','noisy_marker',
            'unrelated_random_event')
HISTORY = FEATURES[1:]

@dataclass(frozen=True)
class Episode:
    episode_id: int
    group: int
    features: tuple[int,...]
    retained_after_departure: int


def make_episodes(n=2400, seed=20261111, transfer_reliability=1.0):
    """Artificial episodes from v0.9 semantics: verified transfer retains a route.

    Samples only previously connected episodes. Consent continues; no direct
    protocol or mediation at departure. Labels depend on retained certification.
    Independent markers are decoys. transfer_reliability below 1 adds post-event
    failure in a *separate*, explicitly shifted environment.
    """
    rng=random.Random(seed)
    result=[]
    for eid in range(n):
        group=eid//12
        # Generate history before departure. All episodes are initially connected:
        # either a direct protocol or valid mediation.
        direct=int(rng.random()<0.48)
        mediated=int((not direct) or (rng.random()<0.55))
        verified=int(mediated and rng.random()<0.87)
        if not direct and not verified:
            verified=1 # required for a connected episode
        authorized=int(rng.random()<0.38)
        transfer=int(mediated and verified and authorized)
        disruption=int(rng.random()<0.31)
        noisy=int((transfer if rng.random()<0.78 else 1-transfer))
        unrelated=int(rng.random()<0.5)
        feats=(1,transfer,int(mediated),direct,disruption,noisy,unrelated)
        # Post-departure continuing consent, no direct route; only certified bridge.
        y=int(transfer and rng.random()<transfer_reliability)
        result.append(Episode(eid,group,feats,y))
    return result


def split_by_group(data, fraction=0.7, seed=27):
    groups=sorted(set(e.group for e in data))
    rng=random.Random(seed);rng.shuffle(groups)
    train_groups=set(groups[:int(len(groups)*fraction)])
    train=[e for e in data if e.group in train_groups]
    test=[e for e in data if e.group not in train_groups]
    assert set(x.episode_id for x in train).isdisjoint(x.episode_id for x in test)
    return train,test


class HistogramPredictor:
    def __init__(self, chosen, alpha=2.0):
        self.chosen=tuple(chosen);self.alpha=alpha
        self.groups={};self.global_rate=0.5
    def fit(self, episodes):
        agg=defaultdict(lambda:[0,0])
        self.global_rate=sum(e.retained_after_departure for e in episodes)/len(episodes)
        for e in episodes:
            key=tuple(e.features[i] for i in self.chosen)
            agg[key][0]+=e.retained_after_departure
            agg[key][1]+=1
        self.groups=dict(agg)
        return self
    def predict(self,e):
        success,n=self.groups.get(tuple(e.features[i] for i in self.chosen),(0,0))
        return (success+self.alpha*self.global_rate)/(n+self.alpha)


def score(model, episodes):
    return sum((model.predict(e)-e.retained_after_departure)**2 for e in episodes)/len(episodes)


def select_history(train, max_features=3, complexity_penalty=0.0006):
    """Discover subset from validation performance only; no oracle feature given.

    Deterministically hold out entire groups inside training. Select subset
    minimizing group-heldout Brier + a fixed feature-count penalty.
    """
    subtrain,valid=split_by_group(train,0.75,seed=913)
    candidates=[]
    for k in range(max_features+1):
        for extras in combinations(range(1,len(FEATURES)),k):
            cols=(0,)+extras
            s=score(HistogramPredictor(cols).fit(subtrain),valid)
            candidates.append((s+complexity_penalty*k, k, extras, s))
    best=min(candidates)
    cols=(0,)+best[2]
    return {'selected_indices':cols,'selected_names':[FEATURES[i] for i in cols],
            'validation_brier':best[3], 'objective':best[0],
            'candidate_count':len(candidates)}


def best_decision_stump(train):
    """Independent standard decision-stump baseline with all features available."""
    best=None
    for j in range(len(FEATURES)):
        model=HistogramPredictor((j,)).fit(train)
        loss=score(model,train)
        if best is None or (loss,j)<(best[0],best[1]):
            best=(loss,j,model)
    return best[1],best[2]


def evaluate(n=2400):
    data=make_episodes(n)
    train,test=split_by_group(data)
    discovery=select_history(train)
    chosen=tuple(discovery['selected_indices'])
    models={'current_only':(0,), 'learned_history':chosen,
            'full_observed_history':tuple(range(len(FEATURES))),
            'single_noisy_marker':(0,5),
            'oracle_transfer_history':(0,1)}
    fitted={name:HistogramPredictor(cols).fit(train) for name,cols in models.items()}
    stump_feature,stump=best_decision_stump(train)
    base={name:round(score(m,test),7) for name,m in fitted.items()}
    base['standard_decision_stump']=round(score(stump,test),7)
    # Pre-registered audit: rebalance the genuine transfer frequency among new
    # episodes, without changing its causal meaning. Still synthetic.
    rare=make_episodes(1200,seed=2222,transfer_reliability=1.0)
    shifted=make_episodes(1200,seed=3333,transfer_reliability=0.55)
    return {
      'version':'1.0', 'scope':'synthetic history discovery, no empirical social claim',
      'train_episodes':len(train),'heldout_episodes':len(test),
      'discovery':discovery,
      'test_brier':base,
      'standard_stump_selected_feature':FEATURES[stump_feature],
      'shifted_reliability_brier':dict({name:round(score(m,shifted),7) for name,m in fitted.items()},
                                       standard_decision_stump=round(score(stump,shifted),7)),
      'train_positive_rate':round(sum(x.retained_after_departure for x in train)/len(train),5),
      'heldout_positive_rate':round(sum(x.retained_after_departure for x in test)/len(test),5),
      'cautions':[
        'Transfer history is an explicit event supplied by the synthetic simulator, not inferred from raw conversation.',
        'Data generation and outcome mechanism were engineered; predictions are not real-world forecasts.',
        'Full-observed-history baseline has same input access but histogram sparsity can reduce performance.',
        'The shifted condition changes an outcome rule; a previously good predictor need not remain calibrated.',
        'Discovery is a model-selection procedure, not discovery of a novel physical or social law.'
      ]}

if __name__=='__main__':
    print(json.dumps(evaluate(),indent=2))
