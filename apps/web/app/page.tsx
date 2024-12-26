import { type Metadata } from 'next'
import { getBlogPosts } from '../lib/blog'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Home',
}

export default function Home() {
  const latestPosts = getBlogPosts().slice(0, 3)

  return (
    <div className="space-y-12">
      <section className="space-y-4">
        <h2 className="text-3xl font-mono tracking-tight">Ryan Cunningham</h2>
        <p className="text-muted-foreground">
          founder // investor.{' '}
          <a href="mailto:rc@edgerunner.io" className="text-primary hover:underline">
            get in touch →
          </a>{' '}
        </p>
        <div className="space-y-4 text-muted-foreground">
          <p>
            Built 9 AI companies at AI Fund. Previously product at Spiketrap (acq. by Reddit), Uber (mobility/delivery), Credit Suisse (tech IB).
          </p>
          <p>
            Now focused on building and investing in AI infrastructure, dev tools, and autonomous systems.
          </p>
        </div>
      </section>

      <div className="max-w-[800px] aspect-[21/9] rounded-xl overflow-hidden bg-background/[var(--glass-opacity)] border border-border">
        <img 
          src="/chongqing.avif" 
          alt="San Francisco"
          className="w-full h-full object-fill"
        />
      </div>

      <section className="space-y-4">
        <p className="text-muted-foreground">
          Fan of aviation ✈️, endurance sports 🏃‍♂️, and building things 🛠️
        </p>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-mono">Highlights</h2>
        <ul className="space-y-2 text-muted-foreground">
          <li>• Founding Partner at <a href="https://www.shack15.com/ventures" className="text-primary hover:underline">SHACK15 Ventures</a>, an SF AI and deeptech fund</li>
          <li>• Built 9 companies w/ Andrew Ng at <a href="https://aifund.ai/" className="text-primary hover:underline">AI Fund</a>, $100M+ deployed</li>
          <li>• Prev. product at <a href="https://techcrunch.com/2022/09/01/reddit-acquires-contextualization-company-spiketrap-to-boost-its-ads-business/" className="text-primary hover:underline">Spiketrap</a> (acq. by Reddit), Uber</li>
          <li>• Led Uber's expansion into micromobility ($10B+ GMV) and urban air mobility</li>
        </ul>
        <p className="pt-4 text-muted-foreground">
          <a href="/cv" className="text-primary hover:underline">
            full CV →
          </a>
        </p>
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