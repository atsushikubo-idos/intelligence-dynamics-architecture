"""Minimal research-integrity regression tests (A: Frame comparison, B: Future Updateability, C: update levels).

Run the SAME file against any implementation:

    IDOS_TARGET=src/idos_reference_v1_1.py                python3 -B -I tests/test_integrity_fix.py
    IDOS_TARGET=src/idos_reference_v1_1_proposed.py       python3 -B -I tests/test_integrity_fix.py
    IDOS_TARGET=src/idos_reference_v1_1_research_safe.py  python3 -B -I tests/test_integrity_fix.py

Optional: IDOS_RESULT_JSON=<path> writes per-test outcomes.

These tests encode the research-safe requirements. They are EXPECTED to fail on implementations that
lack the research-safe behaviour (the frozen v1.1 and the Phase 2 proposed file). A failure there is
a statement about that implementation, not about IDOS. Nothing here validates IDOS scientifically.

Superseded Phase 2 expectation (recorded, not edited in tests/test_phase2_regression.py):
  `FutureUpdateabilityConsistency.test_increased_without_recontact_route_is_rejected` asserted that
  FU=INCREASED without a recontact route RAISES (Phase 2 patch P4). That forced rejection is NOT adopted
  as a specification (no MASTER_MAP v1.1 rule requires it). The replacement expectation is
  `FUJudgmentRecord.test_increased_without_route_is_accepted_not_rejected` below.
"""
import contextlib
import io
import json
import os
import sys
import importlib.util
import unittest

TARGET = os.environ.get("IDOS_TARGET")
if not TARGET:
    raise SystemExit("Set IDOS_TARGET=<path to idos_reference*.py>")
_spec = importlib.util.spec_from_file_location("idos_under_test", TARGET)
m = importlib.util.module_from_spec(_spec)
sys.modules["idos_under_test"] = m
_spec.loader.exec_module(m)

FORBIDDEN_MEASUREMENT_STATUSES = {"estimated", "validated", "measured", "established", "increased", "reduced"}


# ----------------------------------------------------------------------------- helpers
def unit(name="U", frame="F"):
    return m.make_unit(name, "test", frame)


def add_residuals(u, n):
    for i in range(n):
        u.contact_reality(m.RealityContact("s", f"o{i}"), expected=f"e{i}",
                          residual_criterion=m.ExplicitMismatchCriterion(True))


def mk_fu(tc, status, route=True, claimed=None):
    kw = dict(
        status=status,
        can_detect_new_difference=True,
        alternatives_can_emerge=True,
        override_or_revision_exists=True,
        irreversible_dependency_increased=False,
        reality_recontact_route_exists=route,
        updating_structure_can_change=True,
        rationale="integrity test",
    )
    if claimed is not None:
        kw["claimed_perturbation_evidence_ids"] = claimed
    try:
        return m.FutureUpdateabilityAssessment(**kw)
    except TypeError as e:
        tc.fail(f"API missing on this implementation: {e}")


def reopen(u, fu_obj):
    return u.reopen(assessment=fu_obj, action=m.ReopeningAction.MAINTAIN, basis="b", decision_rule_reopened="r")


def last_event(u):
    return u.trajectory.points[-1].event


def flags_of(tc, u):
    ev = last_event(u)
    fl = getattr(ev, "level_flags", None)
    if fl is None:
        tc.fail("API missing on this implementation: UpdateEvent.level_flags")
    return fl


def compare(tc, a, b, **kw):
    cdp = m.CommonDynamicsProtocol()
    try:
        return cdp.compare(cdp.describe(a), cdp.describe(b), **kw)
    except TypeError as e:
        tc.fail(f"API missing on this implementation: {e}")


