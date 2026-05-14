'use client'

import { Revision } from '@/lib/types'
import { useState } from 'react'

interface RevisionPanelProps {
  revisions: Revision[]
  isOpen: boolean
  onClose: () => void
}

function formatTime(date: Date) {
  const now = new Date()
  const d = new Date(date)
  const diffMs = now.getTime() - d.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMins / 60)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins}m ago`
  if (diffHours < 24) return `${diffHours}h ago`

  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) +
    ' at ' + d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
}

export default function RevisionPanel({ revisions, isOpen, onClose }: RevisionPanelProps) {
  const [previewVersion, setPreviewVersion] = useState<number | null>(null)
  const [revertedTo, setRevertedTo] = useState<number | null>(null)

  if (!isOpen) return null

  const sorted = [...revisions].sort((a, b) => b.version - a.version)

  return (
    <div
      className="absolute top-0 right-0 h-full bg-white z-20 panel-slide-in flex flex-col"
      style={{
        width: 340,
        boxShadow: '-2px 0 8px rgba(42,82,121,0.14)',
        borderLeft: '1px solid #eaecee',
      }}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b" style={{ borderColor: '#eaecee' }}>
        <div className="flex items-center gap-2">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1d2d3e" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
          <span className="font-semibold text-sm" style={{ color: '#1d2d3e' }}>Revision History</span>
        </div>
        <button
          onClick={onClose}
          className="flex items-center justify-center w-7 h-7 rounded-md hover:bg-gray-100 transition-colors"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#556b82" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      {/* Revert success banner */}
      {revertedTo !== null && (
        <div
          className="mx-4 mt-3 px-3 py-2 rounded-lg flex items-center gap-2 fade-in"
          style={{ backgroundColor: '#e8f5e8', border: '1px solid #4caf50' }}
        >
          <span style={{ color: '#188918', fontSize: 14 }}>✓</span>
          <span style={{ color: '#1d2d3e', fontSize: 12.5, fontWeight: 500 }}>
            Reverted to version {revertedTo}
          </span>
        </div>
      )}

      {/* Revision list */}
      <div className="flex-1 overflow-y-auto px-4 py-3">
        <div className="flex flex-col gap-0.5">
          {sorted.map((rev, i) => (
            <div key={rev.id} className="relative flex gap-3">
              {/* Timeline line */}
              <div className="flex flex-col items-center" style={{ width: 20 }}>
                <div
                  className="w-3 h-3 rounded-full shrink-0 mt-1.5"
                  style={{
                    backgroundColor: i === 0 ? '#0070f2' : rev.changedBy.color,
                    border: i === 0 ? '2px solid #0070f2' : 'none',
                    boxShadow: i === 0 ? '0 0 0 3px rgba(0,112,242,0.15)' : 'none',
                  }}
                />
                {i < sorted.length - 1 && (
                  <div className="flex-1 w-px" style={{ backgroundColor: '#eaecee' }} />
                )}
              </div>

              {/* Content */}
              <div
                className={`flex-1 pb-4 group ${previewVersion === rev.version ? 'bg-blue-50 -mx-2 px-2 rounded-lg' : ''}`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium" style={{ color: '#556b82' }}>
                    v{rev.version} · {formatTime(rev.timestamp)}
                  </span>
                  {i === 0 && (
                    <span
                      className="text-xs px-1.5 py-0.5 rounded"
                      style={{ backgroundColor: '#e8f5e8', color: '#188918', fontWeight: 600, fontSize: 10 }}
                    >
                      CURRENT
                    </span>
                  )}
                </div>
                <p className="text-xs mt-0.5 mb-1" style={{ color: '#1d2d3e', lineHeight: 1.5 }}>
                  {rev.summary}
                </p>
                <div className="flex items-center gap-2">
                  <div
                    className="w-4 h-4 rounded-full flex items-center justify-center text-white shrink-0"
                    style={{ backgroundColor: rev.changedBy.color, fontSize: 7, fontWeight: 700 }}
                  >
                    {rev.changedBy.initials}
                  </div>
                  <span className="text-xs" style={{ color: '#556b82' }}>
                    {rev.changedBy.name}
                  </span>
                </div>

                {/* Revert button — shown for non-current versions */}
                {i > 0 && (
                  <div className="flex gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => setPreviewVersion(previewVersion === rev.version ? null : rev.version)}
                      className="text-xs px-2.5 py-1 rounded-md border transition-colors hover:bg-gray-50"
                      style={{ borderColor: '#d9d9d9', color: '#556b82', fontWeight: 500 }}
                    >
                      {previewVersion === rev.version ? 'Hide Preview' : 'Preview'}
                    </button>
                    <button
                      onClick={() => {
                        setRevertedTo(rev.version)
                        setPreviewVersion(null)
                        setTimeout(() => setRevertedTo(null), 4000)
                      }}
                      className="text-xs px-2.5 py-1 rounded-md text-white transition-colors hover:opacity-90"
                      style={{ backgroundColor: '#0070f2', fontWeight: 500 }}
                    >
                      Revert to this version
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="px-4 py-3 border-t text-center" style={{ borderColor: '#eaecee' }}>
        <span className="text-xs" style={{ color: '#556b82' }}>
          {revisions.length} revisions · Auto-saved continuously
        </span>
      </div>
    </div>
  )
}
