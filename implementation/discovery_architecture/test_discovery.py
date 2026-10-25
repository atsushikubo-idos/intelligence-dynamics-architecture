import unittest
from discovery_architecture import DiscoveryCycle, EvidenceStatus, ReviewStatus

class Tests(unittest.TestCase):
    def setUp(self):
        self.c = DiscoveryCycle("q", "relation", "frame")

    def test_trace_and_nonautomatic_adoption(self):
        i = self.c.intervene("operation", evidence_ids=("log",), performed=True)
        d = self.c.difference("new distinction", after=i, evidence_ids=("obs",), status=EvidenceStatus.OBSERVED)
        f = self.c.propose_frame("candidate", "proposal only", based_on=d)
        self.assertEqual([x.kind for x in self.c.trace(f.id)], ["performed_intervention", "difference", "frame_proposal"])
        self.assertEqual(self.c.reviews, {})
        self.assertEqual(self.c.baseline_frame_id, "frame")

    def test_no_unsupported_observation(self):
        i = self.c.intervene("operation", evidence_ids=("log",), performed=True)
        with self.assertRaises(ValueError):
            self.c.difference("observed", after=i, status=EvidenceStatus.OBSERVED)

    def test_planned_not_performed(self):
        i = self.c.intervene("plan")
        with self.assertRaises(ValueError):
            self.c.difference("difference", after=i)
        with self.assertRaises(ValueError):
            self.c.intervene("performed", performed=True)

    def test_review_is_judgment_not_auto_adoption(self):
        i = self.c.intervene("operation", evidence_ids=("log",), performed=True)
        d = self.c.difference("difference", after=i)
        f = self.c.propose_frame("candidate", "idea", based_on=d)
        with self.assertRaises(ValueError):
            self.c.recontact(f, "review", evidence_ids=(), judgment=ReviewStatus.SUPPORTED)
        r = self.c.recontact(f, "inconclusive", evidence_ids=("review",), judgment=ReviewStatus.INSUFFICIENT)
        self.assertEqual(self.c.reviews[f.id], ReviewStatus.INSUFFICIENT)
        self.assertEqual(self.c.revise_conditions("next attempt", based_on=r).kind, "discovery_conditions_revision")
        self.assertEqual(self.c.baseline_frame_id, "frame")

if __name__ == "__main__": unittest.main()
