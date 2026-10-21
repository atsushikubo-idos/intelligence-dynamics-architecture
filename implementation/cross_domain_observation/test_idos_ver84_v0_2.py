import unittest
from copy import deepcopy
from idos_ver84_application_v0_2 import MA_DEMO, HIRING_DEMO, analyze, compare_domains, validate

class AdapterTests(unittest.TestCase):
    def test_cross_domain(self):
        out = compare_domains([MA_DEMO, HIRING_DEMO], as_of='2026-10-21')
        self.assertEqual(len(out['coverage']), 2)
        self.assertEqual({x['domain'] for x in out['coverage']}, {'M&A', 'hiring'})
    def test_restricted_never_emitted(self):
        for c in [MA_DEMO, HIRING_DEMO]:
            self.assertNotIn('Do not disclose', str(analyze(c, as_of='2026-10-21')))
            self.assertNotIn('Sensitive private note', str(analyze(c, as_of='2026-10-21')))
    def test_original_commitment_preserved(self):
        r = analyze(MA_DEMO, as_of='2026-10-21')
        self.assertEqual(r['original_and_revised_commitments'][0]['value'], '2x baseline in three years')
    def test_holding_deadline(self):
        r = analyze(HIRING_DEMO, as_of='2026-10-21')
        self.assertEqual(r['holdings'][0]['review_status'], 'review_due')
    def test_revisions(self):
        r = analyze(MA_DEMO, as_of='2026-10-21')
        self.assertTrue(any(x['topic']=='strategy' for x in r['recorded_revisions']))
    def test_duplicate_ids_rejected(self):
        c = deepcopy(MA_DEMO)
        c['events'][1]['id'] = c['events'][0]['id']
        with self.assertRaises(ValueError):
            validate(c)
    def test_invalid_date_rejected(self):
        c = deepcopy(MA_DEMO)
        c['events'][0]['date'] = 'not-a-date'
        with self.assertRaises(ValueError):
            validate(c)

if __name__ == '__main__':
    unittest.main()
