'use client'

import React, { useRef, useState, useCallback, useEffect } from 'react'
import { BpmnElement, BpmnConnection, ElementLock, User } from '@/lib/types'

interface CanvasProps {
  elements: BpmnElement[]
  connections: BpmnConnection[]
  elementLocks: ElementLock[]
  remoteUsers: User[]
  selectedElementId: string | null
  onSelectElement: (id: string | null) => void
  isViewerMode: boolean
}

/* NGM BPMN styles: white fill, #131E29 stroke, rx=12 tasks */

function TaskShape({ el, isSelected, isLocked, lockUser, onClick, isViewerMode }: {
  el: BpmnElement; isSelected: boolean; isLocked: boolean; lockUser?: User; onClick: () => void; isViewerMode: boolean
}) {
  const stroke = isLocked ? (lockUser?.color || '#a461d8') : isSelected ? '#0064D9' : '#131E29'
  const sw = isSelected || isLocked ? 2 : 1.5

  return (
    <g
      className="bpmn-el"
      onClick={e => { e.stopPropagation(); if (!isViewerMode && !isLocked) onClick() }}
      style={{ cursor: isViewerMode ? 'default' : isLocked ? 'not-allowed' : 'move' }}
    >
      {/* Selection box */}
      {isSelected && <rect x={el.x - 1} y={el.y - 1} width={el.width + 2} height={el.height + 2} rx={13} fill="none" stroke="#0064D9" strokeWidth={2} />}

      <rect x={el.x} y={el.y} width={el.width} height={el.height} rx={12} ry={12}
        fill="#fff" stroke={stroke} strokeWidth={sw}
        strokeDasharray={isLocked ? '6 3' : 'none'}
      />
      <text x={el.x + el.width / 2} y={el.y + el.height / 2 + 1} textAnchor="middle" dominantBaseline="middle"
        fill="#131E29" fontSize={12} fontWeight={500}
        style={{ fontFamily: "var(--sapFontFamily, '72','72full',Arial,Helvetica,sans-serif)" }}
      >
        {el.label.length > 22
          ? <><tspan x={el.x + el.width / 2} dy="-7">{el.label.split(' ').slice(0, Math.ceil(el.label.split(' ').length / 2)).join(' ')}</tspan>
             <tspan x={el.x + el.width / 2} dy="15">{el.label.split(' ').slice(Math.ceil(el.label.split(' ').length / 2)).join(' ')}</tspan></>
          : el.label}
      </text>

      {/* Lock indicator */}
      {isLocked && lockUser && (
        <g className="lock-pulse">
          <rect x={el.x + el.width - 8} y={el.y - 14} width={Math.max(lockUser.name.length * 6.5 + 30, 80)} height={24} rx={12} fill={lockUser.color} opacity={0.9}/>
          <text x={el.x + el.width + 6} y={el.y - 2} fontSize={11} fill="white" fontWeight={600}
            style={{ fontFamily: "var(--sapFontFamily)" }}>🔒 {lockUser.name}</text>
        </g>
      )}

      {/* Selection resize handles */}
      {isSelected && !isLocked && (
        <>
          {[[el.x, el.y], [el.x + el.width, el.y], [el.x, el.y + el.height], [el.x + el.width, el.y + el.height]].map(([cx, cy], i) => (
            <rect key={i} x={cx - 4} y={cy - 4} width={8} height={8} rx={2} fill="#fff" stroke="#0064D9" strokeWidth={1.5} />
          ))}
          {/* Connect handles (blue circles at midpoints) */}
          {[[el.x + el.width / 2, el.y], [el.x + el.width, el.y + el.height / 2], [el.x + el.width / 2, el.y + el.height], [el.x, el.y + el.height / 2]].map(([cx, cy], i) => (
            <circle key={`c${i}`} cx={cx} cy={cy} r={4} fill="#0064D9" stroke="#fff" strokeWidth={1.5} style={{ cursor: 'crosshair' }} />
          ))}
        </>
      )}
    </g>
  )
}

