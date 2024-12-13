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
          <li>• Building AI-powered tools for developers</li>
          <li>• Previously at [Company], working on [Project]</li>
          <li>• Writing about AI, technology, and the future</li>
        </ul>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-mono">Latest Posts</h2>
        <div className="space-y-2">
<<<<<<< HEAD
          {latestPosts.map(post => (
            <Link 
              key={post.slug}
              href={`/blog/${post.slug}`} 
              className="block group"
            >
              <span className="text-[#C14BFC] group-hover:underline">{post.title}</span>
              <span className="text-zinc-500 text-sm ml-2">{post.date}</span>
            </Link>
          ))}
=======
          <a href="/blog/modern-web-stack" className="block group">
            <span className="text-primary group-hover:underline">Building a Modern Web Stack</span>
            <span className="text-muted-foreground text-sm ml-2">March 15, 2024</span>
          </a>
          <a href="/blog/future-of-ai" className="block group">
            <span className="text-primary group-hover:underline">The Future of AI Development</span>
            <span className="text-muted-foreground text-sm ml-2">March 10, 2024</span>
          </a>
>>>>>>> a759d4d (added dark mode toggle and CSS logic)
        </div>
      </section>
    </div>
  )
} 