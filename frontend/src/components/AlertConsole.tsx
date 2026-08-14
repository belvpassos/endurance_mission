import type { MissionAlertEntry } from '../types/mission'

type AlertConsoleProps = {
  alerts: MissionAlertEntry[]
}

export function AlertConsole({ alerts }: AlertConsoleProps) {
  return (
    <section className="alert-console panel">
      <div className="section-header">
        <div>
          <p className="eyebrow">Alert Console</p>
          <h2>Active Watchlist</h2>
        </div>
      </div>

      <div className="alert-feed">
        {alerts.length ? (
          alerts.map((alert) => (
            <article key={`${alert.timestamp}-${alert.system}`} className={`alert-item severity-${alert.severity}`}>
              <div className="alert-line">
                <span>{alert.system}</span>
                <strong>{alert.severity}</strong>
              </div>
              <p>{alert.message}</p>
            </article>
          ))
        ) : (
          <p className="empty-state">No active alerts in the current control window.</p>
        )}
      </div>
    </section>
  )
}
