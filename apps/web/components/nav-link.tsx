'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  const pathname = usePathname()
  const isActive = pathname === href
  
  return (
    <Link 
      href={href} 
      className={`block text-[#C14BFC] ${isActive ? 'font-bold' : 'hover:underline'}`}
    >
      {children}
    </Link>
  )
} 