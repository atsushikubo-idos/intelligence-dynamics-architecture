"""Synthetic clinical trajectory for structural testing, not medical advice."""
from idos_ver84_application_v0_2 import ev

CLINICAL_DEMO = {'case_id': 'SYNTHETIC_CLINICAL', 'domain': 'clinical', 'synthetic': True, 'events': [
    ev('C1','2026-01-10','care_team','imagined_future','recovery','Steady functional improvement','Synthetic care plan'),
    ev('C2','2026-01-10','patient','imagined_future','daily_life','Resume usual activities','Synthetic stated goal','consented'),
    ev('C3','2026-01-12','care_team','commitment','follow_up','Review response after six weeks','Synthetic plan'),
    ev('C4','2026-01-15','joint','feasible_option','care_options','Continue monitoring or revise support plan','Synthetic options note'),
    ev('C5','2026-02-10','care_team','observation','functional_status','Mixed response observed','Synthetic follow-up note'),
    ev('C6','2026-02-10','care_team','residual','response_variation','Cause of variation remains unknown','Synthetic review note','consented'),
    ev('C7','2026-02-11','joint','holding','response_variation','Retain multiple explanations for later review','Synthetic review plan','consented',deadline='2026-03-15'),
    ev('C8','2026-02-12','care_team','decision','follow_up','Gather additional observations','Synthetic plan revision'),
    ev('C9','2026-03-15','care_team','observation','functional_status','Variable response persists','Synthetic second follow-up'),
    ev('C10','2026-03-15','joint','option_change','support_options','New support arrangement can be considered','Synthetic options note'),
    ev('C11','2026-03-16','care_team','imagined_future','recovery','Recovery path may remain variable','Synthetic revised plan'),
    ev('C12','2026-03-16','care_team','reference_frame','assessment_basis','Single outcome marker','Synthetic assessment note'),
    ev('C13','2026-04-01','care_team','reference_frame','assessment_basis','Multiple longitudinal markers','Synthetic revised assessment note'),
    ev('C14','2026-04-02','patient','observation','private_detail','Sensitive synthetic note','Synthetic private record','restricted'),
]}
