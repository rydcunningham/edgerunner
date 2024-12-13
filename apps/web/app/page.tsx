import { type Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Home',
}

export default function Home() {
  return (
    <div className="space-y-12">
      <section className="space-y-4">
        <h2 className="text-xl font-mono">About</h2>
        <p className="text-zinc-300 leading-relaxed">
          Hi! I'm a software engineer focused on AI and machine learning.
          Currently exploring the intersection of human creativity and artificial intelligence.
        </p>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-mono">Highlights</h2>
        <ul className="space-y-2 text-zinc-300">
          <li>• Building AI-powered tools for developers</li>
          <li>• Previously at [Company], working on [Project]</li>
          <li>• Writing about AI, technology, and the future</li>
        </ul>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-mono">Latest Posts</h2>
        <div className="space-y-2">
          <a href="/blog/modern-web-stack" className="block group">
            <span className="text-[#C14BFC] group-hover:underline">Building a Modern Web Stack</span>
            <span className="text-zinc-500 text-sm ml-2">March 15, 2024</span>
          </a>
          <a href="/blog/future-of-ai" className="block group">
            <span className="text-[#C14BFC] group-hover:underline">The Future of AI Development</span>
            <span className="text-zinc-500 text-sm ml-2">March 10, 2024</span>
          </a>
        </div>
      </section>
    </div>
  )
} 