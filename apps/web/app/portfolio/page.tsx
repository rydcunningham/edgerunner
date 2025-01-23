'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Image from 'next/image'

type Investment = {
  name: string
  description: string
  round: string
  year: string
  category?: string
  domain?: string
  links: Array<{ label: string, url: string }>
}

export default function Portfolio() {
  const [viewMode, setViewMode] = useState<'table' | 'cards'>('table')
  const [activeCardIndex, setActiveCardIndex] = useState(0)
  const [selectedInvestment, setSelectedInvestment] = useState<Investment | null>(null)

  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (viewMode !== 'cards') return

      if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        setActiveCardIndex(prev => Math.max(0, prev - 1))
      } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        setActiveCardIndex(prev => Math.min(allInvestments.length - 1, prev + 1))
      } else if (e.key === 'Escape') {
        setSelectedInvestment(null)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [viewMode])

  const categories = {
    "AI": [
      /*{
        name: "STEALTH",
        description: "Data center optimization.",
        round: "Pre-seed",
        domain: "infra",
        year: "2025",
        links: [
        ]
      },*/
      {
        name: "Fastino",
        description: "1000x faster LLM inference.",
        round: "Pre-seed",
        domain: "new model architectures",
        year: "2024",
        links: [
          { label: "Site", url: "https://fastino.ai" },
          { label: "VentureBeat", url: "https://venturebeat.com/ai/microsoft-backed-startup-debuts-task-optimized-enterprise-ai-models-that-run-on-cpus/" }
        ]
      },
      {
        name: "Positron",
        description: "Inference ASICs. OOM improvements over Hopper / Blackwell.",
        round: "Seed",
        domain: "infra",
        year: "2024",
        links: [
          { label: "Site", url: "https://positron.ai" },
          { label: "Deep Dive", url: "https://cerebralvalley.ai/blog/positron-is-pushing-the-boundaries-of-ai-hardware-2THN3t9OrS6n50HC3YyWPu" }
        ]
      },
      {
        name: "STEALTH",
        description: "Identity infrastructure for combatting image-based abuse.",
        round: "Angel",
        domain: "app layer",
        year: "2024",
        links: []
      },
      {
        name: "Cerebral Valley",
        description: "AI community and media platform.",
        round: "Angel",
        domain: 'other',
        year: "2023",
        links: [
          { label: "Site", url: "https://cerebralvalley.ai" }
        ]
      }
    ],
    "Deep Tech": [
      {
        name: "HYPR",
        description: "Radically different robotaxis with RL and consumer hardware.",
        round: "Seed",
        domain: "robotics",
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
        domain: "hardware",
        year: "2024",
        links: [
          { label: "Site", url: "https://www.besxar.com/" }
        ]
      },
      {
        name: "Glacier",
        description: "Ending waste with recycling robots.",
        round: "Seed",
        domain: "robotics",
        year: "2023",
        links: [
          { label: "Site", url: "https://www.endwaste.io/" },
          { label: "TechCrunch", url: "https://techcrunch.com/2024/03/06/amazon-teams-with-recycling-robot-firm-to-track-package-waste/" }
        ]
      }
    ]
  }

  // Flatten investments for card view
  const allInvestments = Object.entries(categories).flatMap(([category, investments]) => 
    investments.map(inv => ({ ...inv, category }))
  )

  return (
    <div className="min-h-screen flex flex-col">
      {/* Fixed Header Content */}
      <div className="fixed top-24 left-24 right-24 z-40">
        <h2 className="text-white/90 text-2xl font-medium mb-4">Portfolio</h2>
        <div className="space-y-4">
          <p className="text-white/80">
            early-stage investments in AI, infrastructure, and dev tools.{' '}
          </p>
          <div className="flex gap-4">
            <button
              onClick={() => setViewMode('table')}
              className={`text-sm uppercase tracking-wider transition-colors ${
                viewMode === 'table' ? 'text-[#F75049]' : 'text-white/60 hover:text-[#F75049]'
              }`}
            >
              [Table]
            </button>
            <button
              onClick={() => setViewMode('cards')}
              className={`text-sm uppercase tracking-wider transition-colors ${
                viewMode === 'cards' ? 'text-[#F75049]' : 'text-white/60 hover:text-[#F75049]'
              }`}
            >
              [Cards]
            </button>
          </div>
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="mt-64 px-24">
        {viewMode === 'table' ? (
          <div className="space-y-16">
            {Object.entries(categories).map(([category, investments]) => (
              <section key={category} className="space-y-6">
                <h3 className="text-lg font-mono text-white">{category}</h3>
                <div className="space-y-8">
                  {investments.map((investment) => (
                    <article key={investment.name} className="space-y-4">
                      <h4 className="text-white font-mono">{investment.name}</h4>
                      <div className="max-w-3xl grid grid-cols-[1fr,auto,auto] gap-4">
                        <p className="text-white/80">{investment.description}</p>
                        <div className="text-white/60">{investment.round}</div>
                        <div className="text-white/60">{investment.year}</div>
                      </div>
                      {investment.links.length > 0 && (
                        <div className="flex gap-3 text-sm">
                          {investment.links.map((link) => (
                            <a 
                              key={link.url}
                              href={link.url} 
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-white/60 hover:text-[#F75049]"
                            >
                              {link.label} →
                            </a>
                          ))}
                        </div>
                      )}
                    </article>
                  ))}
                </div>
              </section>
            ))}
          </div>
        ) : (
          <div className="relative h-[600px] flex items-center justify-center">
            <AnimatePresence mode="wait">
              {allInvestments.map((investment, index) => (
                <motion.div
                  key={investment.name}
                  initial={{ opacity: 0, x: 100, rotateY: 45 }}
                  animate={{
                    opacity: index === activeCardIndex ? 1 : 0.3,
                    x: (index - activeCardIndex) * 100,
                    rotateY: index === activeCardIndex ? 0 : 45,
                    scale: index === activeCardIndex ? 1 : 0.9,
                    zIndex: allInvestments.length - Math.abs(index - activeCardIndex)
                  }}
                  exit={{ opacity: 0, x: -100, rotateY: -45 }}
                  transition={{ duration: 0.5 }}
                  className="absolute w-[400px] h-[600px] cursor-pointer"
                  onClick={() => setSelectedInvestment(investment)}
                  style={{
                    perspective: '1000px',
                    transformStyle: 'preserve-3d'
                  }}
                >
                  {/* Grabber SVG */}
                  <Image
                    src="/assets/square_grabber.svg"
                    alt=""
                    width={20}
                    height={400}
                    className="absolute -left-5 top-0 h-full w-auto z-10"
                  />
                  <div className="w-full h-full bg-[#0A0A0A]/90 relative overflow-hidden"
                       style={{
                         clipPath: 'polygon(0% 0%, 97% 0%, 100% 3%, 100% 97%, 97% 100%, 0% 100%)'
                       }}>
                    <div className="absolute inset-0 border border-[#F75049]/20" />
                    <div className="p-8 h-full flex flex-col">
                      <div className="space-y-6">
                        <div className="text-[#F75049]/50 text-sm uppercase tracking-wider">{investment.category}: {investment.domain}</div>
                        <h3 className="text-white text-2xl font-medium">{investment.name}</h3>
                        <p className="text-white/80">{investment.description}</p>
                      </div>
                      
                      {/*Optional Glacier Icon*/}
                      {/*investment.name === 'Glacier' && (
                        <div className="flex-1 flex items-center justify-center">
                          <Image
                            src="/assets/glacier-icon.svg"
                            alt="Glacier Icon"
                            width={120}
                            height={120}
                            className="opacity-50"
                          />
                        </div>
                      )*/}

                      <div className="space-y-4">
                        <div className="flex justify-between text-white/60">
                          <span>{investment.round}</span>
                          <span>{investment.year}</span>
                        </div>
                        {investment.links.length > 0 && (
                          <div className="flex gap-3 text-sm">
                            {investment.links.map((link) => (
                              <a 
                                key={link.url}
                                href={link.url} 
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-white/60 hover:text-[#F75049]"
                                onClick={(e) => e.stopPropagation()}
                              >
                                {link.label} →
                              </a>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            
            {/* Navigation buttons */}
            <button
              onClick={() => setActiveCardIndex(Math.max(0, activeCardIndex - 1))}
              className="absolute left-0 top-1/2 -translate-y-1/2 text-white/60 hover:text-[#F75049] z-50"
            >
              ←
            </button>
            <button
              onClick={() => setActiveCardIndex(Math.min(allInvestments.length - 1, activeCardIndex + 1))}
              className="absolute right-0 top-1/2 -translate-y-1/2 text-white/60 hover:text-[#F75049] z-50"
            >
              →
            </button>
          </div>
        )}
      </div>

      {/* Lightbox */}
      <AnimatePresence>
        {selectedInvestment && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center"
            onClick={() => setSelectedInvestment(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="relative w-[800px] max-h-[80vh] bg-[#0A0A0A] overflow-hidden m-8"
              style={{
                clipPath: 'polygon(0% 0%, 97% 0%, 100% 3%, 100% 97%, 97% 100%, 0% 100%)'
              }}
              onClick={e => e.stopPropagation()}
            >
              {/* Red border effect */}
              <div className="absolute inset-0 border border-[#F75049]/20" />
              
              {/* Close button */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedInvestment(null);
                }}
                className="absolute top-4 right-4 text-white/60 hover:text-[#F75049] z-50"
              >
                [×]
              </button>

              <div className="p-12 space-y-8 overflow-y-auto max-h-[80vh] relative z-20">
                <div>
                  <div className="text-[#F75049]/50 text-sm uppercase tracking-wider mb-2">
                    {selectedInvestment.category}: {selectedInvestment.domain}
                  </div>
                  <h3 className="text-white text-4xl font-medium mb-4">{selectedInvestment.name}</h3>
                  <p className="text-white/80 text-lg leading-relaxed">{selectedInvestment.description}</p>
                </div>

                <div className="space-y-4">
                  <div className="flex gap-8 text-white/60">
                    <div>
                      <div className="text-[#F75049]/50 text-sm uppercase tracking-wider mb-1">Round</div>
                      {selectedInvestment.round}
                    </div>
                    <div>
                      <div className="text-[#F75049]/50 text-sm uppercase tracking-wider mb-1">Year</div>
                      {selectedInvestment.year}
                    </div>
                  </div>

                  {selectedInvestment.links.length > 0 && (
                    <div>
                      <div className="text-[#F75049]/50 text-sm uppercase tracking-wider mb-3">Links</div>
                      <div className="flex flex-wrap gap-4">
                        {selectedInvestment.links.map((link) => (
                          <a
                            key={link.url}
                            href={link.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-white/60 hover:text-[#F75049] transition-colors relative z-30"
                            onClick={(e) => {
                              e.stopPropagation();
                            }}
                          >
                            {link.label} →
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
} 