# ----------------------------------------------------------------------------- A: Frame comparison
class FrameComparisonGate(unittest.TestCase):
    def setUp(self):
        self.a, self.b = unit("A", "Shared-Name"), unit("B", "Shared-Name")
        add_residuals(self.a, 3)

    def test_no_declared_measure_marks_not_established(self):
        self.assertEqual(compare(self, self.a, self.b).get("comparability"), "not_established")

    def test_residual_difference_not_returned_without_shared_measure(self):
        self.assertIsNone(compare(self, self.a, self.b).get("residual_difference"))

    def test_measurement_version_difference_not_returned_without_shared_measure(self):
        self.assertIsNone(compare(self, self.a, self.b).get("measurement_version_difference"))

    def test_same_frame_name_does_not_establish_comparability(self):
        out = compare(self, self.a, self.b)
        self.assertTrue(out["same_frame_name"])  # literal fact is still reported
        self.assertEqual(out.get("comparability"), "not_established")
        self.assertIsNone(out.get("residual_difference"))

    def test_different_frame_names_also_not_established(self):
        c = unit("C", "Other-Name")
        out = compare(self, self.a, c)
        self.assertFalse(out["same_frame_name"])
        self.assertEqual(out.get("comparability"), "not_established")

    def test_blank_shared_measure_is_treated_as_absent(self):
        for blank in ("", "   ", None):
            out = compare(self, self.a, self.b, shared_measure=blank)
            self.assertEqual(out.get("comparability"), "not_established", repr(blank))
            self.assertIsNone(out.get("residual_difference"), repr(blank))

    def test_declared_shared_measure_returns_values_marked_unverified(self):
        out = compare(self, self.a, self.b, shared_measure="count of registered residuals, same coder protocol")
        self.assertEqual(out.get("comparability"), "declared_unverified")
        self.assertEqual(out.get("residual_difference"), 3)
        self.assertEqual(out.get("shared_measure"), "count of registered residuals, same coder protocol")

    def test_literal_field_comparisons_still_present(self):
        out = compare(self, self.a, self.b)
        for k in ("same_phase", "same_frame_name", "both_holding", "future_updateability_equal"):
            self.assertIn(k, out)


