"""Finite-state predictive sufficiency audit: established Markov-chain theory.

Synthetic Markov chain only; refined tag is an ORACLE provenance proxy, not
an observed IDOS signal, a measure of consent, or a scientific discovery.
Uses the Python standard library. No molecular or social datasets.
"""
from __future__ import annotations
import json, math

STATES = ('a1','a2','b1','b2','c1','c2')
GROUPS = {'A': ('a1','a2'), 'B': ('b1','b2'), 'Y': ('c1','c2')}
MACRO = {s: ('X' if s[0] in 'ab' else 'Y') for s in STATES}
REFINED = {s: s[0].upper() if s[0] in 'ab' else 'Y' for s in STATES}
# Rows differ at the micro level but have identical refined-block transition sums
BLOCK_TRANSITIONS = {'A': (.05,.05,.90), 'B': (.05,.85,.10), 'Y': (.25,.25,.50)}
P = {}
for k,s in enumerate(STATES):
    block = REFINED[s]
    # Within-block allocations depend on hidden microstate: an exact compression.
    frac = .3 if k%2==0 else .7
    P[s] = {dst:prob*(frac if j==0 else 1-frac)
            for group,prob in zip(('A','B','Y'),BLOCK_TRANSITIONS[block])
            for j,dst in enumerate(GROUPS[group])}

def stationary(tol=1e-14):
    mu = {s:1/len(STATES) for s in STATES}
    for _ in range(20000):
        new={s:sum(mu[src]*P[src][s] for src in STATES) for s in STATES}
        if max(abs(new[s]-mu[s]) for s in STATES)<tol:
            return new
        mu=new
    raise RuntimeError('stationary iteration did not converge')

def nstep(n):
    mat={s:dict(P[s]) for s in STATES}
    if n==0:return {s:{t:float(s==t) for t in STATES} for s in STATES}
    for _ in range(n-1):
        mat={s:{t:sum(mat[s][m]*P[m][t] for m in STATES) for t in STATES} for s in STATES}
    return mat

def prob_future_Y(n=1):
    mat=nstep(n)
    return {s:sum(mat[s][u] for u in STATES if MACRO[u]=='Y') for s in STATES}

def representation(name):
    if name=='macro':return MACRO
    if name=='refined':return REFINED
    if name=='micro':return {s:s for s in STATES}
    raise ValueError(name)

def forecast_stats(rep, target, pi):
    blocks={b:[] for b in set(rep.values())}
    for s in STATES:blocks[rep[s]].append(s)
    mass={b:sum(pi[s] for s in ss) for b,ss in blocks.items()}
    pred={b:sum(pi[s]*target[s] for s in ss)/mass[b] for b,ss in blocks.items()}
    brier=sum(pi[s]*(target[s]*(1-pred[rep[s]])**2+(1-target[s])*pred[rep[s]]**2) for s in STATES)
    def hb(p):return 0 if p<=0 or p>=1 else -p*math.log2(p)-(1-p)*math.log2(1-p)
    entropy=sum(mass[b]*hb(pred[b]) for b in blocks)
    storage=-sum(w*math.log2(w) for w in mass.values())
    spread=max(abs(target[a]-target[b]) for ss in blocks.values() for a in ss for b in ss)
    return {'states':len(blocks),'storage_entropy_bits':storage,'predictive_entropy_bits':entropy,
            'expected_brier_score':brier,'within_block_probability_spread':spread,
            'predicted_p_future_Y':pred}

def strong_lumpability(rep, tol=1e-12):
    for s in STATES:
        for t in STATES:
            if rep[s]!=rep[t]:continue
            for block in set(rep.values()):
                x=sum(P[s][u] for u in STATES if rep[u]==block)
                y=sum(P[t][u] for u in STATES if rep[u]==block)
                if abs(x-y)>tol:return False
    return True

def macro_history_brier(pi):
    """Optimal prediction of Z_{t+1}=Y using (Z_{t-1}, Z_t) vs Z_t.

    This uses exact joint distributions, not trained or tested samples.
    """
    q=prob_future_Y()
    probs={}
    for s in STATES:
        for t in STATES:
            key=(MACRO[s],MACRO[t]); mass=pi[s]*P[s][t]
            m,y=probs.get(key,(0.,0.))
            probs[key]=(m+mass,y+mass*q[t])
    score=0.
    for mass,weighted in probs.values():
        p=weighted/mass
        score+=mass*p*(1-p)
    return {'brier_macro_previous_and_current':score,
            'posterior_p_Y_by_macro_pair':{f'{a}->{b}':y/m for (a,b),(m,y) in sorted(probs.items())}}

def run():
    pi=stationary(); outcomes={}
    for n in (1,2,3):
        q=prob_future_Y(n)
        outcomes[str(n)]={name:forecast_stats(representation(name),q,pi) for name in ('macro','refined','micro')}
    h=macro_history_brier(pi)
    # Exact conditional info lost by macro relative to micro, in bits
    loss=outcomes['1']['macro']['predictive_entropy_bits']-outcomes['1']['micro']['predictive_entropy_bits']
    return {'model':'six hidden microstates; three refined blocks; two macros; fully specified stationary Markov chain',
      'synthetic':True,'not_empirical':True,'refined_tag_oracle':True,
      'transition_matrix':P,'stationary_microstate_distribution':pi,
      'strong_lumpability':{name:strong_lumpability(representation(name)) for name in ('macro','refined','micro')},
      'forecast_horizons':outcomes,'macro_history':h,
      'one_step_information_lost_by_macro_bits':loss,
      'interpretation_limits':[
        'Refined representation is constructed from the known transition matrix; it is an oracle predictive partition.',
        'Results do not establish that provenance or IDOS variables can be recovered from incomplete social observations.',
        'Full observed microstate and full observed microstate history tie under the first-order Markov assumption.',
        'No IDOS-specific advantage; conventional sufficient-state and Markov lumpability theory explains the result.',
        'No physical atomistic simulation, human data, consent dynamics, or autonomous rule revision.']}

if __name__=='__main__':print(json.dumps(run(),indent=2))
