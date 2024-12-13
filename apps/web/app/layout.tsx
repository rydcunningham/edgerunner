import './globals.css'
import { NavLink } from '../components/nav-link'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body 
        className="min-h-screen bg-fixed"
        style={{
          backgroundImage: "url('/black_sands.avif')",
          backgroundSize: 'cover',
          backgroundColor: 'black'
        }}
      >
        <div className="fixed inset-8">
          <div className="h-full rounded-xl backdrop-blur-xl bg-black/70 border border-zinc-400/10">
            <div className="h-full max-w-7xl mx-auto px-8 py-16 grid grid-cols-[220px,1fr] gap-14">
              <header>
                <div className="border-r-[2px] border-zinc-200/10 pr-14">
                  <nav className="space-y-1 font-mono">
                    <NavLink href="/">home</NavLink>
                    <NavLink href="/bio">bio</NavLink>
                    <NavLink href="/blog">machine yearning</NavLink>
                    <NavLink href="/projects">projects</NavLink>
                    <NavLink href="/investments">investments</NavLink>
                  </nav>
                </div>
                <div className="mt-8 space-y-1">
                  <a href="https://github.com/rydcunningham" className="block text-zinc-400 hover:text-[#C14BFC]">github</a>
                  <a href="https://twitter.com/rydcunningham" className="block text-zinc-400 hover:text-[#C14BFC]">twitter</a>
                  <a href="https://linkedin.com/in/rydcunningham" className="block text-zinc-400 hover:text-[#C14BFC]">linkedin</a>
                </div>
                <div className="mt-8 space-y-1 text-zinc-500 text-sm">
                  <p>© mmxxiv rydcunningham</p>
                </div>
              </header>
              <main className="text-zinc-100 overflow-y-auto">
                {children}
              </main>
            </div>
          </div>
        </div>
      </body>
    </html>
  )
} 