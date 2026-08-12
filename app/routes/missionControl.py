from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alertSystem import AlertSystem, AlertType
from app.models.crew import Crew
from app.models.groundControlLog import GroundControlLog
from app.models.mission import Mission, MissionPhase
from app.models.missionEvents import EventType, MissionEvent
from app.models.navigationSystem import NavigationSystem
from app.models.planet import Planet
from app.models.spacecraft import Spacecraft
from app.models.spacecraftStatus import SpacecraftStatus
from app.services.missionState import derive_mission_phase
from app.schemas.missionControl import (
    DemoBootstrapResponse,
    MissionAlertEntry,
    MissionCelestialContext,
    MissionControlOverview,
    MissionCrewEntry,
    MissionCrewSummary,
    MissionOverviewMetrics,
    MissionOverviewSnapshot,
    MissionPlanetSummary,
    MissionSpacecraftSummary,
    MissionTimelineEntry,
)

router = APIRouter()


PLANET_CONTEXT = {
    "miller": {
        "gravity_source": "Gargantua",
        "orbital_sector": "Accretion Corridor A",
        "time_dilation_ratio": "01 hr : 07 yrs",
    },
    "edmunds": {
        "gravity_source": "Gargantua",
        "orbital_sector": "Habitable Survey Corridor",
        "time_dilation_ratio": "Moderate relativistic offset",
    },
    "mann": {
        "gravity_source": "Gargantua",
        "orbital_sector": "Cryosphere Recon Corridor",
        "time_dilation_ratio": "Moderate relativistic offset",
    },
}


def derive_active_planet(
    latest_navigation: NavigationSystem | None,
    planets: list[Planet],
) -> Planet | None:
    target_hint = (latest_navigation.target_waypoint or "").lower() if latest_navigation else ""
    for planet in planets:
        planet_name = (planet.name or "").lower()
        if planet_name and planet_name in target_hint:
            return planet

    if "landing zone alpha" in target_hint:
        for planet in planets:
            if (planet.name or "").lower() == "miller":
                return planet

    return planets[0] if planets else None


def build_celestial_context(
    active_planet: Planet | None,
    latest_navigation: NavigationSystem | None,
) -> MissionCelestialContext:
    planet_key = (active_planet.name or "").lower() if active_planet else ""
    defaults = PLANET_CONTEXT.get(planet_key, {})
    return MissionCelestialContext(
        gravity_source=defaults.get("gravity_source", "Deep Space Transit"),
        orbital_sector=defaults.get("orbital_sector", "Transfer Corridor"),
        time_dilation_ratio=defaults.get("time_dilation_ratio", "Nominal"),
        target_body=active_planet.name if active_planet else None,
        target_waypoint=latest_navigation.target_waypoint if latest_navigation else None,
    )


def evaluate_readiness(
    latest_status: SpacecraftStatus | None,
    active_alert_models: list[AlertSystem],
    latest_navigation: NavigationSystem | None,
) -> tuple[str, str]:
    critical_alert_count = sum(1 for alert in active_alert_models if alert.alert_type == AlertType.CRITICAL)
    warning_alert_count = sum(1 for alert in active_alert_models if alert.alert_type == AlertType.WARNING)

    if not latest_status or not latest_status.is_operational:
        return "degraded", "Spacecraft status reports degraded or unavailable operations."

    if critical_alert_count > 0:
        return "degraded", "One or more unresolved critical alerts require immediate mission control action."

    if latest_navigation:
        if (
            latest_navigation.alignment_error_deg is not None
            and latest_navigation.alignment_error_deg > 1.0
        ) or (
            latest_navigation.residual_drift_km is not None
            and latest_navigation.residual_drift_km > 20.0
        ):
            return "degraded", "Navigation solution is outside course-correction safety limits."

        if (
            latest_navigation.alignment_error_deg is not None
            and latest_navigation.alignment_error_deg > 0.25
        ) or (
            latest_navigation.residual_drift_km is not None
            and latest_navigation.residual_drift_km > 5.0
        ):
            return "monitoring", "Navigation drift is elevated and remains under active monitoring."

    if warning_alert_count > 0:
        return "monitoring", "Open warning alerts remain under active review."

    return "nominal", "All monitored systems remain within current mission thresholds."


