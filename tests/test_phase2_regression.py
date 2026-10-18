"""Phase 2 regression tests for the IDOS reference implementation.

Run the SAME file against any implementation file:

    IDOS_TARGET=src/idos_reference_v1_1.py          python3 -B -I tests/test_phase2_regression.py
    IDOS_TARGET=src/idos_reference_v1_1_proposed.py python3 -B -I tests/test_phase2_regression.py

Optional: IDOS_RESULT_JSON=<path> writes per-test outcomes for diffing.

Outcome vocabulary (reported separately, never merged):
  pass                 - behaviour matches the assertion
  fail / error         - behaviour (or API) does not match the assertion
  xfail                - OPEN SPEC DECISION: desired behaviour is not yet defined/implemented
  unexpected_success   - an xfail test passed (spec decision may be resolved; review it)

What these tests do NOT do: they do not validate IDOS scientifically. They check
implementation behaviour against stated architectural constraints only.
"""
import contextlib
import dataclasses
import importlib.util
import io
import json
import os
import sys
import unittest

TARGET = os.environ.get("IDOS_TARGET")
if not TARGET:
    raise SystemExit("Set IDOS_TARGET=<path to idos_reference*.py>")
_spec = importlib.util.spec_from_file_location("idos_under_test", TARGET)
m = importlib.util.module_from_spec(_spec)
sys.modules["idos_under_test"] = m
_spec.loader.exec_module(m)


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def unit(name="U", frame="F"):
    return m.make_unit(name, "test", frame)


def registered_residual(u, tag):
    c = m.RealityContact("s", f"observed-{tag}")
    r = u.contact_reality(c, expected=f"expected-{tag}", residual_criterion=m.ExplicitMismatchCriterion(True))
    assert r is not None and r.id in u.residuals
    return r


def ghost_residual():
    """A Residual object the unit never registered (hold() accepts any Residual)."""
    return m.Residual(description="ghost", difference=m.Difference("ghost-diff"))


def fu(status=None, route=True):
    status = status or m.FutureUpdateabilityStatus.PRESERVED
    return m.FutureUpdateabilityAssessment(
        status=status,
        can_detect_new_difference=True,
        alternatives_can_emerge=True,
        override_or_revision_exists=True,
        irreversible_dependency_increased=False,
        reality_recontact_route_exists=route,
        updating_structure_can_change=True,
        rationale="regression test",
    )


def reopen(u, evidence=(), status=None, route=True):
    return u.reopen(
        assessment=fu(status, route),
        action=m.ReopeningAction.MAINTAIN,
        basis="regression test",
        decision_rule_reopened="rule",
        evidence_ids=list(evidence),
    )


def point():
    return m.TrajectoryPoint(
        event=m.UpdateEvent(m.UpdateLevel.L1, "x"), frame_id="f", boundary_id="b", possibility_space_id="p"
    )


def cycle_check(tc, u):
    fn = getattr(u, "cycle_event_order_satisfied", None)
    if fn is None:
        tc.fail("API missing: UpdatingUnit.cycle_event_order_satisfied()")
    return fn()


