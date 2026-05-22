from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.mission import Mission, MissionPhase
from app.models.missionEvents import EventType, MissionEvent


EVENT_PHASE_MAP = {
    EventType.GO_FOR_PROP_LOAD: MissionPhase.PRELAUNCH.value,
    EventType.PROP_LOAD_COMPLETE: MissionPhase.PRELAUNCH.value,
    EventType.TERMINAL_COUNT: MissionPhase.PRELAUNCH.value,
    EventType.ENGINE_IGNITION: MissionPhase.ASCENT.value,
    EventType.LIFTOFF: MissionPhase.ASCENT.value,
    EventType.MAX_Q: MissionPhase.ASCENT.value,
    EventType.MECO: MissionPhase.ASCENT.value,
    EventType.STAGE_SEPARATION: MissionPhase.ASCENT.value,
    EventType.ENGINE_BURN: MissionPhase.ORBITAL_OPERATIONS.value,
    EventType.ORBITAL_INSERTION: MissionPhase.ORBITAL_OPERATIONS.value,
    EventType.COURSE_CORRECTION_BURN: MissionPhase.TRANSFER.value,
    EventType.DEORBIT_BURN: MissionPhase.APPROACH.value,
    EventType.ENTRY_INTERFACE: MissionPhase.APPROACH.value,
    EventType.LANDING_BURN: MissionPhase.LANDING.value,
    EventType.SHIP_LANDING: MissionPhase.SURFACE_OPERATIONS.value,
}


def derive_mission_phase(latest_event: MissionEvent | None, latest_mission: Mission | None) -> str | None:
    event_key = _event_type_value(latest_event.event_type) if latest_event else None
    if event_key:
        for event_type, mission_phase in EVENT_PHASE_MAP.items():
            if event_type.value == event_key:
                return mission_phase
    if latest_mission and latest_mission.phase:
        return latest_mission.phase.value if hasattr(latest_mission.phase, "value") else str(latest_mission.phase)
    return None


def sync_latest_mission_phase_from_event(db: Session, event: MissionEvent | None) -> Mission | None:
    if not event:
        return None
    event_key = _event_type_value(event.event_type)
    phase_value = next(
        (mission_phase for event_type, mission_phase in EVENT_PHASE_MAP.items() if event_type.value == event_key),
        None,
    )
    if not phase_value:
        return None

    latest_mission = db.query(Mission).order_by(Mission.start_time.desc()).first()
    if not latest_mission:
        return None

    latest_mission.phase = phase_value
    return latest_mission


def _event_type_value(event_type: object) -> str | None:
    if event_type is None:
        return None
    return event_type.value if hasattr(event_type, "value") else str(event_type)
