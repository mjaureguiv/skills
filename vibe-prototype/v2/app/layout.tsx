import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'SAP Signavio – Collaborative Process Modeler',
  description: 'Real-time collaborative BPMN process modeling',
  icons: {
    icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%23d1efff'/><g transform='translate(5 2.5) scale(0.56)'><path d='M26.4 48.01C26.1 48.01 25.8 47.95 25.5 47.83L1.5 38.23C0.6 37.87 0 36.97 0 36.01V7.27C0 7.03 0 6.82 0.09 6.61C0.09 6.52 0.15 6.43 0.18 6.34C0.39 5.83 0.78 5.38 1.32 5.08L1.38 5.08L11.1 0.25C11.7-0.05 12.42-0.08 13.05 0.16L37.47 9.76C38.4 10.12 39 11.02 39 11.98V40.78C39 42.1 37.92 43.18 36.6 43.18C35.28 43.18 34.2 42.1 34.2 40.78V13.66L12.27 5.02L8.28 6.97L27.27 14.56C28.17 14.92 28.77 15.82 28.77 16.78V45.58C28.77 46.39 28.38 47.11 27.72 47.56C27.33 47.83 26.85 47.98 26.37 47.98L26.4 48.01Z' fill='%230057D2'/></g></svg>",
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