# ----------------------------------------------------------------------------
# Patch item 1: Holding under partial resolution (+ spec item 3: unknown ids)
# ----------------------------------------------------------------------------
class HoldingResolution(unittest.TestCase):
    def test_partial_resolution_keeps_holding_active(self):
        u = unit()
        r1, r2 = registered_residual(u, 1), registered_residual(u, 2)
        h = u.hold([r1, r2])
        u.resolve_residuals([r1], reason="first only")
        self.assertTrue(r1.resolved)
        self.assertFalse(r2.resolved)
        self.assertTrue(h.active, "Holding deactivated although r2 is still unresolved")

    def test_partial_resolution_visible_in_cdp_description(self):
        u = unit()
        r1, r2 = registered_residual(u, 1), registered_residual(u, 2)
        u.hold([r1, r2])
        u.resolve_residuals([r1], reason="first only")
        self.assertEqual(m.CommonDynamicsProtocol().describe(u).active_holdings, 1)

    def test_full_resolution_deactivates_holding(self):
        u = unit()
        r1, r2 = registered_residual(u, 1), registered_residual(u, 2)
        h = u.hold([r1, r2])
        u.resolve_residuals([r1], reason="a")
        u.resolve_residuals([r2], reason="b")
        self.assertFalse(h.active)

    def test_unregistered_residual_id_is_not_counted_as_resolved(self):
        u = unit()
        r1, ghost = registered_residual(u, 1), ghost_residual()
        h = u.hold([r1, ghost])
        u.resolve_residuals([r1], reason="registered one only")
        self.assertTrue(h.active, "unknown residual id was silently treated as resolved")

    def test_resolving_an_unregistered_residual_does_nothing(self):
        u = unit()
        r1, ghost = registered_residual(u, 1), ghost_residual()
        h = u.hold([r1, ghost])
        u.resolve_residuals([ghost], reason="ghost only")
        self.assertFalse(ghost.resolved)
        self.assertFalse(r1.resolved)
        self.assertTrue(h.active)

    def test_ignored_unregistered_ids_are_recorded_in_provenance(self):
        u = unit()
        ghost = ghost_residual()
        u.resolve_residuals([ghost], reason="ghost only")
        last = [e for e in u.trajectory.provenance if e.event_type == "residual_resolution_judgment"][-1]
        self.assertIn(ghost.id, last.description)


# ----------------------------------------------------------------------------
# Patch item 2: Trajectory phase transitions
# ----------------------------------------------------------------------------
class TrajectoryTransitions(unittest.TestCase):
    def test_record_on_dissolved_trajectory_raises(self):  # parity: holds in both versions
        t = unit().trajectory
        t.transition(m.Phase.DISSOLUTION, "d")
        with self.assertRaises(RuntimeError):
            t.record(point())

    def test_transition_cannot_revive_dissolved_trajectory(self):
        t = unit().trajectory
        t.transition(m.Phase.DISSOLUTION, "d")
        with self.assertRaises(RuntimeError):
            t.transition(m.Phase.PERSISTENCE, "bypass attempt")
        self.assertEqual(t.phase, m.Phase.DISSOLUTION)

    def test_dissolved_to_dissolved_is_allowed(self):  # idempotent re-assertion is not a revival
        t = unit().trajectory
        t.transition(m.Phase.DISSOLUTION, "d")
        t.transition(m.Phase.DISSOLUTION, "again")
        self.assertEqual(t.phase, m.Phase.DISSOLUTION)

    def test_reemergence_phase_requires_predecessor(self):
        t = unit().trajectory
        self.assertEqual(t.parent_trajectory_ids, [])
        with self.assertRaises(RuntimeError):
            t.transition(m.Phase.REEMERGENCE, "no predecessor")

    def test_reemerge_method_still_works(self):  # parity
        t = unit().trajectory
        t.transition(m.Phase.DISSOLUTION, "d")
        child = t.reemerge("child", "later")
        self.assertEqual(child.phase, m.Phase.REEMERGENCE)
        self.assertIn(t.id, child.parent_trajectory_ids)

    def test_branch_dormancy_dissolution_path_still_works(self):  # parity: demo path
        t = unit().trajectory
        b = t.branch("b", "r")
        b.transition(m.Phase.DORMANCY, "pause")
        b.transition(m.Phase.DISSOLUTION, "end")
        self.assertEqual(b.phase, m.Phase.DISSOLUTION)


