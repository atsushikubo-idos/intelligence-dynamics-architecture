"""Three-domain structural experiment and an explicitly limited baseline.

Baseline is an ordinary chronological event log; it is lossless for included
fields. The structured report adds explicit query views, not new facts.
"""
import json
from pathlib import Path
from idos_ver84_application_v0_2 import MA_DEMO, HIRING_DEMO, analyze, compare_domains
from idos_reference_bridge_v0_3 import bridge_domains
from synthetic_clinical_v0_5 import CLINICAL_DEMO

CASES = [MA_DEMO, HIRING_DEMO, CLINICAL_DEMO]

def plain_event_log(case, as_of='2026-10-21'):
    """Lossless permitted-field baseline; no inference and no enrichment."""
    report = analyze(case, as_of=as_of)
    return {'case_id': case['case_id'], 'domain': case['domain'],
            'events': report['timeline'],
            'available_queries': ['filter_by_actor', 'filter_by_date', 'filter_by_kind', 'filter_by_topic'],
            'note': 'Full event fields retained. Other queries can be programmed on this same log.'}

def compare():
    structured = compare_domains(CASES, as_of='2026-10-21')
    bridged = bridge_domains(CASES, as_of='2026-10-21')
    baseline = [plain_event_log(c) for c in CASES]
    rows = []
    for case, report, base, bridged_case in zip(CASES, structured['reports'], baseline, bridged['cases']):
        assert len(base['events']) == len(report['timeline'])
        rows.append({'case_id': case['case_id'], 'domain': case['domain'],
                     'visible_event_count': len(base['events']),
                     'revision_pairs': len(report['recorded_revisions']),
                     'holdings_due': sum(h['review_status']=='review_due' for h in report['holdings']),
                     'reference_provenance_entries': len(bridged_case['provenance']),
                     'reference_frame_revisions': sum(x['kind']=='reference_frame' for x in report['recorded_revisions']),
                     'restricted_excluded': report['privacy']['restricted_count']})
    return {'experiment':'Three-domain synthetic structural coverage vs ordinary event ledger',
            'research_thesis':'Continuously observe complex changes already recognized as important but difficult to handle within a shared structure without erasing differences.',
            'comparison':rows, 'structured':structured, 'baseline':baseline, 'reference_bridge':bridged,
            'limitations':[
                'Synthetic cases; no real clinical, organizational, or transaction outcomes.',
                'A raw event log retains all included facts; the structured report does not prove information gain.',
                'Structured views automate selected queries; the same queries could be implemented over the baseline.',
                'Equal schema coverage does not establish equivalent meanings across domains.',
                'Clinical residual/holding labels are not automatically IDOS reference Residual/HoldingState.',
                'Reference-frame revision is a documented mapping convention, not verified real-world frame transformation.',
                'No causal inference, prediction, measured Future Updateability, or independent validation.',
                'Consented records are present in outputs; this prototype is not an access-control system.'
            ]}

if __name__=='__main__':
    path=Path('three_domain_results_v0_5.json')
    path.write_text(json.dumps(compare(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Wrote',path)
