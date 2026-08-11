'use client'

import React, { createContext, useContext, useEffect, useRef, useState } from 'react'

// Same contract as apps/cortex's ThemeProvider (kept separate per app —
// vendored, not shared — see packages/sim's comment on why small pieces are
// duplicated rather than force a package for this little logic). Distinct
// localStorage key so toggling this product's theme never bleeds into
// another's, even though separate ports already give each its own origin.

type Theme = 'dark' | 'light'
const KEY = 'edgerunner-theme'
const Ctx = createContext<{ theme: Theme; toggle: () => void }>({ theme: 'dark', toggle: () => {} })

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('dark')

  // sync from the class the inline no-FOUC script already applied
  useEffect(() => {
    setTheme(document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark')
  }, [])

  // apply on real toggles only — skip the first run so we don't strip the
  // no-FOUC attribute before the sync above reads it
  const firstRun = useRef(true)
  useEffect(() => {
    if (firstRun.current) { firstRun.current = false; return }
    const el = document.documentElement
    if (theme === 'light') el.setAttribute('data-theme', 'light')
    else el.removeAttribute('data-theme')
  }, [theme])

  const toggle = () =>
    setTheme((prev) => {
      const next: Theme = prev === 'dark' ? 'light' : 'dark'
      window.localStorage.setItem(KEY, next)
      return next
    })

  return <Ctx.Provider value={{ theme, toggle }}>{children}</Ctx.Provider>
}

export const useTheme = () => useContext(Ctx)

// Inline script, run before paint: default is always DARK unless this
// visitor has explicitly chosen light before. Deliberately does NOT fall
// back to prefers-color-scheme like Cortex's script does — most OSes
// default to light, and silently re-theming the black/red hero from a
// stranger's system setting (rather than a click) would be a surprising
// first impression for a brand-driven marketing page.
export const themeScript = `try{if(localStorage.getItem('${KEY}')==='light')document.documentElement.setAttribute('data-theme','light')}catch(e){}`
