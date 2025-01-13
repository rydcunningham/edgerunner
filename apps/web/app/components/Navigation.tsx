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
    <nav className="fixed top-0 left-0 right-0 z-50 bg-black py-8">
      {/* Desktop Navigation */}
      <ul className="hidden md:flex space-x-8 px-24">
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

      {/* Mobile Hamburger Button */}
      <button
        id="hamburger-button"
        className="md:hidden px-6 py-2 absolute left-9 top-6 z-50"
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle menu"
      >
        <div className="w-6 flex flex-col items-start space-y-1.5">
          <span className={`block h-0.5 bg-white/50 transition-all duration-300 ${isOpen ? 'w-6 rotate-45 translate-y-2' : 'w-6'}`} />
          <span className={`block h-0.5 bg-white/50 transition-all duration-300 ${isOpen ? 'opacity-0' : 'w-4'}`} />
          <span className={`block h-0.5 bg-white/50 transition-all duration-300 ${isOpen ? 'w-6 -rotate-45 -translate-y-2' : 'w-5'}`} />
        </div>
      </button>

      {/* Mobile Navigation Menu */}
      <div
        id="mobile-nav"
        className={`md:hidden fixed inset-0 bg-black/95 backdrop-blur-sm transition-transform duration-300 ease-in-out z-45 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        style={{ top: '80px' }}
      >
        <ul className="flex flex-col space-y-8 pt-12 px-24">
          <li className="text-left">
            <Link 
              href="/" 
              className={`text-lg uppercase tracking-wider ${pathname === '/' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
            >
              Home
            </Link>
          </li>
          <li className="text-left">
            <Link 
              href="/bio" 
              className={`text-lg uppercase tracking-wider ${pathname === '/bio' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
            >
              Bio
            </Link>
          </li>
          <li className="text-left">
            <Link 
              href="/work" 
              className={`text-lg uppercase tracking-wider ${pathname === '/work' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
            >
              Work
            </Link>
          </li>
          <li className="text-left">
            <Link 
              href="/investments" 
              className={`text-lg uppercase tracking-wider ${pathname === '/investments' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
            >
              Investments
            </Link>
          </li>
          <li className="text-left">
            <Link 
              href="/blog" 
              className={`text-lg uppercase tracking-wider ${pathname === '/blog' ? 'text-[#5EF6FF] border-b border-[#5EF6FF] pb-1' : 'text-white/30 hover:text-[#F75049]'}`}
            >
              Machine Yearning
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  )
} 