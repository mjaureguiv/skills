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
  onMouseMove?: (x: number, y: number) => void
}

// Pastel fills for BPMN shapes
const TASK_FILL = '#f0f7ff'
const TASK_STROKE = '#b0c4d8'
const EVENT_START_FILL = '#e8f5e8'
const EVENT_START_STROKE = '#4caf50'
const EVENT_END_FILL = '#fce8e8'
const EVENT_END_STROKE = '#d32f2f'
const GATEWAY_FILL = '#fff8e1'
const GATEWAY_STROKE = '#f9a825'
const SELECTED_STROKE = '#0070f2'
const CONNECTION_COLOR = '#8899aa'

function TaskShape({ el, isSelected, isLocked, lockUser, onClick, isViewerMode }: {
  el: BpmnElement
  isSelected: boolean
  isLocked: boolean
  lockUser?: User
  onClick: () => void
  isViewerMode: boolean
}) {
  const strokeColor = isLocked ? lockUser?.color || '#a461d8' : isSelected ? SELECTED_STROKE : TASK_STROKE
  const strokeWidth = isSelected || isLocked ? 2.5 : 1.5

  return (
    <g
      className="bpmn-element"
      onClick={(e) => { e.stopPropagation(); if (!isViewerMode) onClick() }}
      style={{ cursor: isViewerMode ? 'default' : isLocked ? 'not-allowed' : 'pointer' }}
    >
      <rect
        x={el.x}
        y={el.y}
        width={el.width}
        height={el.height}
        rx={8}
        ry={8}
        fill={TASK_FILL}
        stroke={strokeColor}
        strokeWidth={strokeWidth}
        strokeDasharray={isLocked ? '6 3' : 'none'}
      />
      <text
        x={el.x + el.width / 2}
        y={el.y + el.height / 2 + 1}
        textAnchor="middle"
        dominantBaseline="middle"
        fill="#1d2d3e"
        fontSize={12.5}
        fontWeight={500}
        fontFamily="Inter, sans-serif"
      >
        {el.label.length > 22
          ? <>
              <tspan x={el.x + el.width / 2} dy="-6">{el.label.split(' ').slice(0, Math.ceil(el.label.split(' ').length / 2)).join(' ')}</tspan>
              <tspan x={el.x + el.width / 2} dy="15">{el.label.split(' ').slice(Math.ceil(el.label.split(' ').length / 2)).join(' ')}</tspan>
            </>
          : el.label
        }
      </text>

      {/* Lock indicator */}
      {isLocked && lockUser && (
        <g className="lock-pulse">
          {/* Lock icon background */}
          <rect
            x={el.x + el.width - 10}
            y={el.y - 12}
            width={Math.max(lockUser.name.length * 6.5 + 28, 80)}
            height={22}
            rx={11}
            fill={lockUser.color}
            opacity={0.9}
          />
          {/* Lock icon */}
          <text
            x={el.x + el.width + 2}
            y={el.y - 1}
            fontSize={10}
            fill="white"
            fontFamily="Inter, sans-serif"
          >
            🔒
          </text>
          {/* User name */}
          <text
            x={el.x + el.width + 16}
            y={el.y + 0}
            fontSize={10.5}
            fill="white"
            fontWeight={600}
            fontFamily="Inter, sans-serif"
          >
            {lockUser.name}
          </text>
        </g>
      )}

      {/* Selection handles */}
      {isSelected && !isLocked && (
        <>
          {[
            [el.x, el.y], [el.x + el.width, el.y],
            [el.x, el.y + el.height], [el.x + el.width, el.y + el.height],
          ].map(([cx, cy], i) => (
            <rect key={i} x={cx - 4} y={cy - 4} width={8} height={8} rx={2} fill="white" stroke={SELECTED_STROKE} strokeWidth={1.5} />
          ))}
        </>
      )}
    </g>
  )
}

function EventShape({ el, isEnd }: { el: BpmnElement; isEnd: boolean }) {
  const fill = isEnd ? EVENT_END_FILL : EVENT_START_FILL
  const stroke = isEnd ? EVENT_END_STROKE : EVENT_START_STROKE

  return (
    <g>
      <circle
        cx={el.x + el.width / 2}
        cy={el.y + el.height / 2}
        r={el.width / 2}
        fill={fill}
        stroke={stroke}
        strokeWidth={isEnd ? 3 : 2}
      />
      {/* Small inner label below */}
      <text
        x={el.x + el.width / 2}
        y={el.y + el.height + 16}
        textAnchor="middle"
        fill="#556b82"
        fontSize={10}
        fontFamily="Inter, sans-serif"
      >
        {el.label}
      </text>
    </g>
  )
}

