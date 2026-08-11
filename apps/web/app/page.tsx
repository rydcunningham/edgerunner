'use client'

import React from 'react'
import Link from 'next/link'
import { Glyph } from '@edgerunner/brand'
import UpdateRow from './components/UpdateRow'
import { useLang } from './components/providers/LanguageProvider'
import { site } from '../lib/site'
import { HOME_LIMIT, updates } from '../lib/content/updates'

export default function Page() {
  const { lang } = useLang()
  const recent = updates.slice(0, HOME_LIMIT)

  return (
    // Two columns, vertically centred against each other and in the viewport.
    // Same px-6/md:px-20 padding as Navigation and no max-width cap, so the
    // Updates column's right edge lines up exactly with the nav's rightmost
    // link at any viewport size (a capped, mx-auto'd width here would drift
    // from nav's uncapped one as soon as the window is wider than the cap).
    <div className="flex flex-1 items-center px-6 md:px-20 py-16">
      <div className="grid w-full grid-cols-1 items-center gap-x-20 gap-y-14 lg:grid-cols-[minmax(0,1fr)_minmax(0,560px)]">
        <section>
          <div className="text-k-accent mb-5">
            <Glyph size={80} />
          </div>
          {/* EN keeps the underscored brand-mark treatment; zh has no
              case/underscore convention of its own, so site.nameZh
              (the authoritative name, not a machine-guess) renders plain. */}
          <h1 className="text-k-accent text-3xl md:text-4xl font-display font-semibold tracking-wide">
            {lang === 'zh' ? site.nameZh : 'EDGERUNNER_VENTURES'}
          </h1>
          <p className="text-k-dim text-base mt-3">
          <span className="text-k-accent">watt-to-bit</span> capital.
          </p>
        </section>

        <section>
          <div className="flex items-center gap-3 mb-2">
            <span className="k-label">Updates</span>
            <span className="flex-1 h-px bg-k-line-strong" />
            <Link
              href="/updates"
              className="font-mono text-[10px] tracking-[0.14em] uppercase text-k-faint hover:text-k-accent transition-colors"
            >
              All →
            </Link>
          </div>
          <div>
            {recent.map((u) => (
              <UpdateRow key={`${u.date}-${u.title}`} u={u} oneLine />
            ))}
          </div>
        </section>
      </div>
    </div>
  )
}
