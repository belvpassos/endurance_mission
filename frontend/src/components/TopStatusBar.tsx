type TopStatusBarProps = {
  readiness: string
  phase: string
  target: string
  activeAlerts: number
  generatedAt: string
}

export function TopStatusBar({
  readiness,
  phase,
  target,
  activeAlerts,
  generatedAt,
}: TopStatusBarProps) {
  return (
    <section className="top-status-bar panel">
      <div className="status-pill status-pill-primary">
        <span>Readiness</span>
        <strong>{readiness}</strong>
      </div>
      <div className="status-pill">
        <span>Mission Phase</span>
        <strong>{phase}</strong>
      </div>
      <div className="status-pill">
        <span>Target Vector</span>
        <strong>{target}</strong>
      </div>
      <div className="status-pill">
        <span>Alert Count</span>
        <strong>{activeAlerts}</strong>
      </div>
      <div className="status-pill">
        <span>Feed Sync</span>
        <strong>{generatedAt}</strong>
      </div>
    </section>
  )
}
