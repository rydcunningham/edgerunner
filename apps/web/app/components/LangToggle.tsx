'use client'

import { useLang } from './providers/LanguageProvider'

// Kiroshi-spec .k-lang toggle — verbatim shape, same markup Cortex already
// ships. Scope note: this switches the site's own nav chrome, plus the
// brand name itself (site.nameZh — an authoritative name, not a
// machine-guess). Body prose (bio, portfolio, updates) stays English until
// it's actually translated.
export default function LangToggle() {
  const { lang, toggle } = useLang()
  return (
    <button onClick={toggle} title="Toggle language (English / 汉字)" className="k-lang">
      <span className={lang === 'en' ? 'on' : undefined}>EN</span>
      <span className={lang === 'zh' ? 'on' : undefined}>汉字</span>
    </button>
  )
}
