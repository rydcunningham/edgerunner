import { getBlogPosts } from '../../../lib/blog'
import { notFound } from 'next/navigation'
import Link from 'next/link'

export default function BlogPost({ params }: { params: { slug: string } }) {
  const posts = getBlogPosts()
  const post = posts.find(post => post.slug === params.slug)

  if (!post) {
    notFound()
  }

  return (
    <div className="space-y-8">
      <header className="space-y-2 relative">
        <div className="absolute right-0 top-0">
          <Link 
            href="/blog" 
            className="text-sm text-zinc-500 hover:text-[#C14BFC] font-mono"
          >
            ← back to blog
          </Link>
        </div>
        <h2 className="text-xl font-mono text-[#C14BFC]">{post.title}</h2>
        <div className="flex gap-4 text-sm text-zinc-500 font-mono">
          <span>{post.date}</span>
          <span>{post.readTime}</span>
        </div>
      </header>

      <div className="prose prose-invert max-w-none prose-a:text-[#C14BFC] prose-pre:bg-black/50">
        {post.content}
      </div>
    </div>
  )
} 