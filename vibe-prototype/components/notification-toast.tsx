'use client'

interface NotificationToastProps {
  notifications: { id: string; message: string; type: string }[]
  onDismiss: (id: string) => void
}

export default function NotificationToast({ notifications, onDismiss }: NotificationToastProps) {
  if (notifications.length === 0) return null

  // Only show the most recent 3
  const visible = notifications.slice(0, 3)

  return (
    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex flex-col gap-2 z-20">
      {visible.map((n) => (
        <div
          key={n.id}
          className="toast-enter flex items-center gap-2 px-4 py-2.5 bg-white"
          style={{
            borderRadius: 10,
            boxShadow: '0 0 1px rgba(11,41,70,0.32), 0 8px 16px rgba(42,82,121,0.18)',
            minWidth: 240,
          }}
          onClick={() => onDismiss(n.id)}
        >
          <span style={{ fontSize: 14 }}>
            {n.type === 'join' ? '👤' : n.type === 'lock' ? '🔒' : '✏️'}
          </span>
          <span className="text-xs font-medium" style={{ color: '#1d2d3e' }}>
            {n.message}
          </span>
        </div>
      ))}
    </div>
  )
}
