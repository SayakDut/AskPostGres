import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AskPostgres - Natural Language Database Queries',
  description: 'Query your PostgreSQL database using natural language powered by AI',
  keywords: ['PostgreSQL', 'AI', 'Natural Language', 'Database', 'SQL'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}
