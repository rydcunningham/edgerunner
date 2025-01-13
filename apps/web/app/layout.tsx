import React from 'react'
import { Rajdhani } from 'next/font/google'
import Navigation from './components/Navigation'
import DynamicTimestamp from './components/DynamicTimestamp'
import ReadingProgress from './components/ReadingProgress'
import Image from 'next/image'
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
      <body className="min-h-screen relative bg-black">
        {/* Loading Screen */}
        <div className="loading-screen fixed inset-0 z-[200] flex items-center justify-center bg-black">
          <div className="progress-container">
            <div className="progress-bar" />
          </div>
        </div>

        {/* Vertical bar */}
        <div className="fixed top-0 bottom-0 w-[1px] z-[100] bg-[#F75049]/30" style={{ left: '42px' }} />
        
        <Navigation />
        <DynamicTimestamp />
        <ReadingProgress />

        {/* Left bar with slashes */}
        <div className="fixed left-2.5 top-1/2 -translate-y-1/2 z-[100] pointer-events-none">
          <Image
            src="/left_bar_arasaka.svg"
            alt="Decorative left bar"
            width={20}
            height={400}
            className="h-[50vh] w-auto"
          />
        </div>

        <div className="fixed left-7 bottom-3 origin-bottom-left -rotate-90 z-[100] pointer-events-none">
          <p className="text-[#F75049]/50 text-xs">EDGERUNNER VENTURES © 2025</p>
        </div>

        {children}
      </body>
    </html>
  )
} 