function EventShape({ el, isEnd }: { el: BpmnElement; isEnd: boolean }) {
  const cx = el.x + el.width / 2
  const cy = el.y + el.height / 2
  const r = el.width / 2

  return (
    <g>
      {/* White background circle */}
      <circle cx={cx} cy={cy} r={r} fill="white" />
      {/* Main event circle */}
      <circle cx={cx} cy={cy} r={r - 2} fill="none" stroke="#131E29" strokeWidth={isEnd ? 3 : 1.5} />
      {/* End event inner fill */}
      {isEnd && <circle cx={cx} cy={cy} r={r - 6} fill="#131E29" opacity={0.3} />}
      {/* Label below */}
      <text x={cx} y={el.y + el.height + 16} textAnchor="middle" fill="#6a6d70" fontSize={11}
        style={{ fontFamily: "var(--sapFontFamily)" }}>{el.label}</text>
    </g>
  )
}

function GatewayShape({ el, isSelected, isLocked, lockUser, onClick, isViewerMode }: {
  el: BpmnElement; isSelected: boolean; isLocked: boolean; lockUser?: User; onClick: () => void; isViewerMode: boolean
}) {
  const cx = el.x + el.width / 2
  const cy = el.y + el.height / 2
  const stroke = isLocked ? (lockUser?.color || '#a461d8') : isSelected ? '#0064D9' : '#131E29'

  return (
    <g
      className="bpmn-el"
      onClick={e => { e.stopPropagation(); if (!isViewerMode && !isLocked) onClick() }}
      style={{ cursor: isViewerMode ? 'default' : isLocked ? 'not-allowed' : 'move' }}
    >
      {isSelected && <rect x={el.x - 1} y={el.y - 1} width={el.width + 2} height={el.height + 2} fill="none" stroke="#0064D9" strokeWidth={2} />}
      {/* NGM diamond — exact path from template */}
      <svg x={el.x - 4} y={el.y - 4} width={el.width + 8} height={el.height + 8} viewBox="0 0 40 40">
        <path d="M4.45739 24.74C2.01387 22.4156 1.96537 18.5346 4.35003 16.15L16.15 4.35003C18.5346 1.96536 22.4156 2.01387 24.74 4.45739L35.9668 16.26C38.2104 18.6186 38.1639 22.3361 35.8621 24.6379L24.6379 35.8621C22.3361 38.1639 18.6186 38.2104 16.26 35.9668L4.45739 24.74Z"
          fill="white" stroke={stroke} strokeWidth={isSelected || isLocked ? 2 : 1}
          strokeDasharray={isLocked ? '6 3' : 'none'}
        />
        {/* X marker for exclusive */}
        <path d="M14.1367 14.136L26.8646 26.8639" stroke="#131E29" strokeWidth={2.5} strokeLinecap="round"/>
        <path d="M26.8633 14.136L14.1354 26.8639" stroke="#131E29" strokeWidth={2.5} strokeLinecap="round"/>
      </svg>
      {/* Label below */}
      <text x={cx} y={cy + el.height / 2 + 20} textAnchor="middle" fill="#6a6d70" fontSize={11}
        style={{ fontFamily: "var(--sapFontFamily)" }}>{el.label}</text>

      {isLocked && lockUser && (
        <g className="lock-pulse">
          <rect x={cx + el.width / 2 - 5} y={el.y - 18} width={Math.max(lockUser.name.length * 6.5 + 30, 80)} height={24} rx={12} fill={lockUser.color} opacity={0.9}/>
          <text x={cx + el.width / 2 + 9} y={el.y - 6} fontSize={11} fill="white" fontWeight={600}
            style={{ fontFamily: "var(--sapFontFamily)" }}>🔒 {lockUser.name}</text>
        </g>
      )}
    </g>
  )
}

