from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MissionOverviewMetrics(BaseModel):
    missions: int
    spacecraft: int
    crew_members: int
    active_alerts: int
    critical_alerts: int


class MissionOverviewSnapshot(BaseModel):
    mission_name: Optional[str] = None
    mission_status: Optional[str] = None
    mission_phase: Optional[str] = None
    spacecraft_name: Optional[str] = None
    spacecraft_status: Optional[str] = None
    current_flight_stage: Optional[str] = None
    current_target: Optional[str] = None
    course_corrections_executed: int = 0
    readiness_reason: Optional[str] = None
    navigation_status: Optional[str] = None
    alignment_error_deg: Optional[float] = None
    residual_drift_km: Optional[float] = None
    latest_status_timestamp: Optional[datetime] = None
    fuel_level: Optional[float] = None
    oxygen_level: Optional[float] = None
    cabin_temperature: Optional[float] = None
    cabin_pressure: Optional[float] = None


class MissionPlanetSummary(BaseModel):
    name: str
    type: Optional[str] = None
    gravity: Optional[float] = None
    atmosphere: Optional[str] = None
    surface_temperature: Optional[float] = None
    habitability_score: Optional[float] = None
    description: Optional[str] = None


class MissionCelestialContext(BaseModel):
    gravity_source: Optional[str] = None
    orbital_sector: Optional[str] = None
    time_dilation_ratio: Optional[str] = None
    target_body: Optional[str] = None
    target_waypoint: Optional[str] = None


class MissionCrewEntry(BaseModel):
    name: str
    role: str


class MissionCrewSummary(BaseModel):
    total_active: int
    commander: Optional[str] = None
    lead_scientist: Optional[str] = None
    crew_manifest: list[MissionCrewEntry]
    support_units: list[str]


class MissionSpacecraftSummary(BaseModel):
    name: Optional[str] = None
    registry_code: Optional[str] = None
    vehicle_class: Optional[str] = None
    manufacturer: Optional[str] = None
    mission_profile: Optional[str] = None
    home_base: Optional[str] = None
    status: Optional[str] = None


class MissionTimelineEntry(BaseModel):
    timestamp: datetime
    event_type: str
    description: Optional[str] = None


class MissionAlertEntry(BaseModel):
    timestamp: datetime
    severity: str
    system: str
    message: str
    spacecraft_id: int


class MissionControlOverview(BaseModel):
    generated_at: datetime
    operational_readiness: str
    metrics: MissionOverviewMetrics
    latest_snapshot: MissionOverviewSnapshot
    celestial_context: MissionCelestialContext
    active_planet: Optional[MissionPlanetSummary] = None
    crew_summary: MissionCrewSummary
    spacecraft_summary: MissionSpacecraftSummary
    recent_events: list[MissionTimelineEntry]
    active_alerts: list[MissionAlertEntry]


class DemoBootstrapResponse(BaseModel):
    detail: str
    mission_id: int
    spacecraft_id: int
