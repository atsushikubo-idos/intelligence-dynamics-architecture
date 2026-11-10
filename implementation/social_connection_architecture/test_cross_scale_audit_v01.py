import unittest
from itertools import product
from cross_scale_audit_v01 import run_scenario,exhaustive_equivalence,complete_history_baseline
class CrossScaleAuditTests(unittest.TestCase):
    def test_opaque_problem_not_robust(self):
        self.assertEqual('POSSIBLE_NOT_GUARANTEED',run_scenario('x',mediator=False).status)
    def test_observation_can_enable_guarantee(self):
        self.assertEqual(('left',),run_scenario('x',signal=True,mediator=False).robust_actions)
    def test_new_node_without_protocol_not_enough(self):
        self.assertEqual((),run_scenario('x',mediator=True).robust_actions)
    def test_explicit_protocol_expands_choice(self):
        self.assertEqual(('mediated',),run_scenario('x',mediated=True).robust_actions)
    def test_refusal_blocks(self):
        self.assertEqual((),run_scenario('x',mediated=True,consent=False).robust_actions)
    def test_same_triangle_topology_different_result(self):
        self.assertEqual(run_scenario('x',mediated=True).topology,run_scenario('x',mediated=True,consent=False).topology)
        self.assertNotEqual(run_scenario('x',mediated=True).robust_actions,run_scenario('x',mediated=True,consent=False).robust_actions)
    def test_protocol_without_mediator_cannot_create_option(self):
        self.assertEqual((),run_scenario('x',mediated=True,mediator=False).robust_actions)
    def test_existing_baseline_equivalent(self):
        self.assertEqual(16,exhaustive_equivalence())
    def test_no_mysterious_discovery(self):
        self.assertNotIn('mediated',run_scenario('x',mediator=True).candidate_actions)
    def test_observation_and_consent_are_distinct(self):
        self.assertEqual(('left',),run_scenario('x',signal=True,mediated=True,consent=False).robust_actions)
        self.assertEqual(('left','mediated'),run_scenario('x',signal=True,mediated=True,consent=True).robust_actions)
if __name__=='__main__':unittest.main()
