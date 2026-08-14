type SparklineProps = {
  values: number[]
  tone?: 'cyan' | 'amber' | 'red'
}

const toneMap = {
  cyan: '#67d1ff',
  amber: '#ffbe55',
  red: '#ff7070',
}

export function Sparkline({ values, tone = 'cyan' }: SparklineProps) {
  const safeValues = values.length ? values : [0]
  const max = Math.max(...safeValues)
  const min = Math.min(...safeValues)
  const range = max - min || 1
  const latest = safeValues[safeValues.length - 1] ?? 0
  const midpoint = min + range / 2
  const width = 220
  const height = 64
  const chartBottom = height - 4
  const chartTop = 4

  function toY(value: number) {
    return height - ((value - min) / range) * (height - 8) - 4
  }

  const points = safeValues
    .map((value, index) => {
      const x = (index / Math.max(safeValues.length - 1, 1)) * width
      const y = toY(value)
      return `${x},${y}`
    })
    .join(' ')

  const latestX = ((safeValues.length - 1) / Math.max(safeValues.length - 1, 1)) * width
  const latestY = toY(latest)

  function formatMetric(value: number) {
    return value.toFixed(Math.abs(value) >= 10 ? 1 : 2)
  }

  return (
    <div className="sparkline-shell" aria-hidden="true">
      <svg className="sparkline" viewBox={`0 0 ${width} ${height}`} role="img">
        <line x1="0" y1={chartTop} x2="0" y2={chartBottom} className="sparkline-grid sparkline-grid-vertical" />
        <line x1={width * 0.25} y1={chartTop} x2={width * 0.25} y2={chartBottom} className="sparkline-grid sparkline-grid-vertical" />
        <line x1={width * 0.5} y1={chartTop} x2={width * 0.5} y2={chartBottom} className="sparkline-grid sparkline-grid-vertical" />
        <line x1={width * 0.75} y1={chartTop} x2={width * 0.75} y2={chartBottom} className="sparkline-grid sparkline-grid-vertical" />
        <line x1={width} y1={chartTop} x2={width} y2={chartBottom} className="sparkline-grid sparkline-grid-vertical" />
        <line x1="0" y1={chartTop} x2={width} y2={chartTop} className="sparkline-grid" />
        <line x1="0" y1={toY(midpoint)} x2={width} y2={toY(midpoint)} className="sparkline-grid sparkline-grid-mid" />
        <line x1="0" y1={chartBottom} x2={width} y2={chartBottom} className="sparkline-grid" />
        <polyline
          fill="none"
          points={points}
          stroke={toneMap[tone]}
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx={latestX} cy={latestY} r="3.5" fill={toneMap[tone]} className="sparkline-point" />
      </svg>

      <div className="sparkline-meta">
        <div className="sparkline-meta-block">
          <span>Min</span>
          <strong>{formatMetric(min)}</strong>
        </div>
        <div className="sparkline-meta-block sparkline-meta-block-current">
          <span>Now</span>
          <strong>{formatMetric(latest)}</strong>
        </div>
        <div className="sparkline-meta-block">
          <span>Max</span>
          <strong>{formatMetric(max)}</strong>
        </div>
      </div>
    </div>
  )
}
