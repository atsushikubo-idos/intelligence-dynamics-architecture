"""Real-object integration of IDOS discovery -> adoption -> reassessment -> next observation.

Synthetic observations only; no assertion of real-world autonomous discovery.
"""
import tempfile
import unittest
from pathlib import Path
from test_transition_bridge import TransitionIntegration
from idos_reference_v1_2 import ReferenceFrame, FrameGenesisStatus
from generation_conditions import DiscoveryConditions, ConditionApplication, ConditionState
from transition_execution import ControlledTransition, TransitionLedger
from post_transition_reassessment import FrameObservation, reassess, ReassessmentStatus
from transition_feedback_loop import propose_followup
from reference_transition import Decision


class FullTransitionCycleTests(TransitionIntegration):
    def setUp(self):
        super().setUp()
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.ledger = TransitionLedger(Path(temp.name) / 'transition.jsonl')
        self.execution = ControlledTransition(self.adapter, self.ledger)
        self.conditions = DiscoveryConditions(self.bridge.cycle)
        self.new_frame = ReferenceFrame('relation-aware',
            categories=['direct', 'legacy', 'relation'], parent_id=self.bridge.baseline_frame_id)

    def adopt(self):
        kw = {**self.kw, 'new_distinctions': frozenset({'direct', 'legacy', 'relation'})}
        review = self.adapter.evaluate(self.genesis.id, **kw, authorization_id='approval-1')
        self.assertEqual(review.decision, Decision.AUTHORIZED)
        self.execution.adopt(self.genesis.id, self.new_frame,
            authorization_id='approval-1', adoption_evidence=('adoption-independent',))

    def test_real_objects_complete_feedback_cycle(self):
        old_id = self.a.frame.id
        self.adopt()
        self.assertEqual(self.genesis.status, FrameGenesisStatus.ADOPTED)
        self.assertEqual(self.a.frame.id, old_id)
        old = FrameObservation(old_id, frozenset({'direct','legacy','unanticipated'}),
                               frozenset({'post-old'}), '2026-10-27T00:00:00Z')
        new = FrameObservation(self.new_frame.id, frozenset({'direct','legacy','relation'}),
                               frozenset({'post-new'}), '2026-10-27T00:00:00Z')
        result = reassess(self.ledger, old, new, record=True)
        self.assertEqual(result.status, ReassessmentStatus.REGRESSION)
        self.assertEqual(result.old_only, frozenset({'unanticipated'}))
        feedback = propose_followup(result, discovery_bridge=self.bridge,
            frame_proposal=self.proposal, conditions=self.conditions,
            external_evidence_ids=('recontact-independent',), observer='auditor-2',
            authorization_refs=('followup-approval',))
        self.assertIn('unanticipated', feedback.candidate.possible_blind_spots)
        self.assertIn(feedback.condition_change_id, self.conditions.proposals)
        self.assertEqual(self.conditions.applications, {})
        rec = next(r for r in self.bridge.cycle.records if r.id == feedback.recontact_record_id)
        self.conditions.apply(ConditionApplication(feedback.condition_change_id, ConditionState.APPLIED,
            evidence_refs=('recontact-independent',), authorization_refs=('followup-approval',)), based_on=rec)
        self.assertIn(feedback.condition_change_id, self.conditions.records)
        self.assertEqual(self.a.frame.id, old_id)
        self.assertEqual(len(self.execution.history()), 2)

    def test_missing_independent_recontact_stops_feedback(self):
        self.adopt()
        old = FrameObservation(self.a.frame.id, frozenset({'legacy'}), frozenset({'post-old'}), 'T1')
        new = FrameObservation(self.new_frame.id, frozenset({'relation'}), frozenset({'post-new'}), 'T2')
        result = reassess(self.ledger, old, new)
        with self.assertRaises(ValueError):
            propose_followup(result, discovery_bridge=self.bridge, frame_proposal=self.proposal,
                conditions=self.conditions, external_evidence_ids=('post-old',), observer='auditor')

    def test_static_frame_comparator_misses_relation_only_in_synthetic_example(self):
        # Fixed-baseline comparator intentionally has no relation category.
        baseline_categories = {'direct', 'legacy'}
        observation = {'direct', 'legacy', 'relation'}
        fixed_visible = observation & baseline_categories
        self.assertNotIn('relation', fixed_visible)
        self.adopt()
        self.assertIn('relation', self.new_frame.categories)
        # Demonstrates representational coverage, NOT autonomous discovery or superiority.


if __name__ == '__main__':
    unittest.main()
