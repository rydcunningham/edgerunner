'use client'

import { useLang } from './providers/LanguageProvider'
import { footerSocials, properties, site } from '../../lib/site'

export default function SiteFooter() {
  const { lang } = useLang()
  return (
    <footer className="border-t border-k-line px-6 md:px-20 py-6 mt-8">
      <div className="flex flex-col md:flex-row gap-6 md:items-center justify-between">
        <div className="text-k-faint text-xs uppercase tracking-[0.2em] font-mono">
          {lang === 'zh' ? site.nameZh : site.name} · {site.tagline}
        </div>
        <div className="flex items-center gap-6">
          {footerSocials.map((s) => (
            <a
              key={s.label}
              href={s.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-k-accent/90 hover:text-k-accent uppercase text-xs tracking-wider transition-colors"
            >
              [{s.label}]
            </a>
          ))}
        </div>
        <div className="flex items-center gap-5 text-xs uppercase tracking-wider font-mono">
          <a href={properties.cortex} className="text-k-dim hover:text-k-text transition-colors">
            Cortex ↗
          </a>
          <a href={properties.overclock} className="text-k-dim hover:text-k-text transition-colors">
            Overclock ↗
          </a>
          <a
            href={properties.newsletter}
            target="_blank"
            rel="noopener noreferrer"
            className="text-k-dim hover:text-k-text transition-colors"
          >
            Machine Yearning ↗
          </a>
        </div>
      </div>
    </footer>
  )
}