function GatewayShape({ el, isSelected, isLocked, lockUser, onClick, isViewerMode }: {
  el: BpmnElement
  isSelected: boolean
  isLocked: boolean
  lockUser?: User
  onClick: () => void
  isViewerMode: boolean
}) {
  const cx = el.x + el.width / 2
  const cy = el.y + el.height / 2
  const half = el.width / 2
  const strokeColor = isLocked ? lockUser?.color || '#a461d8' : isSelected ? SELECTED_STROKE : GATEWAY_STROKE

  return (
    <g
      className="bpmn-element"
      onClick={(e) => { e.stopPropagation(); if (!isViewerMode) onClick() }}
      style={{ cursor: isViewerMode ? 'default' : isLocked ? 'not-allowed' : 'pointer' }}
    >
      <polygon
        points={`${cx},${cy - half} ${cx + half},${cy} ${cx},${cy + half} ${cx - half},${cy}`}
        fill={GATEWAY_FILL}
        stroke={strokeColor}
        strokeWidth={isSelected || isLocked ? 2.5 : 1.5}
        strokeDasharray={isLocked ? '6 3' : 'none'}
      />
      {/* X icon inside for exclusive gateway */}
      <text
        x={cx}
        y={cy + 1}
        textAnchor="middle"
        dominantBaseline="middle"
        fill={GATEWAY_STROKE}
        fontSize={16}
        fontWeight={700}
        fontFamily="Inter, sans-serif"
      >
        ×
      </text>
      {/* Label below */}
      <text
        x={cx}
        y={cy + half + 18}
        textAnchor="middle"
        fill="#556b82"
        fontSize={11}
        fontFamily="Inter, sans-serif"
      >
        {el.label}
      </text>

      {isLocked && lockUser && (
        <g className="lock-pulse">
          <rect x={cx + half - 5} y={cy - half - 14} width={Math.max(lockUser.name.length * 6.5 + 28, 80)} height={22} rx={11} fill={lockUser.color} opacity={0.9} />
          <text x={cx + half + 7} y={cy - half - 3} fontSize={10} fill="white" fontFamily="Inter, sans-serif">🔒</text>
          <text x={cx + half + 21} y={cy - half - 2} fontSize={10.5} fill="white" fontWeight={600} fontFamily="Inter, sans-serif">{lockUser.name}</text>
        </g>
      )}
    </g>
  )
}

function ConnectionLine({ conn }: { conn: BpmnConnection }) {
  if (conn.waypoints.length < 2) return null

  const pts = conn.waypoints
  let d = `M ${pts[0].x} ${pts[0].y}`
  for (let i = 1; i < pts.length; i++) {
    // Rounded corners for orthogonal segments
    if (i < pts.length - 1) {
      const prev = pts[i - 1]
      const curr = pts[i]
      const next = pts[i + 1]
      const r = 8
      // Simple line with rounded corners at bends
      const dx1 = Math.sign(curr.x - prev.x) * Math.min(r, Math.abs(curr.x - prev.x))
      const dy1 = Math.sign(curr.y - prev.y) * Math.min(r, Math.abs(curr.y - prev.y))
      const dx2 = Math.sign(next.x - curr.x) * Math.min(r, Math.abs(next.x - curr.x))
      const dy2 = Math.sign(next.y - curr.y) * Math.min(r, Math.abs(next.y - curr.y))
      d += ` L ${curr.x - dx1} ${curr.y - dy1}`
      d += ` Q ${curr.x} ${curr.y} ${curr.x + dx2} ${curr.y + dy2}`
    } else {
      d += ` L ${pts[i].x} ${pts[i].y}`
    }
  }

  // Arrow position
  const last = pts[pts.length - 1]
  const prev = pts[pts.length - 2]
  const angle = Math.atan2(last.y - prev.y, last.x - prev.x)

  return (
    <g>
      <path d={d} fill="none" stroke={CONNECTION_COLOR} strokeWidth={1.5} />
      {/* Arrowhead */}
      <polygon
        points={`0,-4.5 9,0 0,4.5`}
        fill={CONNECTION_COLOR}
        transform={`translate(${last.x}, ${last.y}) rotate(${(angle * 180) / Math.PI})`}
      />
      {/* Label */}
      {conn.label && (
        <g>
          <rect
            x={(pts[0].x + pts[Math.min(1, pts.length - 1)].x) / 2 - 14}
            y={(pts[0].y + pts[Math.min(1, pts.length - 1)].y) / 2 - 10}
            width={28}
            height={16}
            rx={4}
            fill="white"
          />
          <text
            x={(pts[0].x + pts[Math.min(1, pts.length - 1)].x) / 2}
            y={(pts[0].y + pts[Math.min(1, pts.length - 1)].y) / 2}
            textAnchor="middle"
            dominantBaseline="middle"
            fill="#556b82"
            fontSize={10}
            fontWeight={500}
            fontFamily="Inter, sans-serif"
          >
            {conn.label}
          </text>
        </g>
      )}
    </g>
  )
}

function RemoteCursor({ user }: { user: User }) {
  if (!user.isOnline || user.cursorX == null || user.cursorY == null) return null

  return (
    <g className="remote-cursor" style={{ transform: `translate(${user.cursorX}px, ${user.cursorY}px)` }}>
      {/* Cursor arrow */}
      <polygon
        points="0,0 0,16 4.5,12.5 8,20 11,18.5 7.5,11 13,11"
        fill={user.color}
        stroke="white"
        strokeWidth={1}
      />
      {/* Name label */}
      <rect
        x={14}
        y={14}
        width={Math.max(user.name.length * 6.5 + 12, 60)}
        height={20}
        rx={4}
        fill={user.color}
      />
      <text
        x={20}
        y={27}
        fill="white"
        fontSize={11}
        fontWeight={500}
        fontFamily="Inter, sans-serif"
      >
        {user.name}
      </text>
    </g>
  )
}

