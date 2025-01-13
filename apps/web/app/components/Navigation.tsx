'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Navigation() {
  const pathname = usePathname()
  
  return (
    <nav className="fixed top-0 left-0 right-0 z-20 bg-black py-8">
      <ul className="flex space-x-8 px-24">
        <li>
          <Link 
            href="/" 
            className={`text-sm uppercase tracking-wider ${pathname === '/' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
          >
            Home
          </Link>
        </li>
        <li>
          <Link 
            href="/bio" 
            className={`text-sm uppercase tracking-wider ${pathname === '/bio' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
          >
            Bio
          </Link>
        </li>
        <li>
          <Link 
            href="/work" 
            className={`text-sm uppercase tracking-wider ${pathname === '/work' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
          >
            Work
          </Link>
        </li>
        <li>
          <Link 
            href="/investments" 
            className={`text-sm uppercase tracking-wider ${pathname === '/investments' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
          >
            Investments
          </Link>
        </li>
        <li>
          <Link 
            href="/blog" 
            className={`text-sm uppercase tracking-wider ${pathname === '/blog' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
          >
            Machine Yearning
          </Link>
        </li>
      </ul>
    </nav>
  )
} 