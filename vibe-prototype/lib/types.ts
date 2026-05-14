export type UserRole = 'modeler' | 'viewer'

export interface User {
  id: string
  name: string
  initials: string
  color: string
  role: UserRole
  cursorX?: number
  cursorY?: number
  isOnline: boolean
  selectedElementId?: string | null
}

export type BpmnElementType = 'startEvent' | 'endEvent' | 'task' | 'gateway' | 'connection'

export interface BpmnElement {
  id: string
  type: BpmnElementType
  x: number
  y: number
  width: number
  height: number
  label: string
  description?: string
}

export interface BpmnConnection {
  id: string
  type: 'connection'
  from: string
  to: string
  label?: string
  waypoints: { x: number; y: number }[]
}

export interface ElementLock {
  elementId: string
  lockedBy: User
  lockedAt: Date
}

export interface Revision {
  id: string
  version: number
  changedBy: User
  timestamp: Date
  summary: string
  elementsSnapshot: BpmnElement[]
}

export interface DiagramState {
  id: string
  name: string
  owner: string
  lastModified: Date
  currentVersion: number
  elements: BpmnElement[]
  connections: BpmnConnection[]
}
