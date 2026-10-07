from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json
from typing import Any, Dict, Iterable, List, Optional, Protocol, Sequence
from uuid import uuid4

"""
Intelligence Dynamics Architecture (IDOS)
Executable Reference Architecture v1.1

Aligned with:
- MASTER_MAP v1.1 (frozen research baseline)
- IDOS Purpose and Use / Q2 canonical definition
- Minimum operational loop:
  Detect -> Preserve -> Update -> Trace -> Recontact -> Reopen

This implementation is intended to make the architecture inspectable,
executable, and criticizable—not to claim that intelligence has been reduced to code.

Successful execution is not scientific validation.

Epistemic labels used in comments/docstrings:
[D] Defined software structure
[P] Provisional architectural mapping
[O] Open research question

v1.1 architectural constraints:
- Reality contact is mediated, not direct access to Reality.
- Difference is more general than Residual.
- Residual is a diagnostic construct, not a universal Core node.
- Holding is a domain-specific update mechanism, not a universal Core node.
- Possibility Space is a generative extension, not a primitive Core element.
- Updating Unit and Boundary are dynamic and revisable.
- Trajectory remains central and non-fixed.
- Reference Frame, Measurement, Provenance, and Future Updateability are explicit.
- Measurement systems can themselves change through updating.
- Physical Entity is not assumed to equal Updating Unit.
- Coupling does not imply Enactment or Agency.
- Provenance supports traceability but does not prove identity or causality.
- CDP supports partial interoperability without representational unification.
- Recontact must be followed by Reopening assessment if the cycle is to satisfy Minimum IDOS.
- Reopening does not require Reconfiguration: Maintain / Adjust / Reconfigure / Abandon are all valid.
- Current performance improvement does not imply Future Updateability improvement.
- All open criteria are replaceable; no universal thresholds are asserted.
"""


