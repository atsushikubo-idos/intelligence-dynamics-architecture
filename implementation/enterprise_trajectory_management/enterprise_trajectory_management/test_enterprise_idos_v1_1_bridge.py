import unittest
from enterprise_trajectory_reference_v0_1 import *
from enterprise_idos_v1_1_bridge import bridge_enterprise, complete_reopening_after_recontact
import idos_reference_v1_1 as core

class TestBridge(unittest.TestCase):
    def test_demo_projection(self):
        source=synthetic_demo(); result=bridge_enterprise(source)
        self.assertIsInstance(result.unit,core.UpdatingUnit)
        self.assertEqual(result.unit.frame.name,'Resilience-oriented')
        self.assertEqual(result.unit.frame.version,2)
        self.assertEqual(len(result.unit.residuals),1)
        self.assertEqual(len(result.unit.holdings),1)
        self.assertEqual(len(result.unit.reopening_history),0)
    def test_difference_is_not_residual(self):
        m=EnterpriseTrajectoryModel('test'); m.observe(Event('d',1,'Difference','enterprise','mismatch'))
        r=bridge_enterprise(m)
        self.assertEqual(len(r.unit.residuals),0)
    def test_relationship_not_automatic_coupling(self):
        r=bridge_enterprise(synthetic_demo())
        self.assertTrue(any(p.event_type=='enterprise_relation_revision' for p in r.unit.trajectory.provenance))
        self.assertEqual(r.unit.component_ids,[])
    def test_governance_pause_not_auto_reopening(self):
        r=bridge_enterprise(synthetic_demo())
        self.assertEqual(r.unit.reopening_history,[])
    def test_explicit_q2_reopening(self):
        r=bridge_enterprise(synthetic_demo())
        assessment=core.FutureUpdateabilityAssessment(
            status=core.FutureUpdateabilityStatus.UNCERTAIN,
            can_detect_new_difference=True, alternatives_can_emerge=True,
            override_or_revision_exists=True, irreversible_dependency_increased=False,
            reality_recontact_route_exists=True, updating_structure_can_change=True,
            rationale='Synthetic assessor judgment, not an empirical score')
        complete_reopening_after_recontact(r,source='synthetic review',observation='reviewed',
            assessment=assessment,action=core.ReopeningAction.MAINTAIN,
            basis='Explicit synthetic decision',decision_rule_reopened='staged investment')
        self.assertEqual(len(r.unit.reopening_history),1)
    def test_empty_model(self):
        r=bridge_enterprise(EnterpriseTrajectoryModel('empty'))
        self.assertEqual(r.unit.frame.name,'Unspecified enterprise frame')
    def test_non_linear_frame_history_rejected(self):
        m=EnterpriseTrajectoryModel('x')
        m.add_frame(ReferenceFrameRevision('f1',None,'one',(),(),'init'))
        m.add_frame(ReferenceFrameRevision('f2',None,'two',(),(),'other root'))
        with self.assertRaises(ValueError): bridge_enterprise(m)

if __name__=='__main__': unittest.main()
