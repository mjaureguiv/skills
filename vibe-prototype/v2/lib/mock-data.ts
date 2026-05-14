import { User, BpmnElement, BpmnConnection, Revision, DiagramState } from './types'

export const CURRENT_USER: User = {
  id: 'user-1',
  name: 'You',
  initials: 'AW',
  color: '#0070f2',
  role: 'modeler',
  isOnline: true,
}

export const REMOTE_USERS: User[] = [
  {
    id: 'user-2',
    name: 'Sarah Chen',
    initials: 'SC',
    color: '#a461d8',
    role: 'modeler',
    isOnline: false,
  },
  {
    id: 'user-3',
    name: 'Marcus Weber',
    initials: 'MW',
    color: '#e76500',
    role: 'viewer',
    isOnline: false,
  },
]

export const DIAGRAM_ELEMENTS: BpmnElement[] = [
  {
    id: 'start-1',
    type: 'startEvent',
    x: 80,
    y: 240,
    width: 36,
    height: 36,
    label: 'Start',
  },
  {
    id: 'task-1',
    type: 'task',
    x: 180,
    y: 218,
    width: 160,
    height: 56,
    label: 'Submit Purchase Request',
    description: 'Requester fills out the purchase request form with item details and cost center',
  },
  {
    id: 'task-2',
    type: 'task',
    x: 410,
    y: 218,
    width: 160,
    height: 56,
    label: 'Review Request',
    description: 'Department manager reviews the purchase request for completeness and budget',
  },
  {
    id: 'gw-1',
    type: 'gateway',
    x: 643,
    y: 233,
    width: 40,
    height: 40,
    label: 'Approved?',
  },
  {
    id: 'task-3',
    type: 'task',
    x: 760,
    y: 218,
    width: 160,
    height: 56,
    label: 'Process Order',
    description: 'Procurement team creates the purchase order in the ERP system',
  },
  {
    id: 'task-4',
    type: 'task',
    x: 990,
    y: 218,
    width: 170,
    height: 56,
    label: 'Send Confirmation',
    description: 'Automated confirmation email sent to requester and supplier',
  },
  {
    id: 'end-1',
    type: 'endEvent',
    x: 1230,
    y: 240,
    width: 36,
    height: 36,
    label: 'Completed',
  },
  {
    id: 'task-5',
    type: 'task',
    x: 760,
    y: 380,
    width: 160,
    height: 56,
    label: 'Notify Requester',
    description: 'Rejection notification with reason sent back to the requester',
  },
  {
    id: 'end-2',
    type: 'endEvent',
    x: 990,
    y: 400,
    width: 36,
    height: 36,
    label: 'Rejected',
  },
]

export const DIAGRAM_CONNECTIONS: BpmnConnection[] = [
  {
    id: 'conn-1',
    type: 'connection',
    from: 'start-1',
    to: 'task-1',
    waypoints: [
      { x: 116, y: 258 },
      { x: 180, y: 258 },
    ],
  },
  {
    id: 'conn-2',
    type: 'connection',
    from: 'task-1',
    to: 'task-2',
    waypoints: [
      { x: 340, y: 246 },
      { x: 410, y: 246 },
    ],
  },
  {
    id: 'conn-3',
    type: 'connection',
    from: 'task-2',
    to: 'gw-1',
    waypoints: [
      { x: 570, y: 246 },
      { x: 643, y: 253 },
    ],
  },
  {
    id: 'conn-4',
    type: 'connection',
    from: 'gw-1',
    to: 'task-3',
    label: 'Yes',
    waypoints: [
      { x: 683, y: 253 },
      { x: 760, y: 246 },
    ],
  },
  {
    id: 'conn-5',
    type: 'connection',
    from: 'gw-1',
    to: 'task-5',
    label: 'No',
    waypoints: [
      { x: 663, y: 273 },
      { x: 663, y: 408 },
      { x: 760, y: 408 },
    ],
  },
  {
    id: 'conn-6',
    type: 'connection',
    from: 'task-3',
    to: 'task-4',
    waypoints: [
      { x: 920, y: 246 },
      { x: 990, y: 246 },
    ],
  },
  {
    id: 'conn-7',
    type: 'connection',
    from: 'task-4',
    to: 'end-1',
    waypoints: [
      { x: 1160, y: 246 },
      { x: 1230, y: 258 },
    ],
  },
  {
    id: 'conn-8',
    type: 'connection',
    from: 'task-5',
    to: 'end-2',
    waypoints: [
      { x: 920, y: 408 },
      { x: 990, y: 418 },
    ],
  },
]

const sarahUser = REMOTE_USERS[0]
const marcusUser = REMOTE_USERS[1]

export const MOCK_REVISIONS: Revision[] = [
  {
    id: 'rev-1',
    version: 1,
    changedBy: CURRENT_USER,
    timestamp: new Date('2026-04-14T09:15:00'),
    summary: 'Created initial diagram with core process flow',
    elementsSnapshot: DIAGRAM_ELEMENTS,
  },
  {
    id: 'rev-2',
    version: 2,
    changedBy: sarahUser,
    timestamp: new Date('2026-04-14T10:32:00'),
    summary: 'Added rejection path with Notify Requester task',
    elementsSnapshot: DIAGRAM_ELEMENTS,
  },
  {
    id: 'rev-3',
    version: 3,
    changedBy: CURRENT_USER,
    timestamp: new Date('2026-04-14T14:05:00'),
    summary: 'Renamed "Create PO" to "Process Order" for clarity',
    elementsSnapshot: DIAGRAM_ELEMENTS,
  },
  {
    id: 'rev-4',
    version: 4,
    changedBy: sarahUser,
    timestamp: new Date('2026-04-14T16:48:00'),
    summary: 'Added Send Confirmation step before end event',
    elementsSnapshot: DIAGRAM_ELEMENTS,
  },
  {
    id: 'rev-5',
    version: 5,
    changedBy: CURRENT_USER,
    timestamp: new Date('2026-04-15T08:20:00'),
    summary: 'Updated gateway labels and connection annotations',
    elementsSnapshot: DIAGRAM_ELEMENTS,
  },
]

export const INITIAL_DIAGRAM: DiagramState = {
  id: 'purchase-order-processing',
  name: 'Purchase Order Processing',
  owner: 'Ariel Weinberger',
  lastModified: new Date('2026-04-15T08:20:00'),
  currentVersion: 5,
  elements: DIAGRAM_ELEMENTS,
  connections: DIAGRAM_CONNECTIONS,
}