def uid(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def unique(values: Iterable[str]) -> List[str]:
    return list(dict.fromkeys(values))


class EpistemicStatus(str, Enum):
    DEFINED = "D"
    PROVISIONAL = "P"
    OPEN = "O"


class Phase(str, Enum):
    BIRTH = "birth"
    PERSISTENCE = "persistence"
    ENACTMENT = "enactment"
    TRANSITION = "transition"
    DORMANCY = "dormancy"
    DISSOLUTION = "dissolution"
    REEMERGENCE = "re-emergence"


class UpdateLevel(str, Enum):
    L1 = "L1_local_absorption"
    L2 = "L2_parameter_update"
    L3 = "L3_frame_transformation"
    L4 = "L4_frame_traversal"
    L5 = "L5_possibility_space_transformation"


class ReopeningAction(str, Enum):
    """[P] Decision after reopening. Change magnitude is deliberately not implied."""

    MAINTAIN = "maintain"
    ADJUST = "adjust"
    RECONFIGURE = "reconfigure"
    ABANDON = "abandon"


class FutureUpdateabilityStatus(str, Enum):
    INCREASED = "increased"
    PRESERVED = "preserved"
    REDUCED = "reduced"
    UNCERTAIN = "uncertain"


# -----------------------------------------------------------------------------
# Reality contact, Difference, Residual, Holding
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class RealityContact:
    """[P] A mediated observation/contact event, not Reality itself."""

    source: str
    observation: Any
    mode: str = "observation"
    timestamp: str = field(default_factory=now)
    id: str = field(default_factory=lambda: uid("contact"))


@dataclass(frozen=True)
class Difference:
    """[D/P] A represented mismatch. It is not automatically a Residual."""

    description: str
    magnitude: Optional[float] = None
    confidence: Optional[float] = None
    id: str = field(default_factory=lambda: uid("diff"))


@dataclass
class Residual:
    """[P] Diagnostic form of Difference not adequately absorbed by the current frame; not a universal Core node."""

    description: str
    difference: Difference
    precision: Optional[float] = None
    salience: Optional[float] = None
    resolved: bool = False
    id: str = field(default_factory=lambda: uid("res"))


class ResidualCriterion(Protocol):
    """[O] No universal criterion for Difference -> Residual is claimed."""

    def evaluate(
        self,
        unit: "UpdatingUnit",
        contact: RealityContact,
        expected: Any,
        difference: Difference,
    ) -> bool: ...


class ExplicitMismatchCriterion:
    """[P] Demo-only criterion: caller chooses whether mismatch counts as Residual."""

    def __init__(self, accept_as_residual: bool = True):
        self.accept_as_residual = accept_as_residual

    def evaluate(
        self,
        unit: "UpdatingUnit",
        contact: RealityContact,
        expected: Any,
        difference: Difference,
    ) -> bool:
        return self.accept_as_residual


@dataclass
class HoldingState:
    """[P] Domain-specific mechanism for preserving unresolved Residual(s); not a universal Core node."""

    residual_ids: List[str] = field(default_factory=list)
    competing_interpretations: List[str] = field(default_factory=list)
    reason: str = "unresolved"
    active: bool = True
    id: str = field(default_factory=lambda: uid("holding"))


# -----------------------------------------------------------------------------
# Mutable architectural contexts
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class ReferenceFrame:
    name: str
    assumptions: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    version: int = 1
    parent_id: Optional[str] = None
    id: str = field(default_factory=lambda: uid("frame"))

    def revise(
        self,
        *,
        name: Optional[str] = None,
        add_assumptions: Sequence[str] = (),
        remove_assumptions: Sequence[str] = (),
        add_categories: Sequence[str] = (),
        remove_categories: Sequence[str] = (),
        add_constraints: Sequence[str] = (),
        remove_constraints: Sequence[str] = (),
    ) -> "ReferenceFrame":
        def changed(old: Sequence[str], add: Sequence[str], remove: Sequence[str]) -> List[str]:
            removed = set(remove)
            return unique([x for x in old if x not in removed] + list(add))

        return ReferenceFrame(
            name=name or self.name,
            assumptions=changed(self.assumptions, add_assumptions, remove_assumptions),
            categories=changed(self.categories, add_categories, remove_categories),
            constraints=changed(self.constraints, add_constraints, remove_constraints),
            version=self.version + 1,
            parent_id=self.id,
        )


@dataclass(frozen=True)
class Boundary:
    included: List[str]
    excluded: List[str] = field(default_factory=list)
    permeability: Optional[float] = None
    version: int = 1
    parent_id: Optional[str] = None
    id: str = field(default_factory=lambda: uid("boundary"))

    def revise(
        self,
        *,
        include: Sequence[str] = (),
        remove_included: Sequence[str] = (),
        exclude: Sequence[str] = (),
        remove_excluded: Sequence[str] = (),
        permeability: Optional[float] = None,
    ) -> "Boundary":
        included = unique([x for x in self.included if x not in set(remove_included)] + list(include))
        excluded = unique([x for x in self.excluded if x not in set(remove_excluded)] + list(exclude))
        return Boundary(
            included=included,
            excluded=excluded,
            permeability=self.permeability if permeability is None else permeability,
            version=self.version + 1,
            parent_id=self.id,
        )


@dataclass(frozen=True)
class PossibilitySpace:
    actions: List[str] = field(default_factory=list)
    frames: List[str] = field(default_factory=list)
    relations: List[str] = field(default_factory=list)
    version: int = 1
    parent_id: Optional[str] = None
    id: str = field(default_factory=lambda: uid("space"))

    def revise(
        self,
        *,
        actions: Sequence[str] = (),
        remove_actions: Sequence[str] = (),
        frames: Sequence[str] = (),
        remove_frames: Sequence[str] = (),
        relations: Sequence[str] = (),
        remove_relations: Sequence[str] = (),
    ) -> "PossibilitySpace":
        def changed(old: Sequence[str], add: Sequence[str], remove: Sequence[str]) -> List[str]:
            removed = set(remove)
            return unique([x for x in old if x not in removed] + list(add))

        return PossibilitySpace(
            actions=changed(self.actions, actions, remove_actions),
            frames=changed(self.frames, frames, remove_frames),
            relations=changed(self.relations, relations, remove_relations),
            version=self.version + 1,
            parent_id=self.id,
        )



# -----------------------------------------------------------------------------
# Dynamic Measurement
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class MeasurementSystem:
    """
    [P] A revisable measurement configuration.

    Implements the MASTER_MAP v1.1/Q2 requirement that not only observations,
    but also frames, observers, and instruments may change through updating.

    Conceptual form:
        Y_t = M(R_t; F_t, O_t, I_t)
    """

    name: str = "default measurement"
    observer: str = "unspecified observer"
    instruments: List[str] = field(default_factory=list)
    metrics: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    version: int = 1
    parent_id: Optional[str] = None
    id: str = field(default_factory=lambda: uid("measure"))

    def revise(
        self,
        *,
        name: Optional[str] = None,
        observer: Optional[str] = None,
        add_instruments: Sequence[str] = (),
        remove_instruments: Sequence[str] = (),
        add_metrics: Sequence[str] = (),
        remove_metrics: Sequence[str] = (),
        add_assumptions: Sequence[str] = (),
        remove_assumptions: Sequence[str] = (),
    ) -> "MeasurementSystem":
        def changed(old: Sequence[str], add: Sequence[str], remove: Sequence[str]) -> List[str]:
            removed = set(remove)
            return unique([x for x in old if x not in removed] + list(add))

        return MeasurementSystem(
            name=name or self.name,
            observer=observer or self.observer,
            instruments=changed(self.instruments, add_instruments, remove_instruments),
            metrics=changed(self.metrics, add_metrics, remove_metrics),
            assumptions=changed(self.assumptions, add_assumptions, remove_assumptions),
            version=self.version + 1,
            parent_id=self.id,
        )


@dataclass(frozen=True)
class FutureUpdateabilityAssessment:
    """
    [P] Explicit second-order assessment required by Q2.

    It does not score "how much the system changed".
    It asks whether the system remains able to detect, reconsider, override,
    recontact Reality, and change its updating structure again.
    """

    status: FutureUpdateabilityStatus
    can_detect_new_difference: bool
    alternatives_can_emerge: bool
    override_or_revision_exists: bool
    irreversible_dependency_increased: bool
    reality_recontact_route_exists: bool
    updating_structure_can_change: bool
    rationale: str
    timestamp: str = field(default_factory=now)
    id: str = field(default_factory=lambda: uid("fu"))


@dataclass(frozen=True)
class ReopeningDecision:
    """
    [P] A decision made after Reality recontact and explicit reopening.

    Reopening is conceptually distinct from Reconfiguration:
    a valid reopened decision may Maintain, Adjust, Reconfigure, or Abandon.
    """

    action: ReopeningAction
    assessment: FutureUpdateabilityAssessment
    basis: str
    decision_rule_reopened: str
    evidence_ids: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=now)
    id: str = field(default_factory=lambda: uid("reopen"))


