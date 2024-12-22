export default function Work() {
  const projects = [
    {
      name: "AI CODE ASSISTANT",
      description: "A VS Code extension that helps developers write better code using GPT-4. Built with TypeScript and the OpenAI API.",
      image: "/projects/ai-code-assistant.png",
      links: [
        { label: "Demo", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "MIKOSHI HOMELAB",
      description: "Franken-lab for self-hosted AI, cloud, and media projects. Built w/ unRAID on Supermicro, Synology, NVIDIA, RPi.",
      image: "/projects/mikoshi-homelab.png",
      links: [
        { label: "Live Site", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "MACHINE LEARNING BLOG ENGINE",
      description: "A Next.js blog platform with AI-powered content suggestions and SEO optimization. Uses OpenAI's GPT-3 for content enhancement.",
      image: "/projects/blog-engine.png",
      links: [
        { label: "GitHub", url: "#" }
      ]
    }
  ]

  return (
    <div className="space-y-12">
      <header className="space-y-2">
        <h2 className="text-xl font-mono">featured work</h2>
        <p className="text-muted-foreground">
          open source projects and contributions.{' '}
          <a href="https://github.com/rydcunningham" className="text-primary hover:underline">
            view on GitHub →
          </a>{' '}
        </p>
      </header>

      <div className="space-y-16">
        {projects.map((project) => (
          <article key={project.name} className="grid grid-cols-[1fr,320px] gap-8 items-start">
            <div className="space-y-4">
              <header className="space-y-3">
                <h3 className="text-2xl font-mono tracking-tight">{project.name}</h3>
                <p className="text-base text-muted-foreground font-light leading-relaxed">
                  {project.description}
                </p>
              </header>
              <div className="flex gap-3 text-sm">
                {project.links.map((link) => (
                  <a 
                    key={`${project.name}-${link.label}`}
                    href={link.url} 
                    className="text-muted-foreground hover:text-primary"
                  >
                    {link.label} →
                  </a>
                ))}
              </div>
            </div>
            <div className="aspect-[16/10] rounded-xl overflow-hidden bg-background/[var(--glass-opacity)] border border-border">
              {project.image && (
                <img 
                  src={project.image} 
                  alt={project.name}
                  className="w-full h-full object-cover"
                />
              )}
            </div>
          </article>
        ))}
      </div>
    </div>
  )
} 