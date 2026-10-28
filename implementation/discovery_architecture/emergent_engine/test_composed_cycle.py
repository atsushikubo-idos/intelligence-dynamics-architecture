import unittest
from composed_cycle import ComposedCycle,GeneratedCandidate,compile_metric,InvalidMetric
from dynamic_cycle import ReplaySource
class TestComposed(unittest.TestCase):
 def test_dynamic_generated_metrics_and_cycle(self):
  s=ReplaySource([GeneratedCandidate('gap','capacity-output',False,'expand_energy','fixture'),GeneratedCandidate('efficiency','output/energy',True,'boost_output','fixture'),None]);e=ComposedCycle(s)
  events=e.run(3,approve_frame=True)
  self.assertEqual([x['frame_after'] for x in events],['F1','F2','F2'])
  self.assertEqual(events[1]['world_before'],events[0]['world_after'])
  self.assertNotEqual(events[0]['metric_before'],events[0]['metric_after'])
  self.assertIn('F0',e.frames)
 def test_unapproved(self):
  e=ComposedCycle(ReplaySource([GeneratedCandidate('gap','capacity-output',False,'expand_energy','fixture')]))
  self.assertEqual(e.step(approve_frame=False)['frame_after'],'F0')
 def test_no_code_execution(self):
  for expr in ['__import__("os").system("id")','wealth.__class__','wealth**100','wealth[0]','unknown','wealth/0','wealth if energy else output']:
   with self.subTest(expr=expr):
    with self.assertRaises(InvalidMetric):compile_metric(expr)
 def test_bad_action(self):
  e=ComposedCycle(ReplaySource([GeneratedCandidate('x','capacity-output',False,'delete_files','x')]))
  self.assertEqual(e.step(approve_frame=True)['review_status'],'rejected')
 def test_not_same_as_unchanged_prompt(self):
  e=ComposedCycle(ReplaySource([GeneratedCandidate('gap','capacity-output',False,'expand_energy','fixture')]))
  x=e.step(approve_frame=True)
  self.assertNotEqual(x['before_old'],x['before_new'])
if __name__=='__main__': unittest.main()
