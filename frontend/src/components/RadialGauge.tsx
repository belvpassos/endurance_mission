type RadialGaugeProps = {
  value: number
  min?: number
  max?: number
  showReadout?: boolean
  tone?: 'cyan' | 'amber' | 'red'
}

const toneMap = {
  cyan: '#67d1ff',
  amber: '#ffbe55',
  red: '#ff7070',
}

export function RadialGauge({ value, min = 0, max = 100, showReadout = false, tone = 'cyan' }: RadialGaugeProps) {
  const progress = Math.max(0, Math.min((value - min) / Math.max(max - min, 1), 1))
  const radius = 34
  const circumference = 2 * Math.PI * radius
  const dashOffset = circumference * (1 - progress)

  function formatMetric(metric: number) {
    return metric.toFixed(Math.abs(max - min) > 10 ? 0 : 1)
  }

  return (
    <div className="radial-gauge-shell" aria-hidden="true">
      <svg className="radial-gauge" viewBox="0 0 96 96" role="img">
        <circle className="radial-gauge-bg" cx="48" cy="48" r={radius} />
        <circle
          className="radial-gauge-progress"
          cx="48"
          cy="48"
          r={radius}
          stroke={toneMap[tone]}
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
        />
        <circle className="radial-gauge-core" cx="48" cy="48" r="22" />
      </svg>

      {showReadout ? (
        <div className="radial-gauge-readout">
          <div className="radial-gauge-readout-block">
            <span>Min</span>
            <strong>{formatMetric(min)}</strong>
          </div>
          <div className="radial-gauge-readout-block radial-gauge-readout-current">
            <span>Now</span>
            <strong>{formatMetric(value)}</strong>
          </div>
          <div className="radial-gauge-readout-block">
            <span>Max</span>
            <strong>{formatMetric(max)}</strong>
          </div>
        </div>
      ) : null}
    </div>
  )
}
