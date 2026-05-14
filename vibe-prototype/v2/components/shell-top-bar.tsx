'use client'

/* SAP Signavio Shell Top Bar — pixel-matched to NGM-Design-Template */

export default function ShellTopBar() {
  return (
    <div style={{
      height: 52, minHeight: 52,
      background: '#fff',
      borderBottom: '1px solid #e5e7eb',
      boxShadow: '0 2px 4px rgba(34,54,73,0.08)',
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0 12px',
      zIndex: 50,
      fontFamily: "var(--sapFontFamily, '72','72full',Arial,Helvetica,sans-serif)",
    }}>
      {/* Shell Start */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, height: 36 }}>
        <ShellBtn title="Menu">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1d2d3e" strokeWidth="2" strokeLinecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </ShellBtn>
        {/* SAP Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 0 }}>
          <svg width="61" height="30" viewBox="0 0 61 30" fill="none"><path fillRule="evenodd" clipRule="evenodd" d="M0 30H30.6493L60.644 0H0V30Z" fill="url(#sapGrad)"/><path fillRule="evenodd" clipRule="evenodd" d="M35.9892 5.9998H29.9999L30.0199 20.0865L24.8045 5.99513H19.6332L15.1812 17.7638C14.7079 14.7691 11.6119 13.7358 9.17586 12.9618C7.56719 12.4451 5.85986 11.6851 5.87719 10.8451C5.89053 10.1558 6.79053 9.51646 8.5792 9.6118C9.7792 9.67646 10.8392 9.77313 12.9479 10.7918L15.0212 7.17846C13.0985 6.1998 10.4399 5.5818 8.25986 5.5798H8.24653C5.70453 5.5798 3.58786 6.40313 2.27586 7.7598C1.36119 8.70646 0.867861 9.91046 0.847861 11.2418C0.814528 13.0738 1.48586 14.3725 2.89653 15.4105C4.08853 16.2838 5.6132 16.8505 6.95653 17.2665C8.6132 17.7798 9.96653 18.2265 9.94986 19.1771C9.93653 19.5238 9.80586 19.8478 9.55653 20.1091C9.14319 20.5358 8.50986 20.6958 7.63319 20.7131C5.94186 20.7491 4.68853 20.4831 2.69119 19.3025L0.846528 22.9625C2.84186 24.0971 4.95986 24.6665 7.36653 24.6665L7.90786 24.6625C10.0025 24.6245 11.7025 24.1225 13.0532 23.0358C13.1305 22.9738 13.1999 22.9111 13.2719 22.8478L13.0452 24.0158L18.0985 23.9998L19.0052 21.6785C19.9585 22.0038 21.0425 22.1838 22.1932 22.1838C23.3145 22.1838 24.3692 22.0131 25.3045 21.7065L25.9365 23.9998L35.0032 24.0085L35.0252 18.7165H36.9545C41.6179 18.7165 44.3745 16.3431 44.3745 12.3631C44.3732 7.93046 41.6932 5.9998 35.9892 5.9998ZM22.1932 18.0411C21.4965 18.0411 20.8432 17.9198 20.2812 17.7065L22.1719 11.7365H22.2085L24.0685 17.7231C23.5085 17.9231 22.8705 18.0411 22.1925 18.0411H22.1932ZM36.3399 14.6111H35.0239V9.7998H36.3405C38.0939 9.7998 39.4939 10.3838 39.4939 12.1745C39.4925 14.0278 38.0939 14.6111 36.3405 14.6111" fill="white"/><defs><linearGradient id="sapGrad" x1="0" y1="30" x2="61" y2="0"><stop stopColor="#00B4F0"/><stop offset="0.5" stopColor="#0070F2"/><stop offset="1" stopColor="#002A86"/></linearGradient></defs></svg>
          <span style={{ fontWeight: 700, fontSize: 16, color: '#002a86' }}>Signavio</span>
        </div>
        <div style={{ width: 1, height: 16, background: '#d9d9d9' }} />
        <button style={{
          border: 'none', background: 'transparent', cursor: 'pointer',
          display: 'flex', alignItems: 'center', gap: 6,
          padding: 10, borderRadius: 8,
          fontFamily: "var(--sapFontFamily)", fontWeight: 600, fontSize: 14, color: '#1d2d3e',
        }}
        onMouseEnter={e => (e.currentTarget.style.background = '#eff1f2')}
        onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
        >
          Globalcorp Process Workspace
          <svg width="10" height="5" viewBox="0 0 10 5" fill="#1d2d3e"><path d="M9.829 0.273C10.092 0.593 10.046 1.066 9.727 1.329L5.479 4.829C5.203 5.057 4.802 5.057 4.525 4.829L0.273 1.329C-0.046 1.066-0.092 0.593 0.171 0.273C0.434-0.046 0.907-0.092 1.227 0.171L5.002 3.278L8.773 0.171C9.093-0.092 9.566-0.046 9.829 0.273Z"/></svg>
        </button>
      </div>
      {/* Shell End */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        {/* Search */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 4,
          width: 341, height: 34, padding: '4px 4px 4px 14px',
          background: '#eff1f2', borderRadius: 18,
          boxShadow: 'inset 0 0 0 1px rgba(85,107,129,0.25)',
        }}>
          <input
            type="text"
            placeholder="Search"
            style={{
              flex: 1, border: 'none', background: 'transparent', outline: 'none',
              fontFamily: "var(--sapFontFamily)", fontSize: 14, color: '#1d2d3e',
            }}
          />
          <button style={{
            width: 28, height: 26, border: 'none', background: 'transparent',
            borderRadius: 17, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <svg width="14" height="14" viewBox="0 0 14 14" fill="#131E29"><path d="M6 0C9.314 0 12 2.686 12 6C12 7.386 11.528 8.662 10.738 9.678L13.78 12.72C14.073 13.013 14.073 13.487 13.78 13.78C13.487 14.073 13.013 14.073 12.72 13.78L9.678 10.738C8.662 11.528 7.386 12 6 12C2.686 12 0 9.314 0 6C0 2.686 2.686 0 6 0ZM6 1.5C3.515 1.5 1.5 3.515 1.5 6C1.5 8.485 3.515 10.5 6 10.5C8.485 10.5 10.5 8.485 10.5 6C10.5 3.515 8.485 1.5 6 1.5Z"/></svg>
          </button>
        </div>
        <ShellBtn title="Joule">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="#131E29"><path d="M9.831 7.76C10.191 6.68 10.681 6.2 11.761 5.83C12.081 5.73 12.081 5.28 11.761 5.17C10.681 4.81 10.201 4.32 9.831 3.24C9.721 2.93 9.281 2.93 9.171 3.24C8.811 4.32 8.321 4.8 7.241 5.17C6.921 5.27 6.921 5.72 7.241 5.83C8.321 6.19 8.801 6.68 9.171 7.76C9.281 8.07 9.721 8.07 9.831 7.76Z"/><path fillRule="evenodd" clipRule="evenodd" d="M7.351 15.67C7.501 15.88 7.741 16 8.001 16C8.261 16 8.501 15.88 8.651 15.67L15.851 5.67C16.041 5.4 16.051 5.03 15.861 4.75L12.861 0.35C12.711 0.13 12.461 0 12.201 0H4.201C3.961 0 3.721 0.11 3.571 0.31L0.171 4.71C-0.049 4.99-0.059 5.38 0.151 5.67L7.351 15.67ZM8.001 13.83L1.801 5.22L4.591 1.6H11.771L14.221 5.19L8.001 13.83Z"/></svg>
        </ShellBtn>
        <div style={{ position: 'relative' }}>
          <ShellBtn title="Notifications">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1d2d3e" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 01-3.46 0"/></svg>
          </ShellBtn>
          <span style={{
            position: 'absolute', top: 0, right: 0,
            background: '#aa0808', color: '#fff', fontSize: 14, fontWeight: 700,
            padding: '0 5px', borderRadius: 16, border: '1px solid #aa0808', lineHeight: 1.2,
          }}>3</span>
        </div>
        <ShellBtn title="Help">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1d2d3e" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        </ShellBtn>
        <div style={{
          width: 36, height: 36, borderRadius: '50%',
          background: '#6b7280', color: '#fff', fontSize: 13, fontWeight: 700,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          cursor: 'pointer', border: '1px solid #e5e7eb',
        }}>AW</div>
      </div>
    </div>
  )
}

function ShellBtn({ title, children, onClick }: { title: string; children: React.ReactNode; onClick?: () => void }) {
  return (
    <button
      title={title}
      onClick={onClick}
      style={{
        width: 36, height: 36, border: 'none', background: 'transparent',
        borderRadius: 8, cursor: 'pointer', display: 'flex',
        alignItems: 'center', justifyContent: 'center', color: '#1d2d3e',
      }}
      onMouseEnter={e => (e.currentTarget.style.background = '#eff1f2')}
      onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
    >{children}</button>
  )
}
