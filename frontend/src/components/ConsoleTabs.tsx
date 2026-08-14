type ConsoleTabsProps = {
  tabs: string[]
  activeTab: string
  onSelect: (tab: string) => void
}

export function ConsoleTabs({ tabs, activeTab, onSelect }: ConsoleTabsProps) {
  return (
    <nav className="console-tabs panel" aria-label="Mission stations">
      <div className="console-tab-list">
        {tabs.map((tab) => (
          <button
            key={tab}
            type="button"
            className={`console-tab${tab === activeTab ? ' console-tab-active' : ''}`}
            onClick={() => onSelect(tab)}
          >
            {tab}
          </button>
        ))}
      </div>
    </nav>
  )
}
