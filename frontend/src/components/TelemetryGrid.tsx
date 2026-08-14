import { ColumnChart } from './ColumnChart'
import { MetricBar } from './MetricBar'
import { RadialGauge } from './RadialGauge'
import { Sparkline } from './Sparkline'

type TelemetryMetric = {
  label: string
  value: string
  detail: string
  chart?: number[]
  visual?: 'sparkline' | 'bar' | 'gauge' | 'number' | 'columns'
  numericValue?: number
  min?: number
  max?: number
  tone?: 'cyan' | 'amber' | 'red'
}

type TelemetryGridProps = {
  metrics: TelemetryMetric[]
}

export function TelemetryGrid({ metrics }: TelemetryGridProps) {
  function renderVisual(metric: TelemetryMetric) {
    if (metric.visual === 'bar') {
      return <MetricBar value={metric.numericValue ?? 0} min={metric.min} max={metric.max} tone={metric.tone} />
    }

    if (metric.visual === 'gauge') {
      return (
        <RadialGauge
          value={metric.numericValue ?? 0}
          min={metric.min}
          max={metric.max}
          showReadout
          tone={metric.tone}
        />
      )
    }

    if (metric.visual === 'number') {
      return (
        <div className="metric-number-visual" aria-hidden="true">
          <div className={`metric-number-dot metric-number-dot-${metric.tone ?? 'cyan'}`} />
          <strong>{metric.value}</strong>
        </div>
      )
    }

    if (metric.visual === 'columns') {
      return <ColumnChart values={metric.chart ?? []} tone={metric.tone} />
    }

    return <Sparkline values={metric.chart ?? []} tone={metric.tone} />
  }

  return (
    <section className="telemetry-grid panel">
      <div className="section-header">
        <div>
          <p className="eyebrow">Telemetry Matrix</p>
          <h2>Vehicle Systems</h2>
        </div>
      </div>

      <div className="telemetry-cards">
        {metrics.map((metric) => (
          <article key={metric.label} className={`telemetry-card telemetry-card-${metric.visual ?? 'sparkline'}`}>
            <div className="telemetry-card-header">
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
            </div>
            {renderVisual(metric)}
            <p>{metric.detail}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