# -----------------------------------------------------------------------------
# Provenance, Update, Trajectory
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class ProvenanceEvent:
    event_type: str
    description: str
    source_ids: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=now)
    id: str = field(default_factory=lambda: uid("prov"))


@dataclass(frozen=True)
class UpdateEvent:
    level: UpdateLevel
    description: str
    residual_ids: List[str] = field(default_factory=list)
    reversible: Optional[bool] = None
    timestamp: str = field(default_factory=now)
    id: str = field(default_factory=lambda: uid("upd"))


@dataclass(frozen=True)
class TrajectoryPoint:
    event: UpdateEvent
    frame_id: str
    boundary_id: str
    possibility_space_id: str
    measurement_id: Optional[str] = None
    timestamp: str = field(default_factory=now)


@dataclass
class Trajectory:
    """
    [P] Traceable update history.

    A Trajectory can change phase, branch, become dormant, dissolve, and be used as
    provenance for a re-emergent trajectory. These operations demonstrate
    'trajectory-centered, but not trajectory-fixed'; they do not define a universal
    ontology of trajectory identity.
    """

    label: str
    id: str = field(default_factory=lambda: uid("traj"))
    phase: Phase = Phase.BIRTH
    points: List[TrajectoryPoint] = field(default_factory=list)
    provenance: List[ProvenanceEvent] = field(default_factory=list)
    parent_trajectory_ids: List[str] = field(default_factory=list)

    def record(self, point: TrajectoryPoint) -> None:
        if self.phase == Phase.DISSOLUTION:
            raise RuntimeError("Cannot append to a dissolved trajectory; create a re-emergent trajectory instead.")
        self.points.append(point)
        if self.phase in (Phase.BIRTH, Phase.DORMANCY, Phase.REEMERGENCE):
            self.phase = Phase.PERSISTENCE
        self.provenance.append(
            ProvenanceEvent(
                event_type="trajectory_record",
                description=point.event.description,
                source_ids=[point.event.id],
            )
        )

    def transition(self, phase: Phase, reason: str) -> None:
        old = self.phase
        self.phase = phase
        self.provenance.append(
            ProvenanceEvent(
                event_type="phase_transition",
                description=f"{old.value} -> {phase.value}: {reason}",
                source_ids=[self.id],
            )
        )

    def branch(self, label: str, reason: str) -> "Trajectory":
        child = Trajectory(
            label=label,
            phase=Phase.BIRTH,
            parent_trajectory_ids=[self.id],
        )
        child.provenance.append(
            ProvenanceEvent(
                event_type="trajectory_branch",
                description=reason,
                source_ids=[self.id],
            )
        )
        self.provenance.append(
            ProvenanceEvent(
                event_type="branch_source",
                description=f"Branched to {child.id}: {reason}",
                source_ids=[child.id],
            )
        )
        return child

    def reemerge(self, label: str, reason: str) -> "Trajectory":
        """[O/P] Creates a new trace linked to an earlier one; identity is not asserted."""
        child = Trajectory(
            label=label,
            phase=Phase.REEMERGENCE,
            parent_trajectory_ids=[self.id],
        )
        child.provenance.append(
            ProvenanceEvent(
                event_type="trajectory_reemergence",
                description=reason,
                source_ids=[self.id],
            )
        )
        return child


