'use client'

import { useState, useCallback } from 'react'
import ShellTopBar from '@/components/shell-top-bar'
import CanvasChrome from '@/components/canvas-chrome'
import BpmnCanvas from '@/components/bpmn-canvas'
import LeftActionPanel from '@/components/left-action-panel'
import ZoomNav from '@/components/zoom-nav'
import RevisionPanel from '@/components/revision-panel'
import NotificationToast from '@/components/notification-toast'
import { useCollaboration } from '@/lib/use-collaboration'
import { CURRENT_USER, INITIAL_DIAGRAM } from '@/lib/mock-data'

export default function DiagramPage() {
  const collab = useCollaboration()
  const [selectedElementId, setSelectedElementId] = useState<string | null>(null)
  const [isViewerMode, setIsViewerMode] = useState(false)
  const [isRevisionOpen, setIsRevisionOpen] = useState(false)

  const handleSelectElement = useCallback((id: string | null) => {
    if (isViewerMode) return
    if (id) {
      const lock = collab.elementLocks.find(l => l.elementId === id)
      if (lock) return
    }
    setSelectedElementId(id)
    if (id) setTimeout(() => collab.triggerAutoSave(), 500)
  }, [isViewerMode, collab])

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', overflow: 'hidden' }}>
      {/* Shell Top Bar — 52px */}
      <ShellTopBar />

      {/* Canvas area — fills remaining height */}
      <div style={{ flex: 1, position: 'relative', overflow: 'hidden' }}>
        <BpmnCanvas
          elements={INITIAL_DIAGRAM.elements}
          connections={INITIAL_DIAGRAM.connections}
          elementLocks={collab.elementLocks}
          remoteUsers={collab.remoteUsers}
          selectedElementId={selectedElementId}
          onSelectElement={handleSelectElement}
          isViewerMode={isViewerMode}
        />

        {/* Floating chrome */}
        <CanvasChrome
          diagramName={INITIAL_DIAGRAM.name}
          autoSaveStatus={collab.autoSaveStatus}
          currentUser={CURRENT_USER}
          remoteUsers={collab.remoteUsers}
          isViewerMode={isViewerMode}
          onToggleViewerMode={() => { setIsViewerMode(v => !v); setSelectedElementId(null) }}
          onOpenRevisions={() => setIsRevisionOpen(v => !v)}
        />

        <LeftActionPanel isViewerMode={isViewerMode} />
        <ZoomNav />

        {/* Revision Panel */}
        <RevisionPanel
          revisions={collab.revisions}
          isOpen={isRevisionOpen}
          onClose={() => setIsRevisionOpen(false)}
        />

        {/* Notifications */}
        <NotificationToast
          notifications={collab.notifications}
          onDismiss={collab.dismissNotification}
        />
      </div>
    </div>
  )
}
