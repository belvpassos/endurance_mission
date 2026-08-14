import { useState } from 'react'

type SidebarSubsystem = {
  label: string
  health: string
  tone: 'nominal' | 'monitor' | 'warning'
}

type SidebarDatum = {
  label: string
  value: string
}

type ConsoleSidebarProps = {
  spacecraftName: string
  missionName: string
  missionPhase: string
  feedMode: string
  readiness: string
  alertCount: number
  celestialContext: SidebarDatum[]
  crewManifest: SidebarDatum[]
  subsystems: SidebarSubsystem[]
}

export function ConsoleSidebar({
  spacecraftName,
  missionName,
  missionPhase,
  feedMode,
  readiness,
  alertCount,
  celestialContext,
  crewManifest,
  subsystems,
}: ConsoleSidebarProps) {
  const [activePanel, setActivePanel] = useState<'context' | 'celestial' | 'crew' | 'health'>('context')

  return (
    <aside className="console-sidebar panel">
      <div className="sidebar-brand">
        <p className="eyebrow">Endurance Console</p>
        <h2>{spacecraftName}</h2>
        <p>{missionName}</p>
      </div>

      <div className="sidebar-panel-tabs" role="tablist" aria-label="Sidebar data layers">
        <button
          type="button"
          className={`sidebar-panel-tab${activePanel === 'context' ? ' sidebar-panel-tab-active' : ''}`}
          onClick={() => setActivePanel('context')}
        >
          Context
        </button>
        <button
          type="button"
          className={`sidebar-panel-tab${activePanel === 'celestial' ? ' sidebar-panel-tab-active' : ''}`}
          onClick={() => setActivePanel('celestial')}
        >
          Celestial
        </button>
        <button
          type="button"
          className={`sidebar-panel-tab${activePanel === 'crew' ? ' sidebar-panel-tab-active' : ''}`}
          onClick={() => setActivePanel('crew')}
        >
          Crew
        </button>
        <button
          type="button"
          className={`sidebar-panel-tab${activePanel === 'health' ? ' sidebar-panel-tab-active' : ''}`}
          onClick={() => setActivePanel('health')}
        >
          Health
        </button>
      </div>

      <div className="sidebar-panel-body">
        {activePanel === 'context' ? (
          <div className="sidebar-block">
            <p className="eyebrow">Mission Context</p>
            <div className="sidebar-context-list">
              <div className="sidebar-context-row">
                <span>Phase</span>
                <strong>{missionPhase}</strong>
              </div>
              <div className="sidebar-context-row">
                <span>Feed</span>
                <strong>{feedMode}</strong>
              </div>
              <div className="sidebar-context-row">
                <span>Ready</span>
                <strong>{readiness}</strong>
              </div>
              <div className="sidebar-context-row">
                <span>Alerts</span>
                <strong>{alertCount}</strong>
              </div>
            </div>
          </div>
        ) : null}

        {activePanel === 'celestial' ? (
          <div className="sidebar-block">
            <p className="eyebrow">Celestial Context</p>
            <div className="sidebar-context-list">
              {celestialContext.map((item) => (
                <div key={item.label} className="sidebar-context-row">
                  <span>{item.label}</span>
                  <strong>{item.value}</strong>
                </div>
              ))}
            </div>
          </div>
        ) : null}

        {activePanel === 'crew' ? (
          <div className="sidebar-block">
            <p className="eyebrow">Crew Manifest</p>
            <div className="sidebar-context-list">
              {crewManifest.map((item) => (
                <div key={item.label} className="sidebar-context-row">
                  <span>{item.label}</span>
                  <strong>{item.value}</strong>
                </div>
              ))}
            </div>
          </div>
        ) : null}

        {activePanel === 'health' ? (
          <div className="sidebar-block sidebar-block-health">
            <p className="eyebrow">Subsystem Health</p>
            <div className="sidebar-health-list">
              {subsystems.map((subsystem) => (
                <div key={subsystem.label} className="sidebar-health-item">
                  <div className="sidebar-health-line">
                    <span>{subsystem.label}</span>
                    <strong>{subsystem.health}</strong>
                  </div>
                  <div className="sidebar-health-track">
                    <div className={`sidebar-health-fill sidebar-health-${subsystem.tone}`} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : null}
      </div>
    </aside>
  )
}
