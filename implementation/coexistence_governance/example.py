from governance import Actor, Proposal, CoexistenceGovernor, Recontact

actors = [
    Actor('human-1', 'human', 'human dignity, consent, local knowledge'),
    Actor('ai-1', 'ai', 'prediction and search efficiency'),
    Actor('org-1', 'organization', 'institutional accountability'),
]
gov = CoexistenceGovernor(actors)
p = Proposal('p1','ai-1',('human-1','org-1'), 'improve shared planning',
             'AI proposes changing the shared decision workflow', True, 'low',
             evidence_refs=('experiment-plan-001',))
print('Without approvals:', gov.assess(p).decision.value)
print('With approvals:', gov.assess(p, approvals=('human-1','org-1')).decision.value)
gov.object('p1','human-1','This could erase a minority perspective')
print('After objection:', gov.assess(p, approvals=('human-1','org-1')).decision.value)
print(gov.export_audit_json())
