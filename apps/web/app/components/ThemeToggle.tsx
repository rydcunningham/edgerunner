'use client'

import { useTheme } from './providers/ThemeProvider'

// Kiroshi-spec .k-theme two-span toggle (DESIGN-SYSTEM.md §12) — verbatim
// shape, same markup Cortex already ships.
export default function ThemeToggle() {
  const { theme, toggle } = useTheme()
  const pick = (t: 'dark' | 'light') => { if (theme !== t) toggle() }
  return (
    <div className="k-theme" title="Toggle theme" aria-label="Toggle theme">
      <span
        role="button"
        tabIndex={0}
        className={theme === 'dark' ? 'on' : undefined}
        onClick={() => pick('dark')}
        onKeyDown={(e) => e.key === 'Enter' && pick('dark')}
      >
        DARK
      </span>
      <span
        role="button"
        tabIndex={0}
        className={theme === 'light' ? 'on' : undefined}
        onClick={() => pick('light')}
        onKeyDown={(e) => e.key === 'Enter' && pick('light')}
      >
        LIGHT
      </span>
    </div>
  )
}
