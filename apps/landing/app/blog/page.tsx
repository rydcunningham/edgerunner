import React from 'react'
import Link from 'next/link'
import { getBlogPosts } from '../../lib/blog'

export default function Blog() {
  const posts = getBlogPosts()

  return (
    <div className="min-h-screen flex flex-col px-24">
      {/* Header */}
      <div className="mt-32 mb-16">
        <h2 className="text-white/90 text-2xl font-medium mb-4">Machine Yearning</h2>
        <p className="text-white/50">
          Subscribe via{' '}
          <a 
            href="https://machineyearning.substack.com" 
            className="text-white/50 hover:text-[#F75049] transition-colors"
            target="_blank"
            rel="noopener noreferrer"
          >
            Substack →
          </a>
        </p>
      </div>

      {/* Posts */}
      <div className="space-y-12">
        {posts.map((post) => (
          <article key={post.slug} className="group">
            <Link href={`/blog/${post.slug}`} className="block space-y-3">
              <h3 className="text-white/90 group-hover:text-[#F75049] transition-colors text-xl">
                {post.title}
              </h3>
              <div className="flex gap-4 text-sm text-white/30">
                <span>{post.date}</span>
                <span>•</span>
                <span>{post.readTime}</span>
              </div>
              <p className="text-white/50 text-base">
                {post.excerpt}
              </p>
            </Link>
          </article>
        ))}
      </div>
    </div>
  )
} 