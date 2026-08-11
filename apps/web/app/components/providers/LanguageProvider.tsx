'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'

export type Lang = 'en' | 'zh'
const KEY = 'edgerunner-lang'
const Ctx = createContext<{ lang: Lang; toggle: () => void }>({ lang: 'en', toggle: () => {} })

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLang] = useState<Lang>('en')

  useEffect(() => {
    const saved = window.localStorage.getItem(KEY)
    if (saved === 'zh' || saved === 'en') setLang(saved)
  }, [])

  useEffect(() => {
    document.body.dataset.lang = lang
  }, [lang])

  const toggle = () =>
    setLang((prev) => {
      const next: Lang = prev === 'en' ? 'zh' : 'en'
      window.localStorage.setItem(KEY, next)
      return next
    })

  return <Ctx.Provider value={{ lang, toggle }}>{children}</Ctx.Provider>
}

export const useLang = () => useContext(Ctx)
