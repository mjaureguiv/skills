'use client'

export default function ZoomControls() {
  const dispatch = (action: string) => {
    window.dispatchEvent(new CustomEvent('zoom-control', { detail: action }))
  }

  return (
    <div
      className="absolute bottom-4 right-4 flex items-center gap-1 p-1 bg-white z-10"
      style={{
        borderRadius: 10,
        boxShadow: '0 0 1px rgba(11,41,70,0.32), 0 4px 4px rgba(42,82,121,0.14)',
      }}
    >
      <button
        onClick={() => dispatch('out')}
        className="flex items-center justify-center w-8 h-8 rounded-md hover:bg-gray-50 transition-colors"
        title="Zoom out"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#556b82" strokeWidth="2">
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
      </button>
      <button
        onClick={() => dispatch('fit')}
        className="flex items-center justify-center px-2 h-8 rounded-md hover:bg-gray-50 transition-colors"
        title="Fit to screen"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#556b82" strokeWidth="2">
          <path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7" />
        </svg>
      </button>
      <button
        onClick={() => dispatch('in')}
        className="flex items-center justify-center w-8 h-8 rounded-md hover:bg-gray-50 transition-colors"
        title="Zoom in"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#556b82" strokeWidth="2">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
      </button>
    </div>
  )
}