@router.get("/mission-control/overview", response_model=MissionControlOverview, tags=["Mission Control"])
def get_mission_control_overview(db: Session = Depends(get_db)):
    mission_count = db.query(Mission).count()
    spacecraft_count = db.query(Spacecraft).count()
    crew_count = db.query(Crew).count()
    active_alert_models = (
        db.query(AlertSystem)
        .filter(AlertSystem.resolved.is_(False))
        .order_by(AlertSystem.timestamp.desc())
        .all()
    )
    critical_alert_count = sum(1 for alert in active_alert_models if alert.alert_type == AlertType.CRITICAL)

    latest_mission = db.query(Mission).order_by(Mission.start_time.desc()).first()
    latest_spacecraft = db.query(Spacecraft).order_by(Spacecraft.created_at.desc()).first()
    latest_status = db.query(SpacecraftStatus).order_by(SpacecraftStatus.timestamp.desc()).first()
    recent_events = db.query(MissionEvent).order_by(MissionEvent.timestamp.desc()).limit(5).all()
    latest_event = db.query(MissionEvent).order_by(MissionEvent.timestamp.desc()).first()
    latest_navigation = db.query(NavigationSystem).order_by(NavigationSystem.last_correction_at.desc()).first()
    planets = (
        db.query(Planet)
        .order_by(Planet.habitability_score.is_(None), Planet.habitability_score.desc(), Planet.name.asc())
        .all()
    )
    crew_query = db.query(Crew)
    if latest_mission:
        crew_query = crew_query.filter(Crew.mission_id == latest_mission.id)
    crew_manifest = crew_query.order_by(Crew.id.asc()).all()
    course_correction_count = (
        db.query(MissionEvent)
        .filter(MissionEvent.event_type == EventType.COURSE_CORRECTION_BURN)
        .count()
    )
    mission_phase = derive_mission_phase(latest_event, latest_mission)
    readiness, readiness_reason = evaluate_readiness(latest_status, active_alert_models, latest_navigation)
    active_planet = derive_active_planet(latest_navigation, planets)
    celestial_context = build_celestial_context(active_planet, latest_navigation)
    commander = next((member.name for member in crew_manifest if "commander" in member.role.lower()), None)
    lead_scientist = next((member.name for member in crew_manifest if "scientist" in member.role.lower()), None)

    snapshot = MissionOverviewSnapshot(
        mission_name=latest_mission.name if latest_mission else None,
        mission_status=latest_mission.status if latest_mission else None,
        mission_phase=mission_phase,
        spacecraft_name=latest_spacecraft.name if latest_spacecraft else None,
        spacecraft_status=latest_spacecraft.status if latest_spacecraft else None,
        current_flight_stage=latest_event.event_type.value if latest_event else None,
        current_target=latest_navigation.target_waypoint if latest_navigation else None,
        course_corrections_executed=course_correction_count,
        readiness_reason=readiness_reason,
        navigation_status=(
            latest_navigation.navigation_system_status.value
            if latest_navigation and hasattr(latest_navigation.navigation_system_status, "value")
            else latest_navigation.navigation_system_status if latest_navigation else None
        ),
        alignment_error_deg=latest_navigation.alignment_error_deg if latest_navigation else None,
        residual_drift_km=latest_navigation.residual_drift_km if latest_navigation else None,
        latest_status_timestamp=latest_status.timestamp if latest_status else None,
        fuel_level=latest_status.fuel_level if latest_status else None,
        oxygen_level=latest_status.oxygen_level if latest_status else None,
        cabin_temperature=latest_status.temperature if latest_status else None,
        cabin_pressure=latest_status.pressure if latest_status else None,
    )

    return MissionControlOverview(
        generated_at=datetime.utcnow(),
        operational_readiness=readiness,
        metrics=MissionOverviewMetrics(
            missions=mission_count,
            spacecraft=spacecraft_count,
            crew_members=crew_count,
            active_alerts=len(active_alert_models),
            critical_alerts=critical_alert_count,
        ),
        latest_snapshot=snapshot,
        celestial_context=celestial_context,
        active_planet=(
            MissionPlanetSummary(
                name=active_planet.name,
                type=active_planet.type,
                gravity=active_planet.gravity,
                atmosphere=active_planet.atmosphere,
                surface_temperature=active_planet.surface_temperature,
                habitability_score=active_planet.habitability_score,
                description=active_planet.description,
            )
            if active_planet
            else None
        ),
        crew_summary=MissionCrewSummary(
            total_active=len(crew_manifest),
            commander=commander,
            lead_scientist=lead_scientist,
            crew_manifest=[
                MissionCrewEntry(name=member.name, role=member.role)
                for member in crew_manifest
            ],
            support_units=["TARS", "CASE"],
        ),
        spacecraft_summary=MissionSpacecraftSummary(
            name=latest_spacecraft.name if latest_spacecraft else None,
            registry_code=latest_spacecraft.registry_code if latest_spacecraft else None,
            vehicle_class=latest_spacecraft.vehicle_class if latest_spacecraft else None,
            manufacturer=latest_spacecraft.manufacturer if latest_spacecraft else None,
            mission_profile=latest_spacecraft.mission_profile if latest_spacecraft else None,
            home_base=latest_spacecraft.home_base if latest_spacecraft else None,
            status=latest_spacecraft.status if latest_spacecraft else None,
        ),
        recent_events=[
            MissionTimelineEntry(
                timestamp=event.timestamp,
                event_type=event.event_type.value if hasattr(event.event_type, "value") else str(event.event_type),
                description=event.description,
            )
            for event in recent_events
        ],
        active_alerts=[
            MissionAlertEntry(
                timestamp=alert.timestamp,
                severity=alert.alert_type.value if hasattr(alert.alert_type, "value") else str(alert.alert_type),
                system=alert.system,
                message=alert.message,
                spacecraft_id=alert.spacecraft_id,
            )
            for alert in active_alert_models[:5]
        ],
    )


