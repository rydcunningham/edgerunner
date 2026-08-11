import Link from 'next/link'
import type { Metadata } from 'next'
import { getAllPosts } from '../../lib/content/posts'
import { properties } from '../../lib/site'

export const metadata: Metadata = {
  title: 'Machine Yearning',
  description:
    'Essays on energy, compute, and sovereign AI. Published on Substack at machineyearning.io.',
}

export default function Writing() {
  const posts = getAllPosts()

  return (
    <div className="px-6 md:px-20 py-14 max-w-[900px]">
      <header className="mb-10">
        <h1 className="font-display font-bold text-2xl tracking-[0.2em] uppercase text-k-text">
          Machine Yearning
        </h1>
        <p className="font-mono text-[11px] tracking-[0.14em] uppercase text-k-dim mt-2">
          Essays on energy, compute, and sovereign AI
        </p>
      </header>

      {/* Canonical home */}
      <a href={properties.newsletter} target="_blank" rel="noopener noreferrer" className="block group mb-14">
        <div className="k-panel transition-colors group-hover:border-k-line-strong">
          <div className="flex items-baseline justify-between gap-4">
            <div>
              <div className="font-display font-semibold tracking-[0.18em] text-lg text-k-text mb-1">
                READ ON MACHINEYEARNING.IO
              </div>
              <p className="text-k-dim text-sm">
                New essays publish on Substack. Subscribe there for the current work.
              </p>
            </div>
            <span className="k-chip k-chip--accent text-[10px] shrink-0">SUBSTACK ↗</span>
          </div>
        </div>
      </a>

      <div className="k-rulehead mb-6">
        Archive
        <span className="font-mono text-k-faint tracking-normal normal-case">· {posts.length}</span>
      </div>
      <ul className="space-y-6">
        {posts.map((post) => (
          <li key={post.slug} className="border-b border-k-line pb-6">
            <Link href={`/writing/${post.slug}`} className="group block">
              <div className="flex items-baseline gap-4 flex-wrap">
                <h2 className="text-k-text group-hover:text-k-accent transition-colors text-lg font-display font-semibold">
                  {post.title}
                </h2>
                <span className="font-mono text-[11px] text-k-faint">{post.date}</span>
              </div>
              {post.excerpt && <p className="text-k-dim text-sm mt-1 max-w-2xl">{post.excerpt}</p>}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}
