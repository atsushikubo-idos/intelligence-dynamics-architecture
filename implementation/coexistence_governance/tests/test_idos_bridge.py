import unittest
from governance import Actor, Proposal, CoexistenceGovernor, Decision
from idos_bridge import assess_with_cdp
from idos_reference_v1_2 import make_unit

class TestBridge(unittest.TestCase):
    def setUp(self):
        self.gov = CoexistenceGovernor([Actor('person','human','consent'), Actor('ai','ai','speed')])
        self.proposal = Proposal('p','ai',('person',),'shared work','suggest',True,'low')
    def test_missing_mapping_requires_review(self):
        result, evidence = assess_with_cdp(self.gov, self.proposal, {}, approvals=('person',))
        self.assertEqual(result.decision, Decision.REVIEW)
        self.assertIsNone(evidence)
    def test_distinct_frames_preserved(self):
        units = {'person':make_unit('Human','human','Dignity'), 'ai':make_unit('AI','ai','Optimization')}
        result, evidence = assess_with_cdp(self.gov, self.proposal, units, approvals=('person',))
        self.assertEqual(result.decision, Decision.ALLOW)
        self.assertEqual(evidence.frames, ('Optimization', 'Dignity'))
        self.assertEqual(len(evidence.translation_residuals), 2)
    def test_objection_is_not_bypassed(self):
        units = {'person':make_unit('Human','human','Dignity'), 'ai':make_unit('AI','ai','Optimization')}
        self.gov.object('p','person','object')
        result, evidence = assess_with_cdp(self.gov, self.proposal, units, approvals=('person',))
        self.assertEqual(result.decision, Decision.BLOCK)
        self.assertIsNotNone(evidence)

if __name__ == '__main__': unittest.main()
