"""Synthetic categorical HMM prediction audit v1.2.

No IDOS-specific method is claimed. Event identities are anonymous;
latent state IDs and their number are not given to the estimator. Ground truth is
available only to the experiment harness and is not passed to model.fit.
"""
from __future__ import annotations
import json
import numpy as np
from sklearn.linear_model import LogisticRegression

ALPHABET = 6
SEQ_LEN = 12
TRUE_PI=np.array([.55,.30,.15])
TRUE_A=np.array([[.83,.14,.03],[.06,.82,.12],[.08,.10,.82]])
TRUE_B=np.array([[.48,.26,.14,.06,.04,.02],[.03,.42,.30,.18,.05,.02],[.02,.03,.07,.20,.31,.37]])
NORMAL_OUTCOME=np.array([.08,.50,.92])
SHIFT_OUTCOME=np.array([.86,.50,.14])


def synthetic(n, seed, shift=False):
    rng=np.random.default_rng(seed)
    z=np.empty((n,SEQ_LEN),dtype=int)
    x=np.empty_like(z)
    z[:,0]=rng.choice(3,size=n,p=TRUE_PI)
    for t in range(SEQ_LEN):
        for state in range(3):
            mask=z[:,t]==state
            if mask.any(): x[mask,t]=rng.choice(ALPHABET,mask.sum(),p=TRUE_B[state])
        if t+1<SEQ_LEN:
            for state in range(3):
                mask=z[:,t]==state
                if mask.any(): z[mask,t+1]=rng.choice(3,mask.sum(),p=TRUE_A[state])
    probs=(SHIFT_OUTCOME if shift else NORMAL_OUTCOME)[z[:,-1]]
    y=(rng.random(n)<probs).astype(int)
    return x,y,z


def fb(x, pi, A, B):
    # Scaled forward/backward on N x T x K arrays; no hidden state ground truth.
    n,tmax=x.shape; k=len(pi)
    alpha=np.empty((n,tmax,k)); scales=np.empty((n,tmax))
    raw=pi[None,:]*B[:,x[:,0]].T
    scales[:,0]=raw.sum(axis=1).clip(1e-300)
    alpha[:,0]=raw/scales[:,0,None]
    for t in range(1,tmax):
        raw=(alpha[:,t-1]@A)*B[:,x[:,t]].T
        scales[:,t]=raw.sum(axis=1).clip(1e-300)
        alpha[:,t]=raw/scales[:,t,None]
    beta=np.ones_like(alpha)
    xi=np.zeros((k,k))
    for t in range(tmax-2,-1,-1):
        future=B[:,x[:,t+1]].T*beta[:,t+1]
        beta[:,t]=(future@A.T)/scales[:,t+1,None]
        raw=alpha[:,t,:,None]*A[None,:,:]*future[:,None,:]
        xi+=(raw / scales[:,t+1,None,None]).sum(axis=0)
    gamma=alpha*beta
    gamma/=gamma.sum(axis=2,keepdims=True)
    loglik=np.log(scales).sum()
    return alpha,gamma,xi,loglik


class CategoricalHMM:
    def __init__(self,k,iterations=35,restarts=2,seed=11):
        self.k=k;self.iterations=iterations;self.restarts=restarts;self.seed=seed
    def fit(self,x):
        rng=np.random.default_rng(self.seed); best=None
        for r in range(self.restarts):
            pi=rng.dirichlet(np.ones(self.k)*1.5)
            A=rng.dirichlet(np.ones(self.k)*1.6,size=self.k)
            B=rng.dirichlet(np.ones(ALPHABET)*1.3,size=self.k)
            for iteration in range(self.iterations):
                _,gamma,xi,ll=fb(x,pi,A,B)
                pi=(gamma[:,0].sum(axis=0)+.3); pi/=pi.sum()
                A=xi+.4;A/=A.sum(axis=1,keepdims=True)
                counts=np.zeros((self.k,ALPHABET))
                for symbol in range(ALPHABET):
                    counts[:,symbol]=gamma[x==symbol].sum(axis=0)
                B=counts+.4;B/=B.sum(axis=1,keepdims=True)
            _,_,_,ll=fb(x,pi,A,B)
            if best is None or ll>best[0]:best=(ll,pi,A,B)
        self.train_log_likelihood=float(best[0]);_,self.pi,self.A,self.B=best
        return self
    def features(self,x):
        alpha,_,_,_=fb(x,self.pi,self.A,self.B)
        return alpha[:,-1,:]
    def log_likelihood(self,x):
        return fb(x,self.pi,self.A,self.B)[3]/len(x)


