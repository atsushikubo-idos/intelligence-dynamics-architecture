"""IDOS cross-scale v1.5: observational equivalence and active probe audit.

Synthetic Bernoulli data. No implication of causal identification without
specified randomized diagnostic intervention and structural assumptions.
Standard-library only; deterministic seed; synthetic results.
"""
from __future__ import annotations
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path

PRE = .80
POST_PASSIVE = .45
PROBE_A = .80
PROBE_B = .15
CHANGE_AT = 200
N = 400
PROBE_START = 240
PROBE_SPACING = 3
LLR_THRESHOLD = math.log(19.0)  # 95% posterior with equal priors
CUSUM_THRESHOLD = 8.0
ROLLING_WINDOW = 25
ROLLING_THRESHOLD = .48

@dataclass
class Trial:
    cause: str
    passive: list[int]
    probes: list[tuple[int, int]]


def bernoulli(rng: random.Random, p: float) -> int:
    return int(rng.random() < p)


def sample_trial(cause: str, seed: int, active: bool = True) -> Trial:
    """Randomized probe schedule is fixed in advance and not outcome-selected."""
    if cause not in ('none', 'A', 'B'):
        raise ValueError(cause)
    rng = random.Random(seed)
    passive = [bernoulli(rng, PRE if cause == 'none' or t < CHANGE_AT else POST_PASSIVE) for t in range(N)]
    probes = []
    if active:
        p = {'none': PRE, 'A': PROBE_A, 'B': PROBE_B}[cause]
        probes = [(t, bernoulli(rng, p)) for t in range(PROBE_START, N, PROBE_SPACING)]
    return Trial(cause, passive, probes)


def observational_likelihood(seq: list[int], cause: str) -> float:
    """Log likelihood conditional on a known change time (known toy model)."""
    if cause not in ('A', 'B'):
        raise ValueError(cause)
    return sum(y*math.log(PRE if t < CHANGE_AT else POST_PASSIVE) +
               (1-y)*math.log(1-(PRE if t < CHANGE_AT else POST_PASSIVE))
               for t,y in enumerate(seq))


def passive_cusum(seq: list[int]) -> int | None:
    """Oracle likelihood-ratio CUSUM with known pre/post Bernoulli rates."""
    g = 0.
    for t,y in enumerate(seq):
        inc = y*math.log(POST_PASSIVE/PRE) + (1-y)*math.log((1-POST_PASSIVE)/(1-PRE))
        g = max(0., g+inc)
        if g >= CUSUM_THRESHOLD:
            return t
    return None


def rolling_drop(seq: list[int]) -> int | None:
    """Basic nonparametric baseline: rolling empirical success-rate drop."""
    for t in range(ROLLING_WINDOW-1,len(seq)):
        window=seq[t-ROLLING_WINDOW+1:t+1]
        if sum(window)/ROLLING_WINDOW < ROLLING_THRESHOLD:
            return t
    return None


def active_attribution(probes: list[tuple[int,int]]) -> tuple[str, int | None, float, int]:
    """Sequential Bayes factor, stops once >=95% posterior. Else abstains."""
    llr=0.
    for j,(t,y) in enumerate(probes,1):
        llr += y*math.log(PROBE_A/PROBE_B) + (1-y)*math.log((1-PROBE_A)/(1-PROBE_B))
        if abs(llr)>=LLR_THRESHOLD:
            posterior = 1/(1+math.exp(-abs(llr)))
            return ('A' if llr>0 else 'B',t,posterior,j)
    return ('undetermined',None,1/(1+math.exp(-abs(llr))),len(probes))


def passive_attribution(passive: list[int]) -> str:
    """A vs B have exactly the same passive probability law: abstain."""
    return 'undetermined'


