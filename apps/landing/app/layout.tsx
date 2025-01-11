import React from 'react'
import { Rajdhani } from 'next/font/google'
import Link from 'next/link'
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
  // Format current date as YYYY.MM.DD
  const formattedDate = new Date().toISOString().split('T')[0].replace(/-/g, '.')

  return (
    <html lang="en" className={rajdhani.className}>
      <body className="min-h-screen relative bg-black">
        {/* Navigation */}
        <nav className="fixed top-8 left-24 z-[100]">
          <ul className="flex space-x-8">
            <li>
              <Link href="/" className="text-white/30 hover:text-[#F75049] text-sm uppercase tracking-wider">
                Home
              </Link>
            </li>
            <li>
              <Link href="/work" className="text-white/30 hover:text-[#F75049] text-sm uppercase tracking-wider">
                Work
              </Link>
            </li>
            <li>
              <Link href="/investments" className="text-white/30 hover:text-[#F75049] text-sm uppercase tracking-wider">
                Investments
              </Link>
            </li>
            <li>
              <Link href="/blog" className="text-white/30 hover:text-[#F75049] text-sm uppercase tracking-wider">
                Machine Yearning
              </Link>
            </li>
          </ul>
        </nav>

        {/* Date text */}
        <div className="fixed left-6 top-24 origin-top-left -rotate-90 z-40 pointer-events-none">
          <p className="text-white/30 text-sm tracking-wider">{formattedDate}</p>
        </div>

        {/* Left bar with slashes */}
        <div className="fixed left-6 top-1/2 -translate-y-1/2 z-30 pointer-events-none">
          <img
            src="assets/left bar.svg"
            alt="Decorative left bar"
            className="h-[50vh] w-auto left-bar-animation"
          />
        </div>

        {/* Footer bar */}
        <div className="fixed bottom-12 left-9 right-9 z-30 pointer-events-none">
          <img
            src="assets/footer bar.svg"
            alt="Decorative footer bar"
            className="w-full h-auto footer-bar-animation"
          />
        </div>

        {/* Bottom text */}
        <div className="fixed bottom-4 left-9 z-40 pointer-events-none">
          <p className="text-white/30 text-xs">EDGERUNNER VENTURES © 2025</p>
        </div>

        {children}
      </body>
    </html>
  )
} 