'use client'

import { useState, useEffect } from 'react'
import { usePathname } from 'next/navigation'

export default function ReadingProgress() {
  const [progress, setProgress] = useState(0)
  const pathname = usePathname()
  const isBlogPost = pathname.startsWith('/blog/') && 
                    pathname !== '/blog' && 
                    !pathname.startsWith('/blog/research')

  useEffect(() => {
    if (!isBlogPost) return

    const updateProgress = () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight
      const scrollPosition = window.scrollY
      const progress = (scrollPosition / scrollHeight) * 100
      setProgress(Math.min(progress, 100))
    }

    window.addEventListener('scroll', updateProgress)
    // Initial progress
    updateProgress()

    return () => window.removeEventListener('scroll', updateProgress)
  }, [isBlogPost])

  if (!isBlogPost) return null

  return (
    <div className="fixed top-8 right-24 flex items-center gap-3 z-[100]">
      <span className="text-[#F75049] text-sm uppercase tracking-wider">Reading Progress</span>
      <div className="w-[100px] h-[10px] bg-white/10">
        <div 
          className="h-full bg-[#5EF6FF] transition-all duration-100"
          style={{ transform: `scaleX(${progress / 100+0.01})`, transformOrigin: 'left' }}
        />
      </div>
    </div>
  )
} 