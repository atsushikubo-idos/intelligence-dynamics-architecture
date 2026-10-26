"""Run with the repository src directory on PYTHONPATH."""
from governance import Actor, Proposal, CoexistenceGovernor
from idos_bridge import assess_with_cdp
from idos_reference_v1_2 import make_unit

actors = [Actor('person','human','consent'), Actor('ai','ai','optimization')]
governor = CoexistenceGovernor(actors)
units = {'person': make_unit('Person','human','Consent frame'),
         'ai': make_unit('Assistant','ai','Optimization frame')}
proposal = Proposal('p1','ai',('person',),'joint planning','AI suggests new workflow',True,'low')
result, connection = assess_with_cdp(governor, proposal, units, approvals=('person',))
print('Governance decision:', result.decision.value)
print('Distinct frames:', connection.frames if connection else None)
print('Translation limitations:', connection.translation_residuals if connection else None)
