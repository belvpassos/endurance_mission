type HeroConsoleProps = {
  missionName: string
  spacecraftName: string
  missionStatus: string
  readinessReason: string
  isLoading: boolean
  onBootstrap: () => void
  onRefresh: () => void
}

export function HeroConsole({
  missionName,
  spacecraftName,
  missionStatus,
  readinessReason,
  isLoading,
  onBootstrap,
  onRefresh,
}: HeroConsoleProps) {
  return (
    <section className="hero-console panel">
      <div className="hero-copy">
        <p className="eyebrow">Endurance Mission Control</p>
        <div className="hero-meta-strip">
          <span>Vehicle // {spacecraftName}</span>
          <span>Mission Feed // Active</span>
          <span>Control Mode // Guided</span>
        </div>
        <h1>{missionName}</h1>
        <p className="hero-summary">
          Live flight deck for {spacecraftName}. This console tracks mission status, navigation drift,
          life-support telemetry, alerts, and operational events as if you were on the mission floor.
        </p>
        <p className="hero-status">{readinessReason}</p>
      </div>

      <div className="hero-centerpiece">
        <div className="hero-radar">
          <div className="hero-sweep" />
          <div className="hero-crosshair hero-crosshair-horizontal" />
          <div className="hero-crosshair hero-crosshair-vertical" />
          <div className="hero-ring hero-ring-outer" />
          <div className="hero-ring hero-ring-inner" />
          <div className="hero-core">
            <span>Vehicle State</span>
            <strong>{missionStatus}</strong>
          </div>
        </div>
      </div>

      <div className="hero-actions">
        <button type="button" className="primary-action" onClick={onBootstrap} disabled={isLoading}>
          {isLoading ? 'Loading...' : 'Initialize Demo Feed'}
        </button>
        <button type="button" className="secondary-action" onClick={onRefresh} disabled={isLoading}>
          Sync Telemetry
        </button>
        <p className="hero-actions-note">Realtime polling window // 4s cadence // mission-safe fallback enabled</p>
      </div>
    </section>
  )
}
