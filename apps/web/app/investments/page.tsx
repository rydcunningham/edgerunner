export default function Investments() {
  const categories = {
    "AI": [
      {
        name: "OpenInfer",
        description: "Local inference. Stealth.",
        round: "Pre-seed",
        year: "2024",
        links: []
      },
      {
        name: "Positron",
        description: "Inference ASICs. OOM improvements over Hopper / Blackwell.",
        round: "Seed",
        year: "2024",
        links: [
          { label: "Site", url: "https://positron.ai" },
          { label: "Deep Dive", url: "https://cerebralvalley.ai/blog/positron-is-pushing-the-boundaries-of-ai-hardware-2THN3t9OrS6n50HC3YyWPu" }
        ]
      },
      {
        name: "Fastino",
        description: "1000x faster LLM inference.",
        round: "Pre-seed",
        year: "2024",
        links: [
          { label: "Site", url: "https://fastino.ai" },
          { label: "VentureBeat", url: "https://venturebeat.com/ai/microsoft-backed-startup-debuts-task-optimized-enterprise-ai-models-that-run-on-cpus/" }
        ]
      }
    ],
    "Deep Tech": [
      {
        name: "HYPR",
        description: "Radically different robotaxis with RL and consumer hardware.",
        round: "Seed",
        year: "2024",
        links: [
          { label: "Site", url: "https://hypr.ai" },
          { label: "Investment Notes", url: "https://www.blackbird.vc/blog/investment-notes-hypr" }
        ]
      },
      {
        name: "Besxar",
        description: "Orbital manufacturing. Stealth",
        round: "Pre-seed",
        year: "2024",
        links: [
          { label: "Site", url: "https://www.besxar.com/" }
        ]
      },
      {
        name: "Glacier",
        description: "Ending waste with recycling robots.",
        round: "Seed",
        year: "2023",
        links: [
          { label: "Site", url: "https://www.endwaste.io/" },
          { label: "TechCrunch", url: "https://techcrunch.com/2024/03/06/amazon-teams-with-recycling-robot-firm-to-track-package-waste/" }
        ]
      }
    ]
  }

  return (
    <div className="space-y-12">
      <header className="space-y-2">
        <h2 className="text-xl font-mono">featured investments</h2>
        <p className="text-zinc-300">
          focused on early-stage investments in AI/ML, developer tools, and enterprise SaaS.{' '}
          <a href="mailto:rc@edgerunner.io" className="text-[#C14BFC] hover:underline">
            get in touch
          </a>{' '}
          →
        </p>
      </header>

      <div className="space-y-16">
        {Object.entries(categories).map(([category, investments]) => (
          <section key={category} className="space-y-6">
            <h3 className="text-lg font-mono text-zinc-400">{category}</h3>
            <div className="space-y-6">
              {investments.map((investment) => (
                <article key={investment.name} className="space-y-4">
                  <h4 className="text-[#C14BFC] font-mono">{investment.name}</h4>
                  <div className="grid grid-cols-[1fr,120px,80px] gap-6">
                    <p className="text-zinc-300">{investment.description}</p>
                    <div className="text-zinc-300 font-mono">{investment.round}</div>
                    <div className="text-zinc-500 font-mono">{investment.year}</div>
                  </div>
                  <div className="flex gap-3 text-sm">
                    {investment.links.map((link) => (
                      <a 
                        key={link.url}
                        href={link.url} 
                        className="text-zinc-500 hover:text-[#C14BFC]"
                      >
                        {link.label} →
                      </a>
                    ))}
                  </div>
                </article>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  )
} 