function ConnectionLine({ conn }: { conn: BpmnConnection }) {
  if (conn.waypoints.length < 2) return null
  const pts = conn.waypoints
  const last = pts[pts.length - 1]
  const prev = pts[pts.length - 2]

  // Build path
  let d = `M ${pts[0].x} ${pts[0].y}`
  for (let i = 1; i < pts.length; i++) {
    if (i < pts.length - 1) {
      const curr = pts[i]
      const next = pts[i + 1]
      const r = 8
      const dx1 = Math.sign(curr.x - pts[i - 1].x) * Math.min(r, Math.abs(curr.x - pts[i - 1].x))
      const dy1 = Math.sign(curr.y - pts[i - 1].y) * Math.min(r, Math.abs(curr.y - pts[i - 1].y))
      const dx2 = Math.sign(next.x - curr.x) * Math.min(r, Math.abs(next.x - curr.x))
      const dy2 = Math.sign(next.y - curr.y) * Math.min(r, Math.abs(next.y - curr.y))
      d += ` L ${curr.x - dx1} ${curr.y - dy1} Q ${curr.x} ${curr.y} ${curr.x + dx2} ${curr.y + dy2}`
    } else {
      d += ` L ${pts[i].x} ${pts[i].y}`
    }
  }

  return (
    <g>
      <defs>
        <marker id={`arrow-${conn.id}`} markerWidth="8.5" markerHeight="14.728" refX="8.17" refY="7.364" orient="auto" markerUnits="userSpaceOnUse">
          <path d="M0.391 0.293C0.781 -0.098 1.414 -0.097 1.805 0.293L8.169 6.657C8.559 7.048 8.559 7.681 8.169 8.071L1.805 14.435C1.414 14.826 0.781 14.826 0.391 14.435C0 14.045 0 13.412 0.391 13.021L5.562 7.85C5.481 7.706 5.435 7.541 5.435 7.364C5.435 7.187 5.481 7.022 5.562 6.878L0.391 1.707C0 1.316 0 0.683 0.391 0.293Z" fill="#131E29"/>
        </marker>
      </defs>
      <path d={d} fill="none" stroke="#131E29" strokeWidth={1.5} markerEnd={`url(#arrow-${conn.id})`} />
      {conn.label && (() => {
        const mx = (pts[0].x + pts[Math.min(1, pts.length - 1)].x) / 2
        const my = (pts[0].y + pts[Math.min(1, pts.length - 1)].y) / 2
        return (
          <text x={mx} y={my - 6} textAnchor="middle" fill="#6a6d70" fontSize={11}
            style={{ fontFamily: "var(--sapFontFamily)" }}>{conn.label}</text>
        )
      })()}
    </g>
  )
}

function RemoteCursor({ user }: { user: User }) {
  if (!user.isOnline || user.cursorX == null || user.cursorY == null) return null
  return (
    <g className="remote-cursor" style={{ transform: `translate(${user.cursorX}px, ${user.cursorY}px)` }}>
      <polygon points="0,0 0,16 4.5,12.5 8,20 11,18.5 7.5,11 13,11" fill={user.color} stroke="white" strokeWidth={1} />
      <rect x={14} y={14} width={Math.max(user.name.length * 6.5 + 12, 60)} height={20} rx={4} fill={user.color} />
      <text x={20} y={27} fill="white" fontSize={11} fontWeight={600}
        style={{ fontFamily: "var(--sapFontFamily)" }}>{user.name}</text>
    </g>
  )
}

