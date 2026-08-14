import type { MissionTimelineEntry } from '../types/mission'

type MissionTimelineProps = {
  events: MissionTimelineEntry[]
}

export function MissionTimeline({ events }: MissionTimelineProps) {
  return (
    <section className="mission-timeline panel">
      <div className="section-header">
        <div>
          <p className="eyebrow">Event Stream</p>
          <h2>Mission Timeline</h2>
        </div>
      </div>

      <div className="timeline-feed">
        {events.map((event) => (
          <article key={`${event.timestamp}-${event.event_type}`} className="timeline-item">
            <div className="timeline-node" />
            <div>
              <div className="timeline-line">
                <strong>{event.event_type}</strong>
                <span>{event.timestamp}</span>
              </div>
              <p>{event.description ?? 'Event registered without narrative detail.'}</p>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