# -----------------------------------------------------------------------------
# Updating Unit
# -----------------------------------------------------------------------------

@dataclass
class UpdatingUnit:
    """[P/O] Temporarily identifiable organization of updating processes."""

    name: str
    unit_type: str
    frame: ReferenceFrame
    boundary: Boundary
    possibility_space: PossibilitySpace
    trajectory: Trajectory
    measurement: MeasurementSystem = field(default_factory=MeasurementSystem)
    id: str = field(default_factory=lambda: uid("unit"))
    component_ids: List[str] = field(default_factory=list)
    residuals: Dict[str, Residual] = field(default_factory=dict)
    holdings: List[HoldingState] = field(default_factory=list)
    reopening_history: List[ReopeningDecision] = field(default_factory=list)

    def contact_reality(
        self,
        contact: RealityContact,
        *,
        expected: Optional[Any] = None,
        residual_criterion: Optional[ResidualCriterion] = None,
    ) -> Optional[Residual]:
        """
        [P] Minimal mediated Reality-contact path.

        Mismatch creates Difference. Difference becomes Residual only through an
        explicit replaceable criterion. This avoids hard-coding Difference = Residual.
        """
        self.trajectory.provenance.append(
            ProvenanceEvent(
                event_type="reality_contact",
                description=f"Contact via {contact.source} ({contact.mode})",
                source_ids=[contact.id],
            )
        )
        if expected is None or expected == contact.observation:
            return None

        difference = Difference(
            description=f"Expected {expected!r}, observed {contact.observation!r}"
        )
        # [O] A mismatch is not promoted to Residual by default.
        # Promotion requires an explicit, replaceable criterion.
        if residual_criterion is None:
            self.trajectory.provenance.append(
                ProvenanceEvent(
                    event_type="difference_unclassified",
                    description=difference.description,
                    source_ids=[difference.id, contact.id],
                )
            )
            return None
        criterion = residual_criterion
        if not criterion.evaluate(self, contact, expected, difference):
            self.trajectory.provenance.append(
                ProvenanceEvent(
                    event_type="difference_not_promoted",
                    description=difference.description,
                    source_ids=[difference.id, contact.id],
                )
            )
            return None

        residual = Residual(
            description=f"Difference treated as unresolved relative to frame '{self.frame.name}'",
            difference=difference,
        )
        self.residuals[residual.id] = residual
        self.trajectory.provenance.append(
            ProvenanceEvent(
                event_type="residual_registered",
                description=residual.description,
                source_ids=[contact.id, difference.id, residual.id],
            )
        )
        return residual

    def hold(
        self,
        residuals: Sequence[Residual],
        *,
        interpretations: Sequence[str] = (),
        reason: str = "unresolved",
    ) -> HoldingState:
        state = HoldingState(
            residual_ids=[r.id for r in residuals],
            competing_interpretations=list(interpretations),
            reason=reason,
        )
        self.holdings.append(state)
        self.trajectory.provenance.append(
            ProvenanceEvent(
                event_type="holding",
                description=f"Holding {len(state.residual_ids)} residual(s): {reason}",
                source_ids=state.residual_ids,
            )
        )
        return state

    def update(
        self,
        level: UpdateLevel,
        description: str,
        *,
        residuals: Sequence[Residual] = (),
        new_frame: Optional[ReferenceFrame] = None,
        new_boundary: Optional[Boundary] = None,
        new_possibility_space: Optional[PossibilitySpace] = None,
        new_measurement: Optional[MeasurementSystem] = None,
        reversible: Optional[bool] = None,
    ) -> UpdateEvent:
        old_frame = self.frame
        old_boundary = self.boundary
        old_space = self.possibility_space
        old_measurement = self.measurement

        event = UpdateEvent(
            level=level,
            description=description,
            residual_ids=[r.id for r in residuals],
            reversible=reversible,
        )

        if new_frame is not None:
            self.frame = new_frame
        if new_boundary is not None:
            self.boundary = new_boundary
        if new_possibility_space is not None:
            self.possibility_space = new_possibility_space
        if new_measurement is not None:
            self.measurement = new_measurement

        # [O] Update does not automatically mean that its motivating Residuals
        # have been resolved. Resolution requires a separate explicit judgment.

        self.trajectory.record(
            TrajectoryPoint(
                event=event,
                frame_id=self.frame.id,
                boundary_id=self.boundary.id,
                possibility_space_id=self.possibility_space.id,
                measurement_id=self.measurement.id,
            )
        )

        if self.frame.id != old_frame.id:
            self.trajectory.provenance.append(
                ProvenanceEvent("frame_revision", description, [old_frame.id, self.frame.id])
            )
        if self.boundary.id != old_boundary.id:
            self.trajectory.provenance.append(
                ProvenanceEvent("boundary_revision", description, [old_boundary.id, self.boundary.id])
            )
        if self.possibility_space.id != old_space.id:
            self.trajectory.provenance.append(
                ProvenanceEvent("possibility_space_revision", description, [old_space.id, self.possibility_space.id])
            )
        if self.measurement.id != old_measurement.id:
            self.trajectory.provenance.append(
                ProvenanceEvent("measurement_revision", description, [old_measurement.id, self.measurement.id])
            )
        return event

    def resolve_residuals(
        self, residuals: Sequence[Residual], *, reason: str
    ) -> None:
        """[P/O] Explicitly records a provisional judgment that Residuals are resolved."""
        ids = []
        for residual in residuals:
            if residual.id in self.residuals:
                residual.resolved = True
                ids.append(residual.id)
        touched = set(ids)
        for holding in self.holdings:
            if holding.active and touched.intersection(holding.residual_ids):
                holding.active = False
        self.trajectory.provenance.append(
            ProvenanceEvent(
                event_type="residual_resolution_judgment",
                description=reason,
                source_ids=ids,
            )
        )

    def recontact(
        self,
        contact: RealityContact,
        *,
        expected: Optional[Any] = None,
        residual_criterion: Optional[ResidualCriterion] = None,
    ) -> Optional[Residual]:
        """[P] Explicit semantic alias emphasizing recursive return to Reality contact."""
        return self.contact_reality(
            contact,
            expected=expected,
            residual_criterion=residual_criterion,
        )


    def reopen(
        self,
        *,
        assessment: FutureUpdateabilityAssessment,
        action: ReopeningAction,
        basis: str,
        decision_rule_reopened: str,
        evidence_ids: Sequence[str] = (),
    ) -> ReopeningDecision:
        """
        [P] Complete the Q2 second-order step after recontact.

        This method intentionally does not require reconfiguration.
        "Maintain" is a valid result if the prior decision/rule was genuinely
        reconsidered against Reality and deliberately selected again.
        """
        decision = ReopeningDecision(
            action=action,
            assessment=assessment,
            basis=basis,
            decision_rule_reopened=decision_rule_reopened,
            evidence_ids=list(evidence_ids),
        )
        self.reopening_history.append(decision)
        self.trajectory.provenance.append(
            ProvenanceEvent(
                event_type="reopening",
                description=(
                    f"Reopened '{decision_rule_reopened}' -> {action.value}; "
                    f"future updateability={assessment.status.value}. {basis}"
                ),
                source_ids=[assessment.id, decision.id] + list(evidence_ids),
            )
        )
        return decision


