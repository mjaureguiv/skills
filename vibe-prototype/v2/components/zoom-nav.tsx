'use client'

/* NGM Zoom Navigation Bar — bottom right */

export default function ZoomNav() {
  const dispatch = (a: string) => window.dispatchEvent(new CustomEvent('zoom-control', { detail: a }))

  return (
    <div style={{
      position: 'fixed', right: 24, bottom: 24, zIndex: 40,
      display: 'flex', alignItems: 'center', gap: 0,
      background: '#fff', borderRadius: 12, padding: 8,
      boxShadow: '0 0 2px rgba(34,54,73,0.2), 0 2px 4px rgba(34,54,73,0.2)',
    }}>
      <ZoomBtn title="Full Screen" onClick={() => {}}>
        <svg width="36" height="36" viewBox="0 0 36 36" fill="currentColor"><path d="M10.8 25.99C10.8 25.99 10.79 25.99 10.78 25.99C10.68 25.99 10.59 25.97 10.51 25.93C10.41 25.89 10.32 25.83 10.24 25.75C10.16 25.67 10.1 25.58 10.06 25.48C10.03 25.4 10.01 25.3 10 25.21C10 25.21 10 25.19 10 25.18V21.78C10 21.35 10.36 20.99 10.8 20.99C11.24 20.99 11.6 21.35 11.6 21.79V23.26L14.63 20.23C14.94 19.92 15.45 19.92 15.76 20.23C16.07 20.54 16.07 21.05 15.76 21.36L12.73 24.39H14.2C14.64 24.39 15 24.75 15 25.19C15 25.63 14.64 25.99 14.2 25.99H10.8ZM23.2 24.99H18.8C18.36 24.99 18 24.63 18 24.19C18 23.75 18.36 23.39 18.8 23.39H23.2C23.31 23.39 23.4 23.3 23.4 23.19V18.79C23.4 18.35 23.76 17.99 24.2 17.99C24.64 17.99 25 18.35 25 18.79V23.19C25 24.18 24.19 24.99 23.2 24.99ZM11.8 17.99C11.36 17.99 11 17.63 11 17.19V12.79C11 11.8 11.81 10.99 12.8 10.99H17.2C17.64 10.99 18 11.35 18 11.79C18 12.23 17.64 12.59 17.2 12.59H12.8C12.69 12.59 12.6 12.68 12.6 12.79V17.19C12.6 17.63 12.24 17.99 11.8 17.99ZM20.8 15.99C20.6 15.99 20.39 15.91 20.23 15.76C19.92 15.45 19.92 14.94 20.23 14.63L23.26 11.6H21.79C21.35 11.6 20.99 11.24 20.99 10.8C20.99 10.36 21.35 10 21.79 10H25.19C25.19 10 25.21 10 25.22 10C25.32 10 25.41 10.02 25.49 10.06C25.59 10.1 25.68 10.16 25.76 10.24C25.84 10.32 25.9 10.41 25.94 10.51C25.97 10.59 25.99 10.69 26 10.78C26 10.78 26 10.8 26 10.81V14.21C26 14.65 25.64 15.01 25.2 15.01C24.76 15.01 24.4 14.65 24.4 14.21V12.74L21.37 15.77C21.21 15.93 21.01 16 20.8 16V15.99Z"/></svg>
      </ZoomBtn>
      <ZoomBtn title="Zoom to Fit" onClick={() => dispatch('fit')}>
        <svg width="36" height="36" viewBox="0 0 36 36" fill="currentColor"><path d="M10.8 11.6C10.8 11.1582 11.1582 10.8 11.6 10.8H14C14.4419 10.8 14.8 11.1582 14.8 11.6C14.8 12.0419 14.4419 12.4 14 12.4H12.4V14C12.4 14.4419 12.0419 14.8 11.6 14.8C11.1582 14.8 10.8 14.4419 10.8 14V11.6ZM21.2 11.6C21.2 11.1582 21.5582 10.8 22 10.8H24.4C24.8419 10.8 25.2 11.1582 25.2 11.6V14C25.2 14.4419 24.8419 14.8 24.4 14.8C23.9582 14.8 23.6 14.4419 23.6 14V12.4H22C21.5582 12.4 21.2 12.0419 21.2 11.6ZM17.6 15.6C16.4955 15.6 15.6 16.4955 15.6 17.6C15.6 18.7046 16.4955 19.6 17.6 19.6C18.7046 19.6 19.6 18.7046 19.6 17.6C19.6 16.4955 18.7046 15.6 17.6 15.6ZM14 17.6C14 15.6118 15.6118 14 17.6 14C19.5883 14 21.2 15.6118 21.2 17.6C21.2 18.3045 20.9977 18.9617 20.648 19.5166L21.7657 20.6344C22.0782 20.9468 22.0782 21.4533 21.7657 21.7657C21.4533 22.0782 20.9468 22.0782 20.6344 21.7657L19.5166 20.648C18.9617 20.9977 18.3045 21.2 17.6 21.2C15.6118 21.2 14 19.5883 14 17.6ZM11.6 21.2C12.0419 21.2 12.4 21.5582 12.4 22V23.6H14C14.4419 23.6 14.8 23.9582 14.8 24.4C14.8 24.8419 14.4419 25.2 14 25.2H11.6C11.1582 25.2 10.8 24.8419 10.8 24.4V22C10.8 21.5582 11.1582 21.2 11.6 21.2ZM24.4 21.2C24.8419 21.2 25.2 21.5582 25.2 22V24.4C25.2 24.8419 24.8419 25.2 24.4 25.2H22C21.5582 25.2 21.2 24.8419 21.2 24.4C21.2 23.9582 21.5582 23.6 22 23.6H23.6V22C23.6 21.5582 23.9582 21.2 24.4 21.2Z"/></svg>
      </ZoomBtn>
      <ZoomBtn title="Zoom Out" onClick={() => dispatch('out')}>
        <svg width="36" height="36" viewBox="0 0 36 36" fill="currentColor"><path d="M24.2 18.9999H11.8C11.36 18.9999 11 18.6399 11 18.1999C11 17.7599 11.36 17.3999 11.8 17.3999H24.2C24.64 17.3999 25 17.7599 25 18.1999C25 18.6399 24.64 18.9999 24.2 18.9999Z"/></svg>
      </ZoomBtn>
      <button style={{
        minWidth: 49, height: 36, display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: 14, fontWeight: 600, color: '#0064d9',
        border: 'none', background: 'transparent', borderRadius: 8, cursor: 'pointer',
        fontFamily: "var(--sapFontFamily)",
      }}
      onMouseEnter={e => (e.currentTarget.style.background = '#eff1f2')}
      onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
      >70%</button>
      <ZoomBtn title="Zoom In" onClick={() => dispatch('in')}>
        <svg width="36" height="36" viewBox="0 0 36 36" fill="currentColor"><path d="M18 25C17.56 25 17.2 24.64 17.2 24.2V18.8H11.8C11.36 18.8 11 18.44 11 18C11 17.56 11.36 17.2 11.8 17.2H17.2V11.8C17.2 11.36 17.56 11 18 11C18.44 11 18.8 11.36 18.8 11.8V17.2H24.2C24.64 17.2 25 17.56 25 18C25 18.44 24.64 18.8 24.2 18.8H18.8V24.2C18.8 24.64 18.44 25 18 25Z"/></svg>
      </ZoomBtn>
    </div>
  )
}

function ZoomBtn({ title, children, onClick }: { title: string; children: React.ReactNode; onClick: () => void }) {
  return (
    <button title={title} onClick={onClick} style={{
      width: 36, height: 36, display: 'flex', alignItems: 'center', justifyContent: 'center',
      borderRadius: 8, border: 'none', background: 'transparent',
      cursor: 'pointer', color: '#0064d9', transition: 'all 0.15s',
    }}
    onMouseEnter={e => (e.currentTarget.style.background = '#eff1f2')}
    onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
    >{children}</button>
  )
}