# ----------------------------------------------------------------------------- B: Future Updateability
class FUJudgmentRecord(unittest.TestCase):
    def test_increased_without_route_is_accepted_not_rejected(self):
        # Replaces Phase 2 P4's forced rejection (see module docstring).
        fu = mk_fu(self, m.FutureUpdateabilityStatus.INCREASED, route=False)
        self.assertEqual(fu.status.value, "increased")

    def test_increased_without_route_carries_non_binding_review_flag(self):
        fu = mk_fu(self, m.FutureUpdateabilityStatus.INCREASED, route=False)
        flags = getattr(fu, "review_flags", None)
        self.assertTrue(flags, "expected a reviewer flag")
        self.assertEqual(fu.status.value, "increased", "flag must not alter the judgment")

    def test_increased_with_route_has_no_flag(self):
        fu = mk_fu(self, m.FutureUpdateabilityStatus.INCREASED, route=True)
        self.assertEqual(getattr(fu, "review_flags", None), [])

    def test_route_presence_alone_neither_confirms_nor_denies(self):
        for st in m.FutureUpdateabilityStatus:
            with_route = mk_fu(self, st, route=True)
            without_route = mk_fu(self, st, route=False)
            self.assertEqual(with_route.status, without_route.status)
            self.assertEqual(with_route.measurement_status, without_route.measurement_status)

    def test_reduced_with_route_is_accepted_and_unflagged(self):
        fu = mk_fu(self, m.FutureUpdateabilityStatus.REDUCED, route=True)
        self.assertEqual(fu.status.value, "reduced")
        self.assertEqual(getattr(fu, "review_flags", None), [])

    def test_record_type_is_evaluator_judgment(self):
        self.assertEqual(getattr(mk_fu(self, m.FutureUpdateabilityStatus.PRESERVED), "record_type", None),
                         "evaluator_judgment")

    def test_measurement_status_not_estimable_without_perturbation_claim(self):
        fu = mk_fu(self, m.FutureUpdateabilityStatus.INCREASED)
        self.assertEqual(getattr(fu, "measurement_status", None), "not_estimable")

    def test_measurement_status_latent_not_validated_with_perturbation_claim(self):
        fu = mk_fu(self, m.FutureUpdateabilityStatus.INCREASED, claimed=["perturbation-1"])
        self.assertEqual(getattr(fu, "measurement_status", None), "latent_not_validated")

    def test_measurement_status_never_asserts_an_estimate(self):
        for st in m.FutureUpdateabilityStatus:
            for claimed in (None, ["p1"]):
                ms = getattr(mk_fu(self, st, claimed=claimed), "measurement_status", None)
                self.assertIn(ms, {"not_estimable", "latent_not_validated"})
                self.assertNotIn(ms, FORBIDDEN_MEASUREMENT_STATUSES)

    def test_reopen_accepts_increased_without_route_and_records_judgment_nature(self):
        u = unit()
        reopen(u, mk_fu(self, m.FutureUpdateabilityStatus.INCREASED, route=False))
        self.assertEqual(len(u.reopening_history), 1)
        desc = [e for e in u.trajectory.provenance if e.event_type == "reopening"][-1].description
        self.assertIn("evaluator", desc)
        self.assertIn("not_estimable", desc)

    def test_cdp_description_exposes_judgment_nature_of_latest_fu(self):
        u = unit()
        d0 = m.CommonDynamicsProtocol().describe(u)
        self.assertIsNone(getattr(d0, "latest_fu_record_type", "MISSING"))
        reopen(u, mk_fu(self, m.FutureUpdateabilityStatus.PRESERVED))
        d1 = m.CommonDynamicsProtocol().describe(u)
        self.assertEqual(getattr(d1, "latest_fu_record_type", None), "evaluator_judgment")
        self.assertEqual(getattr(d1, "latest_fu_measurement_status", None), "not_estimable")

    def test_demo_marks_fu_as_judgment_and_not_estimable(self):
        with contextlib.redirect_stdout(io.StringIO()):
            res = m.demo()
        fu = res["future_updateability"]
        self.assertEqual(fu.get("record_type"), "evaluator_judgment")
        self.assertEqual(fu.get("measurement_status"), "not_estimable")