export default function BpmnCanvas({
  elements,
  connections,
  elementLocks,
  remoteUsers,
  selectedElementId,
  onSelectElement,
  isViewerMode,
}: CanvasProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [viewBox, setViewBox] = useState({ x: -40, y: 80, w: 1400, h: 480 })
  const [isPanning, setIsPanning] = useState(false)
  const [panStart, setPanStart] = useState({ x: 0, y: 0 })
  const [zoom, setZoom] = useState(1)

  const getLockForElement = (elementId: string) => {
    return elementLocks.find(l => l.elementId === elementId)
  }

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if (e.target === svgRef.current || (e.target as SVGElement).tagName === 'svg') {
      setIsPanning(true)
      setPanStart({ x: e.clientX, y: e.clientY })
      onSelectElement(null)
    }
  }, [onSelectElement])

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (isPanning) {
      const dx = (e.clientX - panStart.x) / zoom
      const dy = (e.clientY - panStart.y) / zoom
      setViewBox(prev => ({
        ...prev,
        x: prev.x - dx,
        y: prev.y - dy,
      }))
      setPanStart({ x: e.clientX, y: e.clientY })
    }
  }, [isPanning, panStart, zoom])

  const handleMouseUp = useCallback(() => {
    setIsPanning(false)
  }, [])

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault()
    const delta = e.deltaY > 0 ? 0.95 : 1.05
    const newZoom = Math.max(0.3, Math.min(3, zoom * delta))
    const ratio = zoom / newZoom
    setViewBox(prev => ({
      x: prev.x + (prev.w * (1 - ratio)) / 2,
      y: prev.y + (prev.h * (1 - ratio)) / 2,
      w: prev.w * ratio,
      h: prev.h * ratio,
    }))
    setZoom(newZoom)
  }, [zoom])

  // Expose zoom controls
  useEffect(() => {
    const handler = (e: CustomEvent) => {
      if (e.detail === 'in') {
        setZoom(z => {
          const nz = Math.min(3, z * 1.2)
          const ratio = z / nz
          setViewBox(prev => ({ x: prev.x + (prev.w * (1 - ratio)) / 2, y: prev.y + (prev.h * (1 - ratio)) / 2, w: prev.w * ratio, h: prev.h * ratio }))
          return nz
        })
      } else if (e.detail === 'out') {
        setZoom(z => {
          const nz = Math.max(0.3, z * 0.8)
          const ratio = z / nz
          setViewBox(prev => ({ x: prev.x + (prev.w * (1 - ratio)) / 2, y: prev.y + (prev.h * (1 - ratio)) / 2, w: prev.w * ratio, h: prev.h * ratio }))
          return nz
        })
      } else if (e.detail === 'fit') {
        setViewBox({ x: -40, y: 80, w: 1400, h: 480 })
        setZoom(1)
      }
    }
    window.addEventListener('zoom-control' as any, handler as any)
    return () => window.removeEventListener('zoom-control' as any, handler as any)
  }, [])

  return (
    <svg
      ref={svgRef}
      className={`w-full h-full ${isPanning ? 'cursor-grabbing' : 'canvas-grab'}`}
      viewBox={`${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onWheel={handleWheel}
      style={{ background: 'white' }}
    >
      {/* Grid dots */}
      <defs>
        <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
          <circle cx="12" cy="12" r="0.8" fill="#e0e0e0" />
        </pattern>
      </defs>
      <rect x={-500} y={-500} width={3000} height={2000} fill="url(#grid)" />

      {/* Connections */}
      {connections.map(conn => (
        <ConnectionLine key={conn.id} conn={conn} />
      ))}

      {/* Elements */}
      {elements.map(el => {
        const lock = getLockForElement(el.id)
        const isSelected = selectedElementId === el.id
        const isLocked = !!lock

        if (el.type === 'startEvent') return <EventShape key={el.id} el={el} isEnd={false} />
        if (el.type === 'endEvent') return <EventShape key={el.id} el={el} isEnd />
        if (el.type === 'gateway') {
          return (
            <GatewayShape
              key={el.id}
              el={el}
              isSelected={isSelected}
              isLocked={isLocked}
              lockUser={lock?.lockedBy}
              onClick={() => onSelectElement(el.id)}
              isViewerMode={isViewerMode}
            />
          )
        }
        return (
          <TaskShape
            key={el.id}
            el={el}
            isSelected={isSelected}
            isLocked={isLocked}
            lockUser={lock?.lockedBy}
            onClick={() => {
              if (isLocked) return
              onSelectElement(el.id)
            }}
            isViewerMode={isViewerMode}
          />
        )
      })}

      {/* Remote cursors */}
      {remoteUsers.filter(u => u.isOnline).map(user => (
        <RemoteCursor key={user.id} user={user} />
      ))}
    </svg>
  )
}