# ----------------------------------------------------------------------------
# Patch item 3 / spec item 4: evidence existence vs semantic validity
# ----------------------------------------------------------------------------
class EvidenceChecks(unittest.TestCase):
    def test_unknown_evidence_id_is_rejected(self):
        u = unit()
        with self.assertRaises(ValueError):
            reopen(u, evidence=["fabricated-id"])
        self.assertEqual(u.reopening_history, [], "rejected reopening must not be recorded")

    def test_traceable_evidence_is_accepted(self):  # parity
        u = unit()
        c = m.RealityContact("s", "o")
        u.contact_reality(c, expected="o")
        reopen(u, evidence=[c.id])
        self.assertEqual(len(u.reopening_history), 1)

    def test_existence_check_does_not_imply_semantic_validity(self):
        """LIMITATION DOCUMENTED, NOT ENDORSED: an id that merely exists in provenance but is
        unrelated to the decision (here: the unit's own initialisation event) is accepted.
        Passing this test means 'semantic validity is NOT checked', not that it is correct."""
        u = unit()
        init_event_id = u.trajectory.provenance[0].id
        reopen(u, evidence=[init_event_id])
        self.assertEqual(len(u.reopening_history), 1)

    def test_reopening_provenance_states_semantic_adequacy_not_assessed(self):
        u = unit()
        c = m.RealityContact("s", "o")
        u.contact_reality(c, expected="o")
        reopen(u, evidence=[c.id])
        last = [e for e in u.trajectory.provenance if e.event_type == "reopening"][-1]
        self.assertIn("semantic adequacy not assessed", last.description)

    def test_reopen_without_evidence_still_allowed(self):  # parity (audit record: reopen may precede recontact)
        u = unit()
        reopen(u)
        self.assertEqual(len(u.reopening_history), 1)


# ----------------------------------------------------------------------------
# Patch item 4: FU consistency (interpretive constraint - see spec decisions)
# ----------------------------------------------------------------------------
class FutureUpdateabilityConsistency(unittest.TestCase):
    def test_increased_without_recontact_route_is_rejected(self):
        with self.assertRaises(ValueError):
            fu(m.FutureUpdateabilityStatus.INCREASED, route=False)

    def test_increased_with_route_is_accepted(self):  # parity
        self.assertEqual(fu(m.FutureUpdateabilityStatus.INCREASED, route=True).status.value, "increased")

    def test_uncertain_without_route_remains_recordable(self):  # parity; audit record says UNCERTAIN stays valid
        self.assertEqual(fu(m.FutureUpdateabilityStatus.UNCERTAIN, route=False).status.value, "uncertain")

    def test_reduced_without_route_remains_recordable(self):  # parity
        self.assertEqual(fu(m.FutureUpdateabilityStatus.REDUCED, route=False).status.value, "reduced")

    def test_preserved_without_route_not_constrained(self):  # parity; documents that only INCREASED is guarded
        self.assertEqual(fu(m.FutureUpdateabilityStatus.PRESERVED, route=False).status.value, "preserved")


