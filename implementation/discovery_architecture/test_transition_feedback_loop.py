import unittest
from unittest.mock import Mock
from discovery_architecture import DiscoveryCycle, ReviewStatus
from generation_conditions import DiscoveryConditions, ConditionApplication, ConditionState
from post_transition_reassessment import Reassessment, ReassessmentStatus
from transition_feedback_loop import propose_followup


class FeedbackLoopTests(unittest.TestCase):
    def setUp(self):
        self.cycle = DiscoveryCycle('follow up', 'relation', 'A')
        intervention = self.cycle.intervene('probe', performed=True, evidence_ids=('probe1',))
        diff = self.cycle.difference('difference', after=intervention, evidence_ids=('d1',))
        self.proposal = self.cycle.propose_frame('genesis1', 'test', based_on=diff)
        self.bridge = Mock()
        self.bridge.cycle = self.cycle
        self.bridge._geneses = {self.proposal.id: object()}
        self.bridge.baseline_frame_id = 'A'
        self.bridge.registry.frames = {'A': object(), 'B': object()}
        self.bridge.recontact.side_effect = lambda p, finding, evidence_ids, observer, judgment: self.cycle.recontact(p, finding, evidence_ids=evidence_ids, judgment=judgment)
        self.conditions = DiscoveryConditions(self.cycle)
        self.result = Reassessment('A','B','digest',ReassessmentStatus.REGRESSION,
                                   frozenset({'shared'}),frozenset({'legacy'}),frozenset({'new'}),
                                   frozenset(),frozenset({'old','new'}))

    def run_feedback(self, **kwargs):
        args = dict(discovery_bridge=self.bridge, frame_proposal=self.proposal,
                    conditions=self.conditions, external_evidence_ids=('fresh',), observer='observer')
        args.update(kwargs)
        return propose_followup(self.result, **args)

    def test_regression_proposes_without_applying(self):
        out = self.run_feedback()
        self.assertIn('legacy', out.candidate.possible_blind_spots)
        self.assertIn(out.condition_change_id, self.conditions.proposals)
        self.assertEqual(self.conditions.applications, {})
        self.assertEqual(self.cycle.reviews[self.proposal.id], ReviewStatus.INSUFFICIENT)

    def test_holding_keeps_unresolved(self):
        self.result = Reassessment('A','B','d',ReassessmentStatus.HOLDING,
            frozenset(),frozenset(),frozenset(),frozenset({'unknown'}),frozenset({'old'}))
        self.assertIn('unknown', self.run_feedback().candidate.possible_blind_spots)

    def test_compatible_still_provisional(self):
        self.result = Reassessment('A','B','d',ReassessmentStatus.COMPATIBLE,
            frozenset({'shared'}),frozenset(),frozenset({'novel'}),frozenset(),frozenset({'old'}))
        self.assertEqual(self.run_feedback().candidate.possible_blind_spots, ('novel',))

    def test_reused_evidence_rejected(self):
        with self.assertRaises(ValueError): self.run_feedback(external_evidence_ids=('old',))

    def test_unrelated_proposal_rejected(self):
        with self.assertRaises(ValueError): self.run_feedback(frame_proposal=Mock(id='other'))

    def test_unregistered_new_frame_rejected(self):
        self.bridge.registry.frames = {'A': object()}
        with self.assertRaises(ValueError): self.run_feedback()

    def test_mismatched_conditions_rejected(self):
        other = DiscoveryConditions(DiscoveryCycle('other','rel','A'))
        with self.assertRaises(ValueError): self.run_feedback(conditions=other)

    def test_explicit_authorization_still_required_for_application(self):
        out = self.run_feedback(authorization_refs=('approval',))
        rec = next(r for r in self.cycle.records if r.id == out.recontact_record_id)
        with self.assertRaises(ValueError):
            self.conditions.apply(ConditionApplication(out.condition_change_id, ConditionState.APPLIED,
                evidence_refs=('fresh',), authorization_refs=('wrong',)), based_on=rec)
        self.assertNotIn(out.condition_change_id, self.conditions.applications)
        self.conditions.apply(ConditionApplication(out.condition_change_id, ConditionState.APPLIED,
            evidence_refs=('fresh',), authorization_refs=('approval',)), based_on=rec)
        self.assertIn(out.condition_change_id, self.conditions.records)

if __name__ == '__main__': unittest.main()