# ----------------------------------------------------------------------------- C: update levels
class UpdateLevelConsistency(unittest.TestCase):
    def _upd(self, level, *, frame=False, space=False, boundary=False, measurement=False):
        u = unit()
        kw = {}
        if frame:
            kw["new_frame"] = u.frame.revise(add_assumptions=["x"])
        if space:
            kw["new_possibility_space"] = u.possibility_space.revise(actions=["z"])
        if boundary:
            kw["new_boundary"] = u.boundary.revise(include=["y"])
        if measurement:
            kw["new_measurement"] = u.measurement.revise(add_metrics=["w"])
        u.update(level, "declared", **kw)
        return u

    def _has(self, flags, prefix):
        return any(f.startswith(prefix) for f in flags)

    def test_L1_with_frame_replacement_is_flagged_as_definition_conflict(self):
        u = self._upd(m.UpdateLevel.L1, frame=True)
        self.assertTrue(self._has(flags_of(self, u), "definition_conflict"))

    def test_L2_with_frame_replacement_is_flagged_as_definition_conflict(self):
        u = self._upd(m.UpdateLevel.L2, frame=True)
        self.assertTrue(self._has(flags_of(self, u), "definition_conflict"))

    def test_L3_with_frame_replacement_only_has_no_flags(self):
        u = self._upd(m.UpdateLevel.L3, frame=True)
        self.assertEqual(flags_of(self, u), [])

    def test_L3_without_frame_replacement_is_flagged(self):
        u = self._upd(m.UpdateLevel.L3)
        self.assertTrue(self._has(flags_of(self, u), "definition_conflict"))

    def test_L5_without_space_replacement_is_flagged(self):
        u = self._upd(m.UpdateLevel.L5)
        self.assertTrue(self._has(flags_of(self, u), "definition_conflict"))

    def test_L5_with_space_replacement_has_no_flags(self):
        u = self._upd(m.UpdateLevel.L5, space=True)
        self.assertEqual(flags_of(self, u), [])

    def test_L3_with_frame_and_space_gets_only_convention_dependent_flag(self):
        u = self._upd(m.UpdateLevel.L3, frame=True, space=True)
        fl = flags_of(self, u)
        self.assertTrue(self._has(fl, "convention_dependent"))
        self.assertFalse(self._has(fl, "definition_conflict"))

    def test_boundary_or_measurement_change_alone_is_not_mapped_to_levels(self):
        for kw in ({"boundary": True}, {"measurement": True}, {"boundary": True, "measurement": True}):
            u = self._upd(m.UpdateLevel.L1, **kw)
            self.assertEqual(flags_of(self, u), [], kw)

    def test_L4_is_not_checked_for_frame_replacement(self):
        u = self._upd(m.UpdateLevel.L4, frame=True)
        self.assertEqual(flags_of(self, u), [])

    def test_L1_with_no_change_has_no_flags(self):
        u = self._upd(m.UpdateLevel.L1)
        self.assertEqual(flags_of(self, u), [])

    def test_flags_are_also_recorded_in_provenance(self):
        u = self._upd(m.UpdateLevel.L1, frame=True)
        kinds = [e.event_type for e in u.trajectory.provenance]
        self.assertIn("level_mismatch", kinds)

    def test_declared_level_is_never_altered_or_auto_assigned(self):
        combos = [dict(), dict(frame=True), dict(space=True), dict(frame=True, space=True)]
        for lvl in m.UpdateLevel:
            for kw in combos:
                u = self._upd(lvl, **kw)
                self.assertEqual(last_event(u).level, lvl, (lvl, kw))

    def test_flagged_update_is_still_applied_not_blocked(self):
        u = unit()
        old = u.frame.id
        u.update(m.UpdateLevel.L1, "declared", new_frame=u.frame.revise(add_assumptions=["x"]))
        self.assertNotEqual(u.frame.id, old)
        self.assertEqual(len(u.trajectory.points), 1)

    def test_module_level_checker_is_available_and_consistent(self):
        fn = getattr(m, "check_update_level_consistency", None)
        if fn is None:
            self.fail("API missing on this implementation: check_update_level_consistency")
        self.assertTrue(fn(m.UpdateLevel.L1, frame_replaced=True, possibility_space_replaced=False))
        self.assertEqual(fn(m.UpdateLevel.L3, frame_replaced=True, possibility_space_replaced=False), [])

    def test_demo_update_with_space_change_under_L3_carries_convention_flag(self):
        with contextlib.redirect_stdout(io.StringIO()):
            res = m.demo()
        evs = [e for e in res["human_provenance"] if e["event_type"] == "level_mismatch"]
        self.assertTrue(any("convention_dependent" in e["description"] for e in evs))


