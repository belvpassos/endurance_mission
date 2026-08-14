export type MissionOverviewMetrics = {
  missions: number
  spacecraft: number
  crew_members: number
  active_alerts: number
  critical_alerts: number
}

export type MissionOverviewSnapshot = {
  mission_name: string | null
  mission_status: string | null
  mission_phase: string | null
  spacecraft_name: string | null
  spacecraft_status: string | null
  current_flight_stage: string | null
  current_target: string | null
  course_corrections_executed: number
  readiness_reason: string | null
  navigation_status: string | null
  alignment_error_deg: number | null
  residual_drift_km: number | null
  latest_status_timestamp: string | null
  fuel_level: number | null
  oxygen_level: number | null
  cabin_temperature: number | null
  cabin_pressure: number | null
}

export type MissionPlanetSummary = {
  name: string
  type: string | null
  gravity: number | null
  atmosphere: string | null
  surface_temperature: number | null
  habitability_score: number | null
  description: string | null
}

export type MissionCelestialContext = {
  gravity_source: string | null
  orbital_sector: string | null
  time_dilation_ratio: string | null
  target_body: string | null
  target_waypoint: string | null
}

export type MissionCrewEntry = {
  name: string
  role: string
}

export type MissionCrewSummary = {
  total_active: number
  commander: string | null
  lead_scientist: string | null
  crew_manifest: MissionCrewEntry[]
  support_units: string[]
}

export type MissionSpacecraftSummary = {
  name: string | null
  registry_code: string | null
  vehicle_class: string | null
  manufacturer: string | null
  mission_profile: string | null
  home_base: string | null
  status: string | null
}

export type MissionTimelineEntry = {
  timestamp: string
  event_type: string
  description: string | null
}

export type MissionAlertEntry = {
  timestamp: string
  severity: string
  system: string
  message: string
  spacecraft_id: number
}

export type MissionControlOverview = {
  generated_at: string
  operational_readiness: string
  metrics: MissionOverviewMetrics
  latest_snapshot: MissionOverviewSnapshot
  celestial_context: MissionCelestialContext
  active_planet: MissionPlanetSummary | null
  crew_summary: MissionCrewSummary
  spacecraft_summary: MissionSpacecraftSummary
  recent_events: MissionTimelineEntry[]
  active_alerts: MissionAlertEntry[]
}
