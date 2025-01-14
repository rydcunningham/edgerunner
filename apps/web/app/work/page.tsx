'use client'

import Image from 'next/image'
import { useState, useEffect } from 'react'

interface Project {
  name: string;
  description: string;
  image: string;
  category: string;
  year: number;
  links: Array<{
    label: string;
    url: string;
  }>;
}

export default function Work() {
  const [activeYear, setActiveYear] = useState<string>('')
  const projects: Project[] = [
    {
      name: "CORTEX",
      description: "A local scraping tool for extracting, categorizing, and storing content from websites into a structured database.",
      image: "/img/black_sands.avif",
      category: "[side project]",
      year: 2024,
      links: [
        { label: "Demo", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "CITYSIM",
      description: "Delivery network simulator that tells you where things will break before they do. Optimize costs and throughput by testing assumptions in silico.",
      image: "/img/black_sands.avif",
      category: "[side project]",
      year: 2024,
      links: [
        { label: "Demo", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "MIKOSHI HOMELAB",
      description: "Franken-lab for self-hosted AI, cloud, and media projects. Built w/ unRAID on Supermicro, Synology, NVIDIA, RPi.",
      image: "/img/black_sands.avif",
      category: "[side project]",
      year: 2024,
      links: [
        { label: "Live Site", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "SHACK15 VENTURES",
      description: "The official angel fund of the SHACK15 community, investing in early-stage AI & deep tech startups.",
      image: "/img/black_sands.avif",
      category: "[professional]",
      year: 2024,
      links: [
        { label: "Live Site", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "VALIDMIND",
      description: "Model validation, testing, and documentation for ML in financial services.",
      image: "/img/black_sands.avif",
      category: "[professional]",
      year: 2021,
      links: [
        { label: "Site", url: "https://validmind.ai" }
      ]
    },
    {
      name: "SKYFIRE AI",
      description: "Swarm intelligence for heterogeneous drone fleets.",
      image: "/img/black_sands.avif",
      category: "[professional]",
      year: 2023,
      links: [
        { label: "Site", url: "https://skyfireai.com" }
      ]
    },
    {
      name: "RAPIDFIRE",
      description: "Parallelized model training and experimentation for Data Science teams.",
      image: "/img/black_sands.avif",
      category: "[professional]",
      year: 2023,
      links: [
        { label: "Site", url: "https://rapidfire.ai" }
      ]
    },
    {
      name: "SPEECHLAB",
      description: "Professional voice cloning and synthesis.",
      image: "/img/black_sands.avif",
      category: "[professional]",
      year: 2022,
      links: [
        { label: "Site", url: "https://speechlab.ai" }
      ]
    },
    {
      name: "WORKHELIX",
      description: "Assessing GenAI labor transformation potential for F500 companies using advanced labor, task, and automatability models.",
      image: "/img/black_sands.avif",
      category: "[professional]",
      year: 2023,
      links: [
        { label: "Site", url: "https://workhelix.com" }
      ]
    },
    {
      name: "WHITEPAPER: HOW TO BUILD AN AUTONOMOUS DELIVERY NETWORK",
      description: "First-principles buildup for autonomous delivery networks using sidewalk robots, droids, and drones. Focuses on 3 dimensions: throughput, costs, and scale blocks. Mentioned: Starship, Nuro, Prime Air.",
      image: "/img/black_sands.avif",
      category: "[side project]",
      year: 2018,
      links: [
        { label: "LinkedIn", url: "https://www.linkedin.com/posts/rydcunningham_how-to-build-an-autonomous-delivery-network-activity-6666015742854598657--Jth/" }
      ]
    },
    {
      name: "PATENT: TIME-VARYING LOUDNESS PREDICTION VIA TRAINED MODEL",
      description: "Novel machine-learning method for predicting noise and generating mapping data for urban aviation operating environments, including acoustic impacts from skyports and dynamic skylanes.",
      image: "/img/black_sands.avif",
      category: "[professional]",
      year: 2019,
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

  // Handle scroll and update active year
  useEffect(() => {
    const handleScroll = () => {
      const yearSections = Array.from(document.querySelectorAll('[data-year]'));
      const scrollPosition = window.scrollY + window.innerHeight / 2;

      for (const section of yearSections) {
        const sectionTop = section.getBoundingClientRect().top + window.scrollY;
        const sectionBottom = sectionTop + section.getBoundingClientRect().height;

        if (scrollPosition >= sectionTop && scrollPosition <= sectionBottom) {
          setActiveYear(section.getAttribute('data-year') || '');
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initial check
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

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

      {/* Timeline */}
      <div className="fixed right-12 top-1/2 -translate-y-1/2 z-40 flex flex-col items-center">
        <div className="h-[50vh] relative">
          {sortedYears.map((year, index) => (
            <div
              key={year}
              className="absolute transform -translate-x-1/2"
              style={{
                top: `${(index / (sortedYears.length - 1)) * 100}%`,
                left: '0'
              }}
            >
              {/* Dashed line to next year (except for last year) */}
              {index < sortedYears.length - 1 && (
                <div 
                  className="absolute w-px h-[100px] left-0"
                  style={{
                    background: `repeating-linear-gradient(
                      to bottom,
                      rgba(247, 80, 73, 0.2) 0px,
                      rgba(247, 80, 73, 0.2) 4px,
                      transparent 4px,
                      transparent 8px
                    )`,
                    height: `${100 / (sortedYears.length - 1)}vh`
                  }}
                />
              )}
              
              <div className="flex items-center">
                <div className={`w-1 h-1 rounded-full ${activeYear === year ? 'bg-[#F75049]' : 'bg-[#F75049]/20'}`} />
                <span className={`ml-3 text-sm font-mono ${
                  activeYear === year ? 'text-[#F75049]' : 'text-white/20'
                } transition-colors`}>
                  {year}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="mt-56 px-24 space-y-24">
        {sortedYears.map((year) => {
          const yearProjects = groupedProjects[year] || [];
          return (
            <section key={year} data-year={year} className="space-y-12">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                {yearProjects.map((project) => (
                  <article key={project.name} className="space-y-4">
                    <div className="max-w-[400px] relative">
                      <Image 
                        src="/assets/grabber.svg"
                        alt="Grabber"
                        width={20}
                        height={250}
                        className="absolute -left-2.5 top-0 h-full w-auto"
                      />
                      <div className="absolute inset-0 overflow-hidden" style={{ clipPath: 'polygon(0% 0%, 97% 0%, 100% 3%, 100% 97%, 97% 100%, 0% 100%)' }}>
                        <Image 
                          src={project.image}
                          alt={project.name}
                          width={400}
                          height={250}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <Image 
                        src="/assets/4_2.5_frame.svg"
                        alt="Frame"
                        width={400}
                        height={250}
                        className="w-full h-auto relative z-10"
                      />
                    </div>
                    <header className="space-y-3">
                      <div className="flex items-baseline gap-3">
                        <h3 className="text-xl font-mono tracking-tight text-white">{project.name}</h3>
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