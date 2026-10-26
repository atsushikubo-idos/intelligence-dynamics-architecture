from datetime import datetime, timedelta, timezone
from governance import Actor, CoexistenceGovernor, Proposal
from execution_gate import AIExecutionGate, ExecutionClaim

actors = [Actor('assistant','ai','efficiency'),Actor('operator','human','safety'),Actor('owner','organization','accountability')]
base = CoexistenceGovernor(actors)
gate = AIExecutionGate(base)
p = Proposal('review-1','assistant',('operator','owner'),'reporting','read_report',True,'low')
claim = ExecutionClaim('review-1','assistant','read_report','report-1',datetime.now(timezone.utc)+timedelta(minutes=2),True,True,'external-verifier-demo')
print(gate.gate(p,claim,approvals=('operator','owner'),cdp_ready=True,external_invariants_ok=True))
print('DEMO ONLY: evidence flags are provided, not authenticated by this program.')
