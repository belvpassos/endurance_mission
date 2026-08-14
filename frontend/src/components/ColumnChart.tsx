type ColumnChartProps = {
  values: number[]
  tone?: 'cyan' | 'amber' | 'red'
}

const toneMap = {
  cyan: 'linear-gradient(180deg, #93ebff, #67d1ff)',
  amber: 'linear-gradient(180deg, #ffd978, #ffbe55)',
  red: 'linear-gradient(180deg, #ff9b9b, #ff7070)',
}

export function ColumnChart({ values, tone = 'cyan' }: ColumnChartProps) {
  const safeValues = values.length ? values : [0]
  const visibleValues = safeValues.length > 10 ? safeValues.slice(-10) : safeValues
  const max = Math.max(...visibleValues, 1)
  const min = Math.min(...visibleValues, 0)

  function formatMetric(value: number) {
    return value.toFixed(Math.abs(max) >= 10 ? 0 : 1)
  }

  return (
    <div className="column-chart-shell" aria-hidden="true">
      <div
        className="column-chart"
        style={{ gridTemplateColumns: `repeat(${visibleValues.length}, minmax(0, 1fr))` }}
      >
        {visibleValues.map((value, index) => {
          const height = `${Math.max((value / max) * 100, 8)}%`

          return (
            <div key={`${tone}-${index}`} className="column-chart-slot">
              <span className="column-chart-value">{formatMetric(value)}</span>
              <span
                className="column-chart-bar"
                style={{ height, background: toneMap[tone] }}
              />
              <span className="column-chart-index">{index + 1}</span>
            </div>
          )
        })}
      </div>

      <div className="column-chart-summary">
        <div className="column-chart-summary-block">
          <span>Min</span>
          <strong>{formatMetric(min)}</strong>
        </div>
        <div className="column-chart-summary-block">
          <span>Now</span>
          <strong>{formatMetric(visibleValues[visibleValues.length - 1] ?? 0)}</strong>
        </div>
        <div className="column-chart-summary-block">
          <span>Max</span>
          <strong>{formatMetric(max)}</strong>
        </div>
      </div>
    </div>
  )
}
