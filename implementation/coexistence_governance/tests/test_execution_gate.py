import unittest
from datetime import datetime, timedelta, timezone
from governance import Actor, Proposal, CoexistenceGovernor
from execution_gate import AIExecutionGate, ExecutionClaim, CollectiveSignal, GateStatus

class GateTests(unittest.TestCase):
    def setUp(self):
        self.gov = CoexistenceGovernor([Actor('a','ai','speed'), Actor('h','human','rights'), Actor('o','organization','policy')])
        self.gate = AIExecutionGate(self.gov)
        self.p = Proposal('p','a',('h','o'),'safe planning','read_report',True,'low')
        self.claim = ExecutionClaim('p','a','read_report','report-1',datetime.now(timezone.utc)+timedelta(minutes=5),True,True,'trusted-external-verifier-1')
    def run_gate(self, claim=None, **kwargs):
        return self.gate.gate(self.p, claim or self.claim, approvals=('h','o'),cdp_ready=True, external_invariants_ok=True, **kwargs)
    def test_good_eligible_not_enforced(self):
        self.assertEqual(self.run_gate().status, GateStatus.ELIGIBLE)
    def test_no_attestation_denied(self):
        claim = ExecutionClaim('p','a','read_report','report-1',self.claim.expires_at_utc)
        self.assertEqual(self.run_gate(claim).status, GateStatus.DENY)
    def test_expired_denied(self):
        claim = ExecutionClaim('p','a','read_report','report-1',datetime.now(timezone.utc)-timedelta(seconds=1),True,True,'verifier')
        self.assertEqual(self.run_gate(claim).status, GateStatus.DENY)
    def test_scope_mismatch_denied(self):
        claim = ExecutionClaim('p','a','delete_database','report-1',self.claim.expires_at_utc,True,True,'verifier')
        self.assertEqual(self.run_gate(claim).status, GateStatus.DENY)
    def test_invariants_denied(self):
        self.assertEqual(self.gate.gate(self.p,self.claim,approvals=('h','o'),cdp_ready=True).status, GateStatus.DENY)
    def test_signal_review(self):
        self.gate.report_collective_signal(CollectiveSignal('p','correlated_failure',('log-1',)))
        self.assertEqual(self.run_gate().status, GateStatus.REVIEW)
    def test_cdp_required(self):
        self.assertEqual(self.gate.gate(self.p,self.claim,approvals=('h','o'),external_invariants_ok=True).status, GateStatus.REVIEW)
    def test_human_objection_denies(self):
        self.gov.object('p','h','no')
        self.assertEqual(self.run_gate().status, GateStatus.DENY)
    def test_lock_and_two_reviewers(self):
        self.gate.lock_for_incident('suspected compromise')
        self.assertEqual(self.run_gate().status, GateStatus.PAUSED)
        with self.assertRaises(PermissionError): self.gate.release_lock(reviewers=('h',),evidence_refs=('incident',))
        self.gate.release_lock(reviewers=('h','o'),evidence_refs=('incident',))
        self.assertEqual(self.run_gate().status, GateStatus.ELIGIBLE)
    def test_revision_is_request_only(self):
        self.gate.propose_policy_revision(reason='new risk',reviewers=('h','o'),evidence_refs=('audit',))
        self.assertEqual(self.gate.policy_version,1)
        self.assertEqual(self.gate.policy_history[-1]['status'],'review_requested_not_applied')

if __name__ == '__main__': unittest.main()
