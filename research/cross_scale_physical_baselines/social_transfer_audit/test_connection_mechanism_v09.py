import unittest
from dataclasses import replace
from connection_mechanism_v09 import State,Context,step,scenarios,audit

class MechanismTests(unittest.TestCase):
    def setUp(self):
        self.base=State()
        self.approved=Context(True,True,True,True,False,True)
        self.depart=Context(True,True,False,False,False,False)
    def test_exhaustive_contexts(self):self.assertEqual(len(list(scenarios())),64)
    def test_no_path(self): self.assertFalse(step(self.base,self.depart).feasible)
    def test_no_consent(self):self.assertFalse(step(self.base,replace(self.approved,a_consents=False)).state.connected)
    def test_both_veto(self):self.assertFalse(step(self.base,replace(self.approved,b_consents=False)).state.connected)
    def test_unverified_mediator(self):self.assertFalse(step(self.base,replace(self.approved,mediation_verified=False)).state.connected)
    def test_initial_mediated(self):self.assertTrue(step(self.base,self.approved).formed)
    def test_no_transfer_fails_departure(self):
        s=step(self.base,replace(self.approved,transfer_authorized=False)).state
        self.assertFalse(step(s,self.depart).state.connected)
    def test_transfer_survives_departure(self):
        s=step(self.base,self.approved).state
        self.assertTrue(step(s,self.depart).state.connected)
    def test_transfer_provenance(self):
        s=step(self.base,self.approved).state
        self.assertTrue(s.evidence_id.startswith('verified-transfer:'))
    def test_unverified_not_certified(self):
        self.assertFalse(step(self.base,replace(self.approved,mediation_verified=False)).state.certified_bridge)
    def test_refusal_revokes(self):
        s=step(self.base,self.approved).state
        t=step(s,replace(self.depart,a_consents=False)).state
        self.assertFalse(t.certified_bridge)
    def test_disruption_interrupts(self):
        s=step(self.base,self.approved).state
        t=step(s,replace(self.depart,external_disruption=True))
        self.assertFalse(t.state.connected)
        self.assertTrue(t.state.certified_bridge)
    def test_reopening_after_disruption(self):
        s=step(self.base,self.approved).state
        t=step(s,replace(self.depart,external_disruption=True)).state
        self.assertTrue(step(t,self.depart).state.connected)
    def test_no_provenance_fails(self):
        with self.assertRaises(ValueError):step(self.base,replace(self.approved,consent_evidence=''))
    def test_history_matters(self):
        a=step(self.base,self.approved).state
        b=step(self.base,replace(self.approved,transfer_authorized=False)).state
        self.assertTrue(a.connected and b.connected)
        self.assertNotEqual(step(a,self.depart).state.connected,step(b,self.depart).state.connected)
    def test_entropy_reduction(self):
        r=audit();self.assertGreater(r['conditional_entropy_future_given_connected_bits'],0)
        self.assertEqual(r['conditional_entropy_given_connected_and_transfer_bits'],0)
    def test_brier_reduction(self):
        r=audit();self.assertGreater(r['optimal_brier_coarse'],0)
        self.assertEqual(r['optimal_brier_with_transfer'],0)
    def test_fair_baseline(self):self.assertEqual(audit()['full_information_deterministic_baseline_matches'],64)
    def test_idempotent_read(self):self.assertEqual(audit(),audit())

if __name__=='__main__':unittest.main()
