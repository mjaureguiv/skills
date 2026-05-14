'use client'

import { Revision } from '@/lib/types'
import { useState } from 'react'

interface RevisionPanelProps { revisions: Revision[]; isOpen: boolean; onClose: () => void }

function formatTime(date: Date) {
  const d = new Date(date); const now = new Date()
  const diff = Math.floor((now.getTime() - d.getTime()) / 60000)
  if (diff < 1) return 'Just now'
  if (diff < 60) return `${diff}m ago`
  if (diff < 1440) return `${Math.floor(diff / 60)}h ago`
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) + ' at ' + d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })
}

export default function RevisionPanel({ revisions, isOpen, onClose }: RevisionPanelProps) {
  const [revertedTo, setRevertedTo] = useState<number | null>(null)
  if (!isOpen) return null
  const sorted = [...revisions].sort((a, b) => b.version - a.version)

  return (
    <div className="slide-in-right" style={{
      position: 'fixed', top: 52, right: 0, bottom: 0, zIndex: 45,
      width: 380, background: '#fff', borderLeft: '1px solid #e5e7eb',
      boxShadow: '-4px 0 24px rgba(0,0,0,0.12)', display: 'flex', flexDirection: 'column',
      fontFamily: "var(--sapFontFamily)",
    }}>
      {/* Header */}
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0 16px', height: 44, borderBottom: '1px solid #d9d9d9',
        boxShadow: '0 0 4px rgba(85,107,130,0.16)', flexShrink: 0,
      }}>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: '#131e29', margin: 0 }}>Revision History</h3>
        <button onClick={onClose} style={{
          background: 'transparent', border: 'none', cursor: 'pointer', padding: 4,
          color: '#131e29', display: 'flex', alignItems: 'center', justifyContent: 'center',
          borderRadius: 6, width: 24, height: 24,
        }}
        onMouseEnter={e => (e.currentTarget.style.background = '#f5f6f7')}
        onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
        >
          <svg width="12" height="12" viewBox="0 0 10 10" fill="#131E29"><path d="M9.1925 9.9825C8.9925 9.9825 8.7825 9.9025 8.6225 9.7525L4.9925 6.1225L1.3625 9.7525C1.0525 10.0625 0.5425 10.0625 0.2325 9.7525C-0.0775 9.4425-0.0775 8.9325 0.2325 8.6225L3.8625 4.9925L0.2325 1.3625C-0.0775 1.0525-0.0775 0.5425 0.2325 0.2325C0.5425-0.0775 1.0525-0.0775 1.3625 0.2325L4.9925 3.8625L8.6225 0.2325C8.9325-0.0775 9.4425-0.0775 9.7525 0.2325C10.0625 0.5425 10.0625 1.0525 9.7525 1.3625L6.1225 4.9925L9.7525 8.6225C10.0625 8.9325 10.0625 9.4425 9.7525 9.7525C9.5925 9.9125 9.3925 9.9825 9.1825 9.9825H9.1925Z"/></svg>
        </button>
      </div>

      {revertedTo !== null && (
        <div className="fade-in" style={{
          margin: '12px 16px 0', padding: '8px 12px', borderRadius: 8,
          background: '#e1f4ff', border: '1px solid #7bcfff',
          display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, color: '#131e29',
        }}>
          <span style={{ color: '#0064d9', fontWeight: 600 }}>✓</span>
          Reverted to version {revertedTo}
        </div>
      )}

      {/* Revision list */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px 16px 16px 16px' }}>
        {sorted.map((rev, i) => (
          <div key={rev.id} style={{ display: 'flex', gap: 12, position: 'relative' }}>
            {/* Timeline */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: 16 }}>
              <div style={{
                width: 10, height: 10, borderRadius: '50%', flexShrink: 0, marginTop: 4,
                background: i === 0 ? '#0064d9' : rev.changedBy.color,
                boxShadow: i === 0 ? '0 0 0 3px rgba(0,100,217,0.15)' : 'none',
              }} />
              {i < sorted.length - 1 && <div style={{ flex: 1, width: 1, background: '#e5e7eb' }} />}
            </div>

            {/* Content */}
            <div style={{ flex: 1, paddingBottom: 20 }} className="group">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 12, fontWeight: 600, color: '#556b82' }}>
                  v{rev.version} · {formatTime(rev.timestamp)}
                </span>
                {i === 0 && (
                  <span style={{
                    fontSize: 10, fontWeight: 700, color: '#0064d9',
                    background: '#EDF6FF', padding: '2px 6px', borderRadius: 4,
                  }}>CURRENT</span>
                )}
              </div>
              <p style={{ fontSize: 13, color: '#131e29', marginTop: 4, lineHeight: 1.5 }}>{rev.summary}</p>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 6 }}>
                <div style={{
                  width: 18, height: 18, borderRadius: '50%', background: rev.changedBy.color,
                  color: '#fff', fontSize: 7, fontWeight: 700,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                }}>{rev.changedBy.initials}</div>
                <span style={{ fontSize: 12, color: '#556b82' }}>{rev.changedBy.name}</span>
              </div>

              {i > 0 && (
                <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
                  <button onClick={() => { setRevertedTo(rev.version); setTimeout(() => setRevertedTo(null), 4000) }} style={{
                    fontSize: 13, fontWeight: 600, padding: '6px 14px', borderRadius: 10,
                    background: '#0064D9', color: '#fff', border: 'none', cursor: 'pointer',
                    fontFamily: 'inherit',
                  }}
                  onMouseEnter={e => (e.currentTarget.style.background = '#0054b6')}
                  onMouseLeave={e => (e.currentTarget.style.background = '#0064D9')}
                  >Revert</button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div style={{ padding: '10px 16px', borderTop: '1px solid #e5e7eb', textAlign: 'center' }}>
        <span style={{ fontSize: 12, color: '#556b82' }}>{revisions.length} revisions · Auto-saved continuously</span>
      </div>
    </div>
  )
}
