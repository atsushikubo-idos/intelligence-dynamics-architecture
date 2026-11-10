"""Synthetic, rule-explicit IDOS/physics cross-domain *comparison*, NOT a physical law.

No quantum mechanics, claims of authentic consent, real agent understanding, or
empirical social validity. All rules and inputs are explicit; standard-library only.
"""
from __future__ import annotations
from dataclasses import dataclass, replace, asdict
from collections import defaultdict
from itertools import product
import json
import math

@dataclass(frozen=True)
class State:
    connected: bool = False
    certified_bridge: bool = False
    evidence_id: str = ""
    tick: int = 0

@dataclass(frozen=True)
class Context:
    a_consents: bool
    b_consents: bool
    mediator_present: bool
    mediation_verified: bool
    shared_direct_protocol: bool
    transfer_authorized: bool
    external_disruption: bool = False
    consent_evidence: str = "scenario-declaration"

@dataclass(frozen=True)
class Outcome:
    state: State
    feasible: bool
    formed: bool
    maintained: bool
    reopened_possible: bool
    reason: str


def step(state: State, ctx: Context) -> Outcome:
    """Transition rules: refusal has priority; no implied agreement or verification.

    Certification is reusable only if it was explicitly authorized AND verified
    during an earlier mediation step; it survives departure but not withdrawal.
    External disruption ends current connection; it does not revoke certification.
    """
    if not ctx.consent_evidence:
        raise ValueError('Provenance of declared consent required')
    if not (ctx.a_consents and ctx.b_consents):
        nxt = State(False, False, '', state.tick + 1)
        return Outcome(nxt, False, False, False, False, 'veto-or-withdrawal')
    verified_mediation = ctx.mediator_present and ctx.mediation_verified
    bridge = state.certified_bridge or (
        verified_mediation and ctx.transfer_authorized)
    feasible = ctx.shared_direct_protocol or verified_mediation or state.certified_bridge
    formed = feasible and not state.connected and not ctx.external_disruption
    maintained = feasible and state.connected and not ctx.external_disruption
    connected = feasible and not ctx.external_disruption
    evidence = (state.evidence_id if state.certified_bridge else
                f'verified-transfer:{state.tick + 1}' if verified_mediation and ctx.transfer_authorized else '')
    nxt = State(connected, bridge, evidence, state.tick + 1)
    if ctx.external_disruption:
        reason = 'disruption'
    elif not feasible:
        reason = 'no-compatible-path'
    elif verified_mediation and not ctx.shared_direct_protocol and not state.certified_bridge:
        reason = 'mediated-connection'
    elif state.certified_bridge and not ctx.mediator_present:
        reason = 'certified-transfer'
    else:
        reason = 'direct-or-retained'
    return Outcome(nxt, feasible, formed, maintained,
                   bridge or ctx.shared_direct_protocol or verified_mediation, reason)


def scenarios():
    """Exhaustive 64 consent/mediation/direct/transfer contexts, plus disruptions."""
    for a,b,m,v,d,t in product((False,True), repeat=6):
        yield Context(a,b,m,v,d,t)


def conditional_entropy(pairs, key_fn):
    groups=defaultdict(list)
    for x,y in pairs:
        groups[key_fn(x)].append(y)
    total=len(pairs)
    value=0.0
    for ys in groups.values():
        p=sum(ys)/len(ys)
        if 0 < p < 1:
            value += len(ys)/total * (-p*math.log2(p)-(1-p)*math.log2(1-p))
    return value


def brier_optimal(pairs, key_fn):
    groups=defaultdict(list)
    for x,y in pairs:
        groups[key_fn(x)].append(y)
    return sum(len(ys)/len(pairs)*(sum(ys)/len(ys))*(1-sum(ys)/len(ys)) for ys in groups.values())


def audit():
    base=State()
    stage1=[]
    for ctx in scenarios():
        out=step(base,ctx)
        stage1.append((ctx,out))
    # Counterfactual mediator leaves. No fresh mediation and no direct protocol;
    # both actors keep consent. Any persistent transfer must come from previous step.
    departure=Context(True,True,False,False,False,False)
    pairs=[]
    for first_ctx,first in stage1:
        if first.state.connected:
            future=step(first.state,departure)
            pairs.append(((first.state.connected, first.state.certified_bridge,
                           bool(first.state.evidence_id)), int(future.state.connected)))
    # Exact frequencies over a *uniform artificial design*, not real-world probabilities.
    coarse_entropy=conditional_entropy(pairs,lambda x:x[0])
    provenance_entropy=conditional_entropy(pairs,lambda x:x)
    coarse_brier=brier_optimal(pairs,lambda x:x[0])
    provenance_brier=brier_optimal(pairs,lambda x:x)
    prototypes={
        'no_mediator': Context(True,True,False,False,False,False),
        'unverified_mediator': Context(True,True,True,False,False,True),
        'verified_mediator_no_transfer': Context(True,True,True,True,False,False),
        'verified_mediator_transfer': Context(True,True,True,True,False,True),
        'direct_protocol': Context(True,True,False,False,True,False),
        'veto': Context(False,True,True,True,False,True),
    }
    timelines={}
    for name,ctx in prototypes.items():
        first=step(base,ctx)
        after_departure=step(first.state,departure)
        after_shock=step(after_departure.state, replace(departure,external_disruption=True))
        reopen=step(after_shock.state,departure)
        timelines[name]={
            'initial':asdict(first), 'mediator_departure':asdict(after_departure),
            'external_disruption':asdict(after_shock),'reassessment':asdict(reopen)}
    # Independent direct Boolean baseline, given precisely the same context.
    # It should agree; this audit is not an IDOS advantage claim.
    fair_matches=sum(
        int(out.state.connected) == int(
            c.a_consents and c.b_consents and (
                c.shared_direct_protocol or (c.mediator_present and c.mediation_verified)))
        for c,out in stage1)
    return {
      'version':'0.9','model':'synthetic transition system',
      'exhaustive_initial_contexts':len(stage1),
      'initial_feasible':sum(o.feasible for _,o in stage1),
      'departure_cases_initially_connected':len(pairs),
      'persist_after_departure':sum(y for _,y in pairs),
      'conditional_entropy_future_given_connected_bits':round(coarse_entropy,6),
      'conditional_entropy_given_connected_and_transfer_bits':round(provenance_entropy,6),
      'optimal_brier_coarse':round(coarse_brier,6),
      'optimal_brier_with_transfer':round(provenance_brier,6),
      'full_information_deterministic_baseline_matches':fair_matches,
      'caution':'All outcome probabilities are induced by uniform enumeration of artificial inputs, not measured population frequencies. Transfer is explicitly stipulated, not discovered.',
      'timelines':timelines,
    }

if __name__=='__main__':
    print(json.dumps(audit(),indent=2,ensure_ascii=False))