# -----------------------------------------------------------------------------
# Coupling and Enactment
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Coupling:
    trajectory_ids: List[str]
    description: str
    directionality: str = "mutual"
    strength: Optional[float] = None
    id: str = field(default_factory=lambda: uid("coupling"))


class EnactmentCriterion(Protocol):
    """[O] No universal enactment criterion is claimed."""

    def evaluate(self, units: Sequence[UpdatingUnit], coupling: Coupling) -> bool: ...


class ExplicitAuthorizationCriterion:
    """[P] Demo criterion only. Authorization is not a theory of emergence or agency."""

    def __init__(self, authorized: bool):
        self.authorized = authorized

    def evaluate(self, units: Sequence[UpdatingUnit], coupling: Coupling) -> bool:
        return self.authorized and len(units) >= 2


def enact_higher_order_unit(
    name: str,
    units: Sequence[UpdatingUnit],
    coupling: Coupling,
    criterion: EnactmentCriterion,
) -> Optional[UpdatingUnit]:
    """
    [P/O] Demonstrates Physical Entity != Updating Unit.

    Coupling alone does not enact a unit. No Agency is inferred here.
    """
    if not criterion.evaluate(units, coupling):
        return None

    frame = ReferenceFrame(
        name=f"{name} shared provisional frame",
        assumptions=["component frames remain distinct"],
    )
    boundary = Boundary(
        included=[u.id for u in units],
        permeability=None,  # [O] No universal permeability value is asserted.
    )
    possibilities = PossibilitySpace(
        actions=["joint inquiry", "independent action"],
        relations=["coordinate without unification"],
    )
    trajectory = Trajectory(
        label=f"{name} higher-order trajectory",
        phase=Phase.ENACTMENT,
        parent_trajectory_ids=[u.trajectory.id for u in units],
    )
    trajectory.provenance.append(
        ProvenanceEvent(
            event_type="enactment",
            description=f"Provisional enactment from coupling {coupling.id}",
            source_ids=[coupling.id] + [u.trajectory.id for u in units],
        )
    )
    return UpdatingUnit(
        name=name,
        unit_type="higher_order",
        frame=frame,
        boundary=boundary,
        possibility_space=possibilities,
        trajectory=trajectory,
        measurement=MeasurementSystem(
            name=f"{name} provisional measurement",
            observer="higher-order provisional observer",
            metrics=["cross-unit difference", "recontact evidence"],
            assumptions=["component measurements remain distinct"],
        ),
        component_ids=[u.id for u in units],
    )


