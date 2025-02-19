'use client'

import React from 'react'
import Image from 'next/image'
import Link from 'next/link'
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

export default function Research() {
  const [activeYear, setActiveYear] = useState<string>('')
  const projects: Project[] = [
    {
      name: "OVERCLOCK",
      description: "Energy and infrastructure modeling for exascale computing buildouts.",
      image: "/img/black_sands.avif",
      category: "[side project]",
      year: 2025,
      links: [
        { label: "Demo", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    },
    {
      name: "ARMADA",
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
      name: "SHACK15 VENTURES",
      description: "The official angel fund of the SHACK15 community, investing in early-stage AI & deep tech startups.",
      image: "/img/black_sands.avif",
      category: "[professional]",
      year: 2024,
      links: [
        { label: "Live Site", url: "#" },
        { label: "GitHub", url: "#" }
      ]
    }/*,
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
    }*/
  ]

  // Group projects by year
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
        <h2 className="text-white/90 text-2xl font-medium mb-4">Machine Yearning</h2>
        <div className="space-y-4">
          <p className="text-white/90">
            open source projects and contributions.{' '}
            <a 
              href="https://github.com/rydcunningham" 
              className="text-white/50 hover:text-[#F75049] transition-colors"
              target="_blank"
              rel="noopener noreferrer"
            >
              view on GitHub →
            </a>
          </p>
          <div className="flex gap-4">
            <Link
              href="/blog"
              className="text-white/60 hover:text-[#F75049] text-sm uppercase tracking-wider transition-colors"
            >
              [BLOG]
            </Link>
            <Link
              href="/blog/research"
              className="text-[#F75049] text-sm uppercase tracking-wider transition-colors"
            >
              [RESEARCH]
            </Link>
          </div>
        </div>
      </div>

      {/* Timeline 
      <div className="fixed right-12 top-[200px] z-40">
        <div className="relative">
          {sortedYears.map((year, index) => (
            <div
              key={year}
              className="mb-8 flex items-center"
            >
              <div className="flex items-center">
                <div className={`w-1 h-1 rounded-full ${activeYear === year ? 'bg-[#F75049]' : 'bg-[#F75049]/20'}`} />
                <span className={`ml-3 text-sm font-mono ${
                  activeYear === year ? 'text-[#F75049]' : 'text-white/20'
                } transition-colors`}>
                  {year}
                </span>
              </div>
              {index < sortedYears.length - 1 && (
                <div 
                  className="absolute left-0.5 w-px"
                  style={{
                    top: '12px',
                    height: '28px',
                    background: `repeating-linear-gradient(
                      to bottom,
                      rgba(247, 80, 73, 0.2) 0px,
                      rgba(247, 80, 73, 0.2) 4px,
                      transparent 4px,
                      transparent 8px
                    )`
                  }}
                />
              )}
            </div>
          ))}
        </div>
      </div>*/}

      {/* Scrollable Content */}
      <div className="mt-72 px-24">
        {sortedYears.map((year) => {
          const yearProjects = groupedProjects[year] || [];
          return (
            <section key={year} data-year={year}>
              {yearProjects.map((project) => (
                <article key={project.name} className="group grid grid-cols-1 md:grid-cols-2 gap-12 mb-24">
                  {/* Left Column: Content */}
                  <div className="space-y-4">
                    <h3 className="text-white/90 group-hover:text-[#F75049] transition-colors text-xl">
                      {project.name}
                    </h3>
                    <p className="text-white/50 text-base">
                      {project.description}
                    </p>
                    <div className="flex gap-4">
                      {project.links.map((link) => (
                        <a
                          key={link.label}
                          href={link.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-white/50 hover:text-[#F75049] transition-colors text-sm"
                        >
                          {link.label} →
                        </a>
                      ))}
                    </div>
                  </div>

                  {/* Right Column: Image */}
                  <div className="max-w-[400px] relative justify-self-end">
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
                  </div>
                </article>
              ))}
            </section>
          );
        })}
      </div>
    </div>
  )
} 