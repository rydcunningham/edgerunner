import React from 'react'
import type { Metadata } from 'next'
import { Glyph, LeftRail } from '@edgerunner/brand'
import Navigation from './components/Navigation'
import DynamicTimestamp from './components/DynamicTimestamp'
import SiteFooter from './components/SiteFooter'
import { ThemeProvider, themeScript } from './components/providers/ThemeProvider'
import { LanguageProvider } from './components/providers/LanguageProvider'
import '@edgerunner/tokens/kiroshi.css'
import '@edgerunner/tokens/edgerunner.css'
import '@edgerunner/brand/fonts.css'
import './globals.css'

export const metadata: Metadata = {
  metadataBase: new URL('https://edgerunner.io'),
  title: {
    default: 'Edgerunner Ventures',
    template: '%s · Edgerunner Ventures',
  },
  description: 'Watt-to-bit capital.',
  icons: { icon: '/favicon.svg' },
  openGraph: {
    type: 'website',
    url: 'https://edgerunner.io/',
    title: 'Edgerunner Ventures',
    description: 'Watt-to-bit capital.',
    images: ['/thumbnail.png'],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Edgerunner Ventures',
    description: 'Watt-to-bit capital.',
    images: ['/thumbnail.png'],
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" data-colorway="edgerunner">
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body className="k-page site-body">
        {/* Loading screen — first-paint theatre, fades out via CSS */}
        <div className="loading-screen fixed inset-0 z-[200] flex flex-col items-center justify-center bg-k-bg">
          <div className="w-[200px] mb-8 relative text-k-accent">
            <span className="absolute inset-0 text-k-faint">
              <Glyph size={200} title="" />
            </span>
            <span
              className="block relative"
              style={{ clipPath: 'inset(0 100% 0 0)', animation: 'revealGlyph 700ms ease-in-out forwards' }}
            >
              <Glyph size={200} title="Edgerunner glyph" />
            </span>
          </div>
          <div className="w-[202px] mb-4 overflow-hidden">
            <div className="text-k-accent text-sm uppercase tracking-wider font-mono whitespace-pre">
              LOADING...
            </div>
          </div>
          <div className="progress-container">
            <div className="progress-bar" />
          </div>
        </div>

        {/* Fixed decorative left rail — chrome, not content */}
        <aside className="hidden md:block fixed left-0 top-0 h-full w-[42px] z-[100] bg-k-bg" aria-hidden="true">
          <div className="absolute top-0 bottom-0 w-px bg-k-accent/30" style={{ left: '42px' }} />
          <DynamicTimestamp />
          <div className="absolute left-2.5 top-1/2 -translate-y-1/2 pointer-events-none text-k-accent">
            <LeftRail className="h-[50vh] w-auto" />
          </div>
          <div className="absolute left-7 bottom-3 origin-bottom-left -rotate-90 pointer-events-none">
            <p className="text-k-accent/50 text-xs whitespace-nowrap">
              EDGERUNNER VENTURES © {new Date().getFullYear()}
            </p>
          </div>
        </aside>

        {/* Normal document flow: sticky nav, in-flow main, footer */}
        <ThemeProvider>
          <LanguageProvider>
            <div className="md:pl-[43px] flex min-h-screen flex-col">
              <Navigation />
              {/* flex column so a short page (home) can distribute its own height */}
              <main className="flex-1 flex flex-col">{children}</main>
              <SiteFooter />
            </div>
          </LanguageProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
