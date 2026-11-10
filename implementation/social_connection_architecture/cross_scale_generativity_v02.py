"""IDOS Cross-Scale Generativity Audit v0.2 (synthetic).

An auditable toy negotiation in which a rule *template* is assembled from
independent, complementary agent proposals. No opaque-agent learning or
unbounded novel concepts are claimed. Baseline receives identical messages.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from itertools import product
import json

# A and B face two indistinguishable hidden worlds. Old actions only succeed
# in one hidden world each. A composite mediated action can cover both.
WORLDS=("left", "right")
OLD_ACTIONS=("left", "right")

@dataclass(frozen=True)
class Offer:
    actor: str
    kind: str                # VERIFY, MEDIATE, OPT_OUT, or irrelevant
    evidence: str
    consent: bool = True

@dataclass(frozen=True)
class GenerationRule:
    name: str
    required: tuple[str,...]
    action: str
    # A rule is constructed from proposals, not selected from a stored catalog.
    provenance: tuple[str,...]
    revision: int = 0

@dataclass(frozen=True)
class Outcome:
    proposals: tuple[Offer,...]
    generated_rule: GenerationRule|None
    guaranteed_actions: tuple[str,...]
    complete_history_baseline: tuple[str,...]
    reason: str


def derive_rule(offers:tuple[Offer,...])->GenerationRule|None:
    """A public meta-rule composes two complementary independently supplied
    capabilities; neither individual proposal specifies the resulting action.
    Consent must be affirmatively declared by both proposal owners.
    """
    verification=next((o for o in offers if o.actor=='A' and o.kind=='VERIFY' and o.consent and o.evidence),None)
    mediation=next((o for o in offers if o.actor=='B' and o.kind=='MEDIATE' and o.consent and o.evidence),None)
    veto=any(o.kind=='OPT_OUT' or not o.consent for o in offers)
    if not verification or not mediation or veto:
        return None
    return GenerationRule('composed_verify_then_mediate',('VERIFY','MEDIATE'),
                          'verified_mediation', (f'A:{verification.evidence}',f'B:{mediation.evidence}'))


def allowed(world:str, action:str, rule:GenerationRule|None, *, authorization:bool)->bool:
    if action in OLD_ACTIONS:
        return action==world
    return bool(rule and authorization and action==rule.action and
                rule.required==('VERIFY','MEDIATE'))


def robust_actions(rule:GenerationRule|None, *, authorization:bool=True)->tuple[str,...]:
    candidates=OLD_ACTIONS+((rule.action,) if rule else ())
    return tuple(a for a in candidates if all(allowed(w,a,rule,authorization=authorization) for w in WORLDS))


def equal_information_baseline(offers:tuple[Offer,...], *, authorization:bool=True)->tuple[str,...]:
    """Conventional full-history protocol composer: same proposals, same
    composition grammar, same authorization, no IDOS provenance wrapper.
    """
    kinds={(o.actor,o.kind) for o in offers if o.consent and o.evidence}
    veto=any(o.kind=='OPT_OUT' or not o.consent for o in offers)
    can_compose=(('A','VERIFY') in kinds and ('B','MEDIATE') in kinds and not veto)
    candidates=OLD_ACTIONS+(('verified_mediation',) if can_compose else ())
    return tuple(a for a in candidates if all(
        (a==w if a in OLD_ACTIONS else can_compose and authorization)
        for w in WORLDS))


def run(offers:tuple[Offer,...], *, authorization:bool=True)->Outcome:
    rule=derive_rule(offers)
    actions=robust_actions(rule,authorization=authorization)
    base=equal_information_baseline(offers, authorization=authorization)
    assert actions==base, 'Same-information baseline divergence'
    reason=('co-constructed rule with both parties authorization' if actions
            else 'no robust action: missing complementary proposal, consent, or authorization')
    return Outcome(offers,rule,actions,base,reason)


def update_rule(previous:GenerationRule|None, feedback:tuple[tuple[str,bool],...],
                offers:tuple[Offer,...])->GenerationRule|None:
    """Outcome-dependent rule revision: after a failed verified-mediation
    outcome, a fresh, explicitly consented recovery proposal is required.
    This is a pre-specified deterministic meta-rule, *not autonomous discovery*.
    """
    if previous is None:
        return None
    failures=any(action==previous.action and not success for action,success in feedback)
    if not failures:
        return previous
    recovery=next((o for o in offers if o.actor=='C' and o.kind=='RECOVERY' and o.consent and o.evidence),None)
    if not recovery or any(not o.consent or o.kind=='OPT_OUT' for o in offers):
        return None
    return GenerationRule('recovery_gated_mediation',('VERIFY','MEDIATE','RECOVERY'),
                          'recovered_mediation',previous.provenance+(f'C:{recovery.evidence}',),previous.revision+1)


def audit():
    a=Offer('A','VERIFY','A:verification-capability')
    b=Offer('B','MEDIATE','B:mediation-capability')
    good=run((a,b))
    blocked=run((a,b),authorization=False)
    refused=run((a,Offer('B','MEDIATE','B:mediation-capability',consent=False)))
    revised=update_rule(good.generated_rule,(('verified_mediation',False),),
                        (Offer('C','RECOVERY','C:audited-recovery'),))
    census=0
    for a_present,b_present,consent,authorized in product((False,True),repeat=4):
        offers=tuple([a] if a_present else [])+tuple([Offer('B','MEDIATE','B:mediation-capability',consent)] if b_present else [])
        run(offers,authorization=authorized)
        census+=1
    return {'independent_messages':[asdict(a),asdict(b)],
            'jointly_constructed_rule':asdict(good.generated_rule),
            'before_rule_guarantees':list(robust_actions(None)),
            'after_rule_guarantees':list(good.guaranteed_actions),
            'authorization_blocked':list(blocked.guaranteed_actions),
            'explicit_refusal_blocked':list(refused.guaranteed_actions),
            'updated_rule_after_failure_and_recovery_offer':asdict(revised),
            'equal_information_comparisons':census,
            'limitations':['Finite action grammar is defined in source',
                           'The compositional meta-rule is pre-programmed',
                           'Outcome feedback is synthetic, not independently verified',
                           'Baseline has identical predictive capabilities',
                           'The rule revision is scripted, not self-invented']}

if __name__=='__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))
