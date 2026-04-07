from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alertSystem import AlertSystem, AlertType
from app.models.crew import Crew
from app.models.groundControlLog import GroundControlLog
from app.models.mission import Mission
from app.models.missionEvents import EventType, MissionEvent
from app.models.planet import Planet
from app.models.spacecraft import Spacecraft
from app.models.spacecraftStatus import SpacecraftStatus
from app.schemas.missionControl import (
    DemoBootstrapResponse,
    MissionAlertEntry,
    MissionControlOverview,
    MissionOverviewMetrics,
    MissionOverviewSnapshot,
    MissionTimelineEntry,
)

router = APIRouter()


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

    if latest_status and latest_status.is_operational and critical_alert_count == 0:
        readiness = "nominal"
    elif latest_status and latest_status.is_operational:
        readiness = "monitoring"
    else:
        readiness = "degraded"

    snapshot = MissionOverviewSnapshot(
        mission_name=latest_mission.name if latest_mission else None,
        mission_status=latest_mission.status if latest_mission else None,
        spacecraft_name=latest_spacecraft.name if latest_spacecraft else None,
        spacecraft_status=latest_spacecraft.status if latest_spacecraft else None,
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
        status="mission-ready",
        mission_profile="Deep-space transit and planetary survey coordination",
        home_base="Cooper Station",
    )
    mission = Mission(
        name="Lazarus Relay Expedition",
        status="transit_to_gargantua",
        start_time=datetime(2067, 4, 12, 9, 30),
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
                timestamp=datetime(2067, 4, 12, 12, 42),
                fuel_level=74.9,
                oxygen_level=91.4,
                temperature=22.0,
                pressure=100.9,
                is_operational=True,
                life_support_active=True,
                communication_active=True,
            ),
        ]
    )
    db.add_all(
        [
            MissionEvent(
                event_type=EventType.ORBITAL_INSERTION,
                timestamp=datetime(2067, 4, 12, 12, 5),
                description="Stable insertion achieved on approach vector to Gargantua.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.ENGINE_BURN,
                timestamp=datetime(2067, 4, 12, 12, 22),
                description="Course correction burn completed for Miller descent corridor.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.STAGE_SEPARATION,
                timestamp=datetime(2067, 4, 12, 12, 31),
                description="Survey package separation confirmed for autonomous relay pass.",
                spacecraft_id=spacecraft.id,
            ),
            MissionEvent(
                event_type=EventType.ENGINE_BURN,
                timestamp=datetime(2067, 4, 12, 12, 39),
                description="Fine trim burn executed to stabilize descent geometry.",
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
                timestamp=datetime(2067, 4, 12, 12, 8),
                sender="Cooper Station",
                receiver="Endurance",
                message_type="go_no_go",
                content="Mission control confirms orbital insertion is stable. Proceed to descent review.",
                acknowledged=True,
                spacecraft_id=spacecraft.id,
            ),
            GroundControlLog(
                timestamp=datetime(2067, 4, 12, 12, 30),
                sender="Cooper Station",
                receiver="Endurance",
                message_type="status_report",
                content="Mission control confirms relay uptime and green corridor for descent operations.",
                acknowledged=True,
                spacecraft_id=spacecraft.id,
            ),
            GroundControlLog(
                timestamp=datetime(2067, 4, 12, 12, 44),
                sender="Endurance",
                receiver="Cooper Station",
                message_type="mission_update",
                content="Vehicle nominal. Crew preparing for timed surface reconnaissance sequence.",
                acknowledged=False,
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