# -----------------------------------------------------------------------------
# Common Dynamics Protocol (CDP)
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class CDPDescription:
    unit_id: str
    trajectory_id: str
    phase: str
    frame_name: str
    boundary_version: int
    possibility_space_version: int
    measurement_version: int
    unresolved_residuals: int
    active_holdings: int
    reopening_count: int
    latest_future_updateability: Optional[str]
    component_ids: List[str]
    epistemic_status: EpistemicStatus = EpistemicStatus.PROVISIONAL


class CommonDynamicsProtocol:
    """[P] Candidate interoperability layer; not a universal semantic protocol."""

    def describe(self, unit: UpdatingUnit) -> CDPDescription:
        return CDPDescription(
            unit_id=unit.id,
            trajectory_id=unit.trajectory.id,
            phase=unit.trajectory.phase.value,
            frame_name=unit.frame.name,
            boundary_version=unit.boundary.version,
            possibility_space_version=unit.possibility_space.version,
            measurement_version=unit.measurement.version,
            unresolved_residuals=sum(not r.resolved for r in unit.residuals.values()),
            active_holdings=sum(h.active for h in unit.holdings),
            reopening_count=len(unit.reopening_history),
            latest_future_updateability=(
                unit.reopening_history[-1].assessment.status.value
                if unit.reopening_history else None
            ),
            component_ids=list(unit.component_ids),
        )

    def translate(self, description: CDPDescription, target_label: str) -> Dict[str, Any]:
        """[P/O] Partial translation; internal semantics are deliberately not unified."""
        return {
            "target": target_label,
            "source_unit": description.unit_id,
            "dynamic_state": {
                "phase": description.phase,
                "frame": description.frame_name,
                "unresolved_residuals": description.unresolved_residuals,
                "active_holdings": description.active_holdings,
                "measurement_version": description.measurement_version,
                "reopening_count": description.reopening_count,
                "latest_future_updateability": description.latest_future_updateability,
            },
            "translation_quality": "partial",
            "translation_residual": "Internal semantics and values are not assumed equivalent.",
        }

    def compare(self, a: CDPDescription, b: CDPDescription) -> Dict[str, Any]:
        return {
            "same_phase": a.phase == b.phase,
            "same_frame_name": a.frame_name == b.frame_name,
            "residual_difference": a.unresolved_residuals - b.unresolved_residuals,
            "both_holding": a.active_holdings > 0 and b.active_holdings > 0,
            "measurement_version_difference": a.measurement_version - b.measurement_version,
            "future_updateability_equal": (
                a.latest_future_updateability == b.latest_future_updateability
            ),
            "note": "Comparison does not imply identical internal representation.",
        }

    def coordinate(self, a: UpdatingUnit, b: UpdatingUnit, purpose: str) -> Coupling:
        return Coupling(
            trajectory_ids=[a.trajectory.id, b.trajectory.id],
            description=purpose,
        )

    def trace(self, unit: UpdatingUnit) -> List[Dict[str, Any]]:
        """Traceability only. Provenance does not prove trajectory identity or causality."""
        return [asdict(event) for event in unit.trajectory.provenance]

    def recontact(
        self,
        unit: UpdatingUnit,
        contact: RealityContact,
        *,
        expected: Optional[Any] = None,
        residual_criterion: Optional[ResidualCriterion] = None,
    ) -> Optional[Residual]:
        return unit.recontact(
            contact,
            expected=expected,
            residual_criterion=residual_criterion,
        )


