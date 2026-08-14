type FeedEntry = {
  id: string
  timestamp: string
  system: string
  status: string
  detail: string
  tone: 'cyan' | 'amber' | 'red'
}

type LiveOpsFeedProps = {
  entries: FeedEntry[]
}

export function LiveOpsFeed({ entries }: LiveOpsFeedProps) {
  return (
    <section className="live-ops-feed panel">
      <div className="section-header">
        <div>
          <p className="eyebrow">Realtime Feed</p>
          <h2>Activity Stream</h2>
        </div>
      </div>

      <div className="feed-stream">
        {entries.slice(0, 4).map((entry) => (
          <article key={entry.id} className={`feed-row feed-row-${entry.tone}`}>
            <div className="feed-row-top">
              <span>{entry.timestamp}</span>
              <strong>{entry.system}</strong>
            </div>
            <div className="feed-row-middle">
              <b className={`feed-badge feed-badge-${entry.tone}`}>{entry.status}</b>
            </div>
            <p>{entry.detail.split('. ')[0]}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
