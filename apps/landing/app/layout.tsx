import React from 'react'
import { Rajdhani } from 'next/font/google'
import './globals.css'

const rajdhani = Rajdhani({
  weight: ['300', '400', '500', '600', '700'],
  subsets: ['latin'],
  display: 'swap',
})

export const metadata = {
  title: 'edgerunner.io',
  description: 'Coming soon',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={rajdhani.className}>
      <body className="min-h-screen relative">
        {children}
      </body>
    </html>
  )
} 