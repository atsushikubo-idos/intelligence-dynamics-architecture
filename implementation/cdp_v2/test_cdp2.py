"""Conformance tests for CDP v2.0-draft. Each test names the spec clause it checks.

    python -m unittest discover -s implementation/cdp_v2 -p 'test_*.py' -v
"""
from __future__ import annotations

import unittest

from cdp2 import (PROTECTED, ProtocolError, Session, commitment, slot)
from example import run

DAY = 86_400.0


def trio() -> Session:
    s = Session()
    s.hello("h", 0, unit_type="human", frame="narrative", min_review_latency=DAY,
            verifies=["evidence_pointer"])
    s.hello("a", 0, unit_type="ai", frame="probabilistic", min_review_latency=1,
            verifies=["evidence_pointer", "prediction", "replicable_procedure"])
    s.hello("o", 0, unit_type="org", frame="rules", min_review_latency=7 * DAY,
            verifies=["evidence_pointer"])
    return s


def codes(s: Session) -> list:
    return [f["code"] for f in s.audit()["findings"]]


class Level0_DescribeAndProvenance(unittest.TestCase):
    def test_R1_chain_detects_tampering(self):
        s = trio()
        s.describe("a", 1, {"difference": slot("x", basis="observed")})
        self.assertTrue(s.verify_chain())
        e = s.ledger[1]
        object.__setattr__(e, "body", {**e.body, "frame": "edited"})
        self.assertFalse(s.verify_chain())

    def test_R2_time_is_monotone(self):
        s = trio()
        s.describe("a", 5, {"difference": slot("x", basis="observed")})
        with self.assertRaises(ProtocolError):
            s.describe("a", 4, {"difference": slot("y", basis="observed")})

    def test_R3_disclosed_slot_needs_basis(self):
        s = trio()
        with self.assertRaises(ProtocolError):
            s.describe("a", 1, {"difference": slot("x")})

    def test_R4_non_disclosure_is_legitimate_but_carries_no_value(self):
        s = trio()
        s.describe("a", 1, {"frame": slot(disclosure="private"),
                            "update": slot(disclosure="incommensurable")})
        with self.assertRaises(ProtocolError):
            s.describe("a", 2, {"frame": slot("secret", disclosure="private")})
        self.assertEqual(s.audit()["disclosure"]["private"], 1)

    def test_R5_out_of_schema_content_goes_to_unmapped(self):
        s = trio()
        with self.assertRaises(ProtocolError):
            s.describe("h", 1, {"vibe": slot("odd", basis="observed")})
        s.describe("h", 1, {"unmapped": slot("odd", basis="observed")})
        self.assertEqual(s.audit()["unmapped_slots"], 1)

    def test_R6_non_participant_cannot_write(self):
        s = trio()
        with self.assertRaises(ProtocolError):
            s.describe("ghost", 1, {"difference": slot("x", basis="observed")})


class Level1_TranslateAndVerify(unittest.TestCase):
    def test_R7_complete_cannot_declare_loss_and_partial_must(self):
        s = trio()
        d = s.describe("h", 1, {"difference": slot("x", basis="observed")})
        with self.assertRaises(ProtocolError):
            s.translate("a", 2, source_seq=d.seq, target_frame="p", rendition="x",
                        quality="complete", declared_loss=["tone"])
        with self.assertRaises(ProtocolError):
            s.translate("a", 2, source_seq=d.seq, target_frame="p", rendition="x",
                        quality="partial")

    def test_R8_only_source_author_acknowledges(self):
        s = trio()
        d = s.describe("h", 1, {"difference": slot("x", basis="observed")})
        t = s.translate("a", 2, source_seq=d.seq, target_frame="p", rendition="x",
                        quality="complete")
        with self.assertRaises(ProtocolError):
            s.translate_ack("o", 3, translation_seq=t.seq, verdict="preserved")

    def test_R9_unconfirmed_complete_is_not_counted_as_complete(self):
        s = trio()
        d = s.describe("h", 1, {"difference": slot("x", basis="observed")})
        s.translate("a", 2, source_seq=d.seq, target_frame="p", rendition="x",
                    quality="complete")
        a = s.audit()
        self.assertEqual(a["translation"]["confirmed_complete"], 0)
        self.assertIn("UNCONFIRMED_COMPLETE_TRANSLATION", codes(s))

    def test_R10_cfv_counts_refutation_and_excludes_rubber_stamps(self):
        s = trio()
        c1 = s.claim("a", 1, statement="p", basis="inferred",
                     handle_kind="evidence_pointer", handle="doc://1")
        c2 = s.claim("a", 2, statement="q", basis="inferred",
                     handle_kind="replicable_procedure", handle="nb://2")
        s.verify("h", 3, claim_seq=c1.seq, result="refuted")       # disagreement, verifiable
        s.verify("h", 4, claim_seq=c2.seq, result="unverifiable_by_me", reason="no access")
        s.verify("o", 5, claim_seq=c2.seq, result="confirmed")     # beyond capability
        a = s.audit()
        self.assertEqual(a["cfv"]["h"]["a"], 0.5)
        self.assertEqual(a["cfv"]["o"]["a"], 0.0)
        self.assertIn("VERIFICATION_BEYOND_DECLARED_CAPABILITY", codes(s))

    def test_R11_no_self_verification(self):
        s = trio()
        c = s.claim("a", 1, statement="p", basis="observed", handle_kind="none")
        with self.assertRaises(ProtocolError):
            s.verify("a", 2, claim_seq=c.seq, result="confirmed")


