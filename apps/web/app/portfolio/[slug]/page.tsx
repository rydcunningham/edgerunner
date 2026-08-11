import Link from 'next/link'
import Image from 'next/image'
import { notFound } from 'next/navigation'
import type { Metadata } from 'next'
import MediaPanel from '../../components/MediaPanel'
import { companies, getCompany, sectorLabels, statusChip } from '../../../lib/content/portfolio'
import { TWO_COL_GRID, TWO_COL_PAGE } from '../../../lib/layout'

export function generateStaticParams() {
  return companies.map((c) => ({ slug: c.slug }))
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const c = getCompany(params.slug)
  if (!c) return {}
  return { title: c.name, description: c.oneLiner }
}

export default function CompanyPage({ params }: { params: { slug: string } }) {
  const c = getCompany(params.slug)
  if (!c) notFound()

  const aff = c.affiliations
  const hasMedia = Boolean(c.media?.length)

  return (
    <div className={`px-6 md:px-20 py-14 ${hasMedia ? TWO_COL_PAGE : 'max-w-[900px]'}`}>
      <Link
        href="/portfolio"
        className="font-mono text-[11px] tracking-[0.14em] uppercase text-k-dim hover:text-k-text transition-colors"
      >
        ← Portfolio
      </Link>

      {/* Two columns starting at the same line: profile left, media rail right. */}
      <div className={hasMedia ? TWO_COL_GRID : 'mt-8'}>
        <div>
          <header className="mb-8 flex items-start gap-5">
            {c.logo && (
              <Image
                src={c.logo}
                alt={`${c.name} logo`}
                width={56}
                height={56}
                className="w-14 h-14 object-contain opacity-80"
              />
            )}
            <div>
              <h1 className="font-display font-bold text-3xl tracking-wide text-k-text">{c.name}</h1>
              <p className="text-k-dim mt-1">{c.oneLiner}</p>
            </div>
          </header>

          <div className="flex flex-wrap gap-2 mb-10">
            {/* Full label here — the card shows the short form. Linked to the
                announcement / IR page when there's a source to point at. */}
            {c.status &&
              (c.status.href ? (
                <a
                  href={c.status.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`${statusChip(c.status.kind)} text-[10px] hover:opacity-80 transition-opacity`}
                >
                  {c.status.label} ↗
                </a>
              ) : (
                <span className={`${statusChip(c.status.kind)} text-[10px]`}>{c.status.label}</span>
              ))}
            <span className="k-chip k-chip--accent text-[10px]">{c.round}</span>
            <span className="k-chip text-[10px]">{c.year}</span>
            <span className="k-chip text-[10px]">{sectorLabels[c.sector]}</span>
            <span className="k-chip text-[10px]">{c.domain}</span>
          </div>

          <p className="text-k-text/80 leading-relaxed max-w-2xl mb-10">{c.body}</p>

          {aff && (
            <div className="k-panel mb-10 max-w-2xl" data-title="Network">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-sm">
                {aff.universities && (
                  <div>
                    <div className="k-label mb-2">Universities</div>
                    <ul className="text-k-dim space-y-1">
                      {aff.universities.map((u) => (
                        <li key={u}>{u}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {aff.companies && (
                  <div>
                    <div className="k-label mb-2">Alumni of</div>
                    <ul className="text-k-dim space-y-1">
                      {aff.companies.map((co) => (
                        <li key={co}>{co}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {aff.investors && (
                  <div>
                    <div className="k-label mb-2">Co-investors</div>
                    <ul className="text-k-dim space-y-1">
                      {aff.investors.map((i) => (
                        <li key={i}>{i}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="flex flex-wrap gap-4">
            {c.links.map((l) => (
              <a
                key={l.url}
                href={l.url}
                target="_blank"
                rel="noopener noreferrer"
                className="k-chip k-chip--accent hover:opacity-80 transition-opacity"
              >
                {l.label} ↗
              </a>
            ))}
          </div>
        </div>

        <MediaPanel items={c.media} />
      </div>
    </div>
  )
}
