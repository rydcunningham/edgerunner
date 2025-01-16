import React, { Suspense } from 'react'
import { Rajdhani } from 'next/font/google'
import Navigation from './components/Navigation'
import DynamicTimestamp from './components/DynamicTimestamp'
import ReadingProgress from './components/ReadingProgress'
import Image from 'next/image'
import './globals.css'
import SocialTray from './components/SocialTray'

const rajdhani = Rajdhani({
  weight: ['300', '400', '500', '600', '700'],
  subsets: ['latin'],
  display: 'swap',
})

export const metadata = {
  title: 'edgerunner.io',
  description: 'Coming soon',
  icons: {
    icon: '/favicon.svg',
  },
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
        <div className="loading-screen fixed inset-0 z-[200] flex flex-col items-center justify-center bg-black">
          <div className="w-[200px] mb-8 relative">
            {/* Gray version */}
            <img
              src="/glyph_gray_nobg.svg"
              alt=""
              className="w-full h-auto absolute inset-0"
              style={{ 
                animation: 'revealGlyph 500ms ease-in-out forwards'
              }}
            />
            {/* Red version with reveal animation */}
            <img
              src="/glyph_nobg.svg"
              alt="Edgerunner glyph"
              className="w-full h-auto relative"
              style={{ 
                clipPath: 'inset(0 100% 0 0)',
                animation: 'revealGlyph 700ms ease-in-out forwards'
              }}
            />
          </div>
          <div className="w-[202px] mb-4 overflow-hidden">
            <div className="text-[#F75049] text-sm uppercase tracking-wider font-mono whitespace-pre">
              LOADING...
            </div>
          </div>
          <div className="progress-container">
            <div className="progress-bar" />
          </div>
        </div>

        {/* Left side decorative pane */}
        <div className="fixed left-0 top-0 h-full bg-black w-[42px] z-[100]">
          {/* Vertical bar */}
          <div className="absolute top-0 bottom-0 w-[1px] bg-[#F75049]/30" style={{ left: '42px' }} />
          
          <DynamicTimestamp />
          
          {/* Left bar with slashes */}
          <div className="absolute left-2.5 top-1/2 -translate-y-1/2 pointer-events-none">
            <Image
              src="/left_bar_arasaka.svg"
              alt="Decorative left bar"
              width={20}
              height={400}
              className="h-[50vh] w-auto"
            />
          </div>

          <div className="absolute left-7 bottom-3 origin-bottom-left -rotate-90 pointer-events-none">
            <p className="text-[#F75049]/50 text-xs whitespace-nowrap">EDGERUNNER VENTURES © 2025</p>
          </div>
        </div>

        <Navigation />
        <ReadingProgress />

        {children}
        <Suspense>
          <SocialTray />
        </Suspense>
      </body>
    </html>
  )
} 