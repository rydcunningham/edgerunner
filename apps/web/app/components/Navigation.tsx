'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'
import { Glyph } from '@edgerunner/brand'
import { nav } from '../../lib/site'
import { useLang } from './providers/LanguageProvider'
import LangToggle from './LangToggle'
import ThemeToggle from './ThemeToggle'

function isActive(pathname: string, href: string) {
  return href === '/' ? pathname === '/' : pathname.startsWith(href)
}

export default function Navigation() {
  const pathname = usePathname()
  const { lang } = useLang()
  const [open, setOpen] = useState(false)

  useEffect(() => setOpen(false), [pathname])

  const links = nav.map((item) => {
    const active = isActive(pathname, item.href)
    return (
      <li key={item.href}>
        <Link
          href={item.href}
          className={`uppercase tracking-wider transition-colors ${
            active
              ? 'text-k-accent border-b border-k-accent pb-1'
              : 'text-k-dim hover:text-k-text'
          }`}
        >
          {lang === 'zh' ? item.labelZh : item.label}
        </Link>
      </li>
    )
  })

  return (
    <nav className="sticky top-0 z-[99] border-b border-k-line bg-k-bg/90 backdrop-blur-sm">
      <div className="flex items-center gap-6 px-6 md:px-20 py-5">
        <Link href="/" className="flex items-center gap-3 text-k-accent" aria-label="Edgerunner home">
          <Glyph size={28} title="" />
          {/* Fits at 375px (glyph + wordmark ≈ 170px, hamburger ≈ 40px), so
              there's no reason to drop it to a bare glyph on phones. */}
          <span className="font-display font-semibold tracking-[0.3em] text-sm">
            EDGERUNNER
          </span>
        </Link>

        {/* Desktop */}
        <ul className="hidden md:flex items-center space-x-8 text-sm ml-auto">{links}</ul>
        <div className="hidden md:flex items-center gap-2">
          <LangToggle />
          <ThemeToggle />
        </div>

        {/* Mobile toggle */}
        <button
          className="md:hidden ml-auto p-2"
          onClick={() => setOpen((v) => !v)}
          aria-expanded={open}
          aria-label="Menu"
        >
          <div className="w-6 flex flex-col gap-1.5">
            <span className={`block h-0.5 w-6 bg-k-accent transition-all duration-300 ${open ? 'rotate-45 translate-y-2' : ''}`} />
            <span className={`block h-0.5 w-6 bg-k-accent transition-all duration-300 ${open ? 'opacity-0' : ''}`} />
            <span className={`block h-0.5 w-6 bg-k-accent transition-all duration-300 ${open ? '-rotate-45 -translate-y-2' : ''}`} />
          </div>
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden px-6 pb-6">
          <ul className="flex flex-col space-y-5 text-lg mb-6">{links}</ul>
          <div className="flex items-center gap-2">
            <LangToggle />
            <ThemeToggle />
          </div>
        </div>
      )}
    </nav>
  )
}
