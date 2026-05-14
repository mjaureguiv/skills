'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { User, ElementLock, Revision } from './types'
import { REMOTE_USERS, MOCK_REVISIONS, CURRENT_USER, DIAGRAM_ELEMENTS } from './mock-data'

interface CollaborationState {
  remoteUsers: User[]
  elementLocks: ElementLock[]
  revisions: Revision[]
  notifications: Notification[]
  autoSaveStatus: 'saved' | 'saving' | 'idle'
}

interface Notification {
  id: string
  message: string
  timestamp: Date
  type: 'join' | 'leave' | 'edit' | 'lock'
}

// Cursor path keyframes for Sarah — she moves through the diagram
const SARAH_CURSOR_PATH = [
  { x: 300, y: 150, duration: 1500 },
  { x: 490, y: 246, duration: 2000 },   // hover over Review Request
  { x: 490, y: 246, duration: 3000 },   // stay (selects it)
  { x: 490, y: 260, duration: 1000 },   // minor movement while editing
  { x: 500, y: 250, duration: 1500 },   // still on Review Request
  { x: 663, y: 253, duration: 2000 },   // move to gateway
  { x: 663, y: 253, duration: 2000 },   // hover gateway
  { x: 840, y: 246, duration: 2000 },   // move to Process Order
  { x: 840, y: 246, duration: 3000 },   // stay on Process Order
  { x: 600, y: 180, duration: 2500 },   // idle area
  { x: 490, y: 246, duration: 2000 },   // back to Review Request
]

