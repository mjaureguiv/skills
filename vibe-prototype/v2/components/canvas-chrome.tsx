'use client'

import { User } from '@/lib/types'

/* Canvas Title Bar + Right Toolbar + Collaboration Presence — NGM floating chrome */

interface CanvasChromeProps {
  diagramName: string
  autoSaveStatus: 'saved' | 'saving' | 'idle'
  currentUser: User
  remoteUsers: User[]
  isViewerMode: boolean
  onToggleViewerMode: () => void
  onOpenRevisions: () => void
}

export default function CanvasChrome({
  diagramName, autoSaveStatus, currentUser, remoteUsers,
  isViewerMode, onToggleViewerMode, onOpenRevisions,
}: CanvasChromeProps) {
  const onlineUsers = remoteUsers.filter(u => u.isOnline)

  return (
    <>
      {/* Canvas Title Bar — top left, below shell */}
      <div style={{
        position: 'fixed', left: 24, top: 68, zIndex: 40,
        display: 'flex', alignItems: 'center', gap: 8,
        background: '#fff', borderRadius: 10, padding: 8,
        boxShadow: 'var(--sap-shadow-panel)',
      }}>
        {/* Domain icon */}
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect x="0.5" y="0.5" width="31" height="31" rx="7.5" fill="#D1EFFF" stroke="#D1EFFF"/><path d="M13.6 10.4C13.6 9.51639 14.3163 8.80005 15.2 8.80005H20.8C21.6837 8.80005 22.4 9.51639 22.4 10.4V13.6C22.4 14.4837 21.6837 15.2 20.8 15.2H15.2C14.3163 15.2 13.6 14.4837 13.6 13.6V12.8H11.2V14.0687L12.5657 15.4344C12.8781 15.7468 12.8781 16.2533 12.5657 16.5657L11.2 17.9314V19.2H13.6V18.4C13.6 17.5164 14.3163 16.8 15.2 16.8H20.8C21.6837 16.8 22.4 17.5164 22.4 18.4V21.6C22.4 22.4837 21.6837 23.2 20.8 23.2H15.2C14.3163 23.2 13.6 22.4837 13.6 21.6V20.8H10.4C9.95817 20.8 9.6 20.4419 9.6 20V17.9314L8.23431 16.5657C7.9219 16.2533 7.9219 15.7468 8.23431 15.4344L9.6 14.0687V12C9.6 11.5582 9.95817 11.2 10.4 11.2H13.6V10.4ZM20.8 10.4H15.2V13.6H20.8V10.4ZM20.8 18.4H15.2V21.6H20.8V18.4Z" fill="#0057D2"/></svg>
        <span style={{ fontSize: 20, fontWeight: 900, color: '#131e29', whiteSpace: 'nowrap', lineHeight: 1 }}>
          {diagramName}
        </span>
        {/* Dropdown arrow */}
        <button style={{
          width: 28, height: 26, border: 'none', background: 'transparent',
          cursor: 'pointer', color: '#0064d9', display: 'flex', alignItems: 'center',
          justifyContent: 'center', borderRadius: 6,
        }}>
          <svg width="28" height="26" viewBox="0 0 28 26" fill="currentColor"><path d="M14.0019 16.0006C13.7819 16.0006 13.5719 15.9106 13.4219 15.7506L9.22187 11.3506C8.91187 11.0306 8.93187 10.5206 9.25187 10.2206C9.57187 9.91064 10.0819 9.93065 10.3819 10.2506L14.0019 14.0406L17.6219 10.2506C17.9319 9.93065 18.4319 9.92064 18.7519 10.2206C19.0719 10.5306 19.0819 11.0306 18.7819 11.3506L14.5819 15.7506C14.4319 15.9106 14.2219 16.0006 14.0019 16.0006Z"/></svg>
        </button>
        {/* Draft chip */}
        <span style={{
          display: 'inline-flex', alignItems: 'center', gap: 4,
          background: '#eaecee', borderRadius: 8, padding: '2px 8px 2px 4px',
          height: 20, fontSize: 13, fontWeight: 600, color: '#45484a',
        }}>
          <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M6.63 4H10.8C11.06 4 11.25 4.21 11.25 4.47V5.87C11.25 6.13 11.06 6.34 10.8 6.34C10.54 6.34 10.35 6.13 10.35 5.87V5.04H7.41L7.34 5.1V6.44C7.34 6.95 6.92 7.37 6.42 7.37H5.23L5.06 7.55V12.5H5.47C5.73 12.5 5.92 12.71 5.92 12.97C5.92 13.23 5.73 13.44 5.47 13.44H4.6C4.34 13.44 4.15 13.23 4.15 12.97V7.37C4.15 7.25 4.19 7.14 4.28 7.05L6.9 4.25C6.99 4.15 7.12 4.1 7.25 4.1z"/></svg>
          Draft
        </span>
        {/* Auto-save */}
        <span style={{
          width: 28, height: 26, display: 'flex', alignItems: 'center', justifyContent: 'center',
          color: autoSaveStatus === 'saving' ? '#0064d9' : '#0064d9',
          opacity: autoSaveStatus === 'saving' ? 1 : 0.4,
        }}
        className={autoSaveStatus === 'saving' ? 'saving-anim' : ''}
        title={autoSaveStatus === 'saving' ? 'Saving...' : 'All changes saved'}
        >
          <svg width="16" height="16" viewBox="0 0 28 26" fill="currentColor"><path d="M16.9922 12.7207C17.1421 12.9007 17.3619 13.0007 17.5918 13.0007H17.6118C17.8516 13.0007 18.0714 12.8907 18.2213 12.7107L21.8188 8.31121C22.0986 7.96125 22.0486 7.46131 21.7088 7.18134C21.3591 6.90137 20.8594 6.95137 20.5796 7.29133L17.5818 10.9509L16.4026 9.59107C16.1128 9.2611 15.6032 9.22111 15.2734 9.51107C14.9436 9.80104 14.9037 10.311 15.1935 10.6409L16.9922 12.7207Z"/><path d="M9.41757 19H17.9215C20.1999 19 21.9886 17.1702 21.9886 14.8405C21.9886 14.4005 21.6289 14.0406 21.1892 14.0406C20.7495 14.0406 20.3898 14.4005 20.3898 14.8405C20.3898 16.2803 19.3105 17.4002 17.9215 17.4002H9.41757C8.41828 17.4002 7.59886 16.5503 7.59886 15.5104C7.59886 14.4705 8.41828 13.6206 9.41757 13.6206H10.0671C10.5068 13.6206 10.8665 13.2607 10.8665 12.8207C10.8665 11.2109 11.9058 9.85104 13.3348 9.58107C13.7745 9.50108 14.0543 9.08113 13.9743 8.65118C13.8944 8.21123 13.4847 7.93126 13.045 8.01125C11.1064 8.38121 9.63742 10.011 9.32764 12.0308C7.48894 12.0708 6 13.5806 6 15.5104C6 17.4402 7.53891 19 9.41757 19Z"/></svg>
        </span>
      </div>

      {/* Canvas Right Toolbar — top right, below shell */}
      <div style={{
        position: 'fixed', right: 24, top: 68, zIndex: 40,
        display: 'flex', alignItems: 'center', gap: 8,
      }}>
        {/* Viewer mode badge */}
        {isViewerMode && (
          <div className="fade-in" style={{
            display: 'flex', alignItems: 'center', gap: 6,
            padding: '4px 12px', background: '#fff', borderRadius: 8,
            border: '1px solid #d9d9d9', fontSize: 13, fontWeight: 600, color: '#556b82',
          }}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            View only
          </div>
        )}

        {/* Collaboration presence */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 2,
          background: '#fff', borderRadius: 9, padding: 8,
          boxShadow: 'var(--sap-shadow-panel)',
        }}>
          <UserAvatar user={currentUser} size={32} />
          {onlineUsers.map(u => (
            <div key={u.id} className="fade-in" style={{ marginLeft: -6 }}>
              <UserAvatar user={u} size={32} />
            </div>
          ))}
          {onlineUsers.length > 0 && (
            <span style={{ marginLeft: 6, fontSize: 13, fontWeight: 600, color: '#556b82' }}>
              {onlineUsers.length + 1}
            </span>
          )}
        </div>

        {/* Toolbar actions */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 0,
          background: '#fff', borderRadius: 9, padding: 8,
          boxShadow: 'var(--sap-shadow-panel)',
        }}>
          <TbBtn title="History" onClick={onOpenRevisions}>
            <svg width="36" height="36" viewBox="0 0 36 36" fill="currentColor"><path d="M18 10C13.58 10 10 13.58 10 18C10 22.42 13.58 26 18 26C22.42 26 26 22.42 26 18C26 13.58 22.42 10 18 10ZM18 24.4C14.47 24.4 11.6 21.53 11.6 18C11.6 14.47 14.47 11.6 18 11.6C21.53 11.6 24.4 14.47 24.4 18C24.4 21.53 21.53 24.4 18 24.4ZM18.8 14C18.8 13.56 18.44 13.2 18 13.2C17.56 13.2 17.2 13.56 17.2 14V18C17.2 18.21 17.29 18.42 17.45 18.57L20.25 21.37C20.56 21.68 21.07 21.68 21.38 21.37C21.69 21.06 21.69 20.55 21.38 20.24L18.8 17.66V14Z"/></svg>
          </TbBtn>
          <div style={{ width: 0, height: 36, borderLeft: '1px solid rgba(85,107,129,0.25)' }} />
          <TbBtn title={isViewerMode ? 'Switch to editor' : 'Switch to viewer'} onClick={onToggleViewerMode}>
            {isViewerMode ? (
              <svg width="36" height="36" viewBox="0 0 36 36" fill="currentColor"><path d="M18 11C13.4 11 9.52 13.73 8 17.5C9.52 21.27 13.4 24 18 24C22.6 24 26.48 21.27 28 17.5C26.48 13.73 22.6 11 18 11ZM18 22C15.51 22 13.5 19.99 13.5 17.5C13.5 15.01 15.51 13 18 13C20.49 13 22.5 15.01 22.5 17.5C22.5 19.99 20.49 22 18 22ZM18 14.5C16.34 14.5 15 15.84 15 17.5C15 19.16 16.34 20.5 18 20.5C19.66 20.5 21 19.16 21 17.5C21 15.84 19.66 14.5 18 14.5Z"/></svg>
            ) : (
              <svg width="36" height="36" viewBox="0 0 36 36" fill="currentColor"><path d="M23.7 11.0344C23.3875 10.7219 22.881 10.7219 22.5686 11.0344L11.0344 22.5686C10.7219 22.881 10.7219 23.3875 11.0344 23.7C11.3469 24.0125 11.8534 24.0125 12.1659 23.7L23.7 12.1659C24.0125 11.8534 24.0125 11.3469 23.7 11.0344Z"/><path d="M18 12C15.9 12 14 12.7 12.4 13.8L13.6 15C14.8 14.2 16.3 13.6 18 13.6C21.5 13.6 24.4 16.1 25.5 17.5C25 18.2 23.9 19.5 22.5 20.5L23.7 21.7C25.7 20.3 27 18.5 27.5 17.7C27.7 17.4 27.7 17 27.5 16.7C26.8 15.7 23 11 18 12Z"/><path d="M21.5 17.5C21.5 16.3 20.9 15.3 20 14.7L14.7 20C15.3 20.9 16.3 21.5 17.5 21.5C19.7 21.5 21.5 19.7 21.5 17.5Z"/></svg>
            )}
          </TbBtn>
        </div>
      </div>
    </>
  )
}

function UserAvatar({ user, size }: { user: User; size: number }) {
  return (
    <div
      title={`${user.name} (${user.role})`}
      style={{
        width: size, height: size, borderRadius: '50%',
        background: user.color, color: '#fff',
        fontSize: size * 0.36, fontWeight: 700,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        border: '2px solid #fff',
        cursor: 'pointer', position: 'relative', flexShrink: 0,
      }}
    >
      {user.initials}
      {user.isOnline && (
        <span style={{
          position: 'absolute', bottom: -1, right: -1,
          width: 8, height: 8, borderRadius: '50%',
          background: '#188918', border: '2px solid #fff',
        }} />
      )}
    </div>
  )
}

function TbBtn({ title, children, onClick }: { title: string; children: React.ReactNode; onClick?: () => void }) {
  return (
    <button
      title={title}
      onClick={onClick}
      style={{
        width: 36, height: 36, border: 'none', background: 'transparent',
        cursor: 'pointer', color: '#0064d9', display: 'flex', alignItems: 'center',
        justifyContent: 'center', borderRadius: 8, transition: 'background 0.15s',
      }}
      onMouseEnter={e => (e.currentTarget.style.background = '#eff1f2')}
      onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
    >{children}</button>
  )
}
