'use client'

export default function NotificationToast({ notifications, onDismiss }: {
  notifications: { id: string; message: string; type: string }[]; onDismiss: (id: string) => void
}) {
  if (notifications.length === 0) return null
  return (
    <div style={{ position: 'absolute', bottom: 24, left: '50%', transform: 'translateX(-50%)', display: 'flex', flexDirection: 'column', gap: 8, zIndex: 60 }}>
      {notifications.slice(0, 3).map(n => (
        <div key={n.id} className="toast-in" onClick={() => onDismiss(n.id)} style={{
          display: 'flex', alignItems: 'center', gap: 8, padding: '8px 16px',
          background: '#fff', borderRadius: 12, minWidth: 260, cursor: 'pointer',
          boxShadow: '0 2px 12px rgba(29,45,62,0.16), 0 0 1px rgba(29,45,62,0.12)',
          fontFamily: "var(--sapFontFamily)", fontSize: 13, fontWeight: 500, color: '#131e29',
        }}>
          <span style={{ fontSize: 14 }}>{n.type === 'join' ? '👤' : n.type === 'lock' ? '🔒' : '✏️'}</span>
          {n.message}
        </div>
      ))}
    </div>
  )
}
