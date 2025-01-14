'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState, useEffect } from 'react'

export default function Navigation() {
  const pathname = usePathname()
  const [isOpen, setIsOpen] = useState(false)

  // Close menu when route changes
  useEffect(() => {
    setIsOpen(false)
  }, [pathname])

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const nav = document.getElementById('mobile-nav')
      const button = document.getElementById('hamburger-button')
      if (isOpen && nav && !nav.contains(event.target as Node) && !button?.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isOpen])
  
  return (
    <nav className="fixed top-0 left-0 right-0 z-[99] bg-black">
      
      {/* Mobile menu button */}
      <button
        id="hamburger-button"
        className="block md:hidden p-4 ml-12 m-4"
        onClick={() => setIsOpen(prev => !prev)}
      >
        <div className="w-6 flex flex-col gap-1.5">
          <span className={`block h-0.5 w-6 bg-[#5EF6FF] transition-all duration-300 ${isOpen ? 'rotate-45 translate-y-2' : ''}`} />
          <span className={`block h-0.5 w-6 bg-[#5EF6FF] transition-all duration-300 ${isOpen ? 'opacity-0' : ''}`} />
          <span className={`block h-0.5 w-6 bg-[#5EF6FF] transition-all duration-300 ${isOpen ? '-rotate-45 -translate-y-2' : ''}`} />
        </div>
      </button>


      {/* Mobile Navigation Menu */}
      <div
        id="mobile-nav"
        className={`md:hidden fixed bg-black transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-[43px]' : '-translate-x-full'
        }`}
        style={{ top: '64px', left: 0, right: 0, bottom: 0, zIndex: 80 }}
      >
        <ul className="flex flex-col space-y-6 p-6">
          <li>
            <Link 
              href="/" 
              className={`text-lg uppercase tracking-wider ${pathname === '/' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
            >
              Home
            </Link>
          </li>
          <li>
            <Link 
              href="/bio" 
              className={`text-lg uppercase tracking-wider ${pathname === '/bio' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
            >
              Bio
            </Link>
          </li>
          <li>
            <Link 
              href="/work" 
              className={`text-lg uppercase tracking-wider ${pathname === '/work' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
            >
              Work
            </Link>
          </li>
          <li>
            <Link 
              href="/portfolio" 
              className={`text-lg uppercase tracking-wider ${pathname === '/portfolio' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
            >
              Portfolio
            </Link>
          </li>
          <li>
            <Link 
              href="/blog" 
              className={`text-lg uppercase tracking-wider ${pathname === '/blog' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
            >
              Machine Yearning
            </Link>
          </li>
        </ul>
      </div>

      {/* Desktop Navigation */}
      <ul className="hidden md:flex space-x-8 px-24 py-8">
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
            href="/portfolio" 
            className={`text-sm uppercase tracking-wider ${pathname === '/portfolio' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
          >
            Portfolio
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