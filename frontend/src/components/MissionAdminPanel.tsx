import { useEffect, useState } from 'react'

type MissionOption = {
  id: number
  name: string
}

type EntityRow = {
  id: number
  label: string
  detail: string
}

type MissionAdminPanelProps = {
  onDataChanged: () => void
}

type FormState = {
  missionName: string
  missionStatus: string
  missionPhase: string
  planetName: string
  planetType: string
  planetDistance: string
  planetGravity: string
  planetAtmosphere: string
  crewName: string
  crewRole: string
  crewMissionId: string
  spacecraftName: string
  spacecraftRegistry: string
  spacecraftClass: string
}

const initialForm: FormState = {
  missionName: '',
  missionStatus: 'planning',
  missionPhase: 'prelaunch',
  planetName: '',
  planetType: '',
  planetDistance: '',
  planetGravity: '',
  planetAtmosphere: '',
  crewName: '',
  crewRole: '',
  crewMissionId: '',
  spacecraftName: '',
  spacecraftRegistry: '',
  spacecraftClass: '',
}

export function MissionAdminPanel({ onDataChanged }: MissionAdminPanelProps) {
  const [missions, setMissions] = useState<MissionOption[]>([])
  const [missionRows, setMissionRows] = useState<EntityRow[]>([])
  const [planetRows, setPlanetRows] = useState<EntityRow[]>([])
  const [crewRows, setCrewRows] = useState<EntityRow[]>([])
  const [spacecraftRows, setSpacecraftRows] = useState<EntityRow[]>([])
  const [form, setForm] = useState<FormState>(initialForm)
  const [statusMessage, setStatusMessage] = useState('Admin console online.')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function loadAdminData() {
    try {
      const [missionsResponse, planetsResponse, crewResponse, spacecraftResponse] = await Promise.all([
        fetch('/api/missions'),
        fetch('/api/planets'),
        fetch('/api/crew'),
        fetch('/api/spacecraft'),
      ])

      const [missionsData, planetsData, crewData, spacecraftData] = await Promise.all([
        missionsResponse.json(),
        planetsResponse.json(),
        crewResponse.json(),
        spacecraftResponse.json(),
      ])

      const missionList = Array.isArray(missionsData) ? missionsData : []
      setMissions(missionList.map((mission) => ({ id: mission.id, name: mission.name })))
      setMissionRows(
        missionList.slice(-4).reverse().map((mission) => ({
          id: mission.id,
          label: mission.name,
          detail: `${mission.status} // ${mission.phase}`,
        })),
      )
      setPlanetRows(
        (Array.isArray(planetsData) ? planetsData : []).slice(-4).reverse().map((planet) => ({
          id: planet.id,
          label: planet.name,
          detail: `${planet.type} // ${planet.atmosphere ?? 'No atmosphere data'}`,
        })),
      )
      setCrewRows(
        (Array.isArray(crewData) ? crewData : []).slice(-4).reverse().map((crew) => ({
          id: crew.id,
          label: crew.name,
          detail: `${crew.role} // Mission ${crew.mission_id}`,
        })),
      )
      setSpacecraftRows(
        (Array.isArray(spacecraftData) ? spacecraftData : []).slice(-4).reverse().map((spacecraft) => ({
          id: spacecraft.id,
          label: spacecraft.name,
          detail: `${spacecraft.registry_code} // ${spacecraft.vehicle_class}`,
        })),
      )
    } catch {
      setStatusMessage('Could not load admin data from backend.')
    }
  }

  useEffect(() => {
    void loadAdminData()
  }, [])

  function updateField<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((current) => ({ ...current, [key]: value }))
  }

  async function submitJson(url: string, payload: Record<string, unknown>, successMessage: string, resetKeys: (keyof FormState)[]) {
    setIsSubmitting(true)
    setStatusMessage('Submitting to mission backend...')

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        throw new Error('Request failed')
      }

      setStatusMessage(successMessage)
      setForm((current) => {
        const next = { ...current }
        for (const key of resetKeys) {
          next[key] = initialForm[key]
        }
        return next
      })
      await loadAdminData()
      onDataChanged()
    } catch {
      setStatusMessage('The backend rejected the request. Check required fields and uniqueness constraints.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section className="mission-admin panel">
      <div className="section-header mission-admin-header">
        <div>
          <p className="eyebrow">Mission Administration</p>
          <h1>Control Room Ops</h1>
          <p>Separate the operational flight deck from data-entry and CRUD workflows.</p>
        </div>

        <div className="command-actions">
          <button type="button" className="secondary-action" onClick={() => window.open('/api/docs', '_blank', 'noopener,noreferrer')}>
            Open Swagger
          </button>
          <button type="button" className="secondary-action" onClick={() => void loadAdminData()}>
            Refresh Admin Data
          </button>
        </div>
      </div>

      <div className="admin-status-strip">
        <span>Mission Backend</span>
        <strong>{statusMessage}</strong>
      </div>

      <div className="admin-grid">
        <article className="admin-card">
          <div className="admin-card-header">
            <span>Mission CRUD</span>
            <strong>{missionRows.length || 0}</strong>
          </div>
          <div className="admin-form-grid">
            <input value={form.missionName} onChange={(event) => updateField('missionName', event.target.value)} placeholder="Mission name" />
            <input value={form.missionStatus} onChange={(event) => updateField('missionStatus', event.target.value)} placeholder="Status" />
            <select value={form.missionPhase} onChange={(event) => updateField('missionPhase', event.target.value)}>
              <option value="prelaunch">prelaunch</option>
              <option value="ascent">ascent</option>
              <option value="orbital_operations">orbital_operations</option>
              <option value="transfer">transfer</option>
              <option value="approach">approach</option>
              <option value="landing">landing</option>
              <option value="surface_operations">surface_operations</option>
            </select>
          </div>
          <button
            type="button"
            className="secondary-action admin-submit"
            disabled={isSubmitting || !form.missionName || !form.missionStatus}
            onClick={() =>
              void submitJson(
                '/api/missions',
                {
                  name: form.missionName,
                  status: form.missionStatus,
                  phase: form.missionPhase,
                },
                'Mission created successfully.',
                ['missionName', 'missionStatus', 'missionPhase'],
              )
            }
          >
            Create Mission
          </button>
          <div className="admin-list">
            {missionRows.map((row) => (
              <div key={row.id} className="admin-list-row">
                <span>{row.label}</span>
                <strong>{row.detail}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="admin-card">
          <div className="admin-card-header">
            <span>Planet CRUD</span>
            <strong>{planetRows.length || 0}</strong>
          </div>
          <div className="admin-form-grid">
            <input value={form.planetName} onChange={(event) => updateField('planetName', event.target.value)} placeholder="Planet name" />
            <input value={form.planetType} onChange={(event) => updateField('planetType', event.target.value)} placeholder="Type" />
            <input value={form.planetDistance} onChange={(event) => updateField('planetDistance', event.target.value)} placeholder="Distance from Earth (km)" />
            <input value={form.planetGravity} onChange={(event) => updateField('planetGravity', event.target.value)} placeholder="Gravity" />
            <input value={form.planetAtmosphere} onChange={(event) => updateField('planetAtmosphere', event.target.value)} placeholder="Atmosphere" />
          </div>
          <button
            type="button"
            className="secondary-action admin-submit"
            disabled={isSubmitting || !form.planetName || !form.planetType || !form.planetDistance}
            onClick={() =>
              void submitJson(
                '/api/planets',
                {
                  name: form.planetName,
                  type: form.planetType,
                  distance_from_earth_km: Number(form.planetDistance),
                  gravity: form.planetGravity ? Number(form.planetGravity) : null,
                  atmosphere: form.planetAtmosphere || null,
                },
                'Planet created successfully.',
                ['planetName', 'planetType', 'planetDistance', 'planetGravity', 'planetAtmosphere'],
              )
            }
          >
            Create Planet
          </button>
          <div className="admin-list">
            {planetRows.map((row) => (
              <div key={row.id} className="admin-list-row">
                <span>{row.label}</span>
                <strong>{row.detail}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="admin-card">
          <div className="admin-card-header">
            <span>Crew CRUD</span>
            <strong>{crewRows.length || 0}</strong>
          </div>
          <div className="admin-form-grid">
            <input value={form.crewName} onChange={(event) => updateField('crewName', event.target.value)} placeholder="Crew name" />
            <input value={form.crewRole} onChange={(event) => updateField('crewRole', event.target.value)} placeholder="Role" />
            <select value={form.crewMissionId} onChange={(event) => updateField('crewMissionId', event.target.value)}>
              <option value="">Mission assignment</option>
              {missions.map((mission) => (
                <option key={mission.id} value={mission.id}>
                  {mission.name}
                </option>
              ))}
            </select>
          </div>
          <button
            type="button"
            className="secondary-action admin-submit"
            disabled={isSubmitting || !form.crewName || !form.crewRole || !form.crewMissionId}
            onClick={() =>
              void submitJson(
                '/api/crew',
                {
                  name: form.crewName,
                  role: form.crewRole,
                  mission_id: Number(form.crewMissionId),
                },
                'Crew member created successfully.',
                ['crewName', 'crewRole', 'crewMissionId'],
              )
            }
          >
            Create Crew Member
          </button>
          <div className="admin-list">
            {crewRows.map((row) => (
              <div key={row.id} className="admin-list-row">
                <span>{row.label}</span>
                <strong>{row.detail}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="admin-card">
          <div className="admin-card-header">
            <span>Spacecraft CRUD</span>
            <strong>{spacecraftRows.length || 0}</strong>
          </div>
          <div className="admin-form-grid">
            <input value={form.spacecraftName} onChange={(event) => updateField('spacecraftName', event.target.value)} placeholder="Spacecraft name" />
            <input value={form.spacecraftRegistry} onChange={(event) => updateField('spacecraftRegistry', event.target.value)} placeholder="Registry code" />
            <input value={form.spacecraftClass} onChange={(event) => updateField('spacecraftClass', event.target.value)} placeholder="Vehicle class" />
          </div>
          <button
            type="button"
            className="secondary-action admin-submit"
            disabled={isSubmitting || !form.spacecraftName || !form.spacecraftRegistry || !form.spacecraftClass}
            onClick={() =>
              void submitJson(
                '/api/spacecraft',
                {
                  name: form.spacecraftName,
                  registry_code: form.spacecraftRegistry,
                  vehicle_class: form.spacecraftClass,
                },
                'Spacecraft created successfully.',
                ['spacecraftName', 'spacecraftRegistry', 'spacecraftClass'],
              )
            }
          >
            Create Spacecraft
          </button>
          <div className="admin-list">
            {spacecraftRows.map((row) => (
              <div key={row.id} className="admin-list-row">
                <span>{row.label}</span>
                <strong>{row.detail}</strong>
              </div>
            ))}
          </div>
        </article>
      </div>
    </section>
  )
}
