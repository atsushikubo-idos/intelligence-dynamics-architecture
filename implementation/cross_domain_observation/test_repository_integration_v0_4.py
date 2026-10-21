import unittest
from idos_reference_bridge_v0_3 import bridge_case
from idos_ver84_application_v0_2 import MA_DEMO, HIRING_DEMO

class RepositoryIntegrationTests(unittest.TestCase):
    def test_both_cases_preserve_original_report(self):
        for case in (MA_DEMO, HIRING_DEMO):
            result = bridge_case(case)
            self.assertEqual(result['case_id'], case['case_id'])
            self.assertTrue(result['source_report']['recorded_revisions'])
    def test_restricted_records_not_in_bridge(self):
        for case in (MA_DEMO, HIRING_DEMO):
            report = bridge_case(case)
            self.assertEqual(report['source_report']['privacy']['restricted_count'], 1)
            self.assertTrue(all(e['visibility'] != 'restricted' for e in report['source_report']['timeline']))
    def test_no_inferred_reference_updates(self):
        for case in (MA_DEMO, HIRING_DEMO):
            report = bridge_case(case)
            self.assertEqual(report['reference_description']['phase'], 'birth')

if __name__ == '__main__': unittest.main()
