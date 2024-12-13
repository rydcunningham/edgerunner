import Link from 'next/link'
import { getBlogPosts } from '../../lib/blog'

export default function Blog() {
  const posts = getBlogPosts()

  return (
    <div className="space-y-12">
      <header className="space-y-2">
        <h2 className="text-xl font-mono">machine yearning</h2>
        <p className="text-zinc-300">
          subscribe via{' '}
          <a href="https://edgerunner.substack.com" className="text-[#C14BFC] hover:underline">
            Substack
          </a>{' '}
          →
        </p>
      </header>

      <div className="space-y-6">
        {posts.map((post) => (
          <article key={post.slug} className="group">
            <Link href={`/blog/${post.slug}`} className="block space-y-2">
              <h3 className="text-[#C14BFC] group-hover:underline font-mono">
                {post.title}
              </h3>
              <div className="flex gap-4 text-sm text-zinc-500">
                <span>{post.date}</span>
                <span>{post.readTime}</span>
              </div>
              <p className="text-zinc-300">
                {post.excerpt}
              </p>
            </Link>
          </article>
        ))}
      </div>
    </div>
  )
} 