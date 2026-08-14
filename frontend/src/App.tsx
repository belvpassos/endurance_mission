import { useEffect, useMemo, useState } from 'react'
import { AlertConsole } from './components/AlertConsole'
import { ConsoleSidebar } from './components/ConsoleSidebar'
import { ConsoleTabs } from './components/ConsoleTabs'
import { LiveOpsFeed } from './components/LiveOpsFeed'
import { MissionAdminPanel } from './components/MissionAdminPanel'
import { OverviewSignalStrip } from './components/OverviewSignalStrip'
import { MissionTimeline } from './components/MissionTimeline'
import { OpsOverview } from './components/OpsOverview'
import { SystemsPanel } from './components/SystemsPanel'
import { TelemetryGrid } from './components/TelemetryGrid'
import { TopStatusBar } from './components/TopStatusBar'
import type { MissionControlOverview } from './types/mission'
import './App.css'

const API_BASE = '/api'
const POLL_INTERVAL_MS = 4000
const stationTabs = ['Flight Overview', 'Navigation', 'Propulsion', 'Life Support', 'Planetary', 'Crew', 'Vehicle', 'Communications', 'Event Log', 'Mission Admin']

const fallbackOverview: MissionControlOverview = {
  generated_at: '2067-04-12T14:12:00Z',
  operational_readiness: 'monitoring',
  metrics: {
    missions: 1,
    spacecraft: 1,
    crew_members: 4,
    active_alerts: 2,
    critical_alerts: 0,
  },
  latest_snapshot: {
    mission_name: 'Lazarus Relay Expedition',
    mission_status: 'ship_landed',
    mission_phase: 'surface_operations',
    spacecraft_name: 'Endurance',
    spacecraft_status: 'landed-and-safe',
    current_flight_stage: 'ship_landing',
    current_target: 'Landing Zone Alpha',
    course_corrections_executed: 2,
    readiness_reason: 'Open warning alerts remain under active review.',
    navigation_status: 'operational',
    alignment_error_deg: 0.14,
    residual_drift_km: 1.8,
    latest_status_timestamp: '2067-04-12T14:12:00Z',
    fuel_level: 61.7,
    oxygen_level: 89.9,
    cabin_temperature: 23.1,
    cabin_pressure: 100.4,
  },
  celestial_context: {
    gravity_source: 'Gargantua',
    orbital_sector: 'Accretion Corridor A',
    time_dilation_ratio: '01 hr : 07 yrs',
    target_body: 'Miller',
    target_waypoint: 'Landing Zone Alpha',
  },
  active_planet: {
    name: 'Miller',
    type: 'water_world',
    gravity: 1.3,
    atmosphere: 'Dense vapor and saline aerosols',
    surface_temperature: 4.0,
    habitability_score: 0.42,
    description: 'Ocean world with extreme time dilation near Gargantua.',
  },
  crew_summary: {
    total_active: 4,
    commander: 'Joseph Cooper',
    lead_scientist: 'Amelia Brand',
    crew_manifest: [
      { name: 'Joseph Cooper', role: 'Mission Commander' },
      { name: 'Amelia Brand', role: 'Lead Scientist' },
      { name: 'Romilly', role: 'Systems Physicist' },
      { name: 'Doyle', role: 'Pilot' },
    ],
    support_units: ['TARS', 'CASE'],
  },
  spacecraft_summary: {
    name: 'Endurance',
    registry_code: 'END-PRIME-01',
    vehicle_class: 'Interstellar endurance vehicle',
    manufacturer: 'NASA / Lazarus Program',
    mission_profile: 'Launch, orbital transfer, course correction, descent and landing operations',
    home_base: 'Launch and Recovery Complex 39A',
    status: 'landed-and-safe',
  },
  recent_events: [
    {
      timestamp: '2067-04-12T14:12:00Z',
      event_type: 'ship_landing',
      description: 'Endurance completed final descent and secured in Landing Zone Alpha.',
    },
    {
      timestamp: '2067-04-12T14:02:00Z',
      event_type: 'entry_interface',
      description: 'Vehicle crossed entry interface and began guided atmospheric descent.',
    },
    {
      timestamp: '2067-04-12T13:55:00Z',
      event_type: 'deorbit_burn',
      description: 'Deorbit burn committed the vehicle to its landing trajectory.',
    },
  ],
  active_alerts: [
    {
      timestamp: '2067-04-12T14:05:00Z',
      severity: 'warning',
      system: 'Navigation Guidance',
      message: 'Residual drift remains above the nominal corridor after course trim.',
      spacecraft_id: 1,
    },
    {
      timestamp: '2067-04-12T13:48:00Z',
      severity: 'info',
      system: 'Ground Control Link',
      message: 'Relay latency elevated while final descent corridor was updated.',
      spacecraft_id: 1,
    },
  ],
}

function formatLabel(value: string | null | undefined) {
  if (!value) {
    return 'Unavailable'
  }

  return value.replaceAll('_', ' ').replace(/\b\w/g, (character) => character.toUpperCase())
}

function formatTimestamp(value: string) {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(new Date(value))
}

function formatTimeOnly(value: string) {
  return new Intl.DateTimeFormat('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(new Date(value))
}

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value))
}

function buildLiveSeries(center: number, spread: number, points: number, tick: number, phase = 0) {
  return Array.from({ length: points }, (_, index) => {
    const drift = Math.sin((index + tick) * 0.55 + phase) * spread
    const pulse = Math.cos((tick * 0.25 + index) * 0.8 + phase) * spread * 0.35
    return Math.max(center + drift + pulse, 0)
  })
}

type SystemTone = 'nominal' | 'monitor' | 'warning'

