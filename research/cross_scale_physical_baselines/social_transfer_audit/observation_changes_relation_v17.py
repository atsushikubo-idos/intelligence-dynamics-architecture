"""IDOS v1.7: a reproducible synthetic dual-control / active-observation audit.

No empirical claims about people/AI and no causal discovery from real data.
Standard-library only; synthetic known observation and intervention kernels.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import random
from typing import NamedTuple

@dataclass(frozen=True)
class Action:
    name: str
    p_positive_A: float
    p_positive_B: float
    dissolution_risk: float
    cost: float
    needs_consent: bool = False

ACTIONS = (
    Action('passive', .58, .42, .0, .0),
    Action('gentle_probe', .76, .24, .025, .01, True),
    Action('strong_probe', .93, .07, .23, .015, True),
)

class Choice(NamedTuple):
    name: str
    information_gain: float
    risk: float
    utility: float


def entropy(p: float) -> float:
    return -sum(x * math.log2(x) for x in (p, 1-p) if x > 0)


def info_gain(prior_A: float, action: Action) -> float:
    marginal = prior_A * action.p_positive_A + (1-prior_A) * action.p_positive_B
    return entropy(marginal) - prior_A * entropy(action.p_positive_A) - (1-prior_A) * entropy(action.p_positive_B)


def update(prior_A: float, action: Action, positive: bool) -> float:
    likelihood_A = action.p_positive_A if positive else 1-action.p_positive_A
    likelihood_B = action.p_positive_B if positive else 1-action.p_positive_B
    numerator = prior_A * likelihood_A
    denominator = numerator + (1-prior_A)*likelihood_B
    return numerator / denominator if denominator else prior_A


def choose(prior_A: float, policy: str, consent: bool = True) -> Choice:
    """Prior is known at decision time. Hard refusal is a feasibility constraint."""
    if policy not in ('information_only', 'risk_aware', 'passive_only'):
        raise ValueError(policy)
    permitted = [a for a in ACTIONS if consent or not a.needs_consent]
    if policy == 'passive_only':
        permitted = [ACTIONS[0]]
    def score(a: Action) -> float:
        ig = info_gain(prior_A, a)
        return ig if policy == 'information_only' else ig - 2.7*a.dissolution_risk - a.cost
    chosen = max(permitted, key=score)
    return Choice(chosen.name, info_gain(prior_A, chosen), chosen.dissolution_risk, score(chosen))


def simulate_episode(true_A: bool, policy: str, rng: random.Random, consent: bool=True, max_steps: int=3) -> dict:
    belief = .5
    alive = True
    trace = []
    for step in range(max_steps):
        if not alive or max(belief,1-belief) >= .95:
            break
        c = choose(belief, policy, consent)
        a = next(a for a in ACTIONS if a.name == c.name)
        positive = rng.random() < (a.p_positive_A if true_A else a.p_positive_B)
        # Observation takes place; relationship status then transitions under intervention.
        new_belief = update(belief, a, positive)
        alive = rng.random() >= a.dissolution_risk
        trace.append({'step':step+1,'action':a.name,'prior_A':round(belief,6),
                      'positive':positive,'posterior_A':round(new_belief,6),
                      'survives':alive,'consent':consent})
        belief = new_belief
    return {'truth_A':true_A, 'posterior_A':belief, 'survives':alive,
            'brier':(belief-float(true_A))**2, 'steps':len(trace), 'trace':trace}


def compare(n: int=10000, seed: int=20261111) -> dict:
    # Common latent types, but policy-specific seeded outcome streams.
    truth_rng = random.Random(seed)
    truths = [truth_rng.random() < .5 for _ in range(n)]
    output = {}
    for pidx, policy in enumerate(('passive_only','information_only','risk_aware')):
        rng = random.Random(seed+100+pidx)
        episodes = [simulate_episode(t, policy, rng) for t in truths]
        output[policy] = {
            'mean_brier':round(sum(e['brier'] for e in episodes)/n,6),
            'survival_rate':round(sum(e['survives'] for e in episodes)/n,6),
            'mean_steps':round(sum(e['steps'] for e in episodes)/n,6),
            'mean_confidence':round(sum(max(e['posterior_A'],1-e['posterior_A']) for e in episodes)/n,6),
            'first_action':choose(.5,policy).name,
        }
    output['no_consent'] = {p:choose(.5,p,False).name for p in ('passive_only','information_only','risk_aware')}
    output['prior_information_gain']={a.name:round(info_gain(.5,a),6) for a in ACTIONS}
    output['design']={'n':n,'seed':seed,'horizon':3, 'risk_penalty':2.7,
                      'outcome_order':'observe, then relationship transition',
                      'risk_known_to_planner':True,'simulated':'not empirical'}
    return output

if __name__ == '__main__':
    import json
    print(json.dumps(compare(),indent=2,ensure_ascii=False))
