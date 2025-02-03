import React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { Components } from 'react-markdown'

interface PostData {
  slug: string;
  content: string;
  title: string;
  date: string;
}

function getPostData(slug: string): PostData {
  const postsDirectory = path.join(process.cwd(), 'content/blog')
  const fullPath = path.join(postsDirectory, `${slug}.md`)
  const fileContents = fs.readFileSync(fullPath, 'utf8')
  const matterResult = matter(fileContents)

  return {
    slug,
    content: matterResult.content,
    title: matterResult.data.title,
    date: matterResult.data.date
  }
}

export default function BlogPost({ params }: { params: { slug: string } }) {
  const { slug, content, title, date } = getPostData(params.slug)

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
    <div className="min-h-screen flex flex-col px-24 py-12 pt-36">
      <article className="prose prose-invert max-w-3xl mx-auto">
        <header className="mb-12">
          <h1 className="text-3xl text-white/90 mb-4">{title}</h1>
          <div className="text-white/50 text-sm">{date}</div>
        </header>

        <ReactMarkdown 
          components={components}
          remarkPlugins={[remarkGfm]}
          className="prose prose-invert"
        >
          {content}
        </ReactMarkdown>
      </article>
    </div>
  )
} 