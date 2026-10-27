import tempfile
from pathlib import Path
from test_transition_bridge import TransitionIntegration
import unittest
from idos_reference_v1_2 import ReferenceFrame, FrameGenesisStatus
from transition_execution import ControlledTransition, TransitionLedger

class TransitionExecutionTests(unittest.TestCase):
    def setUp(self):
        TransitionIntegration.setUp(self)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.ledger = TransitionLedger(Path(self.temp.name) / 'history.jsonl')
        self.execution = ControlledTransition(self.adapter, self.ledger)
        self.kw['new_distinctions'] = frozenset({'direct', 'legacy', 'relation'})
        self.frame = ReferenceFrame('relation-aware', categories=['direct','legacy','relation'], parent_id=self.bridge.baseline_frame_id)
    def authorized(self):
        self.adapter.evaluate(self.genesis.id, **self.kw, authorization_id='approval-1')
    def test_adoption_preserves_old_and_active_frames(self):
        baseline = self.a.frame.id
        self.authorized()
        p = self.execution.adopt(self.genesis.id, self.frame, authorization_id='approval-1', adoption_evidence=('independent-2',))
        self.assertEqual(p['old_frame_id'], baseline)
        self.assertEqual(self.a.frame.id, baseline)
        self.assertIn(self.frame.id, self.bridge.registry.frames)
        self.assertEqual(self.genesis.status, FrameGenesisStatus.ADOPTED)
        self.assertEqual(self.execution.history()[0]['new_frame']['categories'], ['direct','legacy','relation'])
    def test_reject_without_authorization(self):
        self.adapter.evaluate(self.genesis.id, **self.kw)
        with self.assertRaises(ValueError):
            self.execution.adopt(self.genesis.id, self.frame, authorization_id='approval-1', adoption_evidence=('e',))
    def test_reject_after_loss(self):
        self.kw['new_distinctions'] = frozenset({'direct','relation'})
        self.adapter.evaluate(self.genesis.id, **self.kw, authorization_id='approval-1')
        with self.assertRaises(ValueError):
            self.execution.adopt(self.genesis.id, self.frame, authorization_id='approval-1', adoption_evidence=('e',))
    def test_reject_frame_missing_reviewed_distinction(self):
        self.authorized()
        bad = ReferenceFrame('bad', categories=['direct'], parent_id=self.bridge.baseline_frame_id)
        with self.assertRaises(ValueError):
            self.execution.adopt(self.genesis.id, bad, authorization_id='approval-1', adoption_evidence=('e',))
    def test_reject_repeated_adoption(self):
        self.authorized()
        self.execution.adopt(self.genesis.id, self.frame, authorization_id='approval-1', adoption_evidence=('e',))
        with self.assertRaises(ValueError):
            self.execution.adopt(self.genesis.id, self.frame, authorization_id='approval-1', adoption_evidence=('e',))
    def test_ledger_tamper_detection(self):
        self.authorized()
        self.execution.adopt(self.genesis.id, self.frame, authorization_id='approval-1', adoption_evidence=('e',))
        raw = self.ledger.path.read_text()
        self.ledger.path.write_text(raw.replace('relation-aware', 'tampered'))
        with self.assertRaises(ValueError):
            self.execution.history()
    def test_no_adoption_without_evidence(self):
        self.authorized()
        with self.assertRaises(ValueError):
            self.execution.adopt(self.genesis.id, self.frame, authorization_id='approval-1', adoption_evidence=())
