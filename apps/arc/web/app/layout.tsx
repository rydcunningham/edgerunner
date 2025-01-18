'use client'

import React from 'react'
import { Rajdhani } from 'next/font/google'
import './globals.css'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const rajdhani = Rajdhani({
  weight: ['300', '400', '500', '600', '700'],
  subsets: ['latin'],
  display: 'swap',
})

const navItems = [
  { name: 'SIM', path: '/main' },
  { name: 'DASH', path: '/dash' },
  { name: 'SYSTEM', path: '#', subItems: [
    { name: 'FILES', path: '/files' },
    { name: 'CONFIG', path: '/config' },
  ]},
]

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  return (
    <html lang="en" className={rajdhani.className}>
      <body className="min-h-screen relative bg-black">
        {/* Sidebar */}
        <div className="fixed left-0 top-0 h-full bg-black w-[200px] z-[100] border-r border-[#5EF6FF]/20">
          <div className="flex flex-col h-full p-4 space-y-4">
            <div className="flex items-center mb-8">
              <img src="/glyph.png" alt="Edgerunner Ventures" className="h-8 w-8" />
              <div className="w-4" /> {/* Spacer */}
              <h1 className="text-[#5EF6FF] text-xl tracking-wide">
                ARC_SYSTEM
              </h1>
            </div>
            <nav>
              <ul className="space-y-4">
                {navItems.map((item) => (
                  <li key={item.name} className="relative group">
                    <Link href={item.path} className={`block hover:text-[#5EF6FF] ${pathname === item.path ? 'text-[#5EF6FF] underline underline-offset-4' : 'text-white/50'}`}>
                      {item.name}
                    </Link>
                    {item.subItems && (
                      <ul className="pl-4 space-y-4 mt-4">
                        {item.subItems.map((subItem) => (
                          <li key={subItem.name}>
                            <Link href={subItem.path} className={`block hover:text-[#5EF6FF] ${pathname === subItem.path ? 'text-[#5EF6FF] underline underline-offset-4' : 'text-white/50'}`}>
                              {subItem.name}
                            </Link>
                          </li>
                        ))}
                      </ul>
                    )}
                  </li>
                ))}
              </ul>
            </nav>
          </div>
        </div>

        <main className="ml-[200px] pt-16">
          {children}
        </main>
      </body>
    </html>
  )
} 