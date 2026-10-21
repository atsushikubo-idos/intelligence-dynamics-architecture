import unittest
from idos_reference_bridge_v0_3 import bridge_case, bridge_domains
from idos_ver84_application_v0_2 import MA_DEMO, HIRING_DEMO

class BridgeTests(unittest.TestCase):
    def test_two_domains(self):
        result = bridge_domains([MA_DEMO, HIRING_DEMO]); self.assertEqual(len(result['cases']), 2)
    def test_no_automatic_residual(self):
        self.assertEqual(bridge_case(MA_DEMO)['reference_description']['unresolved_residuals'], 0)
    def test_no_automatic_holding(self):
        self.assertEqual(bridge_case(HIRING_DEMO)['reference_description']['active_holdings'], 0)
    def test_no_fake_reopening(self):
        self.assertEqual(bridge_case(MA_DEMO)['reference_description']['reopening_count'], 0)
    def test_restricted_absent(self):
        self.assertNotIn('Sensitive private note', str(bridge_case(MA_DEMO)))
        self.assertNotIn('Do not disclose', str(bridge_case(HIRING_DEMO)))
    def test_observation_provenance(self):
        self.assertTrue(any(e['event_type']=='reality_contact' for e in bridge_case(MA_DEMO)['provenance']))
if __name__ == '__main__': unittest.main()
