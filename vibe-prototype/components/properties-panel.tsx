'use client'

import { BpmnElement } from '@/lib/types'

interface PropertiesPanelProps {
  element: BpmnElement | null
  isViewerMode: boolean
  onClose: () => void
}

export default function PropertiesPanel({ element, isViewerMode, onClose }: PropertiesPanelProps) {
  if (!element) return null

  return (
    <div
      className="absolute bottom-4 left-20 bg-white z-10 fade-in"
      style={{
        borderRadius: 12,
        boxShadow: '0 0 1px rgba(11,41,70,0.32), 0 4px 4px rgba(42,82,121,0.14)',
        width: 280,
      }}
    >
      <div className="flex items-center justify-between px-4 py-2.5 border-b" style={{ borderColor: '#eaecee' }}>
        <span className="text-xs font-semibold" style={{ color: '#1d2d3e' }}>Properties</span>
        <button
          onClick={onClose}
          className="flex items-center justify-center w-5 h-5 rounded hover:bg-gray-100 transition-colors"
        >
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#556b82" strokeWidth="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
      <div className="px-4 py-3 space-y-3">
        {/* Name */}
        <div>
          <label className="block text-xs font-medium mb-1" style={{ color: '#556b82' }}>Name</label>
          <input
            type="text"
            defaultValue={element.label}
            disabled={isViewerMode}
            className="w-full px-2.5 py-1.5 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-100"
            style={{
              borderColor: '#d9d9d9',
              color: '#1d2d3e',
              fontSize: 13,
              backgroundColor: isViewerMode ? '#f5f6f7' : 'white',
            }}
          />
        </div>
        {/* Type */}
        <div>
          <label className="block text-xs font-medium mb-1" style={{ color: '#556b82' }}>Type</label>
          <div
            className="px-2.5 py-1.5 border rounded-md text-sm"
            style={{ borderColor: '#d9d9d9', color: '#556b82', fontSize: 13, backgroundColor: '#f5f6f7' }}
          >
            {element.type === 'task' ? 'User Task' : element.type === 'gateway' ? 'Exclusive Gateway' : element.type}
          </div>
        </div>
        {/* Description */}
        {element.description && (
          <div>
            <label className="block text-xs font-medium mb-1" style={{ color: '#556b82' }}>Documentation</label>
            <textarea
              defaultValue={element.description}
              disabled={isViewerMode}
              rows={3}
              className="w-full px-2.5 py-1.5 border rounded-md text-sm outline-none focus:ring-2 focus:ring-blue-100 resize-none"
              style={{
                borderColor: '#d9d9d9',
                color: '#1d2d3e',
                fontSize: 12,
                lineHeight: 1.5,
                backgroundColor: isViewerMode ? '#f5f6f7' : 'white',
              }}
            />
          </div>
        )}
      </div>
    </div>
  )
}
