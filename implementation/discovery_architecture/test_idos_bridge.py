import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from idos_reference_v1_2 import (make_unit, CommonDynamicsProtocol, SocialConnectionRegistry, FrameGenesisStatus)
from idos_bridge import IDOSDiscoveryBridge
from discovery_architecture import EvidenceStatus, ReviewStatus

class Integration(unittest.TestCase):
    def setUp(self):
        self.a=make_unit('A','organization','frame A');self.b=make_unit('B','organization','frame B')
        self.r=SocialConnectionRegistry()
        self.r.register_unit(self.a);self.r.register_unit(self.b)
        self.c=CommonDynamicsProtocol().coordinate(self.a,self.b,'collaboration')
        self.r.register_coupling(self.c)
        self.rel=self.r.enact_relation_trace(self.c.id,(self.a.id,self.b.id))
        self.bridge=IDOSDiscoveryBridge(self.r,self.c.id,self.a.frame.id,'Can a new distinction emerge?')
    def test_end_to_end(self):
        i=self.bridge.intervene('Change review order',performed=True,evidence_ids=('log1',))
        d=self.bridge.difference('Unexpected joint criterion',after=i,evidence_ids=('log2',),observer='reviewer',status=EvidenceStatus.OBSERVED)
        p,g=self.bridge.propose_frame('joint-criterion', 'Cannot capture with original categories',based_on=d,observer='reviewer')
        v=self.bridge.recontact(p,'Not independently reproduced',evidence_ids=('log3',),observer='auditor',judgment=ReviewStatus.INSUFFICIENT)
        self.bridge.revise_conditions('Change sampling', based_on=v)
        self.assertEqual(g.status,FrameGenesisStatus.PROPOSED)
        self.assertEqual(self.a.frame.id,self.bridge.baseline_frame_id)
        self.assertEqual(len(self.rel.changes),1)
        self.assertEqual(len(self.bridge.graph.nodes),1)
        self.assertEqual(self.bridge.cycle.reviews[p.id],ReviewStatus.INSUFFICIENT)
        self.assertGreaterEqual(len(self.rel.trajectory.provenance),4)
    def test_missing_ids_rejected(self):
        with self.assertRaises(ValueError): IDOSDiscoveryBridge(self.r,'fake',self.a.frame.id,'q')
        with self.assertRaises(ValueError): IDOSDiscoveryBridge(self.r,self.c.id,'fake','q')
    def test_plan_not_mistaken_for_performance(self):
        i=self.bridge.intervene('plan')
        with self.assertRaises(ValueError): self.bridge.difference('x',after=i,evidence_ids=('e',),observer='o')
    def test_proposal_cannot_skip_difference(self):
        i=self.bridge.intervene('change',performed=True,evidence_ids=('e',))
        with self.assertRaises(ValueError): self.bridge.propose_frame('f','reason',based_on=i,observer='o')
if __name__=='__main__': unittest.main()
