import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from idos_reference_v1_2 import make_unit, CommonDynamicsProtocol, SocialConnectionRegistry, FrameGenesisStatus
from idos_bridge import IDOSDiscoveryBridge
from discovery_architecture import EvidenceStatus
from transition_bridge import TransitionBridge
from reference_transition import Decision

class TransitionIntegration(unittest.TestCase):
    def setUp(self):
        self.a=make_unit('AI','agent','initial');self.b=make_unit('Observer','organization','observer')
        r=SocialConnectionRegistry();r.register_unit(self.a);r.register_unit(self.b)
        c=CommonDynamicsProtocol().coordinate(self.a,self.b,'evaluation');r.register_coupling(c)
        self.rel=r.enact_relation_trace(c.id,(self.a.id,self.b.id))
        self.bridge=IDOSDiscoveryBridge(r,c.id,self.a.frame.id,'What distinction is missing?')
        i=self.bridge.intervene('Independent audit',performed=True,evidence_ids=('audit-1',))
        d=self.bridge.difference('Unexpected relation structure',after=i,evidence_ids=('trace-1',),observer='auditor',status=EvidenceStatus.OBSERVED)
        self.proposal,self.genesis=self.bridge.propose_frame('relation-aware','Observed relation contrast',based_on=d,observer='auditor')
        self.adapter=TransitionBridge(self.bridge)
        self.kw=dict(old_distinctions=frozenset({'direct','legacy'}),new_distinctions=frozenset({'direct','relation'}),old_evidence=frozenset({'old'}),new_evidence=frozenset({'new'}),independent_evidence=frozenset({'third'}))
    def test_lost_distinction_held_and_recorded(self):
        n=len(self.rel.trajectory.provenance)
        r=self.adapter.evaluate(self.genesis.id,**self.kw,authorization_id='approval')
        self.assertEqual(r.decision,Decision.HOLD)
        self.assertEqual(r.lost,frozenset({'legacy'}))
        self.assertEqual(len(self.rel.trajectory.provenance),n+1)
    def test_ready_and_no_adoption(self):
        kw={**self.kw,'new_distinctions':frozenset({'direct','legacy','relation'})}
        r=self.adapter.evaluate(self.genesis.id,**kw)
        self.assertEqual(r.decision,Decision.READY)
        self.assertEqual(self.genesis.status,FrameGenesisStatus.PROPOSED)
        self.assertEqual(self.a.frame.id,self.bridge.baseline_frame_id)
    def test_authorization_is_only_asserted(self):
        kw={**self.kw,'new_distinctions':frozenset({'direct','legacy','relation'})}
        r=self.adapter.evaluate(self.genesis.id,**kw,authorization_id='approval')
        self.assertEqual(r.decision,Decision.AUTHORIZED)
        self.assertEqual(self.genesis.status,FrameGenesisStatus.PROPOSED)
    def test_missing_evidence_held(self):
        kw={**self.kw,'new_distinctions':frozenset({'direct','legacy','relation'}),'independent_evidence':frozenset()}
        self.assertEqual(self.adapter.evaluate(self.genesis.id,**kw).decision,Decision.HOLD)
    def test_unresolved_held(self):
        kw={**self.kw,'new_distinctions':frozenset({'direct','legacy','relation'})}
        self.assertEqual(self.adapter.evaluate(self.genesis.id,**kw,unresolved=frozenset({'unexplained'})).decision,Decision.HOLD)
    def test_unknown_genesis_rejected(self):
        with self.assertRaises(ValueError):self.adapter.evaluate('missing',**self.kw)
    def test_original_frames_unchanged(self):
        before=dict(self.bridge.registry.frames)
        self.adapter.evaluate(self.genesis.id,**self.kw)
        self.assertEqual(before,self.bridge.registry.frames)
if __name__=='__main__':unittest.main()
