import tempfile
import unittest
from pathlib import Path
from transition_execution import TransitionLedger
from post_transition_reassessment import FrameObservation, reassess, ReassessmentStatus

class ReassessmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ledger = TransitionLedger(Path(self.tmp.name) / 'history.jsonl')
        self.ledger.append({'event':'adopted','old_frame_id':'A','new_frame_id':'B'})

    def obs(self, frame, distinctions, evidence):
        return FrameObservation(frame, frozenset(distinctions), frozenset(evidence), '2026-10-27T00:00:00Z')

    def test_compatible(self):
        r = reassess(self.ledger, self.obs('A', {'x'}, {'a'}), self.obs('B', {'x','y'}, {'b'}))
        self.assertEqual(r.status, ReassessmentStatus.COMPATIBLE)
        self.assertEqual(r.new_only, {'y'})

    def test_old_only_retained_as_regression(self):
        r = reassess(self.ledger, self.obs('A', {'x','legacy'}, {'a'}), self.obs('B', {'x'}, {'b'}), record=True)
        self.assertEqual(r.status, ReassessmentStatus.REGRESSION)
        self.assertEqual(r.old_only, {'legacy'})
        self.assertEqual(self.ledger.read()[-1]['payload']['old_only'], ['legacy'])

    def test_unresolved_holding(self):
        r = reassess(self.ledger, self.obs('A', {'x'}, {'a'}), self.obs('B', {'x'}, {'b'}), unresolved=frozenset({'z'}))
        self.assertEqual(r.status, ReassessmentStatus.HOLDING)

    def test_overlapping_evidence_holding(self):
        r = reassess(self.ledger, self.obs('A', {'x'}, {'same'}), self.obs('B', {'x'}, {'same'}))
        self.assertEqual(r.status, ReassessmentStatus.HOLDING)

    def test_missing_evidence_holding(self):
        r = reassess(self.ledger, self.obs('A', {'x'}, set()), self.obs('B', {'x'}, {'b'}))
        self.assertEqual(r.status, ReassessmentStatus.HOLDING)

    def test_unregistered_transition_rejected(self):
        with self.assertRaises(ValueError):
            reassess(self.ledger, self.obs('A', {'x'}, {'a'}), self.obs('C', {'x'}, {'b'}))

    def test_does_not_modify_adoption(self):
        reassess(self.ledger, self.obs('A', {'x'}, {'a'}), self.obs('B', {'x'}, {'b'}), record=True)
        self.assertEqual(self.ledger.read()[0]['payload']['event'], 'adopted')

    def test_tampered_ledger_rejected(self):
        self.ledger.path.write_text(self.ledger.path.read_text().replace('adopted','tampered'))
        with self.assertRaises(ValueError):
            reassess(self.ledger, self.obs('A', {'x'}, {'a'}), self.obs('B', {'x'}, {'b'}))

if __name__ == '__main__':
    unittest.main()
