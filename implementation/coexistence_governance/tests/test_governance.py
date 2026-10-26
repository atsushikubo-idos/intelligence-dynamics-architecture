import unittest
from governance import *

class TestGovernance(unittest.TestCase):
    def setUp(self):
        self.g = CoexistenceGovernor([Actor('h','human','rights'),Actor('a','ai','speed'),Actor('o','organization','governance')])
        self.p = Proposal('p','a',('h','o'),'collaboration','change workflow',True,'low')
    def test_requires_approval(self):
        self.assertEqual(self.g.assess(self.p).decision,Decision.REVIEW)
    def test_allows_with_approval(self):
        self.assertEqual(self.g.assess(self.p,approvals=('h','o')).decision,Decision.ALLOW)
    def test_objection_blocks(self):
        self.g.object('p','h','no')
        self.assertEqual(self.g.assess(self.p,approvals=('h','o')).decision,Decision.BLOCK)
    def test_unknown_risk_requires_review(self):
        p = Proposal('p2','a',('h',),'x','y',True,'unknown')
        self.assertEqual(self.g.assess(p,approvals=('h',)).decision,Decision.REVIEW)
    def test_pause_and_reopen(self):
        self.g.emergency_pause('h','incident')
        self.assertEqual(self.g.assess(self.p).decision,Decision.PAUSE)
        with self.assertRaises(PermissionError): self.g.reopen('a',('ref',))
        self.g.reopen('h',('ref',))
        self.assertEqual(self.g.assess(self.p,approvals=('h','o')).decision,Decision.ALLOW)
    def test_irreversibility(self):
        p = Proposal('p2','a',('h',),'x','y',False,'low')
        self.assertEqual(self.g.assess(p,approvals=('h',)).decision,Decision.REVIEW)
    def test_recontact(self):
        self.g.assess(self.p,approvals=('h','o'))
        self.assertEqual(self.g.recontact(Recontact('p',('obs',),('better planning',),('unexpected exclusion',),False)),Decision.REVIEW)
    def test_frames_preserved(self):
        d=self.g.assess(self.p)
        self.assertEqual(d.dissenting_frames['h'],'rights')
        self.assertEqual(d.dissenting_frames['o'],'governance')

if __name__ == '__main__': unittest.main()
