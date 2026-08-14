type MissionCommandDeckProps = {
  missionName: string
  missionPhase: string
  missionStatus: string
  target: string
  flightStage: string
  readinessReason: string
  isLoading: boolean
  onBootstrap: () => void
  onRefresh: () => void
}

export function MissionCommandDeck({
  missionName,
  missionPhase,
  missionStatus,
  target,
  flightStage,
  readinessReason,
  isLoading,
  onBootstrap,
  onRefresh,
}: MissionCommandDeckProps) {
  return (
    <section className="command-deck panel">
      <div className="section-header">
        <div>
          <p className="eyebrow">Primary Command Deck</p>
          <h1>{missionName}</h1>
        </div>
        <div className="command-actions">
          <button type="button" className="primary-action" onClick={onBootstrap} disabled={isLoading}>
            {isLoading ? 'Initializing...' : 'Initialize Demo'}
          </button>
          <button type="button" className="secondary-action" onClick={onRefresh} disabled={isLoading}>
            Sync Feed
          </button>
        </div>
      </div>

      <div className="command-layout">
        <div className="command-board">
          <div className="board-row">
            <div className="board-cell">
              <span>Vehicle State</span>
              <strong>{missionStatus}</strong>
            </div>
            <div className="board-cell">
              <span>Mission Phase</span>
              <strong>{missionPhase}</strong>
            </div>
            <div className="board-cell">
              <span>Flight Stage</span>
              <strong>{flightStage}</strong>
            </div>
          </div>

          <div className="command-radar">
            <div className="radar-grid" />
            <div className="radar-grid radar-grid-inner" />
            <div className="radar-axis radar-axis-horizontal" />
            <div className="radar-axis radar-axis-vertical" />
            <div className="radar-sweep" />
            <div className="radar-target">
              <span>{target}</span>
              <strong>{missionStatus}</strong>
            </div>
          </div>
        </div>

        <div className="command-stack">
          <div className="command-strip">
            <span>Target Vector</span>
            <strong>{target}</strong>
          </div>
          <div className="command-strip">
            <span>Mission State</span>
            <strong>{missionStatus}</strong>
          </div>
          <div className="command-brief">
            <p className="eyebrow">Flight Director Note</p>
            <p>{readinessReason}</p>
          </div>
        </div>
      </div>
    </section>
  )
}
