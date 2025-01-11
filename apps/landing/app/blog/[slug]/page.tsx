import React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { getPostData } from '@/lib/blog'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw'
import type { Components } from 'react-markdown'

export default function BlogPost({ params }: { params: { slug: string } }) {
  const post = getPostData(params.slug)

  if (!post) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-white/50">Post not found</p>
      </div>
    )
  }

  const components: Components = {
    img: (props) => {
      const src = props.src || ''
      return (
        <Image
          src={src}
          alt={props.alt || ''}
          width={800}
          height={400}
          className="rounded-lg"
          unoptimized
        />
      )
    },
    a: ({ node, ...props }) => (
      <a
        {...props}
        className="text-white/90 hover:text-[#F75049] transition-colors"
        target={props.href?.startsWith('http') ? '_blank' : undefined}
        rel={props.href?.startsWith('http') ? 'noopener noreferrer' : undefined}
      />
    ),
    h2: ({ node, ...props }) => (
      <h2 {...props} className="text-white/90 text-2xl font-medium mt-12 mb-6" />
    ),
    h3: ({ node, ...props }) => (
      <h3 {...props} className="text-white/90 text-xl font-medium mt-8 mb-4" />
    ),
    p: ({ node, ...props }) => (
      <p {...props} className="text-white/70 mb-6" />
    ),
    ul: ({ node, ...props }) => (
      <ul {...props} className="text-white/70 list-disc pl-6 mb-6" />
    ),
    ol: ({ node, ...props }) => (
      <ol {...props} className="text-white/70 list-decimal pl-6 mb-6" />
    ),
    blockquote: ({ node, ...props }) => (
      <blockquote {...props} className="border-l-2 border-[#F75049] pl-4 my-6 text-white/50 italic" />
    ),
    code: ({ node, ...props }) => (
      <code {...props} className="bg-white/5 rounded px-1.5 py-0.5 text-sm text-[#F75049]" />
    ),
    pre: ({ node, ...props }) => (
      <pre {...props} className="bg-white/5 rounded-lg p-4 overflow-x-auto mb-6" />
    )
  }

  return (
    <div className="min-h-screen flex flex-col px-24">
      <article className="mt-32 mb-16 max-w-3xl">
        {/* Back link */}
        <div className="mb-12">
          <Link 
            href="/blog" 
            className="text-white/30 hover:text-[#F75049] transition-colors"
          >
            ← back to blog
          </Link>
        </div>

        {/* Header */}
        <header className="mb-12">
          <h1 className="text-white/90 text-3xl font-medium mb-4">{post.title}</h1>
          <div className="flex gap-4 text-sm text-white/30">
            <span>{post.date}</span>
          </div>
        </header>

        {/* Content */}
        <div className="prose prose-invert max-w-none">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
            components={components}
          >
            {post.contentHtml}
          </ReactMarkdown>
        </div>
      </article>
    </div>
  )
} 