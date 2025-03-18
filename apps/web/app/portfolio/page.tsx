'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Image from 'next/image'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip } from 'recharts'

type Affiliation = {
  universities?: string[]
  companies?: string[]
  investors?: string[]
}

type Investment = {
  name: string
  description: string
  round: string
  year: string
  category?: string
  domain?: string
  logoPath?: string
  content?: string
  links: Array<{ label: string, url: string }>
  affiliations?: Affiliation[]
}

export default function Portfolio() {
  const [viewMode, setViewMode] = useState<'table' | 'cards'>('cards')
  const [activeCardIndex, setActiveCardIndex] = useState(0)
  const [selectedInvestment, setSelectedInvestment] = useState<Investment | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<string>('All')
  const cardsContainerRef = useRef<HTMLDivElement>(null)
  const cardRefs = useRef<Array<HTMLDivElement | null>>([])

  const categories = {
    "AI": [
      {
        name: "CentralAxis",
        description: "Data center optimization.",
        content: "Leveraging advanced models and digital twins for datacenter hardware asset monitoring, energy optimization, layout planning, and more. Founded by ex-Microsoft team and part of the Y Combinator S25 cohort.",
        round: "Pre-seed",
        domain: "datacenters",
        year: "2025",
        logoPath: "/portfolio/grayscale/centralaxis.png",
        links: [
          { label: "Site", url: "https://centralaxis.com" }
        ],
        affiliations: [
          { universities: ["Georgia Tech"],
            companies: ["Microsoft"],
            investors: ["Y Combinator", "Augur VC"]
          }
        ]
      },
      {
        name: "TensorStax",
        description: "Autonomous data engineering.",
        content: "Self-healing data engineering agents handling pipeline maintenance, DB migrations, etc.. Uses novel reinforcement learning techniques for minimal human hand-holding.",
        round: "Seed",
        domain: "agentic platforms",
        year: "2025",
        logoPath: "/portfolio/grayscale/tensorstax.png",
        links: [
          { label: "Site", url: "https://tensorstax.com" }
        ],
        affiliations: [
          { universities: ["University of Texas at Austin"],
            investors: ["Bee Partners", "Glasswing Ventures"]
          }
        ]
      },
      {
        name: "Fastino",
        description: "1000x faster LLM inference.",
        content: "Revolutionary inference approach that achieves OOM speedups and CPU compatibility. Early benchmarks show sub-millisecond response times. Inherently hallucination-resistant and optimal for sensitive enterprise workflows like structured outputs, PII masking, etc..",
        round: "Pre-seed",
        domain: "new model architectures",
        year: "2024",
        logoPath: "/portfolio/grayscale/fastino.png",
        links: [
          { label: "Site", url: "https://fastino.ai" },
          { label: "VentureBeat", url: "https://venturebeat.com/ai/microsoft-backed-startup-debuts-task-optimized-enterprise-ai-models-that-run-on-cpus/" }
        ],
        affiliations: [
          {
            investors: ["Microsoft M12", "Insight Venture Partners"]
          }
        ]
      },
      {
        name: "Positron",
        description: "Inference ASICs. OOM improvements over Hopper / Blackwell.",
        content: "Custom silicon designed specifically for transformer architecture inference. Ex-Groq, NVIDIA, and Intel team. Currently in production with multiple customers.",
        round: "Seed",
        domain: "infra",
        year: "2024",
        logoPath: "/portfolio/grayscale/positron.png",
        links: [
          { label: "Site", url: "https://positron.ai" },
          { label: "Deep Dive", url: "https://cerebralvalley.ai/blog/positron-is-pushing-the-boundaries-of-ai-hardware-2THN3t9OrS6n50HC3YyWPu" }
        ],
        affiliations: [
          {
            companies: ["NVIDIA", "Intel", "Groq"]
          }
        ]
      },
      {
        name: "Alecto",
        description: "Identity infrastructure. Stealth.",
        content: "Consent layer for identity verification against non-consensual intimate imagery (NCII) on social media platforms. Combines biometrics and survivor-friendly alerting system to detect, flag, and remove possible NCII across multiple platforms. Co-authors of the Take It Down Act (TIDA).",
        round: "Angel",
        domain: "app layer",
        year: "2024",
        logoPath: "/portfolio/grayscale/alecto.png",
        links: [{ label: "Site", url: "https://alectoai.com" }]
      },
      {
        name: "Cerebral Valley",
        description: "AI community and media platform.",
        content: "The definitive hub for hackers, founders, researchers, and investors. Platform includes exclusive events, deep dive content, and a curated network of AI professionals.",
        round: "Angel",
        domain: 'other',
        year: "2023",
        logoPath: "/portfolio/grayscale/cerebralvalley.png",
        links: [
          { label: "Site", url: "https://cerebralvalley.ai" }
        ]
      }
    ],
    "Deep Tech": [
      {
        name: "Paradigm Robotics",
        description: "Robotic first responders.",
        content: "Developing autonomous robotic systems for high-risk emergency response scenarios. Robots can navigate hazardous environments and perform complex rescue operations without putting human lives at risk.",
        round: "Seed",
        domain: "robotics",
        year: "2025",
        logoPath: "/portfolio/grayscale/paradigm_robotics.png",
        links: [{ label: "Site", url: "https://www.paradigmrobotics.tech/" }],
        affiliations: [
          { universities: ["University of Texas at Austin"]
          }
        ]
      },
      {
        name: "Alterego",
        description: "Silent speech for human <> AI interaction.",
        content: "An MIT Media Lab project. Novel neural interface technology enabling silent speech communication through subtle facial muscle detection.",
        round: "Pre-seed",
        domain: "BCI",
        year: "2025",
        links: [{ label: "Site", url: "https://www.media.mit.edu/projects/alterego/overview/" }],
        affiliations: [
          { universities: ["Massachusetts Institute of Technology"]
          }
        ]
      },
      {
        name: "HYPR",
        description: "Radically different robotaxis with RL and consumer hardware.",
        content: "Reinventing autonomous vehicles using reinforcement learning and off-the-shelf sensors. Achieving L4/L5 autonomy at OOM lower costs compared to incumbents. Founder ex-Zoox.",
        round: "Seed",
        domain: "robotics",
        year: "2024",
        logoPath: "/portfolio/grayscale/hypr.png",
        links: [
          { label: "Site", url: "https://hypr.ai" },
          { label: "Investment Notes", url: "https://www.blackbird.vc/blog/investment-notes-hypr" }
        ],
        affiliations: [
          { companies: ["Zoox"],
            investors: ["Blackbird VC"]
          }
        ]
      },
      {
        name: "Besxar",
        description: "Orbital manufacturing. Stealth",
        content: "Pioneering space-based silicon manufacturing using novel microgravity crystallization processes. Founder ex-OpenAI.",
        round: "Pre-seed",
        domain: "hardware",
        year: "2024",
        links: [
          { label: "Site", url: "https://www.besxar.com/" }
        ],
        affiliations: [
          { companies: ["OpenAI"]
          }
        ]
      },
      {
        name: "Glacier",
        description: "Ending waste with recycling robots.",
        content: "AI-powered recycling automation system achieving incredible sorting accuracy. Deployed in major waste management facilities, processing hundreds of tons of material daily.",
        round: "Seed",
        domain: "robotics",
        year: "2023",
        logoPath: "/portfolio/grayscale/glacier.png",
        links: [
          { label: "Site", url: "https://www.endwaste.io/" },
          { label: "TechCrunch", url: "https://techcrunch.com/2024/03/06/amazon-teams-with-recycling-robot-firm-to-track-package-waste/" }
        ],
        affiliations: [
          { companies: ["Amazon"],
            investors: ["Amazon", "New Enterprise Associates"]
          }
        ]
      }
    ]
  }

  // Flatten investments for card view
  const allInvestments = Object.entries(categories).flatMap(([category, investments]) => 
    investments.map(inv => ({ ...inv, category }))
  )

  // Filter investments based on selected category
  const filteredInvestments = selectedCategory === 'All' 
    ? allInvestments 
    : allInvestments.filter(inv => inv.category === selectedCategory)

  // Calculate investment stats by round
  const roundStats = () => {
    const rounds = ['Angel', 'Pre-seed', 'Seed'];
    const counts = rounds.map(round => {
      return {
        label: round,
        count: filteredInvestments.filter(inv => 
          inv.round.toLowerCase() === round.toLowerCase()
        ).length
      };
    });
    
    // Find the maximum count for scaling
    const maxCount = Math.max(...counts.map(item => item.count), 1);
    
    return {
      data: counts,
      maxCount
    };
  };

  // Calculate investment stats by year
  const yearStats = () => {
    // Get unique years and sort them
    const years = Array.from(new Set(filteredInvestments.map(inv => inv.year)))
      .sort((a, b) => parseInt(a) - parseInt(b));
    
    const counts = years.map(year => {
      return {
        label: year,
        count: filteredInvestments.filter(inv => inv.year === year).length
      };
    });
    
    // Find the maximum count for scaling
    const maxCount = Math.max(...counts.map(item => item.count), 1);
    
    return {
      data: counts,
      maxCount
    };
  };

  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (viewMode !== 'cards') return

      if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        setActiveCardIndex(prev => Math.max(0, prev - 1))
      } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        setActiveCardIndex(prev => Math.min(filteredInvestments.length - 1, prev + 1))
      } else if (e.key === 'Escape') {
        setSelectedInvestment(null)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [viewMode, filteredInvestments.length])

  // Auto-scroll to active card when it changes
  useEffect(() => {
    if (viewMode !== 'cards') return
    
    const activeCard = cardRefs.current[activeCardIndex]
    const container = cardsContainerRef.current
    
    if (activeCard && container) {
      // Get the position of the active card relative to the container
      const cardRect = activeCard.getBoundingClientRect()
      const containerRect = container.getBoundingClientRect()
      
      // Always scroll to center the active card when using keyboard navigation
      // Calculate the scroll position to center the card
      const scrollLeft = 
        activeCard.offsetLeft - 
        (container.clientWidth / 2) + 
        (cardRect.width / 2)
      
      // Smooth scroll to the position
      container.scrollTo({
        left: scrollLeft,
        behavior: 'smooth'
      })
    }
  }, [activeCardIndex, viewMode])

  // Reset card refs when filtered investments change
  useEffect(() => {
    cardRefs.current = cardRefs.current.slice(0, filteredInvestments.length)
  }, [filteredInvestments])

  // Reset active card index when changing categories
  useEffect(() => {
    setActiveCardIndex(0)
  }, [selectedCategory])

  // Function to set card ref that properly handles the type
  const setCardRef = (index: number) => (el: HTMLDivElement | null) => {
    cardRefs.current[index] = el
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Fixed Header Content */}
      <div className="fixed top-24 left-24 right-24 z-40">
        <h2 className="text-white/90 text-2xl font-medium mb-4">Portfolio</h2>
        <div className="space-y-4">
          <p className="text-white/80">
            early-stage investments in AI, infrastructure, and dev tools.{' '}
          </p>
          <div className="flex flex-col gap-4">
            <div className="flex gap-4">
              <button
                onClick={() => setViewMode('cards')}
                className={`text-sm uppercase tracking-wider transition-colors ${
                  viewMode === 'cards' ? 'text-[#F75049]' : 'text-white/60 hover:text-[#F75049]'
                }`}
              >
                [Cards]
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`text-sm uppercase tracking-wider transition-colors ${
                  viewMode === 'table' ? 'text-[#F75049]' : 'text-white/60 hover:text-[#F75049]'
                }`}
              >
                [Table]
              </button>
            </div>

            {/* Mobile Filter Controls - Only show in cards view */}
            {viewMode === 'cards' && (
              <div className="md:hidden flex items-center gap-3">
                <div className="text-white/60 text-sm uppercase tracking-wider">Filter:</div>
                <div className="flex gap-3">
                  <button
                    onClick={() => setSelectedCategory('All')}
                    className={`text-sm uppercase tracking-wider transition-colors ${
                      selectedCategory === 'All' ? 'text-[#F75049]' : 'text-white/60 hover:text-[#F75049]'
                    }`}
                  >
                    All
                  </button>
                  {Object.keys(categories).map(category => (
                    <button
                      key={category}
                      onClick={() => setSelectedCategory(category)}
                      className={`text-sm uppercase tracking-wider transition-colors ${
                        selectedCategory === category ? 'text-[#F75049]' : 'text-white/60 hover:text-[#F75049]'
                      }`}
                    >
                      {category}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="px-24">
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
          <div className="flex">
            {/* Sidebar Menu - Hidden on Mobile */}
            <div className="hidden md:block w-56 mr-12 fixed">
              <div className="space-y-6">
                {/* Desktop Filter Controls */}
                <div>
                  <div className="text-white/80 text-sm uppercase tracking-wider mb-2">Filter</div>
                  <div className="space-y-3">
                    <button
                      onClick={() => setSelectedCategory('All')}
                      className={`text-sm uppercase tracking-wider transition-colors block ${
                        selectedCategory === 'All' ? 'text-[#F75049]' : 'text-white/60 hover:text-[#F75049]'
                      }`}
                    >
                      All
                    </button>
                    {Object.keys(categories).map(category => (
                      <button
                        key={category}
                        onClick={() => setSelectedCategory(category)}
                        className={`text-sm uppercase tracking-wider transition-colors block ${
                          selectedCategory === category ? 'text-[#F75049]' : 'text-white/60 hover:text-[#F75049]'
                        }`}
                      >
                        {category}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="border-t border-white/10 pt-6">
                  <div className="text-white/80 text-sm uppercase tracking-wider mb-2">Stats</div>
                  <div className="text-white/60 text-sm">
                    <div className="flex justify-between mb-1">
                      <span>Companies:</span>
                      <span>{filteredInvestments.length}</span>
                    </div>
                    <div className="flex justify-between mb-4">
                      <span>Active:</span>
                      <span>{filteredInvestments.length}</span>
                    </div>
                    
                    {/* Bar Chart - Investments by Round */}
                    <div className="mb-6">
                      <div className="text-white/80 text-xs uppercase tracking-wider mb-2">By Round</div>
                      <div className="space-y-2">
                        {roundStats().data.map((item) => (
                          <div key={item.label} className="space-y-1">
                            <div className="flex justify-between text-xs">
                              <span>{item.label}</span>
                              <span>{item.count}</span>
                            </div>
                            <div className="h-1.5 w-full bg-white/10 rounded-sm overflow-hidden">
                              <div 
                                className="h-full bg-[#F75049]/70 rounded-sm"
                  style={{
                                  width: `${(item.count / roundStats().maxCount) * 100}%`,
                                  transition: 'width 0.5s ease-in-out'
                                }}
                              />
                            </div>
                          </div>
                        ))}
                      </div>
                      </div>
                      
                    {/* Line Chart - Investments by Year */}
                    <div>
                      <div className="text-white/80 text-xs uppercase tracking-wider mb-2">By Year</div>
                      <div className="h-40 relative mt-4 border-l border-b border-white/10">
                        {/* Chart container with grid */}
                        <div className="absolute inset-0">
                          {yearStats().data.length > 0 ? (
                            <ResponsiveContainer width="100%" height="100%">
                              <LineChart
                                data={yearStats().data}
                                margin={{ top: 10, right: 15, left: 15, bottom: 5 }}
                              >
                                <defs>
                                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#F75049" stopOpacity={0.15} />
                                    <stop offset="95%" stopColor="#F75049" stopOpacity={0} />
                                  </linearGradient>
                                </defs>
                                <CartesianGrid 
                                  strokeDasharray="0" 
                                  horizontal={true} 
                                  vertical={true} 
                                  stroke="#ffffff10"
                                />
                                <XAxis 
                                  dataKey="label" 
                                  interval={0}
                                  tick={(props) => {
                                    const { x, y, payload } = props;
                                    return (
                                      <g transform={`translate(${x},${y})`}>
                                        <text 
                                          x={0} 
                                          y={0} 
                                          dy={3}
                                          textAnchor="end" 
                                          fill="#ffffff99" 
                                          fontSize={9}
                                          fontFamily="monospace"
                                          transform="rotate(-90)"
                                        >
                                          {payload.value}
                                        </text>
                                      </g>
                                    );
                                  }}
                                  height={35}
                                  axisLine={{ stroke: '#ffffff10' }}
                                  tickLine={false}
                                />
                                <YAxis 
                                  hide={true}
                                  domain={[0, 'dataMax + 1']}
                                />
                                <Tooltip 
                                  content={(props) => {
                                    const { active, payload } = props;
                                    if (active && payload && payload.length) {
                                      return (
                                        <div className="bg-[#0A0A0A] border border-[#F75049]/20 px-2 py-1 text-[9px] font-mono">
                                          <p className="text-white/80">{`${payload[0].payload.label}: ${payload[0].value}`}</p>
                                        </div>
                                      );
                                    }
                                    return null;
                                  }}
                                />
                                <Line
                                  type="step"
                                  connectNulls={false}
                                  dataKey="count"
                                  stroke="#F75049"
                                  strokeWidth={1.5}
                                  dot={(props) => {
                                    const { cx, cy, payload } = props;
                                    return (
                                      <g>
                                        {/* Glow effect */}
                                        <circle cx={cx} cy={cy} r={4} fill="#F75049" fillOpacity={0.2} />
                                        {/* Point */}
                                        <circle cx={cx} cy={cy} r={2.5} fill="#0A0A0A" stroke="#F75049" strokeWidth={1.5} />
                                        {/* Value label */}
                                        <text x={cx} y={cy - 8} textAnchor="middle" fill="#F75049" fontSize={8} fontFamily="monospace">
                                          {payload.count}
                                        </text>
                                      </g>
                                    );
                                  }}
                                  activeDot={false}
                                  isAnimationActive={true}
                                  animationDuration={800}
                                  fill="url(#colorCount)"
                                  fillOpacity={1}
                                />
                              </LineChart>
                            </ResponsiveContainer>
                          ) : (
                            <div className="w-full h-full flex items-center justify-center text-white/40 text-xs">
                              <span className="font-mono">[NO DATA]</span>
                          </div>
                        )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Cards Container */}
            <div className="flex-1 relative md:ml-72">
              {/* Fixed viewport for cards */}
              <div className="fixed left-24 md:left-[calc(24px+224px+96px)] right-24 overflow-hidden md:top-[220px] top-[280px]">
                <div 
                  ref={cardsContainerRef}
                  className="flex overflow-x-auto pb-8 items-start pl-4 pr-4 scrollbar-hide touch-pan-x"
                  style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
                >
                  {filteredInvestments.map((investment, index) => (
                    <motion.div
                      key={investment.name}
                      ref={setCardRef(index)}
                      initial={{ opacity: 0, x: 50 }}
                      animate={{ 
                        opacity: 1, 
                        x: 0,
                        transition: { delay: index * 0.05 }
                      }}
                      className={`${
                        index === activeCardIndex 
                          ? 'w-[320px] min-w-[320px] h-[480px]' 
                          : 'w-[240px] min-w-[240px] h-[360px]'
                      } mr-6 cursor-pointer transition-all duration-300 ease-in-out relative`}
                      onClick={() => setActiveCardIndex(index)}
                    >
                      {/* Grabber SVG - Now part of the card's relative positioning */}
                      <div className="absolute -left-5 top-0 h-full z-10 pointer-events-none w-5 flex items-center">
                        <div className="h-full w-full relative">
                          <Image
                            src="/assets/square_grabber.svg"
                            alt=""
                            fill
                            style={{ objectFit: 'fill' }}
                            priority
                          />
          </div>
      </div>

                      <div 
                        className="w-full h-full bg-[#0A0A0A]/90 relative overflow-hidden"
              style={{
                clipPath: 'polygon(0% 0%, 97% 0%, 100% 3%, 100% 97%, 97% 100%, 0% 100%)'
              }}
            >
              <div className="absolute inset-0 border border-[#F75049]/20" />
              
                        <div className={`p-5 h-full flex flex-col ${index === activeCardIndex ? 'p-6' : ''} relative z-10`}>
                          <div className="space-y-3">
                            <div className="text-[#F75049]/50 text-xs uppercase tracking-wider">
                              {investment.category}: {investment.domain}
                            </div>
                            
                            {/* Company Logo Placeholder */}
                            <div className="w-12 h-12 bg-[#F75049]/10 flex items-center justify-center rounded-sm mb-2">
                              <span className="text-[#F75049]/70 text-lg font-bold">
                                {investment.name.charAt(0)}
                              </span>
                  </div>
                            
                            <h3 className={`text-white font-medium ${index === activeCardIndex ? 'text-xl' : 'text-lg'}`}>
                              {investment.name}
                            </h3>
                            <p className="text-white/80 text-xs">
                              {investment.description}
                            </p>
                            {index === activeCardIndex && investment.content && (
                              <p className="text-white/30 text-xs mt-3">
                                {investment.content}
                              </p>
                            )}
                </div>

                          {/* Extended information for active card */}
                          {index === activeCardIndex && (
                            <div className="mt-auto space-y-4">
                              <div className="space-y-3 pt-3 border-t border-white/10 mt-3">
                                <div className="grid grid-cols-2 gap-3 text-white/60 text-xs">
                    <div>
                                    <div className="text-[#F75049]/50 text-xs uppercase tracking-wider mb-1">Round</div>
                                    {investment.round}
                    </div>
                    <div>
                                    <div className="text-[#F75049]/50 text-xs uppercase tracking-wider mb-1">Year</div>
                                    {investment.year}
                    </div>
                  </div>

                                {investment.links.length > 0 && (
                    <div>
                                    <div className="text-[#F75049]/50 text-xs uppercase tracking-wider mb-1">Links</div>
                                    <div className="flex flex-wrap gap-2 text-xs">
                                      {investment.links.map((link) => (
                          <a
                            key={link.url}
                            href={link.url}
                            target="_blank"
                            rel="noopener noreferrer"
                                          className="text-white/60 hover:text-[#F75049] transition-colors"
                                          onClick={(e) => e.stopPropagation()}
                          >
                            {link.label} →
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                              </div>
                            </div>
                          )}
                          
                          {/* Basic info for non-active cards */}
                          {index !== activeCardIndex && (
                            <div className="mt-auto">
                              <div className="flex justify-between text-white/60 text-xs">
                                <span>{investment.round}</span>
                                <span>{investment.year}</span>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
                
                {/* Navigation indicators */}
                <div className="absolute bottom-0 left-0 right-0 flex justify-center gap-2">
                  {filteredInvestments.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setActiveCardIndex(index)}
                      className={`w-2 h-2 rounded-full transition-colors ${
                        index === activeCardIndex ? 'bg-[#F75049]' : 'bg-white/30 hover:bg-white/50'
                      }`}
                      aria-label={`Go to card ${index + 1}`}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
} 