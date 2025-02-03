import React from 'react'
import Link from 'next/link'
import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'

function getAllPosts() {
  const postsDirectory = path.join(process.cwd(), 'content/blog')
  if (!fs.existsSync(postsDirectory)) {
    return []
  }
  const fileNames = fs.readdirSync(postsDirectory)
    .filter(fileName => 
      fileName.endsWith('.md') && 
      !fileName.startsWith('image') && 
      fileName !== 'images'
    )
  
  const allPostsData = fileNames.map(fileName => {
    const slug = fileName.replace(/\.md$/, '')
    const fullPath = path.join(postsDirectory, fileName)
    const fileContents = fs.readFileSync(fullPath, 'utf8')
    const matterResult = matter(fileContents)

    return {
      slug,
      title: matterResult.data.title,
      date: matterResult.data.date,
      excerpt: matterResult.data.excerpt
    }
  })

  return allPostsData.sort((a, b) => {
    if (a.date < b.date) {
      return 1
    } else {
      return -1
    }
  })
}

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