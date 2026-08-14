type MetricBarProps = {
  value: number
  min?: number
  max?: number
  tone?: 'cyan' | 'amber' | 'red'
}

const toneMap = {
  cyan: 'linear-gradient(90deg, #67d1ff, #93ebff)',
  amber: 'linear-gradient(90deg, #ffbe55, #ffd978)',
  red: 'linear-gradient(90deg, #ff7070, #ff9b9b)',
}

export function MetricBar({ value, min = 0, max = 100, tone = 'cyan' }: MetricBarProps) {
  const progress = Math.max(0, Math.min(((value - min) / Math.max(max - min, 1)) * 100, 100))
  const checkpoints = [min, min + (max - min) / 3, min + ((max - min) * 2) / 3, max]

  function formatMetric(metric: number) {
    return metric.toFixed(Math.abs(max - min) > 10 ? 0 : 1)
  }

  return (
    <div className="metric-bar" aria-hidden="true">
      <div className="metric-bar-track">
        <div className="metric-bar-fill" style={{ width: `${progress}%`, background: toneMap[tone] }} />
      </div>
      <div className="metric-bar-ticks">
        <span />
        <span />
        <span />
        <span />
      </div>
      <div className="metric-bar-labels">
        {checkpoints.map((checkpoint, index) => (
          <strong key={`${tone}-${index}-${checkpoint}`}>{formatMetric(checkpoint)}</strong>
        ))}
      </div>
      <div className="metric-bar-readout">
        <span>Current</span>
        <strong>{formatMetric(value)}</strong>
      </div>
    </div>
  )
}
