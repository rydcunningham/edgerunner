import { getBlogPosts } from '../../../lib/blog'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw'
import Image from 'next/image'
import Link from 'next/link'

export default function BlogPost({ params }: { params: { slug: string } }) {
  const posts = getBlogPosts()
  const post = posts.find(post => post.slug === params.slug)

  if (!post) {
    return <div>Post not found</div>
  }

  return (
    <article className="prose prose-invert max-w-none">
      <div className="relative mb-8">
        <div className="absolute right-0 top-0">
          <Link 
            href="/blog" 
            className="text-sm text-muted-foreground hover:text-primary font-mono no-underline"
          >
            ← back to blog
          </Link>
        </div>
      </div>
      <h1 className="text-3xl font-mono mb-2">{post.title}</h1>
      <div className="flex gap-4 text-sm text-muted-foreground mb-12">
        <span>{post.date}</span>
        <span>•</span>
        <span>{post.readTime}</span>
      </div>
      <ReactMarkdown 
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={{
          img: (props) => {
            const src = props.src || ''
            console.log('Image src:', src)
            return (
              <Image
                src={src}
                alt={props.alt || ''}
                width={800}
                height={400}
                className="rounded-xl"
                unoptimized
              />
            )
          },
        }}
        className="prose-headings:font-mono prose-a:text-primary prose-pre:bg-background/[var(--glass-opacity)] prose-h1:text-2xl prose-h2:text-xl prose-h3:text-lg"
      >
        {post.content}
      </ReactMarkdown>
    </article>
  )
} 