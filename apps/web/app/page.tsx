import { type Metadata } from 'next'
import { getBlogPosts } from '../lib/blog'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Home',
}

export default function Home() {
  const latestPosts = getBlogPosts().slice(0, 2) // Get latest 2 posts (already sorted by date)

  return (
    <div className="space-y-12">
      <section className="space-y-4">
        <h2 className="text-xl font-mono">About</h2>
        <p className="text-muted-foreground leading-relaxed">
          Hi! I'm a software engineer focused on AI and machine learning.
          Currently exploring the intersection of human creativity and artificial intelligence.
        </p>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-mono">Highlights</h2>
        <ul className="space-y-2 text-muted-foreground">
          <li>• Founding Partner at <a href="https://www.shack15.com/ventures" className="text-primary hover:underline">SHACK15 Ventures</a>, an SF AI and deeptech fund</li>
          <li>• Built 9 companies w/ Andrew Ng at <a href="https://aifund.ai/" className="text-primary hover:underline">AI Fund</a> (incl. ValidMind, Workhelix, Echelon)</li>
          <li>• Prev. product at <a href="https://techcrunch.com/2022/09/01/reddit-acquires-contextualization-company-spiketrap-to-boost-its-ads-business/" className="text-primary hover:underline">Spiketrap</a> (acq. by reddit), Uber</li>
        </ul>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-mono">Latest Posts</h2>
        <div className="space-y-2">
          {latestPosts.map(post => (
            <Link 
              key={post.slug}
              href={`/blog/${post.slug}`} 
              className="block group"
            >
              <span className="text-primary group-hover:underline">{post.title}</span>
              <span className="text-muted-foreground text-sm ml-2">{post.date}</span>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
} 