import Link from 'next/link'
import Image from 'next/image'
import type { Metadata } from 'next'
import { bySector, companies, sectorLabels, statusChip } from '../../lib/content/portfolio'
import type { Company } from '../../lib/content/types'

// Derived, not hardcoded — the count and stage range drift the moment a
// company is added or exits (this description said "13 … angel through seed"
// while the page itself already rendered 18, one of them public).
const STAGES = ['Angel', 'Pre-seed', 'Seed'] as const
const earliest = STAGES.find((s) => companies.some((c) => c.round === s))
const latest = [...STAGES].reverse().find((s) => companies.some((c) => c.round === s))

export const metadata: Metadata = {
  title: 'Portfolio',
  description: `${companies.length} investments across AI and deep tech, ${earliest?.toLowerCase()} through ${latest?.toLowerCase()}.`,
}

function Monogram({ name }: { name: string }) {
  return (
    <div className="w-10 h-10 border border-k-line flex items-center justify-center text-k-dim font-display font-semibold text-sm shrink-0">
      {name.slice(0, 2).toUpperCase()}
    </div>
  )
}

function CompanyCard({ c }: { c: Company }) {
  return (
    <Link href={`/portfolio/${c.slug}`} className="block group">
      <div className="k-panel h-full transition-colors group-hover:border-k-line-strong">
        <div className="flex items-start gap-4">
          {c.logo ? (
            <Image
              src={c.logo}
              alt={`${c.name} logo`}
              width={40}
              height={40}
              className="w-10 h-10 object-contain shrink-0 opacity-80"
            />
          ) : (
            <Monogram name={c.name} />
          )}
          <div className="min-w-0 flex-1">
            <div className="font-display font-semibold tracking-wide text-k-text text-lg leading-tight">
              {c.name}
            </div>
            <p className="text-k-dim text-sm mt-1">{c.oneLiner}</p>
          </div>
          {/* Card uses the short form so a long acquirer name can't wrap the
              header; the full label lives on the company page. */}
          {c.status && (
            <span className={`${statusChip(c.status.kind)} text-[9px] shrink-0`}>
              {c.status.short ?? c.status.label}
            </span>
          )}
        </div>
        <div className="flex flex-wrap gap-2 mt-4">
          <span className="k-chip text-[10px]">{c.round}</span>
          <span className="k-chip text-[10px]">{c.year}</span>
          <span className="k-chip text-[10px]">{c.domain}</span>
        </div>
      </div>
    </Link>
  )
}

export default function Portfolio() {
  return (
    <div className="px-6 md:px-20 py-14 max-w-[1100px]">
      <header className="mb-10">
        <h1 className="font-display font-bold text-2xl tracking-[0.2em] uppercase text-k-text">
          Portfolio
        </h1>
        <p className="font-mono text-[11px] tracking-[0.14em] uppercase text-k-dim mt-2">
          {companies.length} investments · angel through seed
        </p>
      </header>

      {(['ai', 'deep-tech'] as const).map((sector) => {
        const list = bySector(sector)
        return (
          <section key={sector} className="mb-12">
            <div className="k-rulehead mb-5">
              {sectorLabels[sector]}
              <span className="font-mono text-k-faint tracking-normal normal-case">· {list.length}</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {list.map((c) => (
                <CompanyCard key={c.slug} c={c} />
              ))}
            </div>
          </section>
        )
      })}
    </div>
  )
}
