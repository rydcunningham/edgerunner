import Link from 'next/link'
import { getBlogPosts } from '../../lib/blog'

export default function Blog() {
  const posts = getBlogPosts()

  return (
    <div className="space-y-12">
      <header className="space-y-2">
        <h2 className="text-xl font-mono">machine yearning</h2>
        <p className="text-muted-foreground">
          subscribe via{' '}
          <a href="https://machineyearning.substack.com" className="text-primary hover:underline">
            Substack →
          </a>{' '}
        </p>
      </header>

      <div className="space-y-6">
        {posts.map((post) => (
          <article key={post.slug} className="group">
            <Link href={`/blog/${post.slug}`} className="block space-y-2">
              <h3 className="text-primary group-hover:underline font-mono">
                {post.title}
              </h3>
              <div className="flex gap-4 text-sm text-muted-foreground">
                <span>{post.date}</span>
                <span>•</span>
                <span>{post.readTime}</span>
              </div>
              <p className="text-muted-foreground">
                {post.excerpt}
              </p>
            </Link>
          </article>
        ))}
      </div>
    </div>
  )
} 