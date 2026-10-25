import unittest
from discovery_architecture import DiscoveryCycle, EvidenceStatus
from intervention_design import (InterventionAxis, RelationInterventionSpec,
    ExecutionReceipt, ExecutionState, Interpretation, InterventionStudy)

class InterventionDesignTests(unittest.TestCase):
    def setUp(self):
        self.cycle = DiscoveryCycle('unobserved relationship shift', 'rel-1','frame-1')
        self.study = InterventionStudy(self.cycle)
        self.spec = RelationInterventionSpec(InterventionAxis.ROLES_AUTHORITY,
            'rel-1','frame-1','manager decides','both teams can veto',
            'surface previously unspoken concerns','emergent objection categories',
            'compare with unchanged authority',('decision delay',),
            ('no personal data',),('approval-1',),True)

    def test_full_path(self):
        self.study.design(self.spec)
        self.study.record_execution(ExecutionReceipt(self.spec.id,ExecutionState.PERFORMED,('log-1',),('approval-1',)))
        d=self.study.observe(self.spec.id,'new disagreement categories',('log-2',),EvidenceStatus.OBSERVED)
        self.study.interpret(Interpretation(d.id,'hierarchy categories','mutual veto taxonomy',
                                            'speed of decisions',('novelty due to task wording',)))
        p=self.study.propose_from(d,'candidate-1','evaluate mutual veto as separate dimension')
        self.assertEqual(p.kind,'frame_proposal')

    def test_no_authorization(self):
        self.study.design(self.spec)
        with self.assertRaises(ValueError):
            self.study.record_execution(ExecutionReceipt(self.spec.id,ExecutionState.PERFORMED,('log-1',),('wrong',)))

    def test_cannot_observe_plan_only(self):
        self.study.design(self.spec)
        with self.assertRaises(ValueError):
            self.study.observe(self.spec.id,'result',('log-2',))

    def test_no_new_frame_without_interpretation(self):
        self.study.design(self.spec)
        self.study.record_execution(ExecutionReceipt(self.spec.id,ExecutionState.PERFORMED,('log-1',),('approval-1',)))
        d=self.study.observe(self.spec.id,'difference',('log-2',))
        with self.assertRaises(ValueError):
            self.study.propose_from(d,'frame-x','not grounded')

    def test_no_op_invalid(self):
        with self.assertRaises(ValueError):
            RelationInterventionSpec(InterventionAxis.PARTNERS,'r','f','same','same','intent','obs','control')

    def test_wrong_relation_rejected(self):
        bad=RelationInterventionSpec(InterventionAxis.INFORMATION,'other','frame-1','private','shared','i','o','control')
        with self.assertRaises(ValueError):self.study.design(bad)

if __name__=='__main__': unittest.main()
