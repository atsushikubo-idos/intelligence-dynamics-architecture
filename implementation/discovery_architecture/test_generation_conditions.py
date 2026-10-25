import unittest
from discovery_architecture import DiscoveryCycle, EvidenceStatus, ReviewStatus
from generation_conditions import (DiscoveryConditions, GenerationConditionChange,
    ConditionAxis, ConditionState, ConditionApplication)

class TestSecondOrder(unittest.TestCase):
    def setUp(self):
        self.c=DiscoveryCycle('q','relation-id','frame-id')
        performed=self.c.intervene('change relation',performed=True,evidence_ids=('e1',))
        self.d=self.c.difference('unfamiliar distinction',after=performed,evidence_ids=('e2',),status=EvidenceStatus.OBSERVED)
        self.s=DiscoveryConditions(self.c)
        self.change=GenerationConditionChange(ConditionAxis.OBSERVATIONAL_UNIT,'individual','joint process',
            'relations may be unobserved','new interaction pattern',('individual voices',),'unchanged unit',('approval-1',))
    def test_applied_record_is_traceable(self):
        self.s.propose(self.change,based_on=self.d)
        rec=self.s.apply(ConditionApplication(self.change.id,ConditionState.APPLIED,('log',),('approval-1',)),based_on=self.d)
        self.assertEqual(rec.kind,'discovery_conditions_revision')
        self.assertEqual([r.kind for r in self.c.trace(rec.id)],['performed_intervention','difference','discovery_conditions_revision'])
    def test_proposal_is_not_application(self):
        self.s.propose(self.change,based_on=self.d)
        self.assertIsNone(self.s.apply(ConditionApplication(self.change.id,ConditionState.PROPOSED),based_on=self.d))
        self.assertFalse(self.s.records)
    def test_evidence_and_authorization_required(self):
        self.s.propose(self.change,based_on=self.d)
        with self.assertRaises(ValueError):
            ConditionApplication(self.change.id,ConditionState.APPLIED,(),('approval-1',))
        with self.assertRaises(ValueError):
            self.s.apply(ConditionApplication(self.change.id,ConditionState.APPLIED,('log',),('wrong',)),based_on=self.d)
    def test_unrelated_source_rejected(self):
        other=DiscoveryCycle('q','r','f').intervene('plan')
        with self.assertRaises(ValueError):self.s.propose(self.change,based_on=other)
    def test_does_not_adopt_candidate_frame(self):
        self.s.propose(self.change,based_on=self.d)
        self.s.apply(ConditionApplication(self.change.id,ConditionState.APPLIED,('e3',),('approval-1',)),based_on=self.d)
        self.assertEqual(self.c.candidate_frame_ids,[])
if __name__=='__main__':unittest.main()