# ----------------------------------------------------------------------------
# Patch item 5 / spec item 2: event-order check vs theoretical cycle
# ----------------------------------------------------------------------------
class CycleEventOrder(unittest.TestCase):
    def test_reopen_without_any_recontact_is_not_event_order_complete(self):
        u = unit()
        reopen(u)
        self.assertFalse(cycle_check(self, u))

    def test_stale_contact_before_update_does_not_count(self):
        u = unit()
        u.contact_reality(m.RealityContact("s", "o"), expected="o")
        u.update(m.UpdateLevel.L1, "upd")
        reopen(u)
        self.assertFalse(cycle_check(self, u))

    def test_update_then_recontact_then_reopen_satisfies_event_order(self):
        u = unit()
        u.update(m.UpdateLevel.L1, "upd")
        u.recontact(m.RealityContact("s", "o"), expected="o")
        reopen(u)
        self.assertTrue(cycle_check(self, u))

    def test_no_reopening_is_not_satisfied(self):
        u = unit()
        u.update(m.UpdateLevel.L1, "upd")
        u.recontact(m.RealityContact("s", "o"), expected="o")
        self.assertFalse(cycle_check(self, u))

    def test_event_order_true_does_not_imply_theoretical_cycle(self):
        """Event order can be satisfied with NO Difference, NO Residual and NO distribution-change
        record. Operational Protocol v0.2 s.14 requires those for a completed cycle, so the
        method must be understood (and named) as an order check only."""
        u = unit()
        u.update(m.UpdateLevel.L1, "upd")
        u.recontact(m.RealityContact("s", "o"), expected="o")
        reopen(u)
        self.assertTrue(cycle_check(self, u))
        self.assertEqual(len(u.residuals), 0)

    def test_demo_reports_event_order_not_cycle_completion(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = m.demo()
        self.assertIn("minimum_idos_cycle_event_order_satisfied", result)
        self.assertNotIn("minimum_idos_cycle_complete", result)
        self.assertIn("minimum_idos_cycle_theory_assessment", result)


# ----------------------------------------------------------------------------
# Parity / smoke: behaviour that must be identical in both versions
# ----------------------------------------------------------------------------
class ParitySmoke(unittest.TestCase):
    def test_demo_runs(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = m.demo()
        self.assertIsInstance(result, dict)

    def test_difference_is_not_automatically_residual(self):
        u = unit()
        r = u.contact_reality(m.RealityContact("s", "obs"), expected="exp")  # no criterion
        self.assertIsNone(r)
        self.assertEqual(len(u.residuals), 0)

    def test_update_does_not_auto_resolve_residual(self):
        u = unit()
        r = registered_residual(u, 1)
        u.update(m.UpdateLevel.L1, "upd", residuals=[r])
        self.assertFalse(r.resolved)

    def test_coupling_does_not_enact_without_criterion(self):
        a, b = unit("A"), unit("B")
        cdp = m.CommonDynamicsProtocol()
        coupling = cdp.coordinate(a, b, "purpose")
        self.assertIsNone(m.enact_higher_order_unit("X", [a, b], coupling, m.ExplicitAuthorizationCriterion(False)))


# ----------------------------------------------------------------------------
# OPEN SPEC DECISIONS: desired behaviour not yet defined. Expected to fail in BOTH versions.
# An 'unexpected success' means a decision may have been resolved - review before trusting it.
# ----------------------------------------------------------------------------
class OpenSpecDecisions(unittest.TestCase):
    @unittest.expectedFailure
    def test_SPEC1_declared_L1_with_frame_replacement_is_rejected_or_flagged(self):
        u = unit()
        try:
            u.update(m.UpdateLevel.L1, "declared L1", new_frame=u.frame.revise(add_assumptions=["x"]))
        except Exception:
            return  # rejecting is an acceptable resolution
        kinds = [e.event_type for e in u.trajectory.provenance]
        self.assertIn("level_mismatch", kinds)  # flag name is arbitrary; the spec must decide

    @unittest.expectedFailure
    def test_SPEC3_compare_does_not_subtract_residual_counts_across_different_frames(self):
        a, b = unit("A", "same-name"), unit("B", "same-name")
        for _ in range(3):
            registered_residual(a, "a")
        cdp = m.CommonDynamicsProtocol()
        cmp = cdp.compare(cdp.describe(a), cdp.describe(b))
        self.assertNotIsInstance(cmp.get("residual_difference"), int)

    @unittest.expectedFailure
    def test_SPEC4_translate_depends_on_target(self):
        u = unit()
        cdp = m.CommonDynamicsProtocol()
        d = cdp.describe(u)
        x, y = cdp.translate(d, "A"), cdp.translate(d, "B")
        strip = lambda z: {k: v for k, v in z.items() if k != "target"}
        self.assertNotEqual(strip(x), strip(y))

    @unittest.expectedFailure
    def test_SPEC6_holding_has_a_review_or_expiry_condition(self):
        names = {f.name for f in dataclasses.fields(m.HoldingState)}
        self.assertTrue(names & {"review_by", "review_after", "expires", "max_age", "expiry"})

    @unittest.expectedFailure
    def test_SPEC_X2_fu_comparative_status_requires_comparison_basis(self):
        names = {f.name for f in dataclasses.fields(m.FutureUpdateabilityAssessment)}
        self.assertTrue(any("basis" in n or "compar" in n for n in names))


# ----------------------------------------------------------------------------
# runner that records outcomes by category
# ----------------------------------------------------------------------------
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
