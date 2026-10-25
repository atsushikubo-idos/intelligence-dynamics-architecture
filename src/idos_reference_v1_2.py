from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json
from typing import Any, Dict, Iterable, List, Optional, Protocol, Sequence
from uuid import uuid4

"""
Intelligence Dynamics Architecture (IDOS)
Executable Reference Architecture v1.2 (v1.1-compatible; standalone)

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
        "version": "1.2-candidate",
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


# -----------------------------------------------------------------------------
# v1.2 additive social-connection layer — architectural candidates [P/O]
# No new primitive intelligence ontology is asserted. Evidence is not proof.
# -----------------------------------------------------------------------------

class ConnectionError(ValueError):
    """A claimed social connection conflicts with the registered reference objects."""


class ClaimStatus(str, Enum):
    PROPOSED = "proposed"
    ATTESTED = "attested"  # evidence recorded; not a determination of truth
    CONTESTED = "contested"
    WITHDRAWN = "withdrawn"


@dataclass(frozen=True)
class SourceGrounding:
    source_refs: tuple[str, ...]
    observer: str
    interpretation: str
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_refs or not all(x.strip() for x in self.source_refs):
            raise ConnectionError("Nonempty provenance references required")
        if not self.observer.strip() or not self.interpretation.strip():
            raise ConnectionError("Observer and interpretive statement required")


@dataclass(frozen=True)
class ScopeSnapshot:
    """Snapshot of the registered updating unit; an ID alone is insufficient."""
    unit_id: str
    trajectory_id: str
    frame_id: str
    boundary_id: str
    measurement_id: str
    possibility_space_id: str


@dataclass(frozen=True)
class AuthorityClaim:
    """Claims/evidence only: updating unit is not automatically agency or sovereign."""
    unit: ScopeSnapshot
    grounding: SourceGrounding
    agency_claim: Optional[str] = None
    sovereignty_claim: Optional[str] = None
    consent_evidence: tuple[str, ...] = ()
    exit_options: tuple[str, ...] = ()
    responsibility_claims: tuple[str, ...] = ()
    status: ClaimStatus = ClaimStatus.PROPOSED


@dataclass(frozen=True)
class PreArticulationReport:
    """A reported limitation of articulation, NOT an observation of the unobserved."""
    grounding: SourceGrounding
    category: str
    description: str
    open_questions: tuple[str, ...] = ()


@dataclass(frozen=True)
class RelationChange:
    id: str
    description: str
    evidence: SourceGrounding
    participant_state_changes: tuple[str, ...] = ()
    relation_only_changes: tuple[str, ...] = ()
    timestamp: str = field(default_factory=now)


@dataclass
class RelationDynamics:
    """Independent history ABOUT a relation, separate from its participants.

    Does not imply enactment, agency, or a higher-order UpdatingUnit.
    """
    coupling_id: str
    participant_unit_ids: tuple[str, ...]
    participant_trajectory_ids: tuple[str, ...]
    trajectory: Trajectory
    changes: List[RelationChange] = field(default_factory=list)

    def record(self, description: str, evidence: SourceGrounding,
               *, participant_state_changes: Sequence[str] = (),
               relation_only_changes: Sequence[str] = ()) -> RelationChange:
        if not description.strip():
            raise ConnectionError("Relation change description required")
        if not relation_only_changes and not participant_state_changes:
            raise ConnectionError("Describe what changed, including relation-only effects if applicable")
        change = RelationChange(
            id=uid("relation_change"), description=description, evidence=evidence,
            participant_state_changes=tuple(participant_state_changes),
            relation_only_changes=tuple(relation_only_changes),
        )
        self.changes.append(change)
        self.trajectory.provenance.append(ProvenanceEvent(
            event_type="relation_change_recorded", description=description,
            source_ids=[change.id, *evidence.source_refs, self.coupling_id],
        ))
        return change


class FrameGenesisStatus(str, Enum):
    PROPOSED = "proposed"
    ADOPTED = "adopted"
    REJECTED = "rejected"


@dataclass
class FrameGenesis:
    """Proposed-to-adopted frame emergence: adoption is not proof of Reality."""
    id: str
    origin_frame_ids: tuple[str, ...]
    candidate_name: str
    grounding: SourceGrounding
    status: FrameGenesisStatus = FrameGenesisStatus.PROPOSED
    adopted_frame_id: Optional[str] = None
    observability_evidence: List[str] = field(default_factory=list)


class AssetTransitionStatus(str, Enum):
    PROPOSED = "proposed"
    DOCUMENTED = "documented"  # documentation, not metaphysical continuity
    DISPUTED = "disputed"


@dataclass
class AssetBodyTransition:
    """Explicitly distinct origin and receiving unit; no identity is inferred."""
    id: str
    origin: ScopeSnapshot
    receiving: ScopeSnapshot
    asset_description: str
    new_body_role: str
    grounding: SourceGrounding
    status: AssetTransitionStatus = AssetTransitionStatus.PROPOSED
    evidence: List[str] = field(default_factory=list)
    nontransferable: List[str] = field(default_factory=list)
    responsibility_changes: List[str] = field(default_factory=list)


class SocialConnectionRegistry:
    """Typed, instance-local, fail-closed links to the existing v1.1 structures.

    Historical changes are not revalidated against a later unit state: each
    event carries snapshots; registered identity mappings are frozen per event.
    """
    def __init__(self) -> None:
        self.units: Dict[str, UpdatingUnit] = {}
        self.couplings: Dict[str, Coupling] = {}
        self.frames: Dict[str, ReferenceFrame] = {}
        self.relations: Dict[str, RelationDynamics] = {}
        self.geneses: Dict[str, FrameGenesis] = {}
        self.asset_transitions: Dict[str, AssetBodyTransition] = {}
        self.authority_claims: List[AuthorityClaim] = []
        self.pre_articulation_reports: List[PreArticulationReport] = []

    def register_unit(self, unit: UpdatingUnit) -> None:
        if unit.id in self.units and self.units[unit.id] is not unit:
            raise ConnectionError("Duplicate unit ID with different identity")
        if any(u.trajectory.id == unit.trajectory.id and u.id != unit.id for u in self.units.values()):
            raise ConnectionError("Ambiguous shared trajectory across units")
        self.units[unit.id] = unit
        self.register_frame(unit.frame)

    def register_frame(self, frame: ReferenceFrame) -> None:
        if frame.id in self.frames and self.frames[frame.id] != frame:
            raise ConnectionError("Frame ID collision")
        self.frames[frame.id] = frame

    def snapshot(self, unit_id: str) -> ScopeSnapshot:
        if unit_id not in self.units:
            raise ConnectionError(f"Unknown updating unit: {unit_id}")
        u = self.units[unit_id]
        self.register_frame(u.frame)
        return ScopeSnapshot(u.id, u.trajectory.id, u.frame.id, u.boundary.id,
                             u.measurement.id, u.possibility_space.id)

    def register_coupling(self, coupling: Coupling) -> None:
        if len(coupling.trajectory_ids) < 2 or len(set(coupling.trajectory_ids)) != len(coupling.trajectory_ids):
            raise ConnectionError("Coupling must specify at least two distinct trajectories")
        trajectories = {u.trajectory.id for u in self.units.values()}
        if not set(coupling.trajectory_ids).issubset(trajectories):
            raise ConnectionError("Coupling references an unregistered trajectory")
        if coupling.id in self.couplings and self.couplings[coupling.id] != coupling:
            raise ConnectionError("Coupling ID collision")
        self.couplings[coupling.id] = coupling

    def enact_relation_trace(self, coupling_id: str, participant_unit_ids: Sequence[str]) -> RelationDynamics:
        if coupling_id not in self.couplings:
            raise ConnectionError("Unknown coupling")
        if coupling_id in self.relations:
            raise ConnectionError("Relation trace already exists")
        if len(set(participant_unit_ids)) < 2 or len(set(participant_unit_ids)) != len(participant_unit_ids):
            raise ConnectionError("Participants must be distinct")
        snapshots = [self.snapshot(uid_) for uid_ in participant_unit_ids]
        actual = {s.trajectory_id for s in snapshots}
        expected = set(self.couplings[coupling_id].trajectory_ids)
        if actual != expected:
            raise ConnectionError("Relation participants do not match coupling trajectories")
        trace = Trajectory(label=f"relationship evidence trace {coupling_id}",
                           parent_trajectory_ids=[s.trajectory_id for s in snapshots])
        trace.provenance.append(ProvenanceEvent(
            event_type="relation_trace_opened", description="Evidence trace only; no enactment inferred",
            source_ids=[coupling_id, *trace.parent_trajectory_ids],
        ))
        rel = RelationDynamics(coupling_id, tuple(participant_unit_ids),
                               tuple(s.trajectory_id for s in snapshots), trace)
        self.relations[coupling_id] = rel
        return rel

    def propose_frame(self, origin_frame_ids: Sequence[str], candidate_name: str,
                      grounding: SourceGrounding) -> FrameGenesis:
        if not origin_frame_ids or any(x not in self.frames for x in origin_frame_ids):
            raise ConnectionError("Unknown origin frame")
        if not candidate_name.strip():
            raise ConnectionError("Candidate name required")
        event = FrameGenesis(uid("genesis"), tuple(origin_frame_ids), candidate_name, grounding)
        self.geneses[event.id] = event
        return event

    def adopt_frame(self, genesis_id: str, frame: ReferenceFrame, evidence: Sequence[str]) -> None:
        if genesis_id not in self.geneses:
            raise ConnectionError("Unknown frame proposal")
        event = self.geneses[genesis_id]
        if event.status != FrameGenesisStatus.PROPOSED:
            raise ConnectionError("Frame proposal already resolved")
        if not evidence:
            raise ConnectionError("Adoption requires explicit evidence")
        if frame.id in self.frames:
            raise ConnectionError("Adopted frame must have a fresh ID")
        # A new frame may have an origin but is not necessarily a revision.
        if frame.parent_id is not None and frame.parent_id not in event.origin_frame_ids:
            raise ConnectionError("Frame lineage contradicts proposal origins")
        self.register_frame(frame)
        event.status = FrameGenesisStatus.ADOPTED
        event.adopted_frame_id = frame.id
        event.observability_evidence.extend(evidence)

    def propose_asset_transition(self, origin_id: str, receiving_id: str,
                                 asset_description: str, body_role: str,
                                 grounding: SourceGrounding) -> AssetBodyTransition:
        if origin_id == receiving_id:
            raise ConnectionError("Cross-level transition requires distinct units")
        if not asset_description.strip() or not body_role.strip():
            raise ConnectionError("Asset and receiving role required")
        event = AssetBodyTransition(uid("asset_transition"), self.snapshot(origin_id),
                                    self.snapshot(receiving_id), asset_description,
                                    body_role, grounding)
        self.asset_transitions[event.id] = event
        return event

    def document_asset_transition(self, transition_id: str, *, evidence: Sequence[str],
                                  nontransferable: Sequence[str] = (),
                                  responsibility_changes: Sequence[str] = ()) -> None:
        if transition_id not in self.asset_transitions:
            raise ConnectionError("Unknown asset transition")
        event = self.asset_transitions[transition_id]
        if event.status != AssetTransitionStatus.PROPOSED:
            raise ConnectionError("Transition already resolved")
        if not evidence or not any(str(x).strip() for x in evidence):
            raise ConnectionError("Documentation must cite evidence")
        event.evidence.extend(evidence)
        event.nontransferable.extend(nontransferable)
        event.responsibility_changes.extend(responsibility_changes)
        event.status = AssetTransitionStatus.DOCUMENTED

    def add_authority_claim(self, unit_id: str, grounding: SourceGrounding,
                            **claims: Any) -> AuthorityClaim:
        record = AuthorityClaim(unit=self.snapshot(unit_id), grounding=grounding, **claims)
        self.authority_claims.append(record)
        return record

    def add_pre_articulation_report(self, report: PreArticulationReport) -> None:
        self.pre_articulation_reports.append(report)


def social_connection_manifest() -> Dict[str, Any]:
    return {
        "version": "1.2-candidate", "baseline": "Reference 1.1 (unchanged semantics)",
        "additions": ["validated social-reference registry", "relation-specific evidence trajectory",
                      "proposed/adopted reference-frame genesis", "cross-level asset/body evidence",
                      "non-assertive authority and pre-articulation records"],
        "not_claimed": ["social or legal validity", "sovereignty inferred from update",
                        "unobserved reality directly observed", "identity continuity",
                        "scientific validation"],
    }


def demo() -> Dict[str, Any]:
    print("IDOS Executable Reference Architecture v1.2 (v1.1-compatible; standalone)")
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



# -----------------------------------------------------------------------------
# v1.2 Dynamic Social Connection — evidence-linked cross-trajectory interactions
# Integrated into this file to support standalone archival publication.
# Recorded influence claims are not proofs of causality, identity or consent.
# -----------------------------------------------------------------------------

class NodeKind(str, Enum):
    RELATION_CHANGE = 'relation_change'
    FRAME_ADOPTION = 'frame_adoption'
    ASSET_DOCUMENTATION = 'asset_documentation'
    UNIT_UPDATE = 'unit_update'

class LinkKind(str, Enum):
    TEMPORAL = 'temporal_sequence'      # only event order, not influence
    ASSOCIATED = 'associated'            # relationship claimed but unresolved
    INFLUENCE_CLAIM = 'influence_claim' # explicit interpreted influence; not established causation
    CONTESTED = 'contested_influence'

@dataclass(frozen=True)
class ChangeNode:
    id: str
    kind: NodeKind
    trajectory_id: str
    ref_id: str
    evidence_refs: tuple[str, ...]
    description: str
    timestamp: str = field(default_factory=now)

@dataclass(frozen=True)
class InfluenceLink:
    id: str
    source_id: str
    target_id: str
    kind: LinkKind
    grounding: SourceGrounding
    rationale: str
    timestamp: str = field(default_factory=now)

class DynamicInteractionGraph:
    """Append-only evidence graph attached to the real registered v1.2 objects.

    Edges record attributed interpretations, not proven causality. A recorded
    node must match a real change/adoption/documentation/update at registration.
    """
    def __init__(self, registry: SocialConnectionRegistry):
        self.registry = registry
        self.nodes: Dict[str, ChangeNode] = {}
        self.links: Dict[str, InfluenceLink] = {}

    def _add(self, node: ChangeNode) -> ChangeNode:
        if node.id in self.nodes:
            raise ConnectionError('Duplicate graph node ID')
        if not node.evidence_refs or not all(e.strip() for e in node.evidence_refs):
            raise ConnectionError('Change node requires evidence references')
        self.nodes[node.id] = node
        return node

    def record_relation_change(self, coupling_id: str, change_id: str) -> ChangeNode:
        relation = self.registry.relations.get(coupling_id)
        if relation is None:
            raise ConnectionError('Unknown relation')
        change = next((c for c in relation.changes if c.id == change_id), None)
        if change is None:
            raise ConnectionError('Change does not belong to relation')
        return self._add(ChangeNode(change.id, NodeKind.RELATION_CHANGE,
            relation.trajectory.id, change.id, change.evidence.source_refs, change.description))

    def record_frame_adoption(self, genesis_id: str, adopting_unit_id: str) -> ChangeNode:
        genesis = self.registry.geneses.get(genesis_id)
        unit = self.registry.units.get(adopting_unit_id)
        if genesis is None or unit is None or genesis.status != FrameGenesisStatus.ADOPTED:
            raise ConnectionError('Unknown or unadopted frame genesis / unit')
        if unit.frame.id != genesis.adopted_frame_id:
            raise ConnectionError('Unit does not hold the adopted frame; record its update first')
        evidence = tuple(genesis.observability_evidence)
        return self._add(ChangeNode(f'frame_adoption:{genesis_id}:{adopting_unit_id}',
            NodeKind.FRAME_ADOPTION, unit.trajectory.id, genesis_id, evidence,
            f'Unit {adopting_unit_id} holds adopted frame {genesis.adopted_frame_id}'))

    def record_asset_documentation(self, transition_id: str) -> ChangeNode:
        transition = self.registry.asset_transitions.get(transition_id)
        if transition is None or transition.status != AssetTransitionStatus.DOCUMENTED:
            raise ConnectionError('Asset transition must be documented first')
        # Asset migration is not conflated with either party's trajectory.
        return self._add(ChangeNode(f'asset_documentation:{transition_id}',
            NodeKind.ASSET_DOCUMENTATION,
            f'cross_level:{transition.origin.trajectory_id}:{transition.receiving.trajectory_id}',
            transition_id, tuple(transition.evidence),
            f'Documented asset-to-body role: {transition.new_body_role}'))

    def record_unit_update(self, unit_id: str, update_id: str, evidence_refs: Sequence[str]) -> ChangeNode:
        unit = self.registry.units.get(unit_id)
        if unit is None:
            raise ConnectionError('Unknown unit')
        points = [p for p in unit.trajectory.points if p.event.id == update_id]
        if len(points) != 1:
            raise ConnectionError('Update event not found uniquely in unit trajectory')
        point = points[0]
        return self._add(ChangeNode(update_id, NodeKind.UNIT_UPDATE,
            unit.trajectory.id, update_id, tuple(evidence_refs), point.event.description))

    def link(self, source_id: str, target_id: str, kind: LinkKind,
             grounding: SourceGrounding, rationale: str) -> InfluenceLink:
        if source_id not in self.nodes or target_id not in self.nodes:
            raise ConnectionError('Both link endpoints must be registered change nodes')
        if source_id == target_id:
            raise ConnectionError('Self-links are unsupported')
        if not isinstance(kind, LinkKind):
            raise ConnectionError('Explicit link type required')
        if not rationale.strip():
            raise ConnectionError('Interpretation rationale required')
        if any(l.source_id == source_id and l.target_id == target_id and l.kind == kind
               for l in self.links.values()):
            raise ConnectionError('Duplicate edge assertion')
        edge = InfluenceLink(uid('link'), source_id, target_id, kind, grounding, rationale)
        self.links[edge.id] = edge
        return edge

    def incoming(self, node_id: str) -> List[InfluenceLink]:
        if node_id not in self.nodes: raise ConnectionError('Unknown node')
        return [e for e in self.links.values() if e.target_id == node_id]

    def outgoing(self, node_id: str) -> List[InfluenceLink]:
        if node_id not in self.nodes: raise ConnectionError('Unknown node')
        return [e for e in self.links.values() if e.source_id == node_id]

    def trace_back(self, node_id: str) -> dict:
        """Walk registered claims; no inferred transitive causality."""
        if node_id not in self.nodes: raise ConnectionError('Unknown node')
        visited = set(); edges = []
        def walk(current: str) -> None:
            if current in visited: return
            visited.add(current)
            for edge in self.incoming(current):
                edges.append(edge)
                walk(edge.source_id)
        walk(node_id)
        return {'nodes': [self.nodes[n] for n in visited], 'links': edges,
                'notice': 'Trace of recorded claims, NOT proof of causality or identity.'}


if __name__ == "__main__":
    demo()
