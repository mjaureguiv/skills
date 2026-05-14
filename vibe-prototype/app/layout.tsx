import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'SAP Signavio – Collaborative Process Modeler',
  description: 'Real-time collaborative BPMN process modeling',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
