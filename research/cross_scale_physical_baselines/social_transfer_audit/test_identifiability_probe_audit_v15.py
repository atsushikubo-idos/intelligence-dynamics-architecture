import math
import unittest
from identifiability_probe_audit_v15 import (
    sample_trial, observational_likelihood,passive_cusum,rolling_drop,
    active_attribution,passive_attribution,decision_policy,evaluate,
    CHANGE_AT, PROBE_START,PROBE_SPACING,N,PRE,POST_PASSIVE
)

class TestIdentifiabilityProbeAudit(unittest.TestCase):
    def test_observational_equivalence_exact(self):
        for s in (0,7,42,99):
            t=sample_trial('A',s)
            self.assertEqual(observational_likelihood(t.passive,'A'),observational_likelihood(t.passive,'B'))
    def test_passive_abstains(self):
        self.assertEqual(passive_attribution(sample_trial('A',8).passive),'undetermined')
    def test_identical_passive_with_same_seed(self):
        self.assertEqual(sample_trial('A',13).passive,sample_trial('B',13).passive)
    def test_probe_response_can_differ(self):
        self.assertNotEqual(sample_trial('A',14).probes,sample_trial('B',14).probes)
    def test_no_probe_abstains(self):
        self.assertEqual(active_attribution([])[0],'undetermined')
    def test_no_permission_abstains(self):
        r=decision_policy(sample_trial('A',3), probe_permitted=False)
        self.assertEqual(r['cause'],'undetermined')
    def test_forced_A(self):
        self.assertEqual(active_attribution([(t,1) for t in range(PROBE_START,PROBE_START+21,3)])[0],'A')
    def test_forced_B(self):
        self.assertEqual(active_attribution([(t,0) for t in range(PROBE_START,PROBE_START+21,3)])[0],'B')
    def test_probe_schedule_fixed(self):
        self.assertEqual([t for t,_ in sample_trial('B',1).probes],list(range(PROBE_START,N,PROBE_SPACING)))
    def test_prechange_passive_rate_population(self):
        self.assertEqual(PRE,.8)
        self.assertEqual(POST_PASSIVE,.45)
    def test_detection_exists_for_clear_shift(self):
        sample=[1]*CHANGE_AT+[0]*(N-CHANGE_AT)
        self.assertIsNotNone(passive_cusum(sample))
        self.assertIsNotNone(rolling_drop(sample))
    def test_determinism(self):
        self.assertEqual(evaluate(20,10),evaluate(20,10))
    def test_report_reason(self):
        t=sample_trial('A',9)
        r=decision_policy(t,False)
        self.assertIn(r['reason'],('Probe not permitted','No detected shift'))
    def test_numeric_no_100percent_claim(self):
        res=evaluate(50,22)['results']
        self.assertLessEqual(res['A']['active_correct_fraction'],1)
        self.assertLessEqual(res['B']['active_correct_fraction'],1)

if __name__=='__main__': unittest.main()
