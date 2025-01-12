interface Project {
  name: string;
  description: string;
  image?: string;
  category: string;
  year: string;
  links: Array<{
    label: string;
    url: string;
  }>;
}

export default function Work() {
  const projects: Project[] = [
    {
      name: "CORTEX",
      description: "A local scraping tool for extracting, categorizing, and storing content from websites into a structured database.",
      image: "/projects/ai-code-assistant.png",
      category: "[side project]",
      year: "2024",
      links: [
        { label: "Demo", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "CITYSIM",
      description: "Delivery network simulator that tells you where things will break before they do. Optimize costs and throughput by testing assumptions in silico.",
      image: "/projects/ai-code-assistant.png",
      category: "[side project]",
      year: "2024",
      links: [
        { label: "Demo", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "MIKOSHI HOMELAB",
      description: "Franken-lab for self-hosted AI, cloud, and media projects. Built w/ unRAID on Supermicro, Synology, NVIDIA, RPi.",
      image: "/projects/mikoshi-homelab.png",
      category: "[side project]",
      year: "2024",
      links: [
        { label: "Live Site", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "SHACK15 VENTURES",
      description: "The official angel fund of the SHACK15 community, investing in early-stage AI & deep tech startups.",
      image: "/projects/mikoshi-homelab.png",
      category: "[professional]",
      year: "2024",
      links: [
        { label: "Live Site", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "VALIDMIND",
      description: "Model validation, testing, and documentation for ML in financial services.",
      image: "/projects/blog-engine.png",
      category: "[professional]",
      year: "2021",
      links: [
        { label: "Site", url: "https://validmind.ai" }
      ]
    },
    {
      name: "SKYFIRE AI",
      description: "Swarm intelligence for heterogeneous drone fleets.",
      image: "/projects/blog-engine.png",
      category: "[professional]",
      year: "2023",
      links: [
        { label: "Site", url: "https://skyfireai.com" }
      ]
    },
    {
      name: "RAPIDFIRE",
      description: "Parallelized model training and experimentation for Data Science teams.",
      image: "/projects/blog-engine.png",
      category: "[professional]",
      year: "2023",
      links: [
        { label: "Site", url: "https://rapidfire.ai" }
      ]
    },
    {
      name: "SPEECHLAB",
      description: "Professional voice cloning and synthesis.",
      image: "/projects/blog-engine.png",
      category: "[professional]",
      year: "2022",
      links: [
        { label: "Site", url: "https://speechlab.ai" }
      ]
    },
    {
      name: "WORKHELIX",
      description: "Assessing GenAI labor transformation potential for F500 companies using advanced labor, task, and automatability models.",
      image: "/projects/blog-engine.png",
      category: "[professional]",
      year: "2023",
      links: [
        { label: "Site", url: "https://workhelix.ai" }
      ]
    },
    {
      name: "HOW TO BUILD AN AUTONOMOUS DELIVERY NETWORK",
      description: "First-principles buildup for autonomous delivery networks using sidewalk robots, droids, and drones. Focuses on 3 dimensions: throughput, costs, and scale blocks. Mentioned: Starship, Nuro, Prime Air.",
      image: "/projects/blog-engine.png",
      category: "[side project]",
      year: "2018",
      links: [
        { label: "LinkedIn", url: "https://www.linkedin.com/posts/rydcunningham_how-to-build-an-autonomous-delivery-network-activity-6666015742854598657--Jth/" }
      ]
    },
    {
      name: "PATENT: TIME-VARYING LOUDNESS PREDICTION VIA TRAINED MODEL",
      description: "Novel machine-learning method for predicting noise and generating mapping data for urban aviation operating environments, including acoustic impacts from skyports and dynamic skylanes.",
      image: "/projects/blog-engine.png",
      category: "[professional]",
      year: "2019",
      links: [
        { label: "Google Patents", url: "https://patents.google.com/patent/US11900818B2/en" }
      ]
    }
  ]

  // Group projects by year instead of category
  const groupedProjects = projects.reduce((acc, project) => {
    if (!acc[project.year]) {
      acc[project.year] = [];
    }
    acc[project.year].push(project);
    return acc;
  }, {} as Record<string, Project[]>);

  // Sort years in descending order
  const sortedYears = Object.keys(groupedProjects).sort((a, b) => parseInt(b) - parseInt(a));

  return (
    <div className="min-h-screen flex flex-col">
      {/* Fixed Header Content */}
      <div className="fixed top-24 left-24 right-24 z-40">
        <h2 className="text-white/90 text-2xl font-medium mb-4">Work</h2>
        <p className="text-white/80">
          open source projects and contributions.{' '}
          <a href="https://github.com/rydcunningham" className="text-white/80 hover:text-[#F75049] transition-colors">
            view on GitHub →
          </a>{' '}
        </p>
      </div>

      {/* Scrollable Content */}
      <div className="mt-56 px-24 space-y-24">
        {sortedYears.map((year) => {
          const yearProjects = groupedProjects[year] || [];
          return (
            <section key={year} className="space-y-12">
              <h3 className="text-3xl font-mono tracking-tight text-white">{year}</h3>
              <div className="grid grid-cols-2 gap-12">
                {yearProjects.map((project) => (
                  <article key={project.name} className="space-y-4">
                    <div className="max-w-[400px]">
                      <div className="aspect-[16/10] rounded-xl overflow-hidden bg-background/[var(--glass-opacity)] border border-border">
                        {project.image && (
                          <img 
                            src={project.image} 
                            alt={project.name}
                            className="w-full h-full object-cover"
                          />
                        )}
                      </div>
                    </div>
                    <header className="space-y-3">
                      <div className="flex items-baseline gap-3">
                        <h3 className="text-xl font-mono tracking-tight text-white">{project.name}</h3>
                        <span className="text-sm text-white/60 font-mono">{project.category}</span>
                      </div>
                      <p className="text-base text-white/80 font-light leading-relaxed">
                        {project.description}
                      </p>
                    </header>
                    <div className="flex gap-3 text-sm">
                      {project.links.map((link) => (
                        <a 
                          key={`${project.name}-${link.label}`}
                          href={link.url} 
                          className="text-white/60 hover:text-[#F75049]"
                        >
                          {link.label} →
                        </a>
                      ))}
                    </div>
                  </article>
                ))}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  )
} 