def simple_features(x,kind):
    n,t=x.shape
    if kind=='last':return np.eye(ALPHABET)[x[:,-1]]
    if kind=='bag':return np.column_stack([(x==c).sum(axis=1) for c in range(ALPHABET)])/t
    if kind=='last3':return np.eye(ALPHABET)[x[:,-3:]].reshape(n,-1)
    if kind=='counts_last3':return np.column_stack([simple_features(x,'bag'),simple_features(x,'last3')])
    raise ValueError(kind)


def logreg(F,y):
    return LogisticRegression(C=2.,max_iter=400,random_state=7).fit(F,y)

def brier(p,y):return float(np.mean((p-y)**2))
def cross_entropy(p,y):
    p=np.clip(p,1e-7,1-1e-7)
    return float(-np.mean(y*np.log(p)+(1-y)*np.log(1-p)))


def run():
    X,y,_=synthetic(1600,11021)
    train=(X[:1200],y[:1200]);valid=(X[1200:1600],y[1200:1600])
    models={}
    for key in ('last','bag','last3','counts_last3'):
        fit=logreg(simple_features(train[0],key),train[1])
        models[key]=(fit,lambda x, key=key:simple_features(x,key))
    candidates={};hmm_models={}
    # State count is tuned on VALIDATION likelihood, never on test labels.
    for k in (2,3,4):
        hmm=CategoricalHMM(k,iterations=32,restarts=2,seed=120+k).fit(train[0])
        candidates[k]=float(hmm.log_likelihood(valid[0]))
        hmm_models[k]=hmm
    selected=max(candidates,key=candidates.get)
    hmm=hmm_models[selected]
    supervised=logreg(hmm.features(train[0]),train[1])
    models['hmm_unsupervised_filter']=(supervised,hmm.features)
    # An oracle upper reference sees actual hidden state. It is NOT available to learners.
    Xt,yt,zt=synthetic(400,11022)
    # Separate independent test is used for all models; X generated above unused test partition.
    results={name:{'brier':round(brier(fit.predict_proba(feat(Xt))[:,1],yt),6),
                   'log_loss':round(cross_entropy(fit.predict_proba(feat(Xt))[:,1],yt),6)}
             for name,(fit,feat) in models.items()}
    oracle=brier(NORMAL_OUTCOME[zt[:,-1]],yt)
    # Regime shift changes OUTCOME mapping only; emission and transition process held fixed.
    Xs,ys,_=synthetic(800,11023,shift=True)
    calibrate_n=180; xcal,ycal=Xs[:calibrate_n],ys[:calibrate_n]
    xeval,yeval=Xs[calibrate_n:],ys[calibrate_n:]
    shift_fixed={};shift_retrained={}
    for name,(fit,feature) in models.items():
        shift_fixed[name]=round(brier(fit.predict_proba(feature(xeval))[:,1],yeval),6)
        # Compare adaptation under the SAME labeled calibration budget.
        # Retraining the classifier only: HMM emissions/transitions stay unchanged.
        adjusted=logreg(feature(xcal),ycal)
        shift_retrained[name]=round(brier(adjusted.predict_proba(feature(xeval))[:,1],yeval),6)
    # Permutation control: event-order model should lose signal when its tokens are shuffled.
    rng=np.random.default_rng(47)
    scrambled=Xt.copy()
    for row in scrambled:rng.shuffle(row)
    shuffle_effect={name:round(brier(fit.predict_proba(feature(scrambled))[:,1],yt),6)
                     for name,(fit,feature) in models.items()}
    return {'version':'1.2','source':'synthetic categorical hidden-state Markov generator',
      'episode_length':SEQ_LEN,'train':len(train[1]),'validation':len(valid[1]),
      'independent_test':len(yt),'shift_calibration':calibrate_n,'shift_test':len(yeval),
      'state_count_selection_validation_log_likelihood':{str(k):round(v,6) for k,v in candidates.items()},
      'selected_states':selected,'unseen_test':results,
      'unavailable_oracle_hidden_state_brier':round(oracle,6),
      'shift_fixed_brier':shift_fixed,'shift_after_equal_label_budget_brier':shift_retrained,
      'shuffled_token_order_test_brier':shuffle_effect,
      'limitations':['Ground truth is synthetic and is exactly of HMM type.',
        'HMM latent states are statistical clusters, not semantic provenance or actor intent.',
        'No real interactions, autonomy, consent, or refusal are observed.',
        'The generator has a fixed known state family; K is selected from 2, 3, 4 only.',
        'Adaptation uses 180 observed labeled outcomes, and only the outcome classifier is refit.',
        'This evaluates established baselines; it does not demonstrate an IDOS-specific gain.']}

if __name__=='__main__':print(json.dumps(run(),indent=2,ensure_ascii=False))
