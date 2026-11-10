import unittest
from itertools import product
from cross_scale_generativity_v02 import (Offer,derive_rule,run,robust_actions,
    equal_information_baseline,update_rule,audit)

A=Offer('A','VERIFY','proofA')
B=Offer('B','MEDIATE','proofB')

class GenerativityAudit(unittest.TestCase):
    def test_baseline_no_guaranteed_action(self):
        self.assertEqual((),robust_actions(None))
    def test_separate_A_proposal_not_enough(self):
        self.assertIsNone(derive_rule((A,)))
    def test_separate_B_proposal_not_enough(self):
        self.assertIsNone(derive_rule((B,)))
    def test_composition_from_independent_offers(self):
        self.assertEqual(('verified_mediation',),run((A,B)).guaranteed_actions)
    def test_provenance_of_two_parties(self):
        self.assertEqual(('A:proofA','B:proofB'),derive_rule((A,B)).provenance)
    def test_permission_denial(self):
        self.assertEqual((),run((A,B),authorization=False).guaranteed_actions)
    def test_declined_B(self):
        self.assertEqual((),run((A,Offer('B','MEDIATE','proofB',False))).guaranteed_actions)
    def test_explicit_veto(self):
        self.assertEqual((),run((A,B,Offer('C','OPT_OUT','veto'))).guaranteed_actions)
    def test_evidence_required(self):
        self.assertIsNone(derive_rule((A,Offer('B','MEDIATE',''))))
    def test_unrelated_offer_insufficient(self):
        self.assertIsNone(derive_rule((A,Offer('B','VERIFY','proofB'))))
    def test_failed_rule_without_recovery_suspends(self):
        self.assertIsNone(update_rule(derive_rule((A,B)),(('verified_mediation',False),),()))
    def test_success_keeps_same_rule(self):
        rule=derive_rule((A,B))
        self.assertEqual(rule,update_rule(rule,(('verified_mediation',True),),()))
    def test_recovery_offer_changes_rule(self):
        rule=derive_rule((A,B))
        new=update_rule(rule,(('verified_mediation',False),),(Offer('C','RECOVERY','proofC'),))
        self.assertEqual('recovered_mediation',new.action)
        self.assertEqual(1,new.revision)
        self.assertEqual(('A:proofA','B:proofB','C:proofC'),new.provenance)
    def test_recovery_veto_blocks(self):
        rule=derive_rule((A,B))
        self.assertIsNone(update_rule(rule,(('verified_mediation',False),),(Offer('C','RECOVERY','proofC',False),)))
    def test_complete_baseline_matches_all_16(self):
        n=0
        for pa,pb,cb,auth in product((False,True),repeat=4):
            offers=tuple([A] if pa else [])+tuple([Offer('B','MEDIATE','proofB',cb)] if pb else [])
            self.assertEqual(run(offers,authorization=auth).guaranteed_actions,
                             equal_information_baseline(offers,authorization=auth))
            n+=1
        self.assertEqual(16,n)
    def test_audit_records_limitations(self):
        self.assertEqual(16,audit()['equal_information_comparisons'])
        self.assertTrue(any('pre-programmed' in x for x in audit()['limitations']))

if __name__=='__main__':unittest.main()