def evaluate(reps: int=200, seed: int=20261111) -> dict:
    rng=random.Random(seed)
    rows={cause: {'cusum':[],'rolling':[],'active':[],'decision_time':[],'probes_to_decision':[]} for cause in ['none','A','B']}
    for cause in rows:
        for _ in range(reps):
            trial=sample_trial(cause, rng.randrange(2**32))
            c=passive_cusum(trial.passive)
            r=rolling_drop(trial.passive)
            label,at,post,num=active_attribution(trial.probes)
            rows[cause]['cusum'].append(c)
            rows[cause]['rolling'].append(r)
            rows[cause]['active'].append(label)
            rows[cause]['decision_time'].append(at)
            rows[cause]['probes_to_decision'].append(num)
    out={}
    for cause,row in rows.items():
        detected=[x for x in row['cusum'] if x is not None and x>=CHANGE_AT]
        roll=[x for x in row['rolling'] if x is not None and x>=CHANGE_AT]
        correct=sum(x==cause for x in row['active'])
        wrong=sum(x not in (cause,'undetermined') for x in row['active'])
        out[cause]={
            'n':reps,
            'cusum_any_alarm_rate':sum(v is not None for v in row['cusum'])/reps,
            'cusum_prechange_false_alarm_rate':sum(v is not None and v<CHANGE_AT for v in row['cusum'])/reps,
            'cusum_postchange_detection_rate':len(detected)/reps,
            'cusum_mean_postchange_delay':(sum(v-CHANGE_AT for v in detected)/len(detected) if detected else None),
            'rolling_any_alarm_rate':sum(v is not None for v in row['rolling'])/reps,
            'rolling_prechange_false_alarm_rate':sum(v is not None and v<CHANGE_AT for v in row['rolling'])/reps,
            'rolling_postchange_detection_rate':len(roll)/reps,
            'rolling_mean_postchange_delay':(sum(v-CHANGE_AT for v in roll)/len(roll) if roll else None),
            'active_correct_fraction':correct/reps if cause !='none' else None,
            'active_wrong_fraction':wrong/reps if cause !='none' else None,
            'active_abstention_fraction':sum(x=='undetermined' for x in row['active'])/reps,
            'active_avg_probes_until_stop':sum(row['probes_to_decision'])/reps,
        }
    return {'config': {'N':N,'change_at':CHANGE_AT,'probe_start':PROBE_START,
            'probe_spacing':PROBE_SPACING,'pre_passive_p':PRE,
            'post_passive_p_A_and_B':POST_PASSIVE,'probe_p_A':PROBE_A,'probe_p_B':PROBE_B,
            'cusum_threshold':CUSUM_THRESHOLD,'rolling_window':ROLLING_WINDOW,
            'rolling_threshold':ROLLING_THRESHOLD,'posterior_threshold':.95,
            'replicates_per_condition':reps,'seed':seed},'results':out,
            'limitations':['A/B are structurally identical under passive observation by construction.',
            'Diagnostic probe is a specified randomized experimental operation, not natural social consent.',
            'CUSUM knows the pre/post rates (oracle baseline); rolling threshold is heuristic.',
            'Sequential nominal 95% posterior is not a guaranteed frequentist error rate.',
            'Probe operation is available only under assumed permissions; real-world causality is not established.']}


if __name__=='__main__':
    output=evaluate()
    print(json.dumps(output,indent=2,ensure_ascii=False))


def decision_policy(trial: Trial, probe_permitted: bool = True) -> dict:
    """Conservative workflow: detect change, verify permission, then probe.

    Note: attribution assumes either A or B after a true change. Probe data
    are only interpreted after an alarm and permission; causal claims need
    stronger real-world assumptions.
    """
    alarm=passive_cusum(trial.passive)
    if alarm is None:
        return {'change':'no_alarm','cause':'undetermined','reason':'No detected shift'}
    if not probe_permitted:
        return {'change':'alarm','cause':'undetermined','reason':'Probe not permitted'}
    observations=[pair for pair in trial.probes if pair[0]>=alarm]
    if not observations:
        return {'change':'alarm','cause':'undetermined','reason':'No diagnostic observations'}
    label,t,p,n=active_attribution(observations)
    return {'change':'alarm','cause':label,'reason':'Probe evidence' if label!='undetermined' else 'Insufficient probe evidence',
            'decision_time':t,'confidence_given_A_or_B':p,'probes_used':n}
