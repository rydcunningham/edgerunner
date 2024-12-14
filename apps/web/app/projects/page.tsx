export default function Projects() {
  const projects = [
    {
      name: "AI Code Assistant",
      description: "A VS Code extension that helps developers write better code using GPT-4. Built with TypeScript and the OpenAI API.",
      links: [
        { label: "Demo", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "MIKOSHI HomeLab",
      description: "Franken-lab for self-hosted AI, cloud, and media projects. Built w/ unRAID on Supermicro, Synology, NVIDIA, RPi.",
      links: [
        { label: "Live Site", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "Machine Learning Blog Engine",
      description: "A Next.js blog platform with AI-powered content suggestions and SEO optimization. Uses OpenAI's GPT-3 for content enhancement.",
      links: [
        { label: "GitHub", url: "#" }
      ]
    }
  ]

  return (
    <div className="space-y-12">
      <header className="space-y-2">
        <h2 className="text-xl font-mono">featured projects</h2>
        <p className="text-muted-foreground">
          open source work and side projects.{' '}
          <a href="https://github.com/rydcunningham" className="text-primary hover:underline">
            view on GitHub →
          </a>{' '}
        </p>
      </header>

      <div className="space-y-8">
        {projects.map((project) => (
          <article key={project.name} className="space-y-2">
            <h3 className="text-primary font-mono">{project.name}</h3>
            <p className="text-muted-foreground">
              {project.description}
            </p>
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
          </article>
        ))}
      </div>
    </div>
  )
} 