export default function BpmnCanvas({
  elements, connections, elementLocks, remoteUsers,
  selectedElementId, onSelectElement, isViewerMode,
}: CanvasProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [viewBox, setViewBox] = useState({ x: -40, y: 80, w: 1400, h: 480 })
  const [isPanning, setIsPanning] = useState(false)
  const [panStart, setPanStart] = useState({ x: 0, y: 0 })
  const [zoom, setZoom] = useState(1)

  const getLock = (id: string) => elementLocks.find(l => l.elementId === id)

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if (e.target === svgRef.current || (e.target as SVGElement).tagName === 'svg' || (e.target as SVGElement).tagName === 'rect' && (e.target as SVGElement).getAttribute('fill') === 'url(#grid)') {
      setIsPanning(true)
      setPanStart({ x: e.clientX, y: e.clientY })
      onSelectElement(null)
    }
  }, [onSelectElement])

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (isPanning) {
      const dx = (e.clientX - panStart.x) / zoom
      const dy = (e.clientY - panStart.y) / zoom
      setViewBox(prev => ({ ...prev, x: prev.x - dx, y: prev.y - dy }))
      setPanStart({ x: e.clientX, y: e.clientY })
    }
  }, [isPanning, panStart, zoom])

  const handleMouseUp = useCallback(() => setIsPanning(false), [])

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault()
    const delta = e.deltaY > 0 ? 0.95 : 1.05
    const nz = Math.max(0.3, Math.min(3, zoom * delta))
    const ratio = zoom / nz
    setViewBox(prev => ({ x: prev.x + (prev.w * (1 - ratio)) / 2, y: prev.y + (prev.h * (1 - ratio)) / 2, w: prev.w * ratio, h: prev.h * ratio }))
    setZoom(nz)
  }, [zoom])

  useEffect(() => {
    const handler = (e: CustomEvent) => {
      if (e.detail === 'in') { setZoom(z => { const nz = Math.min(3, z * 1.2); const r = z / nz; setViewBox(p => ({ x: p.x + (p.w * (1 - r)) / 2, y: p.y + (p.h * (1 - r)) / 2, w: p.w * r, h: p.h * r })); return nz }) }
      else if (e.detail === 'out') { setZoom(z => { const nz = Math.max(0.3, z * 0.8); const r = z / nz; setViewBox(p => ({ x: p.x + (p.w * (1 - r)) / 2, y: p.y + (p.h * (1 - r)) / 2, w: p.w * r, h: p.h * r })); return nz }) }
      else if (e.detail === 'fit') { setViewBox({ x: -40, y: 80, w: 1400, h: 480 }); setZoom(1) }
    }
    window.addEventListener('zoom-control' as any, handler as any)
    return () => window.removeEventListener('zoom-control' as any, handler as any)
  }, [])

  return (
    <svg ref={svgRef}
      className={isPanning ? 'cursor-grabbing' : 'canvas-grab'}
      style={{ width: '100%', height: '100%', background: '#f5f5f5' }}
      viewBox={`${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`}
      onMouseDown={handleMouseDown} onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp} onMouseLeave={handleMouseUp}
      onWheel={handleWheel}
    >
      {/* Dot grid */}
      <defs>
        <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
          <circle cx="12" cy="12" r="0.7" fill="#d9d9d9" />
        </pattern>
      </defs>
      <rect x={-500} y={-500} width={3000} height={2000} fill="url(#grid)" />

      {connections.map(c => <ConnectionLine key={c.id} conn={c} />)}

      {elements.map(el => {
        const lock = getLock(el.id)
        const sel = selectedElementId === el.id
        if (el.type === 'startEvent') return <EventShape key={el.id} el={el} isEnd={false} />
        if (el.type === 'endEvent') return <EventShape key={el.id} el={el} isEnd />
        if (el.type === 'gateway') return <GatewayShape key={el.id} el={el} isSelected={sel} isLocked={!!lock} lockUser={lock?.lockedBy} onClick={() => onSelectElement(el.id)} isViewerMode={isViewerMode} />
        return <TaskShape key={el.id} el={el} isSelected={sel} isLocked={!!lock} lockUser={lock?.lockedBy} onClick={() => onSelectElement(el.id)} isViewerMode={isViewerMode} />
      })}

      {remoteUsers.filter(u => u.isOnline).map(u => <RemoteCursor key={u.id} user={u} />)}
    </svg>
  )
}
