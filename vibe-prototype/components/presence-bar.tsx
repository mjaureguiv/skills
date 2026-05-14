'use client'

import { User } from '@/lib/types'

interface PresenceBarProps {
  currentUser: User
  remoteUsers: User[]
  isViewerMode: boolean
  onToggleViewerMode: () => void
  autoSaveStatus: 'saved' | 'saving' | 'idle'
  onOpenRevisions: () => void
  diagramName: string
}

function UserAvatar({ user, size = 32 }: { user: User; size?: number }) {
  return (
    <div
      className="relative flex items-center justify-center rounded-full font-semibold text-white shrink-0"
      style={{
        width: size,
        height: size,
        backgroundColor: user.color,
        fontSize: size * 0.37,
        border: `2px solid white`,
        boxShadow: '0 0 0 1px rgba(0,0,0,0.08)',
      }}
      title={`${user.name} (${user.role})`}
    >
      {user.initials}
      {/* Online indicator */}
      {user.isOnline && (
        <span
          className="absolute bottom-0 right-0 rounded-full border-2 border-white"
          style={{ width: 8, height: 8, backgroundColor: '#188918' }}
        />
      )}
    </div>
  )
}

export default function PresenceBar({
  currentUser,
  remoteUsers,
  isViewerMode,
  onToggleViewerMode,
  autoSaveStatus,
  onOpenRevisions,
  diagramName,
}: PresenceBarProps) {
  const onlineUsers = remoteUsers.filter(u => u.isOnline)

  return (
    <>
      {/* Title toolbar — top left */}
      <div
        className="absolute top-4 left-4 flex items-center gap-3 px-4 py-2.5 bg-white z-10"
        style={{
          borderRadius: 12,
          boxShadow: '0 0 1px rgba(11,41,70,0.32), 0 4px 4px rgba(42,82,121,0.14)',
        }}
      >
        {/* Signavio logo mark */}
        <div className="flex items-center gap-2">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <rect width="20" height="20" rx="4" fill="#0070f2" />
            <path d="M5 10h4v4h-4v-4zm6-4h4v8h-4v-8z" fill="white" opacity="0.9"/>
          </svg>
          <span className="text-sm font-semibold" style={{ color: '#1d2d3e', fontSize: '1.05rem' }}>
            {diagramName}
          </span>
        </div>

        {/* Auto-save indicator */}
        <div className="flex items-center gap-1.5 ml-2 pl-3 border-l" style={{ borderColor: '#eaecee' }}>
          {autoSaveStatus === 'saving' ? (
            <>
              <span className="pulse" style={{ color: '#556b82', fontSize: 12 }}>●</span>
              <span style={{ color: '#556b82', fontSize: 12 }}>Saving...</span>
            </>
          ) : (
            <>
              <span style={{ color: '#188918', fontSize: 12 }}>✓</span>
              <span style={{ color: '#556b82', fontSize: 12 }}>Saved</span>
            </>
          )}
        </div>
      </div>

      {/* Controls toolbar — top right */}
      <div
        className="absolute top-4 right-4 flex items-center gap-2 z-10"
      >
        {/* Viewer mode badge */}
        {isViewerMode && (
          <div
            className="flex items-center gap-1.5 px-3 py-1.5 bg-white fade-in"
            style={{
              borderRadius: 8,
              border: '1px solid #d9d9d9',
              color: '#556b82',
              fontSize: 12,
              fontWeight: 600,
            }}
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
            View only
          </div>
        )}

        {/* Presence avatars */}
        <div
          className="flex items-center gap-1 px-3 py-1.5 bg-white"
          style={{
            borderRadius: 12,
            boxShadow: '0 0 1px rgba(11,41,70,0.32), 0 4px 4px rgba(42,82,121,0.14)',
          }}
        >
          <UserAvatar user={currentUser} size={28} />
          {onlineUsers.map(user => (
            <div key={user.id} className="fade-in -ml-1.5">
              <UserAvatar user={user} size={28} />
            </div>
          ))}
          {onlineUsers.length > 0 && (
            <span className="ml-1 text-xs" style={{ color: '#556b82' }}>
              {onlineUsers.length + 1} online
            </span>
          )}
        </div>

        {/* Action buttons */}
        <div
          className="flex items-center gap-1 px-2 py-1.5 bg-white"
          style={{
            borderRadius: 12,
            boxShadow: '0 0 1px rgba(11,41,70,0.32), 0 4px 4px rgba(42,82,121,0.14)',
          }}
        >
          {/* Revision history */}
          <button
            onClick={onOpenRevisions}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg hover:bg-gray-50 transition-colors"
            title="Revision history"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#556b82" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
            <span style={{ color: '#556b82', fontSize: 12, fontWeight: 500 }}>History</span>
          </button>

          {/* Mode toggle (demo control) */}
          <button
            onClick={onToggleViewerMode}
            className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg hover:bg-gray-50 transition-colors"
            title={isViewerMode ? 'Switch to editor mode' : 'Switch to viewer mode'}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#556b82" strokeWidth="2">
              {isViewerMode ? (
                <>
                  <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" />
                  <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
                </>
              ) : (
                <>
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                  <circle cx="12" cy="12" r="3" />
                </>
              )}
            </svg>
            <span style={{ color: '#556b82', fontSize: 12, fontWeight: 500 }}>
              {isViewerMode ? 'Edit' : 'View'}
            </span>
          </button>
        </div>
      </div>
    </>
  )
}
