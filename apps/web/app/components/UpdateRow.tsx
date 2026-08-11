import Link from 'next/link'
import { kindLabels } from '../../lib/content/updates'
import type { Update } from '../../lib/content/types'

// One update per row. Rests at low opacity so the list reads as quiet chrome;
// hover brings the whole row — text, date, rule — up to full.
export default function UpdateRow({ u, oneLine }: { u: Update; oneLine?: boolean }) {
  const inner = (
    <>
      <span className="font-mono text-[11px] tabular-nums text-k-faint shrink-0 w-[52px]">
        {u.date}
      </span>
      <span className="k-label shrink-0 w-[84px] hidden sm:block">{kindLabels[u.kind]}</span>
      {/* oneLine keeps the home rail's five rows a uniform height; the full
          title always renders on /updates. */}
      <span className={`text-k-text flex-1 min-w-0 ${oneLine ? 'truncate' : ''}`}>{u.title}</span>
      <span className="text-k-accent shrink-0 text-sm">{u.external ? '↗' : '→'}</span>
    </>
  )

  const className =
    'group flex items-baseline gap-4 border-b border-k-line py-3.5 opacity-50 hover:opacity-100 transition-opacity duration-200'

  return u.external ? (
    <a href={u.href} target="_blank" rel="noopener noreferrer" className={className}>
      {inner}
    </a>
  ) : (
    <Link href={u.href} className={className}>
      {inner}
    </Link>
  )
}
