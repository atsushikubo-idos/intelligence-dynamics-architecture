"""Synthetic sequence-only audit of predictive history (v1.1).

Observations are anonymous event-token sequences. The learner is not given
semantic flags (transfer, consent, provenance) or the generator's latent state.
The generator itself has a planted event-order mechanism, so successful
prediction does NOT demonstrate autonomous discovery from natural dialogue.
No external requirements; deterministic seed; no leakage across episodes.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product
import math, random, json

ALPHABET = 'abcdef'
# PRIVATE GENERATOR MECHANISM; never passed to prediction functions.
_HIDDEN_FIRST, _HIDDEN_SECOND = 'b', 'e'

@dataclass(frozen=True)
class Episode:
    idx: int
    tokens: tuple[str, ...]
    retained: int
    regime: int


def event_motif(tokens, a, b):
    """Ordered, not necessarily adjacent, distinct events."""
    seen = False
    for t in tokens:
        if t == b and seen:
            return 1
        if t == a:
            seen = True
    return 0


def make_episodes(n=6000, seed=101, regime=0):
    rng = random.Random(seed)
    episodes=[]
    for i in range(n):
        # Token counts deliberately varied; identity of planted mechanism hidden
        # among similar-frequency distractors. Force nontrivial pairs with random order.
        seq = [rng.choice(ALPHABET) for _ in range(rng.randint(5,10))]
        if rng.random()<0.65:
            positions=rng.sample(range(len(seq)), 2)
            seq[positions[0]]=_HIDDEN_FIRST
            seq[positions[1]]=_HIDDEN_SECOND
        motif=event_motif(seq,_HIDDEN_FIRST,_HIDDEN_SECOND)
        # Regime 0: motif predicts success; regime 1: same motif becomes unreliable.
        success_prob=(0.90 if motif else 0.10) if regime==0 else (0.52 if motif else 0.10)
        outcome=int(rng.random()<success_prob)
        episodes.append(Episode(i,tuple(seq),outcome,regime))
    return episodes


def split(data, train_fraction=.60, valid_fraction=.20):
    n=len(data);a=int(n*train_fraction);b=int(n*(train_fraction+valid_fraction))
    return data[:a],data[a:b],data[b:]


class BetaRate:
    """Binomial model with prior centered on training positive rate."""
    def __init__(self, feature, concentration=6):
        self.feature=feature;self.concentration=concentration
    def fit(self, episodes):
        self.base=sum(e.retained for e in episodes)/len(episodes)
        self.counts=defaultdict(lambda:[0,0])
        for e in episodes:
            k=self.feature(e.tokens)
            self.counts[k][0]+=e.retained
            self.counts[k][1]+=1
        return self
    def predict(self, tokens):
        positive,total=self.counts[self.feature(tokens)]
        return (positive+self.concentration*self.base)/(total+self.concentration)


def brier(model, episodes):
    return sum((model.predict(e.tokens)-e.retained)**2 for e in episodes)/len(episodes)


def log_loss(model, episodes):
    s=0
    for e in episodes:
        p=max(1e-9,min(1-1e-9,model.predict(e.tokens)))
        s-=e.retained*math.log(p)+(1-e.retained)*math.log(1-p)
    return s/len(episodes)


def bag_feature(tokens):
    return tuple(sorted(set(tokens)))


def last_feature(tokens):
    return tokens[-1]


def all_pairs_feature(tokens):
    return tuple(event_motif(tokens,a,b) for a,b in product(ALPHABET,repeat=2) if a!=b)


class LogisticPairs:
    """Standard L2-regularized logistic regression over every ordered pair.

    Independent fair baseline: sees the SAME token sequences, and learns
    predictive pair weights without receiving the planted event pair.
    """
    def __init__(self, l2=0.02, steps=350, lr=0.7):
        self.pairs=[(a,b) for a,b in product(ALPHABET,repeat=2) if a!=b]
        self.l2=l2;self.steps=steps;self.lr=lr
        self.weights=[0.0]*(len(self.pairs)+1)
    def vector(self,seq):
        return [1.0]+[event_motif(seq,a,b) for a,b in self.pairs]
    def fit(self,episodes):
        features=[self.vector(e.tokens) for e in episodes]
        targets=[e.retained for e in episodes]
        n=len(episodes); dim=len(self.weights)
        for _ in range(self.steps):
            grad=[0.0]*dim
            for row,y in zip(features,targets):
                z=sum(w*x for w,x in zip(self.weights,row))
                pred=1.0/(1.0+math.exp(-max(-30,min(30,z))))
                for j,x in enumerate(row):
                    grad[j]+=(pred-y)*x
            for j in range(dim):
                penalty=0 if j==0 else self.l2*self.weights[j]
                self.weights[j]-=self.lr*(grad[j]/n+penalty)
        return self
    def predict(self,seq):
        z=sum(w*x for w,x in zip(self.weights,self.vector(seq)))
        return 1.0/(1.0+math.exp(-max(-30,min(30,z))))


def discover(train, validation):
    """Select ordered token pair using held-out validation *only*.

    Candidate list and feature semantics are generic and predeclared. A model
    with these features cannot discover arbitrary new event abstractions.
    """
    candidates=[]
    for a,b in product(ALPHABET,repeat=2):
        if a==b:continue
        f=lambda seq,a=a,b=b: event_motif(seq,a,b)
        m=BetaRate(f).fit(train)
        candidates.append((brier(m,validation),a,b))
    loss,a,b=min(candidates)
    fitted=BetaRate(lambda seq:event_motif(seq,a,b)).fit(train+validation)
    return (a,b),float(loss),fitted,len(candidates)


def online_recalibration(model, samples, window=250, min_samples=40):
    """Predict each episode *before* revealing its outcome, then update only
    with recent outcomes. Discovering the motif and recalibrating are separate.
    """
    observations=[]; predictions=[]
    for e in samples:
        predictions.append(model.predict(e.tokens))
        observations.append(e)
        if len(observations)>=min_samples:
            model.fit(observations[-window:])
    return sum((p-e.retained)**2 for p,e in zip(predictions,samples))/len(samples),predictions


def evaluate():
    stable=make_episodes(6000, seed=20261111)
    tr,va,te=split(stable)
    selected,valid_loss,model,ncand=discover(tr,va)
    current=BetaRate(lambda seq:1).fit(tr+va)
    last=BetaRate(last_feature).fit(tr+va)
    bag=BetaRate(bag_feature).fit(tr+va)
    all_pairs=BetaRate(all_pairs_feature).fit(tr+va)
    models={'current_only':current,'last_event':last,'bag_of_tokens':bag,
            'all_ordered_pairs_sparse_histogram':all_pairs,'standard_logistic_all_pairs':LogisticPairs().fit(tr+va),'selected_ordered_pair':model}
    nominal={k:round(brier(v,te),6) for k,v in models.items()}
    shifted=make_episodes(2400,seed=20261112,regime=1)
    shifted_fixed={k:round(brier(v,shifted),6) for k,v in models.items()}
    fresh_model=BetaRate(lambda seq:event_motif(seq,*selected)).fit(tr+va)
    adaptive, preds=online_recalibration(fresh_model,shifted)
    # A strong standard method may access all unordered and ordered features;
    # no proprietary IDOS comparator or predicted advantage asserted.
    return {'version':'1.1','data':'synthetic anonymous token sequences',
      'train':len(tr),'validation':len(va),'test':len(te),
      'selected_pair':list(selected),'hidden_generator_pair_for_audit_only':[_HIDDEN_FIRST,_HIDDEN_SECOND],
      'candidates':ncand,'validation_brier':round(valid_loss,6),
      'heldout_brier':nominal,'shifted_fixed_brier':shifted_fixed,
      'shifted_online_recalibration_brier':round(adaptive,6),
      'shifted_prequential_examples':len(preds),
      'limitations':[
        'Synthetic event tokens; no real conversation, consent, or autonomy modeled.',
        'Ground-truth predictive mechanism was deliberately planted by experimenter.',
        'Learned features come from a predefined ordered-pair feature family.',
        'Online adaptation uses observed outcomes after each prior prediction.',
        'No latent physical state or causal mechanism identified; no IDOS advantage shown.'
      ]}

if __name__=='__main__':print(json.dumps(evaluate(),indent=2))