# ----------------------------------------------------------------------------- gap guards (added during review)
class GapGuards(unittest.TestCase):
    """Added after an independent review found gaps the first test draft did not cover."""

    def test_caller_cannot_inject_derived_fu_fields(self):
        base = mk_fu(self, m.FutureUpdateabilityStatus.INCREASED)
        # guard against a vacuous pass: on implementations without these fields TypeError is trivial
        self.assertIsNotNone(getattr(base, "measurement_status", None), "derived FU fields missing on this implementation")
        kw = dict(
            status=m.FutureUpdateabilityStatus.INCREASED,
            can_detect_new_difference=True,
            alternatives_can_emerge=True,
            override_or_revision_exists=True,
            irreversible_dependency_increased=False,
            reality_recontact_route_exists=True,
            updating_structure_can_change=True,
            rationale="injection attempt",
        )
        for extra in ({"measurement_status": "validated"}, {"record_type": "measurement"}, {"review_flags": []}):
            with self.assertRaises(TypeError, msg=repr(extra)):
                m.FutureUpdateabilityAssessment(**kw, **extra)

    def test_blank_or_non_string_perturbation_claims_stay_not_estimable(self):
        for claimed in ([""], ["   "], [None]):
            fu = mk_fu(self, m.FutureUpdateabilityStatus.INCREASED, claimed=claimed)
            self.assertEqual(getattr(fu, "measurement_status", None), "not_estimable", repr(claimed))

    def test_one_non_blank_claim_among_blanks_is_enough_for_latent_not_validated(self):
        fu = mk_fu(self, m.FutureUpdateabilityStatus.INCREASED, claimed=["", "p-1"])
        self.assertEqual(getattr(fu, "measurement_status", None), "latent_not_validated")

    def test_translate_carries_fu_judgment_nature(self):
        u = unit()
        reopen(u, mk_fu(self, m.FutureUpdateabilityStatus.PRESERVED))
        cdp = m.CommonDynamicsProtocol()
        ds = cdp.translate(cdp.describe(u), "Target")["dynamic_state"]
        self.assertEqual(ds.get("latest_fu_record_type"), "evaluator_judgment")
        self.assertEqual(ds.get("latest_fu_measurement_status"), "not_estimable")

    def test_compare_output_has_no_numeric_values_without_shared_measure(self):
        a, b = unit("A", "Same"), unit("B", "Same")
        add_residuals(a, 4)
        out = compare(self, a, b)
        numeric = {k: v for k, v in out.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
        self.assertEqual(numeric, {}, "numeric cross-unit values returned without a declared shared measure")

    def test_L5_with_frame_replacement_only_is_flagged(self):
        u = unit()
        u.update(m.UpdateLevel.L5, "declared L5", new_frame=u.frame.revise(add_assumptions=["z"]))
        self.assertTrue(any(f.startswith("definition_conflict") for f in flags_of(self, u)))


# ----------------------------------------------------------------------------- parity
class Parity(unittest.TestCase):
    def test_demo_runs(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertIsInstance(m.demo(), dict)

    def test_update_applies_changes_for_unflagged_case(self):
        u = unit()
        u.update(m.UpdateLevel.L3, "ok", new_frame=u.frame.revise(add_assumptions=["x"]))
        self.assertEqual(len(u.trajectory.points), 1)


# ----------------------------------------------------------------------------- runner
class _Rec(unittest.TextTestResult):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.status = {}

    def _s(self, t, v):
        self.status[t.id().split(".", 1)[-1]] = v

    def addSuccess(self, t):
        super().addSuccess(t); self._s(t, "pass")

    def addFailure(self, t, e):
        super().addFailure(t, e); self._s(t, "fail")

    def addError(self, t, e):
        super().addError(t, e); self._s(t, "error")

    def addExpectedFailure(self, t, e):
        super().addExpectedFailure(t, e); self._s(t, "xfail")

    def addUnexpectedSuccess(self, t):
        super().addUnexpectedSuccess(t); self._s(t, "unexpected_success")

    def addSkip(self, t, r):
        super().addSkip(t, r); self._s(t, "skip")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    res = unittest.TextTestRunner(verbosity=2, resultclass=_Rec).run(suite)
    out = os.environ.get("IDOS_RESULT_JSON")
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump({"target": TARGET, "status": res.status}, f, indent=1, sort_keys=True)
    counts = {}
    for v in res.status.values():
        counts[v] = counts.get(v, 0) + 1
    print("\nSUMMARY", json.dumps(counts, sort_keys=True))
    sys.exit(0 if res.wasSuccessful() else 1)
