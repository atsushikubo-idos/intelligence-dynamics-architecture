import unittest
from copy import deepcopy
from idos_ver84_application_v0_2 import analyze, validate
from idos_reference_bridge_v0_3 import bridge_case
from synthetic_clinical_v0_5 import CLINICAL_DEMO
from three_domain_experiment_v0_5 import compare, plain_event_log

class ThreeDomainTests(unittest.TestCase):
    def test_clinical_validates(self):
        self.assertTrue(validate(CLINICAL_DEMO))
    def test_three_domains(self):
        result=compare()
        self.assertEqual({x['domain'] for x in result['comparison']},{'M&A','hiring','clinical'})
    def test_restricted_not_in_report(self):
        result=compare()
        self.assertNotIn('Sensitive synthetic note',str(result))
    def test_baseline_preserves_visible_events(self):
        raw=plain_event_log(CLINICAL_DEMO)
        structured=analyze(CLINICAL_DEMO,as_of='2026-10-21')
        self.assertEqual(raw['events'],structured['timeline'])
    def test_frame_revision_mapped(self):
        b=bridge_case(CLINICAL_DEMO)
        self.assertTrue(any(p['event_type']=='frame_revision' for p in b['provenance']))
    def test_residual_not_promoted(self):
        b=bridge_case(CLINICAL_DEMO)
        self.assertTrue(any('residual' in s for s in b['unmapped_semantics']))
    def test_clinical_holding_due(self):
        report=analyze(CLINICAL_DEMO,as_of='2026-10-21')
        self.assertEqual(report['holdings'][0]['review_status'],'review_due')
    def test_duplicate_clinical_ids_rejected(self):
        c=deepcopy(CLINICAL_DEMO)
        c['events'][1]['id']=c['events'][0]['id']
        with self.assertRaises(ValueError): validate(c)

if __name__=='__main__': unittest.main()