# -----------------------------------------------------------------------------
# Construction and executable demonstration
# -----------------------------------------------------------------------------


def make_unit(name: str, unit_type: str, frame_name: str) -> UpdatingUnit:
    unit = UpdatingUnit(
        name=name,
        unit_type=unit_type,
        frame=ReferenceFrame(frame_name),
        boundary=Boundary(included=[name]),
        possibility_space=PossibilitySpace(actions=["observe", "act", "hold", "reopen"]),
        trajectory=Trajectory(label=f"{name} trajectory"),
        measurement=MeasurementSystem(
            name=f"{name} measurement",
            observer=name,
            metrics=["difference", "residual", "future updateability"],
        ),
    )
    unit.trajectory.provenance.append(
        ProvenanceEvent(
            event_type="unit_initialized",
            description=f"Initialized {unit_type} updating unit '{name}'",
            source_ids=[unit.id],
        )
    )
    return unit



def architecture_manifest() -> Dict[str, Any]:
    """
    [D/P] Machine-readable statement of what this reference implementation
    treats as central, derived/repositioned, and operational.

    This is not a claim that the manifest is the ontology of intelligence.
    """
    return {
        "version": "1.1",
        "baseline": "MASTER_MAP_v1.1",
        "q1": "Can the system remain capable of changing how it changes?",
        "q2": (
            "Maintain and reconfigure the capacity of evolving heterogeneous systems "
            "to update again without losing contact with Reality."
        ),
        "design_principles": [
            "Difference without Isolation",
            "Connection without Unification",
            "Update without Erasure",
        ],
        "surviving_core_candidates": [
            "Updating Unit",
            "Dynamic Boundary",
            "Trajectory",
            "Reference Frame",
            "Measurement",
            "Provenance",
            "Future Updateability",
        ],
        "repositioned_constructs": {
            "Residual": "diagnostic form of Difference",
            "Holding": "domain-specific update mechanism",
            "Possibility Space": "generative extension",
            "12PDM": "dynamic observation/description protocol",
            "CDP": "relational/application interoperability layer",
        },
        "minimum_operational_loop": [
            "Detect",
            "Preserve",
            "Update",
            "Trace",
            "Recontact",
            "Reopen",
        ],
        "reopening_actions": [a.value for a in ReopeningAction],
        "non_equivalences": [
            "Current Performance != Future Updateability",
            "Reopening != Reconfiguration",
            "Provenance != Causality",
            "Meaning Unification != Interoperability",
            "Physical Entity != Updating Unit",
        ],
    }