export function useCollaboration() {
  const [state, setState] = useState<CollaborationState>({
    remoteUsers: REMOTE_USERS.map(u => ({ ...u, isOnline: false })),
    elementLocks: [],
    revisions: [...MOCK_REVISIONS],
    notifications: [],
    autoSaveStatus: 'saved',
  })

  const animFrameRef = useRef<number>(0)
  const timeoutsRef = useRef<NodeJS.Timeout[]>([])
  const cursorPathIndex = useRef(0)
  const cursorStartTime = useRef(0)
  const isAnimating = useRef(false)

  const addNotification = useCallback((message: string, type: Notification['type']) => {
    const n: Notification = { id: Date.now().toString(), message, timestamp: new Date(), type }
    setState(prev => ({
      ...prev,
      notifications: [n, ...prev.notifications].slice(0, 10),
    }))
  }, [])

  const setUserOnline = useCallback((userId: string, online: boolean) => {
    setState(prev => ({
      ...prev,
      remoteUsers: prev.remoteUsers.map(u =>
        u.id === userId ? { ...u, isOnline: online } : u
      ),
    }))
  }, [])

  const setUserCursor = useCallback((userId: string, x: number, y: number) => {
    setState(prev => ({
      ...prev,
      remoteUsers: prev.remoteUsers.map(u =>
        u.id === userId ? { ...u, cursorX: x, cursorY: y } : u
      ),
    }))
  }, [])

  const setUserSelection = useCallback((userId: string, elementId: string | null) => {
    setState(prev => {
      const newLocks = elementId
        ? [...prev.elementLocks.filter(l => l.lockedBy.id !== userId), {
            elementId,
            lockedBy: prev.remoteUsers.find(u => u.id === userId) || REMOTE_USERS[0],
            lockedAt: new Date(),
          }]
        : prev.elementLocks.filter(l => l.lockedBy.id !== userId)

      return {
        ...prev,
        remoteUsers: prev.remoteUsers.map(u =>
          u.id === userId ? { ...u, selectedElementId: elementId } : u
        ),
        elementLocks: newLocks,
      }
    })
  }, [])

  // Animate Sarah's cursor along path
  const animateSarahCursor = useCallback(() => {
    if (!isAnimating.current) return

    const pathIdx = cursorPathIndex.current
    const nextIdx = (pathIdx + 1) % SARAH_CURSOR_PATH.length
    const current = SARAH_CURSOR_PATH[pathIdx]
    const next = SARAH_CURSOR_PATH[nextIdx]
    const elapsed = Date.now() - cursorStartTime.current
    const progress = Math.min(elapsed / current.duration, 1)

    // Ease in-out
    const eased = progress < 0.5
      ? 2 * progress * progress
      : 1 - Math.pow(-2 * progress + 2, 2) / 2

    const x = current.x + (next.x - current.x) * eased
    const y = current.y + (next.y - current.y) * eased

    setUserCursor('user-2', x, y)

    if (progress >= 1) {
      cursorPathIndex.current = nextIdx
      cursorStartTime.current = Date.now()
    }

    animFrameRef.current = requestAnimationFrame(animateSarahCursor)
  }, [setUserCursor])

  // Trigger auto-save flash
  const triggerAutoSave = useCallback(() => {
    setState(prev => ({ ...prev, autoSaveStatus: 'saving' }))
    const t = setTimeout(() => {
      setState(prev => ({ ...prev, autoSaveStatus: 'saved' }))
    }, 800)
    timeoutsRef.current.push(t)
  }, [])

  // Add a revision from Sarah's edits
  const addSarahRevision = useCallback((summary: string) => {
    setState(prev => {
      const newVersion = prev.revisions.length + 1
      const rev: Revision = {
        id: `rev-${newVersion}`,
        version: newVersion,
        changedBy: REMOTE_USERS[0],
        timestamp: new Date(),
        summary,
        elementsSnapshot: DIAGRAM_ELEMENTS,
      }
      return {
        ...prev,
        revisions: [...prev.revisions, rev],
      }
    })
  }, [])

  // Run the simulation timeline
  useEffect(() => {
    const timeouts: NodeJS.Timeout[] = []

    // 2s — Sarah joins
    timeouts.push(setTimeout(() => {
      setUserOnline('user-2', true)
      setUserCursor('user-2', 200, 150)
      addNotification('Sarah Chen joined the session', 'join')
    }, 2000))

    // 3.5s — Start Sarah's cursor animation
    timeouts.push(setTimeout(() => {
      isAnimating.current = true
      cursorStartTime.current = Date.now()
      cursorPathIndex.current = 0
      animFrameRef.current = requestAnimationFrame(animateSarahCursor)
    }, 3500))

    // 5s — Marcus joins as viewer
    timeouts.push(setTimeout(() => {
      setUserOnline('user-3', true)
      addNotification('Marcus Weber joined (view only)', 'join')
    }, 5000))

    // 7s — Sarah selects "Review Request"
    timeouts.push(setTimeout(() => {
      setUserSelection('user-2', 'task-2')
      addNotification('Sarah Chen is editing Review Request', 'lock')
    }, 7000))

    // 9s — auto-save flash
    timeouts.push(setTimeout(() => triggerAutoSave(), 9000))

    // 12s — Sarah's edit completes, she adds a revision
    timeouts.push(setTimeout(() => {
      addSarahRevision('Renamed "Review Request" to "Review & Validate Request"')
      triggerAutoSave()
    }, 12000))

    // 14s — Sarah deselects
    timeouts.push(setTimeout(() => {
      setUserSelection('user-2', null)
    }, 14000))

    // 18s — Sarah selects gateway
    timeouts.push(setTimeout(() => {
      setUserSelection('user-2', 'gw-1')
      addNotification('Sarah Chen is editing Approved?', 'lock')
    }, 18000))

    // 22s — Sarah deselects gateway
    timeouts.push(setTimeout(() => {
      setUserSelection('user-2', null)
    }, 22000))

    // 24s — Sarah selects Process Order
    timeouts.push(setTimeout(() => {
      setUserSelection('user-2', 'task-3')
    }, 24000))

    // 28s — Sarah deselects, auto-save
    timeouts.push(setTimeout(() => {
      setUserSelection('user-2', null)
      addSarahRevision('Updated Process Order task description')
      triggerAutoSave()
    }, 28000))

    timeoutsRef.current = timeouts

    return () => {
      timeouts.forEach(clearTimeout)
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current)
      isAnimating.current = false
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const dismissNotification = useCallback((id: string) => {
    setState(prev => ({
      ...prev,
      notifications: prev.notifications.filter(n => n.id !== id),
    }))
  }, [])

  return {
    ...state,
    dismissNotification,
    triggerAutoSave,
  }
}
