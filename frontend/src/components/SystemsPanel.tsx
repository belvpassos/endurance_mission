type SubsystemEntry = {
  label: string
  status: string
  detail: string
  tone: 'nominal' | 'monitor' | 'warning'
}

type SystemsPanelProps = {
  systems: SubsystemEntry[]
}

export function SystemsPanel({ systems }: SystemsPanelProps) {
  return (
    <section className="systems-panel panel">
      <div className="section-header">
        <div>
          <p className="eyebrow">Subsystem Matrix</p>
          <h2>Health Indicators</h2>
        </div>
      </div>

      <div className="systems-grid">
        {systems.map((system) => (
          <article key={system.label} className={`system-card system-card-${system.tone}`}>
            <div className="system-row">
              <span>{system.label}</span>
              <strong>{system.status}</strong>
            </div>
            <p>{system.detail}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