def demo() -> Dict[str, Any]:
    print("IDOS Executable Reference Architecture v1.1")
    print("Executable != validated\n")

    human = make_unit("Human", "human", "Efficiency-first frame")
    ai = make_unit("AI", "ai", "Optimization frame")

    # 1. Mediated Reality contact -> Difference -> explicitly accepted Residual.
    contact = RealityContact(
        source="joint task outcome",
        observation="higher efficiency but reduced option diversity",
    )
    residual = human.contact_reality(
        contact,
        expected="higher efficiency with preserved option diversity",
        residual_criterion=ExplicitMismatchCriterion(True),
    )
    assert residual is not None

    # 2. Holding keeps multiple interpretations open temporarily.
    human.hold(
        [residual],
        interpretations=[
            "the optimization objective is incomplete",
            "the reference frame may be too narrow",
        ],
    )

    # 3. A deeper update changes frame, boundary, and possibility space.
    revised_frame = human.frame.revise(
        name="Efficiency-and-optionality frame",
        add_assumptions=["future option diversity matters"],
    )
    revised_boundary = human.boundary.revise(
        include=["AI advisory process"],
        permeability=0.65,
    )
    revised_space = human.possibility_space.revise(
        actions=["test alternative objective", "preserve minority option", "reopen prior decision"],
        frames=["optionality-sensitive frame"],
    )
    revised_measurement = human.measurement.revise(
        add_metrics=["option diversity", "override availability", "recontact quality"],
        add_assumptions=["measurement itself may need revision"],
    )
    human.update(
        UpdateLevel.L3,
        "Revised frame and measurement after holding unresolved residual",
        residuals=[residual],
        new_frame=revised_frame,
        new_boundary=revised_boundary,
        new_possibility_space=revised_space,
        new_measurement=revised_measurement,
    )

    # 4. Reality re-contact: the revised frame is exposed again to a new outcome.
    recontact = RealityContact(
        source="follow-up task outcome",
        observation="efficiency retained and option diversity partially restored",
    )
    second_residual = human.recontact(
        recontact,
        expected="efficiency retained and option diversity partially restored",
    )
    assert second_residual is None
    human.resolve_residuals(
        [residual],
        reason="Follow-up Reality contact provisionally supports treating the earlier Residual as resolved.",
    )

    # 5. Q2 / Reopening: evaluate whether the system can update again.
    fu = FutureUpdateabilityAssessment(
        status=FutureUpdateabilityStatus.PRESERVED,
        can_detect_new_difference=True,
        alternatives_can_emerge=True,
        override_or_revision_exists=True,
        irreversible_dependency_increased=False,
        reality_recontact_route_exists=True,
        updating_structure_can_change=True,
        rationale=(
            "The updated system retains independent detection, alternative actions, "
            "override, Reality recontact, and revisable updating structure."
        ),
    )
    reopening = human.reopen(
        assessment=fu,
        action=ReopeningAction.MAINTAIN,
        basis=(
            "Follow-up evidence supports maintaining the current rule for now; "
            "maintenance is deliberate, not automatic closure."
        ),
        decision_rule_reopened="efficiency-and-optionality decision rule",
        evidence_ids=[contact.id, recontact.id],
    )

    # 6. CDP coordinates trajectories; Coupling alone does not enact a new unit.
    cdp = CommonDynamicsProtocol()
    coupling = cdp.coordinate(
        human,
        ai,
        "Joint inquiry into efficiency versus future optionality",
    )
    rejected_joint = enact_higher_order_unit(
        "Rejected Human-AI Inquiry",
        [human, ai],
        coupling,
        ExplicitAuthorizationCriterion(authorized=False),
    )
    assert rejected_joint is None

    # 7. A replaceable demo criterion permits provisional higher-order enactment.
    joint = enact_higher_order_unit(
        "Human-AI Inquiry",
        [human, ai],
        coupling,
        ExplicitAuthorizationCriterion(authorized=True),
    )
    assert joint is not None
    assert set(joint.component_ids) == {human.id, ai.id}

    # 8. Trajectory is not fixed: branch, dormancy, dissolution, and linked re-emergence.
    branch = human.trajectory.branch(
        "Human alternative inquiry trajectory",
        "Preserve an alternative line of inquiry without asserting identity equivalence.",
    )
    branch.transition(Phase.DORMANCY, "Alternative inquiry paused")
    branch.transition(Phase.DISSOLUTION, "This trace is no longer actively updated")
    reemergent = branch.reemerge(
        "Human re-emergent inquiry trajectory",
        "A later inquiry reuses historical provenance; sameness is not asserted.",
    )
    assert branch.id in reemergent.parent_trajectory_ids
    assert reemergent.id != branch.id

    human_desc = cdp.describe(human)
    ai_desc = cdp.describe(ai)
    joint_desc = cdp.describe(joint)

    result = {
        "architecture_manifest": architecture_manifest(),
        "human": asdict(human_desc),
        "ai": asdict(ai_desc),
        "comparison": cdp.compare(human_desc, ai_desc),
        "translation_to_ai": cdp.translate(human_desc, "AI"),
        "coupling": asdict(coupling),
        "coupling_without_enactment": rejected_joint is None,
        "higher_order_unit": asdict(joint_desc),
        "trajectory_nonfixity_demo": {
            "branch_id": branch.id,
            "branch_phase": branch.phase.value,
            "reemergent_id": reemergent.id,
            "reemergent_phase": reemergent.phase.value,
            "identity_claimed": False,
        },
        "future_updateability": asdict(fu),
        "reopening": asdict(reopening),
        "minimum_idos_cycle_complete": bool(human.reopening_history),
        "human_provenance": cdp.trace(human),
    }

    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return result


if __name__ == "__main__":
    demo()
