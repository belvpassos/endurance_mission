import { ColumnChart } from './ColumnChart'
import { MetricBar } from './MetricBar'
import { RadialGauge } from './RadialGauge'
import { Sparkline } from './Sparkline'

type SignalMetric = {
  label: string
  value: string
  visual: 'sparkline' | 'bar' | 'gauge' | 'columns'
  chart?: number[]
  numericValue?: number
  min?: number
  max?: number
  tone?: 'cyan' | 'amber' | 'red'
}

type OverviewSignalStripProps = {
  metrics: SignalMetric[]
}

export function OverviewSignalStrip({ metrics }: OverviewSignalStripProps) {
  function renderGaugeReadout(metric: SignalMetric) {
    if (metric.visual !== 'gauge') {
      return null
    }

    const min = metric.min ?? 0
    const max = metric.max ?? 100
    const current = metric.numericValue ?? 0

    function formatMetric(value: number) {
      return value.toFixed(Math.abs(max - min) > 10 ? 0 : 1)
    }

    return (
      <div className="overview-gauge-readout">
        <div className="overview-gauge-readout-block">
          <span>Min</span>
          <strong>{formatMetric(min)}</strong>
        </div>
        <div className="overview-gauge-readout-block overview-gauge-readout-current">
          <span>Current</span>
          <strong>{formatMetric(current)}</strong>
        </div>
        <div className="overview-gauge-readout-block">
          <span>Max</span>
          <strong>{formatMetric(max)}</strong>
        </div>
      </div>
    )
  }

  function renderVisual(metric: SignalMetric) {
    if (metric.visual === 'bar') {
      return <MetricBar value={metric.numericValue ?? 0} min={metric.min} max={metric.max} tone={metric.tone} />
    }

    if (metric.visual === 'gauge') {
      return <RadialGauge value={metric.numericValue ?? 0} min={metric.min} max={metric.max} tone={metric.tone} />
    }

    if (metric.visual === 'columns') {
      return <ColumnChart values={metric.chart ?? []} tone={metric.tone} />
    }

    return <Sparkline values={metric.chart ?? []} tone={metric.tone} />
  }

  return (
    <section className="overview-signal-strip panel">
      <div className="section-header">
        <div>
          <p className="eyebrow">Signal Strip</p>
          <h2>Critical Vitals</h2>
        </div>
      </div>

      <div className="overview-signal-grid">
        {metrics.map((metric) => (
          <article key={metric.label} className={`overview-signal-card overview-signal-card-${metric.visual}`}>
            <div className="overview-signal-head">
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
            </div>
            <div className="overview-signal-visual">{renderVisual(metric)}</div>
            {renderGaugeReadout(metric)}
          </article>
        ))}
      </div>
    </section>
  )
}
