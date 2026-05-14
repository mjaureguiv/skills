'use client'

interface ShapePaletteProps {
  isViewerMode: boolean
}

const SHAPES = [
  { id: 'task', label: 'Task', icon: (
    <svg width="28" height="20" viewBox="0 0 28 20">
      <rect x="1" y="1" width="26" height="18" rx="4" fill="#f0f7ff" stroke="#b0c4d8" strokeWidth="1.2"/>
    </svg>
  )},
  { id: 'gateway', label: 'Gateway', icon: (
    <svg width="22" height="22" viewBox="0 0 22 22">
      <polygon points="11,1 21,11 11,21 1,11" fill="#fff8e1" stroke="#f9a825" strokeWidth="1.2"/>
    </svg>
  )},
  { id: 'start', label: 'Start', icon: (
    <svg width="20" height="20" viewBox="0 0 20 20">
      <circle cx="10" cy="10" r="8" fill="#e8f5e8" stroke="#4caf50" strokeWidth="1.5"/>
    </svg>
  )},
  { id: 'end', label: 'End', icon: (
    <svg width="20" height="20" viewBox="0 0 20 20">
      <circle cx="10" cy="10" r="8" fill="#fce8e8" stroke="#d32f2f" strokeWidth="2.5"/>
    </svg>
  )},
  { id: 'intermediate', label: 'Event', icon: (
    <svg width="20" height="20" viewBox="0 0 20 20">
      <circle cx="10" cy="10" r="8" fill="#f0f7ff" stroke="#0070f2" strokeWidth="1.5"/>
      <circle cx="10" cy="10" r="5.5" fill="none" stroke="#0070f2" strokeWidth="1"/>
    </svg>
  )},
  { id: 'pool', label: 'Pool', icon: (
    <svg width="28" height="20" viewBox="0 0 28 20">
      <rect x="1" y="1" width="26" height="18" rx="2" fill="none" stroke="#b0c4d8" strokeWidth="1.2"/>
      <line x1="7" y1="1" x2="7" y2="19" stroke="#b0c4d8" strokeWidth="1"/>
    </svg>
  )},
]

export default function ShapePalette({ isViewerMode }: ShapePaletteProps) {
  return (
    <div
      className={`absolute left-4 top-1/2 -translate-y-1/2 flex flex-col gap-1 p-1.5 bg-white z-10 ${isViewerMode ? 'toolbar-disabled' : ''}`}
      style={{
        borderRadius: 12,
        boxShadow: '0 0 1px rgba(11,41,70,0.32), 0 4px 4px rgba(42,82,121,0.14)',
      }}
    >
      {SHAPES.map(shape => (
        <button
          key={shape.id}
          className="flex flex-col items-center justify-center w-11 h-11 rounded-lg hover:bg-gray-50 transition-colors"
          title={shape.label}
          disabled={isViewerMode}
        >
          {shape.icon}
        </button>
      ))}
      {/* Separator */}
      <div className="mx-2 border-t" style={{ borderColor: '#eaecee' }} />
      {/* Connection tool */}
      <button
        className="flex flex-col items-center justify-center w-11 h-11 rounded-lg hover:bg-gray-50 transition-colors"
        title="Connection"
        disabled={isViewerMode}
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#556b82" strokeWidth="1.5">
          <line x1="5" y1="18" x2="19" y2="6" />
          <polyline points="15,6 19,6 19,10" />
        </svg>
      </button>
      {/* Text annotation */}
      <button
        className="flex flex-col items-center justify-center w-11 h-11 rounded-lg hover:bg-gray-50 transition-colors"
        title="Text"
        disabled={isViewerMode}
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#556b82" strokeWidth="1.5">
          <path d="M4 7V4h16v3M9 20h6M12 4v16" />
        </svg>
      </button>
    </div>
  )
}
