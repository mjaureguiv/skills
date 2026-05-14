'use client'

import { useState, useCallback } from 'react'
import BpmnCanvas from '@/components/bpmn-canvas'
import PresenceBar from '@/components/presence-bar'
import ShapePalette from '@/components/shape-palette'
import ZoomControls from '@/components/zoom-controls'
import RevisionPanel from '@/components/revision-panel'
import NotificationToast from '@/components/notification-toast'
import PropertiesPanel from '@/components/properties-panel'
import { useCollaboration } from '@/lib/use-collaboration'
import { CURRENT_USER, INITIAL_DIAGRAM } from '@/lib/mock-data'

export default function DiagramPage() {
  const collaboration = useCollaboration()
  const [selectedElementId, setSelectedElementId] = useState<string | null>(null)
  const [isViewerMode, setIsViewerMode] = useState(false)
  const [isRevisionPanelOpen, setIsRevisionPanelOpen] = useState(false)

  const handleSelectElement = useCallback((id: string | null) => {
    if (isViewerMode) return

    // Check if element is locked by another user
    if (id) {
      const lock = collaboration.elementLocks.find(l => l.elementId === id)
      if (lock) return // Can't select locked elements
    }

    setSelectedElementId(id)

    // Trigger auto-save when selecting (simulating an edit action)
    if (id) {
      setTimeout(() => collaboration.triggerAutoSave(), 500)
    }
  }, [isViewerMode, collaboration])

  const selectedElement = selectedElementId
    ? INITIAL_DIAGRAM.elements.find(el => el.id === selectedElementId) || null
    : null

  return (
    <div className="relative w-screen h-screen overflow-hidden" style={{ background: 'white' }}>
      {/* Main BPMN Canvas */}
      <BpmnCanvas
        elements={INITIAL_DIAGRAM.elements}
        connections={INITIAL_DIAGRAM.connections}
        elementLocks={collaboration.elementLocks}
        remoteUsers={collaboration.remoteUsers}
        selectedElementId={selectedElementId}
        onSelectElement={handleSelectElement}
        isViewerMode={isViewerMode}
      />

      {/* Floating UI overlays */}
      <PresenceBar
        currentUser={CURRENT_USER}
        remoteUsers={collaboration.remoteUsers}
        isViewerMode={isViewerMode}
        onToggleViewerMode={() => {
          setIsViewerMode(v => !v)
          setSelectedElementId(null)
        }}
        autoSaveStatus={collaboration.autoSaveStatus}
        onOpenRevisions={() => setIsRevisionPanelOpen(v => !v)}
        diagramName={INITIAL_DIAGRAM.name}
      />

      {/* Shape Palette — left side */}
      <ShapePalette isViewerMode={isViewerMode} />

      {/* Zoom Controls — bottom right */}
      <ZoomControls />

      {/* Properties Panel — bottom left, shown when element selected */}
      <PropertiesPanel
        element={selectedElement}
        isViewerMode={isViewerMode}
        onClose={() => setSelectedElementId(null)}
      />

      {/* Revision Panel — slides from right */}
      <RevisionPanel
        revisions={collaboration.revisions}
        isOpen={isRevisionPanelOpen}
        onClose={() => setIsRevisionPanelOpen(false)}
      />

      {/* Notification Toasts */}
      <NotificationToast
        notifications={collaboration.notifications}
        onDismiss={collaboration.dismissNotification}
      />
    </div>
  )
}