function formatShortName(value: string | null | undefined) {
  if (!value) {
    return 'Unavailable'
  }

  const parts = value.split(' ')
  return parts[parts.length - 1]
}

function App() {
  const [overview, setOverview] = useState<MissionControlOverview>(fallbackOverview)
  const [isLoading, setIsLoading] = useState(false)
  const [useFallback, setUseFallback] = useState(true)
  const [activeTab, setActiveTab] = useState(stationTabs[0])
  const [liveTick, setLiveTick] = useState(0)

  async function loadOverview() {
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE}/mission-control/overview`)
      if (!response.ok) {
        throw new Error('Feed offline')
      }

      const data = (await response.json()) as MissionControlOverview
      setOverview(data)
      setUseFallback(false)
    } catch {
      setUseFallback(true)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    void loadOverview()
    const intervalId = window.setInterval(() => {
      void loadOverview()
    }, POLL_INTERVAL_MS)

    return () => window.clearInterval(intervalId)
  }, [])

  useEffect(() => {
    const intervalId = window.setInterval(() => {
      setLiveTick((value) => value + 1)
    }, 1200)

    return () => window.clearInterval(intervalId)
  }, [])

  const activeOverview = useMemo(() => {
    if (!useFallback) {
      return overview
    }

    const base = overview.latest_snapshot

    return {
      ...overview,
      generated_at: new Date(Date.now() - 500 + (liveTick % 5) * 140).toISOString(),
      latest_snapshot: {
        ...base,
        fuel_level: clamp((base.fuel_level ?? 61.7) + Math.sin(liveTick * 0.18) * 1.4, 42, 78),
        oxygen_level: clamp((base.oxygen_level ?? 89.9) + Math.cos(liveTick * 0.16) * 0.9, 82, 96),
        cabin_temperature: clamp((base.cabin_temperature ?? 23.1) + Math.sin(liveTick * 0.13 + 0.6) * 0.6, 19, 27),
        cabin_pressure: clamp((base.cabin_pressure ?? 100.4) + Math.cos(liveTick * 0.11) * 0.45, 98.5, 102.2),
        residual_drift_km: clamp((base.residual_drift_km ?? 1.8) + Math.sin(liveTick * 0.22 + 1.1) * 0.28, 0.8, 2.6),
        alignment_error_deg: clamp((base.alignment_error_deg ?? 0.14) + Math.cos(liveTick * 0.21 + 0.3) * 0.04, 0.03, 0.34),
      },
    }
  }, [overview, useFallback, liveTick])

  const snapshot = activeOverview.latest_snapshot
  const series = (center: number, spread: number, points: number, phase = 0) =>
    buildLiveSeries(center, spread, points, liveTick, phase)

  const celestialContext = useMemo(
    () => [
      { label: 'Planet', value: activeOverview.active_planet?.name ?? 'Unavailable' },
      { label: 'Mass', value: activeOverview.celestial_context.gravity_source ?? 'Unavailable' },
      { label: 'Orbit', value: activeOverview.celestial_context.orbital_sector ?? 'Unavailable' },
      { label: 'Time', value: activeOverview.celestial_context.time_dilation_ratio ?? 'Unavailable' },
    ],
    [activeOverview.active_planet?.name, activeOverview.celestial_context.gravity_source, activeOverview.celestial_context.orbital_sector, activeOverview.celestial_context.time_dilation_ratio],
  )

  const crewManifest = useMemo(
    () => [
      { label: 'Crew', value: `${activeOverview.crew_summary.total_active} Active` },
      { label: 'Lead', value: formatShortName(activeOverview.crew_summary.commander) },
      { label: 'Science', value: formatShortName(activeOverview.crew_summary.lead_scientist) },
      { label: 'Support', value: activeOverview.crew_summary.support_units.join(' / ') || 'Unavailable' },
    ],
    [activeOverview.crew_summary],
  )

  const telemetryMetrics = useMemo(
    () => [
      {
        label: 'Fuel Reserve',
        value: `${snapshot.fuel_level?.toFixed(1) ?? '--'}%`,
        detail: 'Cryogenic reserve available for propulsion and contingency burns.',
        visual: 'columns' as const,
        chart: series(snapshot.fuel_level ?? 61.7, 5.4, 10, 0.2),
        tone: 'amber' as const,
      },
      {
        label: 'Oxygen Balance',
        value: `${snapshot.oxygen_level?.toFixed(1) ?? '--'}%`,
        detail: 'Cabin and suit loop levels across life-support circulation.',
        visual: 'columns' as const,
        chart: series(snapshot.oxygen_level ?? 89.9, 2.2, 10, 0.8),
        tone: 'cyan' as const,
      },
      {
        label: 'Cabin Temperature',
        value: `${snapshot.cabin_temperature?.toFixed(1) ?? '--'} C`,
        detail: 'Thermal control equilibrium in the current habitat envelope.',
        visual: 'sparkline' as const,
        chart: series(snapshot.cabin_temperature ?? 23.1, 0.9, 16, 1.3),
        tone: 'cyan' as const,
      },
      {
        label: 'Cabin Pressure',
        value: `${snapshot.cabin_pressure?.toFixed(1) ?? '--'} kPa`,
        detail: 'Pressurization control loop and habitat seal stability.',
        visual: 'sparkline' as const,
        chart: series(snapshot.cabin_pressure ?? 100.4, 0.55, 16, 1.9),
        tone: 'cyan' as const,
      },
      {
        label: 'Alignment Error',
        value: `${snapshot.alignment_error_deg?.toFixed(2) ?? '--'} deg`,
        detail: 'Navigation attitude delta against the commanded descent corridor.',
        visual: 'number' as const,
        numericValue: snapshot.alignment_error_deg ?? 0.14,
        tone: 'red' as const,
      },
      {
        label: 'Residual Drift',
        value: `${snapshot.residual_drift_km?.toFixed(1) ?? '--'} km`,
        detail: 'Current guidance residual after latest correction burn sequence.',
        visual: 'gauge' as const,
        numericValue: snapshot.residual_drift_km ?? 1.8,
        min: 0,
        max: 3,
        tone: 'amber' as const,
      },
    ],
    [series, snapshot],
  )

  const systemHealth = useMemo(
    () => [
      {
        label: 'Propulsion',
        status: (snapshot.fuel_level ?? 0) > 45 ? 'Nominal' : 'Monitor',
        detail: `${snapshot.fuel_level?.toFixed(1) ?? '--'}% reserve available for transfer and correction burns.`,
        tone: ((snapshot.fuel_level ?? 0) > 45 ? 'nominal' : 'monitor') as SystemTone,
      },
      {
        label: 'Life Support',
        status: (snapshot.oxygen_level ?? 0) > 85 ? 'Nominal' : 'Warning',
        detail: `${snapshot.oxygen_level?.toFixed(1) ?? '--'}% oxygen balance with cabin pressure at ${
          snapshot.cabin_pressure?.toFixed(1) ?? '--'
        } kPa.`,
        tone: ((snapshot.oxygen_level ?? 0) > 85 ? 'nominal' : 'warning') as SystemTone,
      },
      {
        label: 'Guidance',
        status: (snapshot.residual_drift_km ?? 0) < 1 ? 'Nominal' : 'Monitor',
        detail: `${snapshot.residual_drift_km?.toFixed(1) ?? '--'} km residual drift after ${
          snapshot.course_corrections_executed
        } correction events.`,
        tone: ((snapshot.residual_drift_km ?? 0) < 1 ? 'nominal' : 'monitor') as SystemTone,
      },
      {
        label: 'Thermal Control',
        status:
          (snapshot.cabin_temperature ?? 0) >= 18 && (snapshot.cabin_temperature ?? 0) <= 27 ? 'Nominal' : 'Monitor',
        detail: `${snapshot.cabin_temperature?.toFixed(1) ?? '--'} C cabin envelope under active regulation.`,
        tone:
          ((snapshot.cabin_temperature ?? 0) >= 18 && (snapshot.cabin_temperature ?? 0) <= 27
            ? 'nominal'
            : 'monitor') as SystemTone,
      },
      {
        label: 'Communications',
        status: useFallback ? 'Fallback' : 'Live',
        detail: useFallback
          ? 'Local simulated feed active while backend telemetry is unavailable.'
          : 'Backend telemetry linked and updating on live polling cadence.',
        tone: (useFallback ? 'warning' : 'nominal') as SystemTone,
      },
    ],
    [snapshot, useFallback],
  )

  const opsCards = useMemo(
    () => [
      {
        label: 'Vehicle State',
        value: formatLabel(snapshot.spacecraft_status),
        meta: `Readiness ${formatLabel(activeOverview.operational_readiness)}`,
        tone: 'cyan' as const,
      },
      {
        label: 'Flight Stage',
        value: formatLabel(snapshot.current_flight_stage),
        meta: `Phase ${formatLabel(snapshot.mission_phase)}`,
        tone: 'cyan' as const,
      },
      {
        label: 'Nav Status',
        value: formatLabel(snapshot.navigation_status),
        meta: `${snapshot.course_corrections_executed} correction burns`,
        tone: 'cyan' as const,
      },
      {
        label: 'Target',
        value: formatLabel(snapshot.current_target),
        meta: 'Primary intercept solution',
        tone: 'amber' as const,
      },
      {
        label: 'Residual Drift',
        value: `${snapshot.residual_drift_km?.toFixed(1) ?? '--'} km`,
        meta: 'Guidance corridor delta',
        tone: 'amber' as const,
      },
      {
        label: 'Alignment Error',
        value: `${snapshot.alignment_error_deg?.toFixed(2) ?? '--'} deg`,
        meta: 'Attitude tracking offset',
        tone: 'red' as const,
      },
      {
        label: 'Cabin Pressure',
        value: `${snapshot.cabin_pressure?.toFixed(1) ?? '--'} kPa`,
        meta: 'Habitat pressure loop',
        tone: 'cyan' as const,
      },
      {
        label: 'Oxygen Balance',
        value: `${snapshot.oxygen_level?.toFixed(1) ?? '--'}%`,
        meta: 'Life support reserve',
        tone: 'cyan' as const,
      },
    ],
    [activeOverview.operational_readiness, snapshot],
  )

  const liveFeedEntries = useMemo(() => {
    const alertEntries = activeOverview.active_alerts.map((alert, index) => ({
      id: `alert-${index}-${alert.timestamp}`,
      sortKey: alert.timestamp,
      timestamp: formatTimestamp(alert.timestamp),
      system: alert.system,
      status: alert.severity.toUpperCase(),
      detail: alert.message,
      tone:
        alert.severity === 'critical'
          ? ('red' as const)
          : alert.severity === 'warning'
            ? ('amber' as const)
            : ('cyan' as const),
    }))

    const eventEntries = activeOverview.recent_events.map((event, index) => ({
      id: `event-${index}-${event.timestamp}`,
      sortKey: event.timestamp,
      timestamp: formatTimestamp(event.timestamp),
      system: formatLabel(event.event_type),
      status: 'EVENT',
      detail: event.description ?? 'Mission event registered without detail.',
      tone: 'cyan' as const,
    }))

    const heartbeatEntry = {
      id: `heartbeat-${liveTick}`,
      sortKey: new Date().toISOString(),
      timestamp: formatTimestamp(new Date().toISOString()),
      system: useFallback ? 'Simulated Control Loop' : 'Telemetry Uplink',
      status: useFallback ? 'HEARTBEAT' : 'SYNC',
      detail: useFallback
        ? 'Fallback mission stream generating live telemetry until backend feed returns.'
        : 'Mission-control feed synchronized with latest telemetry snapshot.',
      tone: 'cyan' as const,
    }

    return [heartbeatEntry, ...alertEntries, ...eventEntries]
      .sort((left, right) => new Date(right.sortKey).getTime() - new Date(left.sortKey).getTime())
      .slice(0, 6)
      .map(({ sortKey: _sortKey, ...entry }) => entry)
  }, [activeOverview.active_alerts, activeOverview.recent_events, formatTimestamp, liveTick, useFallback])

  const navigationMetrics = useMemo(
    () => [
      telemetryMetrics[4],
      {
        label: 'Target Vector',
        value: formatLabel(snapshot.current_target),
        detail: 'Current intercept and descent target tracked by guidance.',
        visual: 'number' as const,
        numericValue: snapshot.residual_drift_km ?? 1.8,
        tone: 'amber' as const,
      },
      {
        label: 'Correction Count',
        value: `${snapshot.course_corrections_executed}`,
        detail: 'Executed course trims across current mission segment.',
        visual: 'columns' as const,
        chart: series(snapshot.course_corrections_executed, 0.4, 8, 3.9),
        tone: 'cyan' as const,
      },
      {
        label: 'Guidance Status',
        value: formatLabel(snapshot.navigation_status),
        detail: 'Autopilot and guidance stack state for the current navigation solution.',
        visual: 'number' as const,
        numericValue: snapshot.alignment_error_deg ?? 0.14,
        tone: 'cyan' as const,
      },
    ],
    [series, snapshot, telemetryMetrics],
  )

  const propulsionMetrics = useMemo(
    () => [
      telemetryMetrics[0],
      {
        label: 'Burn Window',
        value: formatLabel(snapshot.current_flight_stage),
        detail: 'Active propulsion regime for the current mission stage.',
        visual: 'number' as const,
        numericValue: snapshot.fuel_level ?? 61.7,
        tone: 'amber' as const,
      },
      {
        label: 'Trim Sequence',
        value: `${snapshot.course_corrections_executed}`,
        detail: 'Correction burns committed to current trajectory solution.',
        visual: 'columns' as const,
        chart: series(snapshot.course_corrections_executed, 0.35, 8, 4.8),
        tone: 'cyan' as const,
      },
      telemetryMetrics[5],
    ],
    [series, snapshot, telemetryMetrics],
  )

  const lifeSupportMetrics = useMemo(
    () => [telemetryMetrics[1], telemetryMetrics[2], telemetryMetrics[3]],
    [telemetryMetrics],
  )

  const communicationMetrics = useMemo(
    () => [
      {
        label: 'Feed Mode',
        value: useFallback ? 'Fallback' : 'Live',
        detail: 'Current telemetry source serving the control dashboard.',
        visual: 'number' as const,
        numericValue: useFallback ? 1 : 2,
        tone: useFallback ? ('amber' as const) : ('cyan' as const),
      },
      {
        label: 'Feed Sync',
        value: formatTimestamp(activeOverview.generated_at),
        detail: 'Latest mission-control synchronization timestamp.',
        visual: 'sparkline' as const,
        chart: series(42, 1.1, 14, 5.8),
        tone: 'cyan' as const,
      },
      {
        label: 'Alert Traffic',
        value: `${activeOverview.metrics.active_alerts}`,
        detail: 'Current communications and control-channel watch items.',
        visual: 'columns' as const,
        chart: series(activeOverview.metrics.active_alerts, 0.25, 8, 6.1),
        tone: 'amber' as const,
      },
    ],
    [activeOverview.generated_at, activeOverview.metrics.active_alerts, series, useFallback],
  )

  const timelineEvents = activeOverview.recent_events.map((event) => ({
    ...event,
    event_type: formatLabel(event.event_type),
    timestamp: formatTimestamp(event.timestamp),
  }))

  const planetaryMetrics = useMemo(
    () => [
      {
        label: 'Target Body',
        value: activeOverview.active_planet?.name ?? 'Unavailable',
        detail: activeOverview.active_planet?.description ?? 'No planetary briefing available.',
        visual: 'number' as const,
        numericValue: activeOverview.active_planet?.gravity ?? 1,
        tone: 'amber' as const,
      },
      {
        label: 'Surface Gravity',
        value: `${activeOverview.active_planet?.gravity?.toFixed(2) ?? '--'} g`,
        detail: 'Estimated surface gravity at the current mission destination.',
        visual: 'gauge' as const,
        numericValue: activeOverview.active_planet?.gravity ?? 1.3,
        min: 0,
        max: 2,
        tone: 'amber' as const,
      },
      {
        label: 'Surface Temp',
        value: `${activeOverview.active_planet?.surface_temperature?.toFixed(1) ?? '--'} C`,
        detail: 'Observed planetary surface temperature from latest survey pass.',
        visual: 'sparkline' as const,
        chart: series(activeOverview.active_planet?.surface_temperature ?? 4, 1.1, 16, 2.4),
        tone: 'cyan' as const,
      },
      {
        label: 'Habitability',
        value: `${Math.round((activeOverview.active_planet?.habitability_score ?? 0.42) * 100)}%`,
        detail: 'Relative viability score for sustained mission operations.',
        visual: 'bar' as const,
        numericValue: (activeOverview.active_planet?.habitability_score ?? 0.42) * 100,
        min: 0,
        max: 100,
        tone: 'cyan' as const,
      },
    ],
    [activeOverview.active_planet, series],
  )

  const crewStationMetrics = useMemo(
    () => [
      {
        label: 'Crew Active',
        value: `${activeOverview.crew_summary.total_active}`,
        detail: 'Crew members currently assigned to the active mission profile.',
        visual: 'columns' as const,
        chart: series(activeOverview.crew_summary.total_active, 0.2, 8, 3.4),
        tone: 'cyan' as const,
      },
      {
        label: 'Commander',
        value: formatShortName(activeOverview.crew_summary.commander),
        detail: 'Primary mission commander currently leading vehicle operations.',
        visual: 'number' as const,
        numericValue: activeOverview.crew_summary.total_active,
        tone: 'amber' as const,
      },
      {
        label: 'Lead Science',
        value: formatShortName(activeOverview.crew_summary.lead_scientist),
        detail: 'Lead science authority for destination assessment and mission analysis.',
        visual: 'number' as const,
        numericValue: activeOverview.crew_summary.total_active,
        tone: 'cyan' as const,
      },
      {
        label: 'Support Units',
        value: activeOverview.crew_summary.support_units.join(' / ') || 'Unavailable',
        detail: 'Autonomous mission support assets integrated with the crew stack.',
        visual: 'number' as const,
        numericValue: activeOverview.crew_summary.support_units.length,
        tone: 'cyan' as const,
      },
    ],
    [activeOverview.crew_summary, series],
  )

  const vehicleMetrics = useMemo(
    () => [
      {
        label: 'Registry',
        value: activeOverview.spacecraft_summary.registry_code ?? 'Unavailable',
        detail: 'Primary spacecraft registry designation for mission control reference.',
        visual: 'number' as const,
        numericValue: 1,
        tone: 'cyan' as const,
      },
      {
        label: 'Vehicle Class',
        value: activeOverview.spacecraft_summary.vehicle_class ?? 'Unavailable',
        detail: 'Flight vehicle classification used for mission planning and operations.',
        visual: 'number' as const,
        numericValue: 1,
        tone: 'amber' as const,
      },
      {
        label: 'Fuel Reserve',
        value: `${snapshot.fuel_level?.toFixed(1) ?? '--'}%`,
        detail: 'Vehicle propellant reserve available across the current mission envelope.',
        visual: 'columns' as const,
        chart: series(snapshot.fuel_level ?? 61.7, 2.6, 10, 4.4),
        tone: 'amber' as const,
      },
      {
        label: 'Vehicle Status',
        value: formatLabel(activeOverview.spacecraft_summary.status),
        detail: activeOverview.spacecraft_summary.mission_profile ?? 'No mission profile available.',
        visual: 'number' as const,
        numericValue: 1,
        tone: 'cyan' as const,
      },
    ],
    [activeOverview.spacecraft_summary, series, snapshot.fuel_level],
  )

  const overviewSignalMetrics = useMemo(
    () => [
      {
        label: 'Fuel',
        value: `${snapshot.fuel_level?.toFixed(1) ?? '--'}%`,
        visual: 'bar' as const,
        numericValue: snapshot.fuel_level ?? 61.7,
        min: 0,
        max: 100,
        tone: 'amber' as const,
      },
      {
        label: 'Oxygen',
        value: `${snapshot.oxygen_level?.toFixed(1) ?? '--'}%`,
        visual: 'columns' as const,
        chart: series(snapshot.oxygen_level ?? 89.9, 2.2, 10, 0.8),
        tone: 'cyan' as const,
      },
      {
        label: 'Drift',
        value: `${snapshot.residual_drift_km?.toFixed(1) ?? '--'} km`,
        visual: 'gauge' as const,
        numericValue: snapshot.residual_drift_km ?? 1.8,
        min: 0,
        max: 3,
        tone: 'amber' as const,
      },
      {
        label: 'Cabin Temp',
        value: `${snapshot.cabin_temperature?.toFixed(1) ?? '--'} C`,
        visual: 'sparkline' as const,
        chart: series(snapshot.cabin_temperature ?? 23.1, 0.8, 14, 1.3),
        tone: 'cyan' as const,
      },
    ],
    [series, snapshot.cabin_temperature, snapshot.fuel_level, snapshot.oxygen_level, snapshot.residual_drift_km],
  )

  const renderStationView = () => {
    if (activeTab === 'Navigation') {
      return (
        <section className="workspace-grid">
          <section className="workspace-main-column">
            <OpsOverview
              missionName="Navigation Station"
              cards={opsCards.slice(2, 6)}
              primaryTrend={{
                label: 'Residual Drift',
                value: `${snapshot.residual_drift_km?.toFixed(1) ?? '--'} km`,
                detail: 'Guidance residual against the commanded corridor.',
                chart: series(snapshot.residual_drift_km ?? 1.8, 0.34, 24, 7.4),
                visual: 'gauge',
                numericValue: snapshot.residual_drift_km ?? 1.8,
                min: 0,
                max: 3,
                tone: 'amber',
              }}
              secondaryTrend={{
                label: 'Alignment Response',
                value: `${snapshot.alignment_error_deg?.toFixed(2) ?? '--'} deg`,
                detail: 'Attitude convergence after latest correction maneuvers.',
                chart: series(snapshot.alignment_error_deg ?? 0.14, 0.03, 24, 7.9),
                visual: 'sparkline',
                tone: 'red',
              }}
              isLoading={isLoading}
              onRefresh={() => void loadOverview()}
            />
            <TelemetryGrid metrics={navigationMetrics} />
          </section>

          <section className="workspace-side-column">
            <SystemsPanel systems={systemHealth.filter((system) => ['Guidance', 'Communications'].includes(system.label))} />
            <LiveOpsFeed entries={liveFeedEntries.filter((entry) => entry.system.includes('Navigation') || entry.system.includes('Entry') || entry.system.includes('Deorbit')).slice(0, 5)} />
          </section>
        </section>
      )
    }

    if (activeTab === 'Propulsion') {
      return (
        <section className="workspace-grid">
          <section className="workspace-main-column">
            <OpsOverview
              missionName="Propulsion Station"
              cards={[opsCards[1], opsCards[4], { label: 'Fuel Reserve', value: `${snapshot.fuel_level?.toFixed(1) ?? '--'}%`, meta: 'Cryogenic reserve', tone: 'amber' as const }, { label: 'Burn Count', value: `${snapshot.course_corrections_executed}`, meta: 'Committed trim burns', tone: 'cyan' as const }]}
              primaryTrend={{
                label: 'Fuel Drawdown',
                value: `${snapshot.fuel_level?.toFixed(1) ?? '--'}%`,
                detail: 'Propellant reserve profile across descent and correction phases.',
                chart: series(snapshot.fuel_level ?? 61.7, 1.8, 24, 8.4),
                visual: 'bar',
                numericValue: snapshot.fuel_level ?? 61.7,
                min: 0,
                max: 100,
                tone: 'amber',
              }}
              secondaryTrend={{
                label: 'Trim Burn Cadence',
                value: `${snapshot.course_corrections_executed}`,
                detail: 'Correction sequence pacing through current propulsion window.',
                chart: series(snapshot.course_corrections_executed, 0.2, 24, 8.9),
                visual: 'columns',
                tone: 'cyan',
              }}
              isLoading={isLoading}
              onRefresh={() => void loadOverview()}
            />
            <TelemetryGrid metrics={propulsionMetrics} />
          </section>

          <section className="workspace-side-column">
            <SystemsPanel systems={systemHealth.filter((system) => ['Propulsion', 'Guidance'].includes(system.label))} />
            <LiveOpsFeed entries={liveFeedEntries.filter((entry) => entry.system.includes('Deorbit') || entry.system.includes('Navigation') || entry.system.includes('Ground Control')).slice(0, 5)} />
          </section>
        </section>
      )
    }

    if (activeTab === 'Life Support') {
      return (
        <section className="workspace-grid">
          <section className="workspace-main-column">
            <OpsOverview
              missionName="Life Support Station"
              cards={[opsCards[6], opsCards[7], { label: 'Cabin Temp', value: `${snapshot.cabin_temperature?.toFixed(1) ?? '--'} C`, meta: 'Habitat thermal envelope', tone: 'cyan' as const }, { label: 'Crew Manifest', value: `${activeOverview.metrics.crew_members}`, meta: 'Active crew monitoring', tone: 'cyan' as const }]}
              primaryTrend={{
                label: 'Oxygen Stability',
                value: `${snapshot.oxygen_level?.toFixed(1) ?? '--'}%`,
                detail: 'Life-support reserve trend through the active mission phase.',
                chart: series(snapshot.oxygen_level ?? 89.9, 0.8, 24, 9.4),
                visual: 'bar',
                numericValue: snapshot.oxygen_level ?? 89.9,
                min: 0,
                max: 100,
                tone: 'cyan',
              }}
              secondaryTrend={{
                label: 'Cabin Thermal Loop',
                value: `${snapshot.cabin_temperature?.toFixed(1) ?? '--'} C`,
                detail: 'Temperature control trend across habitat circulation loops.',
                chart: series(snapshot.cabin_temperature ?? 23.1, 0.5, 24, 9.9),
                visual: 'sparkline',
                tone: 'cyan',
              }}
              isLoading={isLoading}
              onRefresh={() => void loadOverview()}
            />
            <TelemetryGrid metrics={lifeSupportMetrics} />
          </section>

          <section className="workspace-side-column">
            <SystemsPanel systems={systemHealth.filter((system) => ['Life Support', 'Thermal Control'].includes(system.label))} />
            <AlertConsole alerts={activeOverview.active_alerts} />
          </section>
        </section>
      )
    }

    if (activeTab === 'Communications') {
      return (
        <section className="workspace-grid">
          <section className="workspace-main-column">
            <OpsOverview
              missionName="Communications Station"
              cards={[{ label: 'Feed Mode', value: useFallback ? 'Fallback' : 'Live', meta: 'Active telemetry transport', tone: useFallback ? ('amber' as const) : ('cyan' as const) }, { label: 'Latency', value: '042 ms', meta: 'Relay response time', tone: 'cyan' as const }, { label: 'Alert Traffic', value: `${activeOverview.metrics.active_alerts}`, meta: 'Open comm-channel watch items', tone: 'amber' as const }, { label: 'Critical Alerts', value: `${activeOverview.metrics.critical_alerts}`, meta: 'Escalated control messages', tone: activeOverview.metrics.critical_alerts ? ('red' as const) : ('cyan' as const) }]}
              primaryTrend={{
                label: 'Feed Sync Stability',
                value: formatTimestamp(activeOverview.generated_at),
                detail: 'Control-network synchronization heartbeat over the polling window.',
                chart: series(42, 1.1, 24, 6.5),
                visual: 'sparkline',
                tone: 'cyan',
              }}
              secondaryTrend={{
                label: 'Channel Alert Volume',
                value: `${activeOverview.metrics.active_alerts}`,
                detail: 'Realtime control-channel watch activity and relay notices.',
                chart: series(activeOverview.metrics.active_alerts, 0.2, 24, 7.0),
                visual: 'columns',
                tone: 'amber',
              }}
              isLoading={isLoading}
              onRefresh={() => void loadOverview()}
            />
            <TelemetryGrid metrics={communicationMetrics} />
          </section>

          <section className="workspace-side-column">
            <LiveOpsFeed entries={liveFeedEntries} />
            <SystemsPanel systems={systemHealth.filter((system) => ['Communications', 'Guidance'].includes(system.label))} />
          </section>
        </section>
      )
    }

    if (activeTab === 'Planetary') {
      return (
        <section className="workspace-grid">
          <section className="workspace-main-column">
            <OpsOverview
              missionName={`${activeOverview.active_planet?.name ?? 'Planetary'} Station`}
              cards={[
                {
                  label: 'Target Body',
                  value: activeOverview.active_planet?.name ?? 'Unavailable',
                  meta: formatLabel(activeOverview.active_planet?.type),
                  tone: 'amber' as const,
                },
                {
                  label: 'Gravity Source',
                  value: activeOverview.celestial_context.gravity_source ?? 'Unavailable',
                  meta: activeOverview.celestial_context.orbital_sector ?? 'No orbital sector available',
                  tone: 'cyan' as const,
                },
                {
                  label: 'Time Dilation',
                  value: activeOverview.celestial_context.time_dilation_ratio ?? 'Unavailable',
                  meta: 'Relativistic environment estimate',
                  tone: 'amber' as const,
                },
                {
                  label: 'Atmosphere',
                  value: activeOverview.active_planet?.atmosphere ?? 'Unavailable',
                  meta: 'Environmental survey',
                  tone: 'cyan' as const,
                },
              ]}
              primaryTrend={{
                label: 'Gravitational Envelope',
                value: `${activeOverview.active_planet?.gravity?.toFixed(2) ?? '--'} g`,
                detail: 'Predicted gravitational loading across the current target environment.',
                chart: series(activeOverview.active_planet?.gravity ?? 1.3, 0.08, 24, 11.2),
                visual: 'gauge',
                numericValue: activeOverview.active_planet?.gravity ?? 1.3,
                min: 0,
                max: 2,
                tone: 'amber',
              }}
              secondaryTrend={{
                label: 'Surface Thermal Track',
                value: `${activeOverview.active_planet?.surface_temperature?.toFixed(1) ?? '--'} C`,
                detail: 'Thermal readings gathered from the active planetary approach solution.',
                chart: series(activeOverview.active_planet?.surface_temperature ?? 4, 0.7, 24, 11.8),
                visual: 'sparkline',
                tone: 'cyan',
              }}
              isLoading={isLoading}
              onRefresh={() => void loadOverview()}
            />
            <TelemetryGrid metrics={planetaryMetrics} />
          </section>

          <section className="workspace-side-column">
            <SystemsPanel
              systems={[
                {
                  label: 'Gravity Well',
                  status: activeOverview.celestial_context.gravity_source ?? 'Unknown',
                  detail: activeOverview.celestial_context.time_dilation_ratio ?? 'No relativistic context available.',
                  tone: 'monitor',
                },
                {
                  label: 'Target Orbit',
                  status: 'Tracked',
                  detail: activeOverview.celestial_context.orbital_sector ?? 'No orbital sector available.',
                  tone: 'nominal',
                },
              ]}
            />
            <LiveOpsFeed entries={liveFeedEntries.filter((entry) => entry.detail.includes('Gargantua') || entry.detail.includes('landing') || entry.detail.includes('descent')).slice(0, 4)} />
          </section>
        </section>
      )
    }

    if (activeTab === 'Crew') {
      return (
        <section className="workspace-grid">
          <section className="workspace-main-column">
            <OpsOverview
              missionName="Crew Operations"
              cards={[
                {
                  label: 'Commander',
                  value: formatShortName(activeOverview.crew_summary.commander),
                  meta: 'Mission command authority',
                  tone: 'amber' as const,
                },
                {
                  label: 'Lead Science',
                  value: formatShortName(activeOverview.crew_summary.lead_scientist),
                  meta: 'Science mission lead',
                  tone: 'cyan' as const,
                },
                {
                  label: 'Crew Active',
                  value: `${activeOverview.crew_summary.total_active}`,
                  meta: 'Assigned crew complement',
                  tone: 'cyan' as const,
                },
                {
                  label: 'Support Units',
                  value: activeOverview.crew_summary.support_units.join(' / ') || 'Unavailable',
                  meta: 'Autonomous support assets',
                  tone: 'cyan' as const,
                },
              ]}
              primaryTrend={{
                label: 'Crew Readiness',
                value: `${activeOverview.crew_summary.total_active} active`,
                detail: 'Crew availability and assignment continuity across the mission stack.',
                chart: series(activeOverview.crew_summary.total_active, 0.15, 24, 12.2),
                visual: 'columns',
                tone: 'cyan',
              }}
              secondaryTrend={{
                label: 'Support Coordination',
                value: `${activeOverview.crew_summary.support_units.length} units`,
                detail: 'Autonomous support availability aligned with crew mission tasks.',
                chart: series(activeOverview.crew_summary.support_units.length, 0.08, 24, 12.8),
                visual: 'columns',
                tone: 'amber',
              }}
              isLoading={isLoading}
              onRefresh={() => void loadOverview()}
            />
            <TelemetryGrid metrics={crewStationMetrics} />
          </section>

          <section className="workspace-side-column">
            <SystemsPanel
              systems={activeOverview.crew_summary.crew_manifest.slice(0, 4).map((member) => ({
                label: formatShortName(member.name),
                status: member.role,
                detail: `${member.name} assigned to current mission segment operations.`,
                tone: 'nominal' as const,
              }))}
            />
            <AlertConsole alerts={activeOverview.active_alerts} />
          </section>
        </section>
      )
    }

    if (activeTab === 'Vehicle') {
      return (
        <section className="workspace-grid">
          <section className="workspace-main-column">
            <OpsOverview
              missionName={activeOverview.spacecraft_summary.name ?? 'Vehicle Station'}
              cards={[
                {
                  label: 'Registry',
                  value: activeOverview.spacecraft_summary.registry_code ?? 'Unavailable',
                  meta: activeOverview.spacecraft_summary.vehicle_class ?? 'No class available',
                  tone: 'cyan' as const,
                },
                {
                  label: 'Vehicle State',
                  value: formatLabel(activeOverview.spacecraft_summary.status),
                  meta: formatLabel(activeOverview.operational_readiness),
                  tone: 'amber' as const,
                },
                {
                  label: 'Manufacturer',
                  value: activeOverview.spacecraft_summary.manufacturer ?? 'Unavailable',
                  meta: 'Vehicle origin',
                  tone: 'cyan' as const,
                },
                {
                  label: 'Home Base',
                  value: activeOverview.spacecraft_summary.home_base ?? 'Unavailable',
                  meta: 'Primary launch and recovery site',
                  tone: 'cyan' as const,
                },
              ]}
              primaryTrend={{
                label: 'Vehicle Health',
                value: `${snapshot.fuel_level?.toFixed(1) ?? '--'}% fuel`,
                detail: 'Operational vehicle endurance signal from the latest status frame.',
                chart: series(snapshot.fuel_level ?? 61.7, 1.2, 24, 13.4),
                visual: 'bar',
                numericValue: snapshot.fuel_level ?? 61.7,
                min: 0,
                max: 100,
                tone: 'amber',
              }}
              secondaryTrend={{
                label: 'Cabin Envelope',
                value: `${snapshot.cabin_pressure?.toFixed(1) ?? '--'} kPa`,
                detail: 'Cabin pressure and habitability envelope under current systems load.',
                chart: series(snapshot.cabin_pressure ?? 100.4, 0.4, 24, 13.9),
                visual: 'sparkline',
                tone: 'cyan',
              }}
              isLoading={isLoading}
              onRefresh={() => void loadOverview()}
            />
            <TelemetryGrid metrics={vehicleMetrics} />
          </section>

          <section className="workspace-side-column">
            <SystemsPanel systems={systemHealth} />
            <LiveOpsFeed entries={liveFeedEntries.slice(0, 4)} />
          </section>
        </section>
      )
    }

    if (activeTab === 'Event Log') {
      return (
        <section className="workspace-grid">
          <section className="workspace-main-column">
            <MissionTimeline events={timelineEvents} />
            <LiveOpsFeed entries={liveFeedEntries} />
          </section>

          <section className="workspace-side-column">
            <AlertConsole alerts={activeOverview.active_alerts} />
            <SystemsPanel systems={systemHealth} />
          </section>
        </section>
      )
    }

    if (activeTab === 'Mission Admin') {
      return <MissionAdminPanel onDataChanged={() => void loadOverview()} />
    }

    return (
      <section className="workspace-grid">
        <section className="workspace-main-column">
          <OpsOverview
            missionName={snapshot.mission_name ?? 'Endurance Mission'}
            cards={[opsCards[1], opsCards[3], opsCards[0], opsCards[2]]}
            primaryTrend={{
              label: 'Guidance Drift Trend',
              value: `${snapshot.residual_drift_km?.toFixed(1) ?? '--'} km`,
              detail: 'Residual drift history after course trimming and terminal guidance updates.',
              chart: series(snapshot.residual_drift_km ?? 1.8, 0.36, 24, 10.3),
              visual: 'sparkline',
              tone: 'amber',
            }}
            secondaryTrend={{
              label: 'Life Support Stability',
              value: `${snapshot.oxygen_level?.toFixed(1) ?? '--'}%`,
              detail: 'Oxygen reserve and circulation response across current mission phase.',
              chart: series(snapshot.oxygen_level ?? 89.9, 0.8, 24, 10.8),
              visual: 'bar',
              numericValue: snapshot.oxygen_level ?? 89.9,
              min: 0,
              max: 100,
              tone: 'cyan',
            }}
            isLoading={isLoading}
            onRefresh={() => void loadOverview()}
          />
        </section>

        <section className="workspace-side-column">
          <OverviewSignalStrip metrics={overviewSignalMetrics} />
          <LiveOpsFeed entries={liveFeedEntries.slice(0, 2)} />
          <SystemsPanel systems={systemHealth.slice(0, 2)} />
        </section>
      </section>
    )
  }

  return (
    <main className="app-shell">
        <ConsoleSidebar
          spacecraftName={snapshot.spacecraft_name ?? 'Endurance'}
          missionName={snapshot.mission_name ?? 'Endurance Mission'}
          missionPhase={formatLabel(snapshot.mission_phase)}
          feedMode={useFallback ? 'Fallback' : 'Live'}
          readiness={formatLabel(activeOverview.operational_readiness)}
          alertCount={activeOverview.metrics.active_alerts}
          celestialContext={celestialContext}
          crewManifest={crewManifest}
          subsystems={systemHealth.slice(0, 4).map((system) => ({
            label: system.label,
            health: system.status,
            tone: system.tone,
          }))}
      />

      <section className="console-main">
        <div className="console-frame">
          <span>ENDURANCE // ORBITAL CONTROL NETWORK</span>
          <span>LATENCY 042 MS</span>
          <span>{useFallback ? 'FALLBACK FEED' : 'LIVE FEED'}</span>
        </div>

        <ConsoleTabs tabs={stationTabs} activeTab={activeTab} onSelect={setActiveTab} />

        <TopStatusBar
          readiness={formatLabel(activeOverview.operational_readiness)}
          phase={formatLabel(snapshot.mission_phase)}
          target={formatLabel(snapshot.current_target)}
          activeAlerts={activeOverview.metrics.active_alerts}
          generatedAt={formatTimeOnly(activeOverview.generated_at)}
        />
        {renderStationView()}
      </section>
    </main>
  )
}

export default App