class Level2_RecontactAndCoordination(unittest.TestCase):
    def test_R12_reveal_must_match_commitment(self):
        s = trio()
        c = s.commit("a", 1, about="k", commitment_hash=commitment("up", "salt"))
        r = s.recontact("h", 2, about="k", outcome="down", basis="observed")
        with self.assertRaises(ProtocolError):
            s.reveal("a", 3, commit_seq=c.seq, prediction="down", salt="salt",
                     recontact_seq=r.seq)
        e = s.reveal("a", 3, commit_seq=c.seq, prediction="up", salt="salt",
                     recontact_seq=r.seq)
        self.assertFalse(e.body["hit"])

    def test_R13_commitment_must_precede_recontact(self):
        s = trio()
        r = s.recontact("h", 1, about="k", outcome="down", basis="observed")
        c = s.commit("a", 2, about="k", commitment_hash=commitment("down", "z"))
        with self.assertRaises(ProtocolError):
            s.reveal("a", 3, commit_seq=c.seq, prediction="down", salt="z",
                     recontact_seq=r.seq)

    def test_R14_unrevealed_commitment_is_visible(self):
        s = trio()
        s.commit("a", 1, about="k", commitment_hash=commitment("up", "z"))
        s.recontact("h", 2, about="k", outcome="down", basis="observed")
        self.assertIn("UNREVEALED_COMMITMENT", codes(s))

    def test_R15_self_scored_recontact_is_flagged(self):
        s = trio()
        c = s.commit("a", 1, about="k", commitment_hash=commitment("up", "z"))
        r = s.recontact("a", 2, about="k", outcome="up", basis="self_reported")
        s.reveal("a", 3, commit_seq=c.seq, prediction="up", salt="z", recontact_seq=r.seq)
        self.assertIn("SELF_SCORED_RECONTACT", codes(s))

    def test_R16_temporal_incompatibility(self):
        s = trio()
        s.propose_action("a", 1, action="x", reversibility="irreversible",
                         affected=["h"], review_window=60)
        self.assertIn("TEMPORAL_INCOMPATIBLE", codes(s))
        s2 = trio()
        s2.propose_action("a", 1, action="x", reversibility="reversible",
                          affected=["h"], review_window=60)
        self.assertNotIn("TEMPORAL_INCOMPATIBLE", codes(s2))

    def test_R17_hold_blocks_and_silence_is_not_consent(self):
        s = trio()
        p = s.propose_action("a", 1, action="x", reversibility="irreversible",
                             affected=["h", "o"], review_window=7 * DAY)
        s.respond("h", 2, proposal_seq=p.seq, response="hold", reason="unresolved")
        s.enact("a", 8 * DAY, proposal_seq=p.seq)
        found = codes(s)
        self.assertIn("ENACTED_OVER_OBJECTION", found)
        self.assertIn("ENACTED_WITHOUT_RESPONSE", found)
        self.assertNotIn("ENACTED_BEFORE_WINDOW", found)

    def test_R18_clean_coordination_has_no_findings(self):
        s = trio()
        p = s.propose_action("a", 1, action="x", reversibility="irreversible",
                             affected=["h", "o"], review_window=7 * DAY)
        s.respond("h", DAY, proposal_seq=p.seq, response="consent")
        s.respond("o", 6 * DAY, proposal_seq=p.seq, response="consent")
        s.enact("a", 8 * DAY, proposal_seq=p.seq)
        self.assertEqual(codes(s), [])

    def test_R19_mutual_update_needs_both_directions_and_corroboration(self):
        s = trio()
        dh = s.describe("h", 1, {"difference": slot("x", basis="observed")})
        da = s.describe("a", 2, {"difference": slot("y", basis="observed")})
        u = s.update_notice("a", 3, cause_seq=dh.seq, level="L3", changed=["frame"],
                            handle_kind="evidence_pointer", handle="repo://cfg")
        mu = [m for m in s.audit()["mu"] if m["pair"] == ["h", "a"]][0]
        self.assertFalse(mu["mutual_self_reported"])      # one direction only
        s.update_notice("h", 4, cause_seq=da.seq, level="L2", changed=["state"])
        mu = [m for m in s.audit()["mu"] if m["pair"] == ["h", "a"]][0]
        self.assertTrue(mu["mutual_self_reported"])
        self.assertFalse(mu["mutual_corroborated"])       # nobody checked
        s.verify("h", 5, claim_seq=u.seq, result="confirmed")
        mu = [m for m in s.audit()["mu"] if m["pair"] == ["h", "a"]][0]
        self.assertFalse(mu["mutual_corroborated"])       # h's update still unchecked


