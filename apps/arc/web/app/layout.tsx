import React from 'react'
import { Rajdhani } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const rajdhani = Rajdhani({
  weight: ['300', '400', '500', '600', '700'],
  subsets: ['latin'],
  display: 'swap',
})

export const metadata = {
  title: 'Arc',
  description: 'Arc System Interface',
}

const navItems = [
  { name: 'FILE', path: '/files' },
  { name: 'CONFIG', path: '/config' },
  { name: 'SIM', path: '/sim' },
  { name: 'DASH', path: '/dash' },
  { name: 'HELP', path: '/help' },
]

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={rajdhani.className}>
      <body className="min-h-screen relative bg-black">
        {/* Left side decorative pane */}
        <div className="fixed left-0 top-0 h-full bg-black w-[42px] z-[100]">
          <div className="absolute top-0 bottom-0 w-[1px] bg-[#F75049]/30" style={{ left: '42px' }} />
          <div className="absolute left-7 bottom-3 origin-bottom-left -rotate-90 pointer-events-none">
            <p className="text-[#F75049]/50 text-xs whitespace-nowrap">ARC SYSTEM © 2025</p>
          </div>
        </div>

        {/* Header bar */}
        <header className="fixed top-0 left-0 right-0 h-16 bg-black/90 z-40 backdrop-blur-sm border-b border-[#F75049]/20">
          <div className="flex justify-between items-center h-full px-6 ml-[42px]">
            {/* Logo and Wordmark */}
            <div className="flex items-center">
              <img src="/glyph.png" alt="Edgerunner Ventures" className="h-8 w-8" />
              <div className="w-4" /> {/* Spacer */}
              <h1 className="text-[#F75049] text-xl tracking-wide">
                ARC_SYSTEM
              </h1>
              <div className="w-4" /> {/* Spacer */}
              <h3 className="text-white/50 text-xs tracking-wide">
                AV FLEET SIMULATOR
              </h3>
            </div>

            {/* Navigation */}
            <nav>
              <ul className="flex space-x-8">
                {navItems.map((item) => (
                  <li key={item.name}>
                    <Link href={item.path} className="nav-link">
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </nav>
          </div>
        </header>

        <main className="pt-16">
          {children}
        </main>
      </body>
    </html>
  )
} 