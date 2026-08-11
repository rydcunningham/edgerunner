import type { Metadata } from 'next'
import UpdateRow from '../components/UpdateRow'
import { updates } from '../../lib/content/updates'

// Full archive. Deliberately not in the nav — reached from the home feed.
export const metadata: Metadata = {
  title: 'Updates',
  description: 'Product releases, new investments, and press for Edgerunner Ventures.',
}

export default function Updates() {
  return (
    <div className="px-6 md:px-20 py-14 max-w-[900px]">
      <header className="mb-10">
        <h1 className="font-display font-bold text-2xl tracking-[0.2em] uppercase text-k-text">
          Updates
        </h1>
        <p className="font-mono text-[11px] tracking-[0.14em] uppercase text-k-dim mt-2">
          {updates.length} entries · products, investments, press
        </p>
      </header>

      <div>
        {updates.map((u) => (
          <UpdateRow key={`${u.date}-${u.title}`} u={u} />
        ))}
      </div>
    </div>
  )
}