@router.post("/demo/bootstrap", response_model=DemoBootstrapResponse, tags=["Demo Data"])
def bootstrap_demo_data(db: Session = Depends(get_db)):
    spacecraft = db.query(Spacecraft).filter(Spacecraft.registry_code == "END-PRIME-01").first()
    if spacecraft:
        mission = db.query(Mission).filter(Mission.name == "Lazarus Relay Expedition").first()
        return DemoBootstrapResponse(
            detail="Demo dataset already available.",
            mission_id=mission.id if mission else 0,
            spacecraft_id=spacecraft.id,
        )

    spacecraft = Spacecraft(
        name="Endurance",
        registry_code="END-PRIME-01",
        vehicle_class="Interstellar endurance vehicle",
        manufacturer="NASA / Lazarus Program",
        status="landed-and-safe",
        mission_profile="Launch, orbital transfer, course correction, descent and landing operations",
        home_base="Launch and Recovery Complex 39A",
    )
    mission = Mission(
        name="Lazarus Relay Expedition",
        status="ship_landed",
        phase=MissionPhase.SURFACE_OPERATIONS,
        start_time=datetime(2067, 4, 12, 8, 15),
    )
    planets = [
        Planet(
            name="Miller",
            description="Ocean world with extreme time dilation near Gargantua.",
            type="water_world",
            distance_from_earth_km=1.2e14,
            has_life=False,
            surface_temperature=4.0,
            discovered_by="Lazarus Program",
            gravity=1.3,
            atmosphere="Dense vapor and saline aerosols",
            habitability_score=0.42,
        ),
        Planet(
            name="Edmunds",
            description="Candidate habitable world with frozen terrain and nitrogen-rich atmosphere.",
            type="terrestrial",
            distance_from_earth_km=1.2e14,
            has_life=False,
            surface_temperature=-18.0,
            discovered_by="Lazarus Program",
            gravity=0.93,
            atmosphere="Nitrogen-oxygen trace mix",
            habitability_score=0.81,
        ),
        Planet(
            name="Mann",
            description="Ice planet with deceptive surface stability and severe atmospheric hazards.",
            type="ice_world",
            distance_from_earth_km=1.2e14,
            has_life=False,
            surface_temperature=-120.0,
            discovered_by="Lazarus Program",
            gravity=0.84,
            atmosphere="Ammonia and frozen particulates",
            habitability_score=0.18,
        ),
    ]
    crew_members = [
        Crew(name="Joseph Cooper", role="Mission Commander", mission=mission),
        Crew(name="Amelia Brand", role="Lead Scientist", mission=mission),
        Crew(name="Romilly", role="Systems Physicist", mission=mission),
        Crew(name="Doyle", role="Pilot", mission=mission),
    ]

    db.add(spacecraft)
    db.add(mission)
    db.add_all(planets)
    db.flush()

    db.add_all(crew_members)
    db.add_all(
        [
            SpacecraftStatus(
                mission_id=mission.id,
                timestamp=datetime(2067, 4, 12, 11, 45),
                fuel_level=78.4,
                oxygen_level=92.1,
                temperature=21.5,
                pressure=101.1,
                is_operational=True,
                life_support_active=True,
                communication_active=True,
            ),
            SpacecraftStatus(
                mission_id=mission.id,
                timestamp=datetime(2067, 4, 12, 14, 12),
                fuel_level=61.7,
                oxygen_level=89.9,
                temperature=23.1,
                pressure=100.4,
                is_operational=True,
                life_support_active=True,
                communication_active=True,
            ),
        ]
    )
    db.add(
        NavigationSystem(
            trajectory="Launch ascent -> parking orbit -> transfer corridor -> deorbit approach -> landing corridor",
            target_waypoint="Landing Zone Alpha",
            course_correction=2,
            delta_v_mps=184.6,
            burn_duration_seconds=96.0,
            alignment_error_deg=0.14,
            residual_drift_km=1.8,
            maneuver_window_open=datetime(2067, 4, 12, 12, 34),
            maneuver_window_close=datetime(2067, 4, 12, 12, 44),
            last_correction_at=datetime(2067, 4, 12, 12, 39),
            navigation_system_status="operational",
            spacecraft_id=spacecraft.id,
        )
    )
    db.add_all(
        [
            MissionEvent(
                event_type=EventType.GO_FOR_PROP_LOAD,
                timestamp=datetime(2067, 4, 12, 8, 15),
                description="Flight director issued go for propellant loading on the Endurance launch stack.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.PROP_LOAD_COMPLETE,
                timestamp=datetime(2067, 4, 12, 8, 44),
                description="Cryogenic propellant load completed and tanking stable.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.TERMINAL_COUNT,
                timestamp=datetime(2067, 4, 12, 9, 20),
                description="Terminal count entered with guidance, navigation and control polling nominal.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.ENGINE_IGNITION,
                timestamp=datetime(2067, 4, 12, 9, 29),
                description="Main engines at ignition start with chamber pressure rise within expected envelope.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.LIFTOFF,
                timestamp=datetime(2067, 4, 12, 9, 30),
                description="Endurance lifted off and cleared the tower on initial ascent.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.MAX_Q,
                timestamp=datetime(2067, 4, 12, 9, 31),
                description="Vehicle passed through maximum dynamic pressure.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.MECO,
                timestamp=datetime(2067, 4, 12, 9, 38),
                description="Main engine cutoff confirmed on schedule.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.ORBITAL_INSERTION,
                timestamp=datetime(2067, 4, 12, 9, 51),
                description="Stable orbital insertion achieved with guidance residuals within tolerance.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.COURSE_CORRECTION_BURN,
                timestamp=datetime(2067, 4, 12, 11, 22),
                description="Primary course correction burn completed for transfer toward the Gargantua approach corridor.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.STAGE_SEPARATION,
                timestamp=datetime(2067, 4, 12, 11, 31),
                description="Autonomous relay package separation confirmed after orbital systems checkout.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.COURSE_CORRECTION_BURN,
                timestamp=datetime(2067, 4, 12, 12, 39),
                description="Fine trim course correction executed to stabilize entry geometry for final descent.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.DEORBIT_BURN,
                timestamp=datetime(2067, 4, 12, 13, 55),
                description="Deorbit burn committed the vehicle to its landing trajectory.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.ENTRY_INTERFACE,
                timestamp=datetime(2067, 4, 12, 14, 2),
                description="Vehicle crossed entry interface and began guided atmospheric descent.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.LANDING_BURN,
                timestamp=datetime(2067, 4, 12, 14, 9),
                description="Landing burn initiated with vertical velocity converging to target values.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.SHIP_LANDING,
                timestamp=datetime(2067, 4, 12, 14, 12),
                description="Ship landing confirmed. Endurance safe on landing zone with crew in nominal condition.",
                spacecraft_id=spacecraft.id,
            ),
        ]
    )
    db.add_all(
        [
            AlertSystem(
                timestamp=datetime(2067, 4, 12, 12, 18),
                system="Navigation",
                alert_type=AlertType.WARNING,
                message="Time dilation envelope approaching operational threshold.",
                acknowledged=True,
                resolved=False,
                spacecraft_id=spacecraft.id,
            ),
            AlertSystem(
                timestamp=datetime(2067, 4, 12, 12, 26),
                system="Telemetry",
                alert_type=AlertType.INFO,
                message="Gravitational lensing data stream locked for Gargantua observation.",
                acknowledged=False,
                resolved=False,
                spacecraft_id=spacecraft.id,
            ),
            AlertSystem(
                timestamp=datetime(2067, 4, 12, 12, 11),
                system="Thermal Control",
                alert_type=AlertType.CRITICAL,
                message="Transient thermal spike detected during lensing observation window.",
                acknowledged=True,
                resolved=True,
                resolved_at=datetime(2067, 4, 12, 12, 16),
                spacecraft_id=spacecraft.id,
            ),
        ]
    )
    db.add_all(
        [
            GroundControlLog(
                timestamp=datetime(2067, 4, 12, 8, 12),
                sender="Launch Director",
                receiver="Endurance",
                message_type="go_for_prop_load",
                content="Launch control is go for propellant load. Begin cryogenic loading sequence.",
                acknowledged=True,
                spacecraft_id=spacecraft.id,
            ),
            GroundControlLog(
                timestamp=datetime(2067, 4, 12, 9, 18),
                sender="Launch Director",
                receiver="Endurance",
                message_type="terminal_count",
                content="Terminal count is authorized. Guidance, nav and flight software are green.",
                acknowledged=True,
                spacecraft_id=spacecraft.id,
            ),
            GroundControlLog(
                timestamp=datetime(2067, 4, 12, 11, 24),
                sender="Cooper Station",
                receiver="Endurance",
                message_type="course_correction_report",
                content="Primary course correction accepted. Residual drift is below corridor threshold.",
                acknowledged=True,
                spacecraft_id=spacecraft.id,
            ),
            GroundControlLog(
                timestamp=datetime(2067, 4, 12, 14, 13),
                sender="Endurance",
                receiver="Cooper Station",
                message_type="landing_confirmation",
                content="Endurance on the ground. Landing burn successful and crew condition nominal.",
                acknowledged=True,
                spacecraft_id=spacecraft.id,
            ),
        ]
    )

    db.commit()

    return DemoBootstrapResponse(
        detail="Demo dataset created for Endurance mission walkthrough.",
        mission_id=mission.id,
        spacecraft_id=spacecraft.id,
    )
