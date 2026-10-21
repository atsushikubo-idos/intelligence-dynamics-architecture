"""Conservative adapter: descriptive case ledger -> IDOS reference objects.

No automatic Difference->Residual promotion, inferred Holding, causality,
Future Updateability assessment, or Reopening. Synthetic cases only.
"""
from dataclasses import asdict
from pathlib import Path
import sys

# Use the existing repository reference implementation, without copying it into this folder.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_REF_DIR = _REPO_ROOT / "src"
if str(_REF_DIR) not in sys.path:
    sys.path.insert(0, str(_REF_DIR))
from idos_reference_v1_1 import (make_unit, RealityContact, ProvenanceEvent,
                                   CommonDynamicsProtocol, UpdateLevel)
from idos_ver84_application_v0_2 import validate, analyze


def bridge_case(case, as_of='2026-10-21'):
    validate(case)
    report = analyze(case, as_of=as_of)
    unit = make_unit(case['case_id'], case['domain'], f"{case['domain']} provisional observation frame")
    # Only non-restricted events are processed; original input must still be protected.
    for e in report['timeline']:
        eid = e['id'] or f"ledger:{e['date']}:{e['actor']}:{e['topic']}"
        if e['kind'] == 'observation':
            unit.contact_reality(RealityContact(source=e['evidence'], observation=e['value'],
                                              timestamp=e['date']))
        # A source-labeled residual is NOT automatically promoted to a reference Residual.
        # An explicit criterion and an observed mismatch are required for that.
        unit.trajectory.provenance.append(ProvenanceEvent(
            event_type=f"ledger_{e['kind']}", description=f"{e['actor']} / {e['topic']}: {e['value']}",
            source_ids=[str(eid)], timestamp=e['date']))
    # Only explicitly recorded changes in a reference-frame category trigger a frame revision.
    for revision in report['recorded_revisions']:
        if revision['kind'] == 'reference_frame':
            revised = unit.frame.revise(add_assumptions=[str(revision['after'])])
            unit.update(UpdateLevel.L3, 'Explicitly recorded frame revision', new_frame=revised)
    cdp = CommonDynamicsProtocol()
    return {'case_id': case['case_id'], 'domain': case['domain'],
            'reference_description': asdict(cdp.describe(unit)),
            'provenance': cdp.trace(unit),
            'source_report': report,
            'interpretation': 'Descriptive software interoperability only; no construct validity or predictive claim.',
            'unmapped_semantics': ['ledger residual != reference Residual without criterion',
                                   'ledger holding != reference HoldingState without explicit residual linkage',
                                   'ledger option_change != measured Future Updateability',
                                   'reopening requires explicit recontact and assessment']}


def bridge_domains(cases, as_of='2026-10-21'):
    return {'cases': [bridge_case(c, as_of) for c in cases],
            'claim': 'Shared representational interface, not cross-domain outcome equivalence.'}
