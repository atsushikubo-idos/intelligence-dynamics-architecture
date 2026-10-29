import unittest
from relational_value_delta import Case, RegisteredComparison, DecisionEffect, evaluate

REG = RegisteredComparison(('model_a','model_b'),'composition','shared_eval_v1')

def cases():
    return [Case(str(i), float(i), {'model_a':float(i)+2,'model_b':float(i)-3,'composition':float(i)+0.5},
                 'before' if i<3 else 'after', 'relation_trace_01',f'evidence_{i}') for i in range(6)]

class DeltaTests(unittest.TestCase):
    def test_positive_delta(self):
        r=evaluate(REG,cases(),losses=('participant-specific meaning may be hidden',))
        self.assertEqual(r.status,'incremental_gain_observed_on_cases')
        self.assertAlmostEqual(r.gain,1.5)
        self.assertEqual(r.before_gain,r.after_gain)
        self.assertIn('semantic_novelty_not_established',r.unresolved)
    def test_no_gain(self):
        cs=[Case(c.case_id,c.truth,{**c.predictions,'composition':c.truth+4},c.relation_phase,c.relation_ref,c.evidence_ref) for c in cases()]
        self.assertEqual(evaluate(REG,cs).status,'not_established')
    def test_missing_predictions(self):
        c=cases()[0]
        with self.assertRaises(ValueError):
            evaluate(REG,[Case(c.case_id,c.truth,{'model_a':1},c.relation_phase,c.relation_ref,c.evidence_ref)])
    def test_duplicate_case(self):
        with self.assertRaises(ValueError): evaluate(REG,[cases()[0],cases()[0]])
    def test_small_sample(self):
        self.assertEqual(evaluate(REG,cases()[:2]).status,'not_established')
    def test_decision_evidence(self):
        ds=[DecisionEffect(c.case_id,1.,2.,'decision_'+c.case_id) for c in cases()]
        r=evaluate(REG,cases(),decisions=ds,decision_evidence='simulation')
        self.assertEqual(r.decision_delta,1)
        self.assertIn('decision_effect_only_simulated',r.unresolved)
    def test_missing_phase(self):
        cs=[Case(c.case_id,c.truth,c.predictions,'after',c.relation_ref,c.evidence_ref) for c in cases()]
        self.assertIn('missing_before_or_after_relation_phase',evaluate(REG,cs).unresolved)
    def test_no_cases(self):
        self.assertEqual(evaluate(REG,[]).status,'insufficient_evidence')

if __name__=='__main__':unittest.main()
