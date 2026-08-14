import { ColumnChart } from './ColumnChart'
import { MetricBar } from './MetricBar'
import { RadialGauge } from './RadialGauge'
import { Sparkline } from './Sparkline'

type OpsCard = {
  label: string
  value: string
  meta: string
  tone?: 'cyan' | 'amber' | 'red'
}

type TrendPanel = {
  label: string
  value: string
  detail: string
  chart: number[]
  visual?: 'sparkline' | 'bar' | 'gauge' | 'columns'
  numericValue?: number
  min?: number
  max?: number
  tone?: 'cyan' | 'amber' | 'red'
}

type OpsOverviewProps = {
  missionName: string
  cards: OpsCard[]
  primaryTrend: TrendPanel
  secondaryTrend: TrendPanel
  isLoading: boolean
  onRefresh: () => void
}

export function OpsOverview({
  missionName,
  cards,
  primaryTrend,
  secondaryTrend,
  isLoading,
  onRefresh,
}: OpsOverviewProps) {
  const [primaryA, primaryB, secondaryA, secondaryB] = cards

  function renderTrendVisual(trend: TrendPanel) {
    if (trend.visual === 'bar') {
      return <MetricBar value={trend.numericValue ?? 0} min={trend.min} max={trend.max} tone={trend.tone} />
    }

    if (trend.visual === 'gauge') {
      return (
        <RadialGauge
          value={trend.numericValue ?? 0}
          min={trend.min}
          max={trend.max}
          showReadout
          tone={trend.tone}
        />
      )
    }

    if (trend.visual === 'columns') {
      return <ColumnChart values={trend.chart} tone={trend.tone} />
    }

    return <Sparkline values={trend.chart} tone={trend.tone} />
  }

  return (
    <section className="ops-overview panel">
      <div className="section-header">
        <div>
          <p className="eyebrow">Mission Operations</p>
          <h1>{missionName}</h1>
        </div>

        <div className="command-actions">
          <button type="button" className="secondary-action" onClick={onRefresh} disabled={isLoading}>
            {isLoading ? 'Syncing...' : 'Sync Feed'}
          </button>
        </div>
      </div>

      <div className="ops-overview-grid">
        <section className="ops-primary-grid">
          {[primaryA, primaryB].filter(Boolean).map((card) => (
            <article key={card.label} className={`ops-card ops-card-primary ops-card-${card.tone ?? 'cyan'}`}>
              <span>{card.label}</span>
              <strong>{card.value}</strong>
              <p>{card.meta}</p>
            </article>
          ))}
        </section>

        <section className="ops-secondary-stack">
          {[secondaryA, secondaryB].filter(Boolean).map((card) => (
            <article key={card.label} className={`ops-card ops-card-secondary ops-card-${card.tone ?? 'cyan'}`}>
              <div className="ops-card-secondary-head">
                <span>{card.label}</span>
                <strong>{card.value}</strong>
              </div>
              <p>{card.meta}</p>
            </article>
          ))}
        </section>
      </div>

      <div className="trend-grid">
        {[primaryTrend, secondaryTrend].map((trend) => (
          <article key={trend.label} className={`trend-panel trend-panel-${trend.visual ?? 'sparkline'}`}>
            <div className="trend-panel-header">
              <div>
                <span>{trend.label}</span>
                <strong>{trend.value}</strong>
              </div>
            </div>
            <div className="trend-panel-visual">{renderTrendVisual(trend)}</div>
            <p>{trend.detail}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
