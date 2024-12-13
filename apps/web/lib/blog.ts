import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { formatDistance } from 'date-fns'

const postsDirectory = path.join(process.cwd(), 'content/blog')

export type BlogPost = {
  slug: string
  title: string
  date: string
  excerpt: string
  readTime: string
  content: string
}

export function getBlogPosts(): BlogPost[] {
  const fileNames = fs.readdirSync(postsDirectory)
  const posts = fileNames
    .filter(fileName => fileName.endsWith('.md'))
    .map(fileName => {
      const slug = fileName.replace(/\.md$/, '')
      const fullPath = path.join(postsDirectory, fileName)
      const fileContents = fs.readFileSync(fullPath, 'utf8')
      const { data, content } = matter(fileContents)
      
      const wordCount = content.split(/\s+/g).length
      const readTime = `${Math.ceil(wordCount / 200)} min read`

      return {
        slug,
        title: data.title,
        date: data.date,
        excerpt: data.excerpt,
        readTime,
        content
      }
    })
    .sort((a, b) => (new Date(b.date)).getTime() - (new Date(a.date)).getTime())

  return posts
} 