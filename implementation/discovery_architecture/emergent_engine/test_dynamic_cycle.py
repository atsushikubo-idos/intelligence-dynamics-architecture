import unittest
from dynamic_cycle import DynamicCycle,ReplaySource,Candidate

class DynamicTests(unittest.TestCase):
    def test_four_conditions_with_scripted_fixture(self):
        s=ReplaySource([Candidate('physical constraint','energy_ceiling_gap',False,'expand_energy','hypothesis'),Candidate('underused capacity','unmet_capacity',False,'boost_output','hypothesis'),None])
        e=DynamicCycle(s); x=e.run(3,approve_frame=True)
        self.assertEqual([v['frame_after'] for v in x],['F1','F2','F2'])
        self.assertEqual([v['action'] for v in x],['expand_energy','boost_output','boost_output'])
        self.assertNotEqual(x[0]['metric_before'],x[0]['metric_after'])
        self.assertNotEqual(x[0]['eligible_interventions_before'],x[0]['eligible_interventions_after_frame_change'])
        self.assertEqual(x[1]['world_before'],x[0]['world_after'])
        self.assertEqual(x[2]['world_before'],x[1]['world_after'])
    def test_no_approval_no_frame_change(self):
        e=DynamicCycle(ReplaySource([Candidate('x','energy',True,'expand_energy','h')]))
        x=e.step(approve_frame=False)
        self.assertEqual(x['frame_after'],'F0')
        self.assertEqual(x['action'],'subsidize')
    def test_unsupported_sensor_rejected(self):
        e=DynamicCycle(ReplaySource([Candidate('x','imaginary_sensor',True,'inspect','h')]))
        x=e.step(approve_frame=True)
        self.assertEqual(x['review_status'],'rejected');self.assertEqual(x['frame_after'],'F0')
    def test_old_frame_remains_available(self):
        e=DynamicCycle(ReplaySource([Candidate('x','energy',True,'expand_energy','h')]))
        x=e.step(approve_frame=True)
        self.assertIn('F0',e.frames)
        self.assertEqual(x['score_before_on_old_frame'],x['world_before']['wealth'])
    def test_no_hidden_authority_escalation(self):
        e=DynamicCycle(ReplaySource([Candidate('x','energy',True,'delete_database','h')]))
        x=e.step(approve_frame=True)
        self.assertEqual(x['frame_after'],'F0');self.assertEqual(x['review_status'],'rejected')
if __name__=='__main__':unittest.main()
