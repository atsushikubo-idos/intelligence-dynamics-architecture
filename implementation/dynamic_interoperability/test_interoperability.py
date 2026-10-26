import unittest
from interoperability import Ledger, Claim, Assessment, Disposition
from idos_bridge import exchange_via_cdp
from idos_reference_v1_2 import make_unit

class TestDifferencePreservation(unittest.TestCase):
    def setUp(self):
        self.h = make_unit('Human','human','Human frame')
        self.a = make_unit('AI','ai','AI frame')
        self.l = Ledger()
        self.c = [Claim('c','Do not erase minority interpretation','human','Human frame')]

    def send(self, assessments=None, **kw):
        return exchange_via_cdp(self.l,self.h,self.a,self.c,'Consolidate answers',
                                assessments or [],round=1,declared_by='reviewer',**kw)

    def test_uses_reference_cdp(self):
        e = self.send()
        self.assertEqual(e.cdp_quality,'partial')
        self.assertEqual(e.source_frame,'Human frame')
        self.assertNotEqual(e.source_trajectory,e.target_trajectory)

    def test_unknown_not_silently_preserved(self):
        e = self.send()
        self.assertEqual(e.assessments[0].disposition,Disposition.UNRESOLVED)

    def test_verified_loss_stays_visible(self):
        self.send([Assessment('c',Disposition.OMITTED,'Absent from translated text','reviewer')])
        self.assertEqual(self.l.open_issues()[0]['state'],'omitted')

    def test_unverified_loss_rejected(self):
        with self.assertRaises(ValueError): self.send([Assessment('c',Disposition.OMITTED)])

    def test_double_assessment_rejected(self):
        with self.assertRaises(ValueError): self.send([Assessment('c',Disposition.CONTESTED), Assessment('c',Disposition.UNRESOLVED)])

    def test_unknown_claim_rejected(self):
        with self.assertRaises(ValueError): self.send([Assessment('x',Disposition.CONTESTED)])

    def test_history_chain(self):
        e = self.send()
        later = self.send(previous_exchange_id=e.id)
        self.assertEqual(later.previous_exchange_id,e.id)

    def test_reverse_direction(self):
        exchange_via_cdp(self.l,self.a,self.h,[Claim('x','Reverse','ai','AI frame')],
                         'Reverse',[],round=1,declared_by='reviewer')
        self.assertEqual(self.l.exchanges[0].source_frame,'AI frame')

    def test_no_proof_of_semantics(self):
        e = self.send([Assessment('c',Disposition.PRESERVED,'Reviewer compared texts','reviewer')])
        self.assertEqual(e.assessments[0].assessor,'reviewer')
        self.assertIn('not assumed equivalent',e.cdp_residual)

if __name__ == '__main__': unittest.main()

from semantic_detection import detect, Candidate
from relation_analysis import analyze, compare_directions

class TestAutomatedCandidates(unittest.TestCase):
    def test_negation(self):
        c = Claim('n','Never remove human override','h','f')
        result = detect([c],'Remove human override')[0]
        self.assertEqual(result.proposed,Disposition.ALTERED)
        self.assertEqual(result.to_assessment().disposition,Disposition.UNRESOLVED)

    def test_numbers(self):
        c = Claim('n','Limit to 30 days','h','f')
        self.assertEqual(detect([c],'Limit to 60 days')[0].proposed,Disposition.ALTERED)

    def test_ai_provider_is_provisional(self):
        c = Claim('n','Allow appeal','h','f')
        result = detect([c],'Allow appeal',lambda a,b:(Disposition.PRESERVED,'Proposed equivalence'))[0]
        self.assertEqual(result.method,'external-ai')
        self.assertEqual(result.to_assessment().disposition,Disposition.UNRESOLVED)

    def test_provider_requires_evidence(self):
        c = Claim('n','Allow appeal','h','f')
        with self.assertRaises(ValueError):
            detect([c],'Allow appeal',lambda a,b:(Disposition.PRESERVED,''))

    def test_trajectory_direction(self):
        h=make_unit('h','human','h-frame'); a=make_unit('a','ai','a-frame'); l=Ledger()
        exchange_via_cdp(l,h,a,[Claim('x','Keep appeal','h','h-frame')],'Keep appeal',
                         [Assessment('x',Disposition.PRESERVED,'Human verified','reviewer')],round=1,declared_by='reviewer')
        exchange_via_cdp(l,a,h,[Claim('y','Keep appeal','a','a-frame')],'Unknown',[],round=2,declared_by='reviewer')
        reports=analyze(l)
        self.assertEqual(len(reports),2)
        self.assertEqual(len(compare_directions(l)),1)
        self.assertEqual(sorted(x.retention_rate for x in reports),[0.,1.])

    def test_unreviewed_not_retained(self):
        h=make_unit('h','human','h-frame'); a=make_unit('a','ai','a-frame'); l=Ledger()
        exchange_via_cdp(l,h,a,[Claim('x','Protect choice','h','h-frame')],'Protect choice',
                         [],round=1,declared_by='unreviewed')
        self.assertEqual(analyze(l)[0].retention_rate,0)
        self.assertEqual(analyze(l)[0].tentative_count,1)
