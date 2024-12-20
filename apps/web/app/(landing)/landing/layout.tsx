import React from 'react'

export default function LandingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <main className="fixed inset-0 flex items-center justify-center">
      {children}
    </main>
  )
} 