import Link from 'next/link'
import type { Metadata } from 'next'
import { archive, products } from '../../lib/content/research'

export const metadata: Metadata = {
  title: 'Research',
  description:
    'Edgerunner Research — Cortex, the energy-compute knowledge base, and Overclock, the digital-twin simulator.',
}

export default function Research() {
  return (
    <div className="px-6 md:px-20 py-14 max-w-[1100px]">
      <header className="mb-10">
        <h1 className="font-display font-bold text-2xl tracking-[0.2em] uppercase text-k-text">
          EDGERUNNER RESEARCH
        </h1>
        <p className="font-mono text-[11px] tracking-[0.14em] uppercase text-k-dim mt-2">
          Instruments for the energy-compute stack
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-14">
        {products.map((p) => (
          <Link key={p.slug} href={`/research/${p.slug}`} className="block group">
            <div className="k-panel h-full transition-colors group-hover:border-k-line-strong">
              <div className="flex items-baseline justify-between gap-4 mb-3">
                <span className="font-display font-bold tracking-[0.24em] text-xl text-k-text">
                  {p.name}
                </span>
                <span className="k-chip k-chip--accent text-[10px]">{p.status}</span>
              </div>
              <p className="text-k-accent text-sm mb-3">{p.tagline}</p>
              <p className="text-k-dim text-sm">{p.body[0]}</p>
              <div className="mt-4 font-mono text-[11px] tracking-[0.14em] uppercase text-k-dim group-hover:text-k-text transition-colors">
                DOSSIER →
              </div>
            </div>
          </Link>
        ))}
      </div>

      <div className="k-rulehead mb-5">Archive</div>
      <div className="space-y-3 max-w-2xl">
        {archive.map((a) => (
          <div key={a.name} className="flex items-baseline gap-4 border-b border-k-line pb-3">
            <span className="font-display font-semibold tracking-[0.18em] text-k-dim">{a.name}</span>
            <span className="font-mono text-[10px] text-k-faint">{a.year}</span>
            <span className="k-chip text-[9px] ml-auto shrink-0">{a.status}</span>
            <p className="hidden md:block text-k-faint text-sm flex-1">{a.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