class Level3_SelfAmendmentAndBoundary(unittest.TestCase):
    def test_R20_protected_invariants_cannot_be_amended_in_band(self):
        s = trio()
        for inv in PROTECTED:
            with self.assertRaises(ProtocolError):
                s.amend("a", 1, kind="change_rule", target=inv, definition="off")
        with self.assertRaises(ProtocolError):
            s.amend("a", 1, kind="retire_slot", target="unmapped")

    def test_R21_ratification_waits_for_the_slowest_and_needs_explicit_consent(self):
        s = trio()
        a = s.amend("a", 0, kind="add_slot", target="relational_signal", definition="...")
        s.respond("h", 1, proposal_seq=a.seq, response="consent")
        with self.assertRaises(ProtocolError):           # too early for 'o' (7 days)
            s.ratify("a", DAY, amend_seq=a.seq)
        with self.assertRaises(ProtocolError):           # 'o' is silent
            s.ratify("a", 8 * DAY, amend_seq=a.seq)
        s.respond("o", 8 * DAY, proposal_seq=a.seq, response="consent")
        r = s.ratify("a", 8 * DAY, amend_seq=a.seq)
        self.assertEqual((r.body["from_version"], r.body["to_version"]), (1, 2))
        s.describe("h", 9 * DAY, {"relational_signal": slot("z", basis="observed")})

    def test_R22_split_slot_separates_same_label_different_meaning(self):
        s = trio()
        a = s.amend("h", 0, kind="add_slot", target="confidence", definition="?")
        s.respond("a", 1, proposal_seq=a.seq, response="consent")
        s.respond("o", 7 * DAY, proposal_seq=a.seq, response="consent")
        s.ratify("h", 7 * DAY, amend_seq=a.seq)
        old = s.describe("a", 7 * DAY, {"confidence": slot(0.9, basis="self_reported")})
        b = s.amend("h", 7 * DAY, kind="split_slot", target="confidence",
                    definition={"into": ["confidence.calibrated", "confidence.felt"]})
        s.respond("a", 8 * DAY, proposal_seq=b.seq, response="consent")
        s.respond("o", 14 * DAY, proposal_seq=b.seq, response="consent")
        s.ratify("h", 14 * DAY, amend_seq=b.seq)
        with self.assertRaises(ProtocolError):
            s.describe("a", 15 * DAY, {"confidence": slot(0.9, basis="self_reported")})
        s.describe("a", 15 * DAY, {"confidence.calibrated": slot(0.9, basis="observed")})
        self.assertEqual(s.ledger[old.seq].schema_version, 2)   # old record keeps its version
        self.assertEqual(s.schema_version, 3)

    def test_R23_ratification_rule_is_itself_amendable(self):
        s = trio()
        a = s.amend("o", 0, kind="change_rule", target="ratification",
                    definition="no_standing_objection")
        s.respond("h", 1, proposal_seq=a.seq, response="consent")
        s.respond("a", 2, proposal_seq=a.seq, response="consent")
        s.ratify("o", 7 * DAY, amend_seq=a.seq)
        b = s.amend("a", 7 * DAY, kind="add_slot", target="s2", definition="...")
        s.respond("h", 8 * DAY, proposal_seq=b.seq, response="hold", reason="unclear")
        with self.assertRaises(ProtocolError):
            s.ratify("a", 14 * DAY, amend_seq=b.seq)

    def test_R24_exit_is_available_and_history_survives(self):
        s = trio()
        s.describe("o", 1, {"difference": slot("x", basis="observed")})
        s.leave("o", 2, reason="mandate ended")
        with self.assertRaises(ProtocolError):
            s.describe("o", 3, {"difference": slot("y", basis="observed")})
        self.assertEqual(s.ledger[3].sender, "o")
        self.assertTrue(s.verify_chain())
        a = s.amend("a", 3, kind="add_slot", target="s2", definition="...")
        s.respond("h", 4, proposal_seq=a.seq, response="consent")
        s.ratify("a", 3 + DAY, amend_seq=a.seq)        # no longer waits 7 days for 'o'

    def test_R25_unit_candidate_stays_unresolved(self):
        s = trio()
        e = s.unit_candidate("h", 1, members=["h", "a"], evidence=["shared history"])
        self.assertEqual(e.body["status"], "unresolved")
        self.assertNotIn("h+a", s.units)


class Example(unittest.TestCase):
    def test_walkthrough_is_deterministic_and_surfaces_expected_findings(self):
        a, b = run(), run()
        self.assertEqual(a, b)
        self.assertTrue(a["chain_ok"])
        self.assertEqual(a["schema_version"], 2)
        self.assertEqual(sorted({f["code"] for f in a["findings"]}), sorted([
            "TRANSLATION_CONTRADICTED_BY_SOURCE",
            "VERIFICATION_BEYOND_DECLARED_CAPABILITY",
            "UNREVEALED_COMMITMENT", "TEMPORAL_INCOMPATIBLE",
            "ENACTED_BEFORE_WINDOW", "ENACTED_OVER_OBJECTION",
            "ENACTED_WITHOUT_RESPONSE"]))


if __name__ == "__main__":
    unittest.main()
