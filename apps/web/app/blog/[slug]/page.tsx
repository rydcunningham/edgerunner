import { getBlogPosts } from '../../../lib/blog'
import { notFound } from 'next/navigation'

export default function BlogPost({ params }: { params: { slug: string } }) {
  const posts = getBlogPosts()
  const post = posts.find(post => post.slug === params.slug)

  if (!post) {
    notFound()
  }

  return (
    <div className="space-y-8">
      <header className="space-y-2">
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