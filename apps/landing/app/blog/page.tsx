import React from 'react'
import Link from 'next/link'
import { getAllPosts } from '../lib/blog.js'

export default function Blog() {
  const posts = getAllPosts()

  return (
    <div className="min-h-screen flex flex-col">
      {/* Fixed Header Content */}
      <div className="fixed top-24 left-24 right-24 z-40">
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

      {/* Scrollable Posts */}
      <div className="mt-56 px-24 space-y-12">
        {posts.map((post) => (
          <article key={post.slug} className="group">
            <Link href={`/blog/${post.slug}`} className="block space-y-3">
              <h3 className="text-white/90 group-hover:text-[#F75049] transition-colors text-xl">
                {post.title}
              </h3>
              <div className="flex gap-4 text-sm text-white/30">
                <span>{post.date}</span>
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