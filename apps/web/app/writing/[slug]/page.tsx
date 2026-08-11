import React from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { notFound } from 'next/navigation'
import type { Metadata } from 'next'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import type { Components } from 'react-markdown'
import { getAllPosts, getPost } from '../../../lib/content/posts'
import { properties } from '../../../lib/site'

export function generateStaticParams() {
  return getAllPosts().map((p) => ({ slug: p.slug }))
}

export function generateMetadata({ params }: { params: { slug: string } }): Metadata {
  const post = getPost(params.slug)
  if (!post) return {}
  return { title: post.title, description: post.excerpt }
}

// Slug-aware because post images are addressed two different ways in the
// markdown: some absolute (/blog/images/<slug>/x.png), some as bare
// filenames (image-2.png). A bare name resolves against the PAGE url, so
// /writing/<slug> asked for /writing/image-2.png and 404'd even though the
// file was sitting at /blog/images/<slug>/image-2.png. Normalize here rather
// than hand-editing every post.
function makeComponents(slug: string): Components {
  const resolveSrc = (raw: string) =>
    /^(https?:)?\/\//.test(raw) || raw.startsWith('/') ? raw : `/blog/images/${slug}/${raw}`

  return {
    img: (props) => (
      <Image
        src={resolveSrc(props.src || '')}
        alt={props.alt || ''}
        width={800}
        height={400}
        // h-auto keeps the aspect ratio once max-w-full kicks in on narrow
        // screens; without it the intrinsic 800x400 would letterbox oddly.
        className="border border-k-line max-w-full h-auto"
        unoptimized
      />
    ),
    a: ({ node, ...props }) => (
      <a
        {...props}
        // Raw URLs are auto-linked by remark and run to 750px+ unbroken,
        // which blew past a 375px viewport before this.
        className="text-k-text hover:text-k-accent transition-colors underline decoration-k-line underline-offset-4 break-words"
        target={props.href?.startsWith('http') ? '_blank' : undefined}
        rel={props.href?.startsWith('http') ? 'noopener noreferrer' : undefined}
      />
    ),
    h2: ({ node, ...props }) => (
      <h2 {...props} className="text-k-text text-2xl font-display font-semibold mt-12 mb-6" />
    ),
    h3: ({ node, ...props }) => (
      <h3 {...props} className="text-k-text text-xl font-display font-semibold mt-8 mb-4" />
    ),
    p: ({ node, ...props }) => <p {...props} className="text-k-text/70 mb-6 break-words" />,
    ul: ({ node, ...props }) => <ul {...props} className="text-k-text/70 list-disc pl-6 mb-6" />,
    ol: ({ node, ...props }) => <ol {...props} className="text-k-text/70 list-decimal pl-6 mb-6" />,
    blockquote: ({ node, ...props }) => (
      <blockquote {...props} className="border-l-2 border-k-accent pl-4 my-6 text-k-dim italic" />
    ),
    code: ({ node, ...props }) => (
      <code {...props} className="bg-k-raise px-1.5 py-0.5 text-sm text-k-accent break-words" />
    ),
    pre: ({ node, ...props }) => (
      <pre {...props} className="bg-k-raise border border-k-line p-4 overflow-x-auto mb-6" />
    ),
    // Wide markdown tables scroll in their own container rather than
    // widening the page.
    table: ({ node, ...props }) => (
      <div className="overflow-x-auto mb-6">
        <table {...props} className="w-full text-sm border border-k-line" />
      </div>
    ),
  }
}

export default function ArchivePost({ params }: { params: { slug: string } }) {
  const post = getPost(params.slug)
  if (!post) notFound()

  return (
    <div className="px-6 md:px-20 py-14">
      <article className="max-w-3xl mx-auto">
        <Link
          href="/writing"
          className="font-mono text-[11px] tracking-[0.14em] uppercase text-k-dim hover:text-k-text transition-colors"
        >
          ← Machine Yearning
        </Link>

        <header className="mt-6 mb-10">
          <h1 className="text-3xl text-k-text font-display font-semibold mb-3">{post.title}</h1>
          <div className="flex items-center gap-4 flex-wrap">
            <span className="text-k-dim text-sm font-mono">{post.date}</span>
            <span className="k-chip text-[9px]">Archive</span>
            <a
              href={properties.newsletter}
              target="_blank"
              rel="noopener noreferrer"
              className="text-k-faint hover:text-k-dim text-xs transition-colors"
            >
              New essays publish on machineyearning.io ↗
            </a>
          </div>
        </header>

        <ReactMarkdown components={makeComponents(params.slug)} remarkPlugins={[remarkGfm]}>
          {post.content}
        </ReactMarkdown>
      </article>
    </div>
  )
}
