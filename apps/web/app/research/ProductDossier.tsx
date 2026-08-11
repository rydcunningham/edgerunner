import Link from 'next/link'
import MediaPanel from '../components/MediaPanel'
import { getProduct } from '../../lib/content/research'
import { TWO_COL_GRID, TWO_COL_PAGE } from '../../lib/layout'
import { socials } from '../../lib/site'

const X_URL = socials.find((s) => s.label === 'x')!.url

// Shared front-door template for the two products. Access runs through a
// DM, not a form or an email address — there's no backend in M1 to receive
// a request, and this is the channel that's actually read.
export default function ProductDossier({ slug }: { slug: 'cortex' | 'overclock' }) {
  const p = getProduct(slug)!
  const hasMedia = Boolean(p.media?.length)

  return (
    <div className={`px-6 md:px-20 py-14 ${hasMedia ? TWO_COL_PAGE : 'max-w-[900px]'}`}>
      <Link
        href="/research"
        className="font-mono text-[11px] tracking-[0.14em] uppercase text-k-dim hover:text-k-text transition-colors"
      >
        ← Research
      </Link>

      {/* Two columns starting at the same line: dossier left, media rail right. */}
      <div className={hasMedia ? TWO_COL_GRID : 'mt-8'}>
        <div>
          <header className="mb-10">
            <div className="flex items-baseline gap-4 flex-wrap">
              <h1 className="font-display font-bold text-3xl tracking-[0.24em] text-k-text">
                {p.name}
              </h1>
              <span className="k-chip k-chip--accent text-[10px]">{p.status}</span>
            </div>
            <p className="text-k-accent mt-2">{p.tagline}</p>
          </header>

          <div className="space-y-5 text-k-text/80 leading-relaxed max-w-2xl mb-10">
            {p.body.map((para, i) => (
              <p key={i}>{para}</p>
            ))}
          </div>

          {/* No form, no app link here: the app is invite-walled and
              desktop/tablet-only, so a request goes straight to a DM. */}
          <div className="flex items-center gap-4 flex-wrap">
            <a
              href={X_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block border border-k-accent text-k-accent hover:bg-k-accent hover:text-k-bg transition-colors font-display font-semibold tracking-[0.2em] uppercase text-sm px-6 py-3"
            >
              Request access (DM on X) ↗
            </a>
          </div>
        </div>

        <MediaPanel items={p.media} />
      </div>
    </div>
  )
}
