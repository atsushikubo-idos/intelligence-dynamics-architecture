"""Deterministic walk-through of CDP v2.0-draft with three unlike units.

Synthetic scenario. It shows what the protocol makes checkable; it is not
evidence that the protocol improves real coordination.

Run from the repository root:
    python implementation/cdp_v2/example.py
"""
from __future__ import annotations

import json

from cdp2 import Session, commitment, slot

DAY = 86_400.0


def run() -> dict:
    s = Session()

    # Three units with very different clocks and ways of checking things.
    s.hello("human", 0, unit_type="human", frame="narrative/contextual",
            min_review_latency=1 * DAY, verifies=["evidence_pointer"])
    s.hello("ai", 0, unit_type="ai_system", frame="probabilistic",
            min_review_latency=1.0,
            verifies=["evidence_pointer", "prediction", "replicable_procedure"])
    s.hello("org", 0, unit_type="organization", frame="rules/authority/workflow",
            min_review_latency=7 * DAY, verifies=["evidence_pointer"])

    # 1. Describe: partial disclosure is legitimate, basis is mandatory.
    d = s.describe("ai", 10, {
        "difference": slot("demand forecast error tripled in segment B",
                           basis="observed", evidence=["metrics://forecast/B"]),
        "frame": slot(disclosure="private"),
        "update": slot(disclosure="unresolved"),
    })

    # 2. The human sees something the schema has no place for.
    s.describe("human", 20, {
        "unmapped": slot("customers stopped arguing with us; they just leave quietly",
                         basis="observed"),
    }, refs=[d.seq])

    # 3. Translate: the AI claims a complete rendition; the source disagrees.
    h = s.describe("human", 30, {
        "difference": slot("trust is thinning, not only volume", basis="inferred")})
    tr = s.translate("ai", 31, source_seq=h.seq, target_frame="probabilistic",
                     rendition={"churn_probability": "+0.08"}, quality="complete")
    s.translate_ack("human", 30 + DAY, translation_seq=tr.seq, verdict="altered",
                    notes=["'trust' was reduced to churn; the relational part is gone"])

    # 4. Claim with a verification handle; a weaker verifier says so honestly.
    c = s.claim("ai", 40 + DAY, statement="segment B decline is causal, not seasonal",
                basis="inferred", handle_kind="replicable_procedure",
                handle="notebook://causal/B#v3")
    s.verify("human", 50 + DAY, claim_seq=c.seq, result="unverifiable_by_me",
             reason="cannot run or audit the causal model")
    s.verify("org", 60 + DAY, claim_seq=c.seq, result="confirmed")  # rubber stamp

    # 5. Commit before reality contact; score only what was committed.
    salt = "s-0001"
    cm = s.commit("ai", 70 + DAY, about="segment_B_q4",
                  commitment_hash=commitment("decline", salt))
    cm2 = s.commit("org", 71 + DAY, about="segment_B_q4",
                   commitment_hash=commitment("recovery", "s-0002"))
    rc = s.recontact("human", 30 * DAY, about="segment_B_q4", outcome="decline",
                     basis="observed", evidence=["ledger://sales/q4"])
    s.reveal("ai", 30 * DAY + 1, commit_seq=cm.seq, prediction="decline",
             salt=salt, recontact_seq=rc.seq)
    # org never reveals cm2 -> visible in the audit.

    # 6. Coordinate: a fast unit proposes an irreversible step with a short window.
    p = s.propose_action("ai", 31 * DAY, action="terminate segment B contracts",
                         reversibility="irreversible", affected=["human", "org"],
                         review_window=3600.0)
    s.respond("human", 31 * DAY + 600, proposal_seq=p.seq, response="hold",
              reason="the unmapped observation is still unexplained")
    s.enact("ai", 31 * DAY + 900, proposal_seq=p.seq)

    # 7. Mutual updateability: who actually changed because of whom?
    u = s.update_notice("ai", 32 * DAY, cause_seq=h.seq, level="L3",
                        changed=["frame"], handle_kind="evidence_pointer",
                        handle="repo://model/config@relational-feature")
    s.verify("human", 33 * DAY, claim_seq=u.seq, result="confirmed")
    s.update_notice("human", 34 * DAY, cause_seq=d.seq, level="L2", changed=["state"])

    # 8. The protocol amends itself: the unmapped observation gets a slot.
    a = s.amend("human", 35 * DAY, kind="add_slot", target="relational_signal",
                definition="changes in how parties engage, independent of volume",
                window=7 * DAY)
    s.respond("ai", 35 * DAY + 1, proposal_seq=a.seq, response="consent")
    s.respond("org", 41 * DAY, proposal_seq=a.seq, response="consent")
    s.ratify("human", 42 * DAY, amend_seq=a.seq)
    s.describe("human", 43 * DAY, {
        "relational_signal": slot("silent exits rising", basis="observed")})

    return s.audit()


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
