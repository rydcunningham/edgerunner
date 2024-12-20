import './globals.css'
import { NavLink } from '../components/nav-link'
import { ThemeToggle } from '../components/theme-toggle'

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
          backgroundColor: 'hsl(var(--background))'
        }}
      >
        <div className="fixed inset-8">
          <div className="relative h-full rounded-xl backdrop-blur-xl bg-background/[var(--glass-opacity)] border border-border">
            <div className="h-full max-w-7xl mx-auto px-8 py-16 grid grid-cols-[220px,1fr] gap-14">
              <header>
                <div className="border-r-[2px] border-border pr-14">
                  <nav className="space-y-1 font-mono">
                    <NavLink href="/">home</NavLink>
                    <NavLink href="/bio">bio</NavLink>
                    <NavLink href="/blog">machine yearning</NavLink>
                    <NavLink href="/projects">projects</NavLink>
                    <NavLink href="/investments">investments</NavLink>
                  </nav>
                </div>
                <div className="mt-8 space-y-1">
                  <a href="https://github.com/rydcunningham" className="block text-muted-foreground hover:text-primary">github</a>
                  <a href="https://twitter.com/rydcunningham" className="block text-muted-foreground hover:text-primary">twitter</a>
                  <a href="https://linkedin.com/in/rydcunningham" className="block text-muted-foreground hover:text-primary">linkedin</a>
                </div>
                <div className="mt-8 space-y-1 text-muted-foreground text-sm">
                  <p>© mmxxiv rydcunningham</p>
                </div>
              </header>
              <main className="text-foreground overflow-y-auto">
                {children}
              </main>
            </div>
            <div className="absolute bottom-4 left-4">
              <ThemeToggle />
            </div>
          </div>
        </div>
      </body>
    </html>
  )
} 