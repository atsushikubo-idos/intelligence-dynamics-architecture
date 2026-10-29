import unittest
from discovery_adapter import (provenance_from_events, evaluate_discovery_delta,
                               EvaluatedObservation)
from relational_value_delta import RegisteredComparison

class TestDiscoveryAdapter(unittest.TestCase):
    def setUp(self):
        self.events = [{'record_hash':f'h{i}', 'cycle':i,'frame_before':'F0',
                        'frame_after':'F1','generated_expression':'output / capacity',
                        'review_status':'authorized','source_type':'unverified_generator'}
                       for i in range(6)]
        self.comparison = RegisteredComparison(('A','B'),'AB','original_frame',min_cases=4)

    def test_linked_paired_evidence(self):
        prov = provenance_from_events(self.events,relation_ref='relation:r1',evidence_ref='log:1')
        obs = [EvaluatedObservation(str(i),float(i),
                {'A':float(i)+2,'B':float(i)+3,'AB':float(i)+.5},
                'after' if i>2 else 'before',f'h{i}',f'observed:{i}') for i in range(6)]
        report = evaluate_discovery_delta(self.comparison,prov,obs,losses=('old-frame:unknown',))
        self.assertEqual(report.status,'incremental_gain_observed_on_cases')
        self.assertAlmostEqual(report.gain,1.5)
        self.assertIn('discovery_candidate_not_proof_of_new_value',report.unresolved)
        self.assertIn('old-frame:unknown',report.old_frame_losses)

    def test_reject_unlinked_observation(self):
        prov = provenance_from_events(self.events,relation_ref='r',evidence_ref='e')
        obs = [EvaluatedObservation('x',1,{'A':1,'B':1,'AB':1},'after','missing','e')]
        with self.assertRaises(ValueError):evaluate_discovery_delta(self.comparison,prov,obs)

    def test_reject_unapproved(self):
        self.events[0]['review_status']='rejected'
        prov = provenance_from_events(self.events,relation_ref='r',evidence_ref='e')
        obs = [EvaluatedObservation('x',1,{'A':1,'B':1,'AB':1},'after','h0','e')]
        with self.assertRaises(ValueError):evaluate_discovery_delta(self.comparison,prov,obs)

    def test_reject_duplicate_hash(self):
        self.events[1]['record_hash']='h0'
        with self.assertRaises(ValueError):provenance_from_events(self.events,relation_ref='r',evidence_ref='e')

    def test_reject_missing_relation(self):
        with self.assertRaises(ValueError):provenance_from_events(self.events,relation_ref='',evidence_ref='e')

if __name__=='__main__':unittest.main()
