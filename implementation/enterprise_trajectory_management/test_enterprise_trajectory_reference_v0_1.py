import unittest
from enterprise_trajectory_reference_v0_1 import *

class TestEnterpriseReference(unittest.TestCase):
    def test_demo(self):
        m = synthetic_demo()
        self.assertEqual(len(m.events),5)
        self.assertEqual(len(m.futures),2)
        self.assertEqual(m.frames['rf2'].previous_id,'rf1')
        self.assertEqual(m.relations['rel2'].previous_id,'rel1')
        self.assertEqual(m.decisions[0].action,'pause')
        self.assertIn('res1',m.holdings)
    def test_difference_not_residual(self):
        m=EnterpriseTrajectoryModel('x')
        m.observe(Event('d',1,'Difference','x','observed mismatch'))
        with self.assertRaises(ValueError): m.hold('d','unresolved')
    def test_residual_explicit(self):
        m=EnterpriseTrajectoryModel('x')
        with self.assertRaises(ValueError): m.observe(Event('r',1,'Residual','x','mismatch'))
    def test_evidence_required(self):
        m=EnterpriseTrajectoryModel('x')
        with self.assertRaises(ValueError): m.observe(Event('e',1,'Reality','x','note',('missing',)))
    def test_no_duplicate(self):
        m=EnterpriseTrajectoryModel('x')
        m.observe(Event('e',1,'Reality','x','note'))
        with self.assertRaises(ValueError): m.observe(Event('e',2,'Reality','x','note'))
    def test_order(self):
        m=EnterpriseTrajectoryModel('x')
        with self.assertRaises(ValueError): m.observe(Event('e',2,'Reality','x','note'))
    def test_invalid_action(self):
        m=EnterpriseTrajectoryModel('x')
        with self.assertRaises(ValueError): m.decide(GovernanceDecision('g','x','auto_optimize','invalid'))
    def test_all_processes_declared(self):
        self.assertEqual(len(PROCESSES),12)
    def test_report_limits(self):
        self.assertIn('no empirical validation',synthetic_demo().report()['limitations'])

if __name__=='__main__': unittest.main()
