import type { Company, Sector } from "./types";

// The 13 portfolio companies, extracted from the old 770-line client
// component. Logos are explicit and only where a real file exists —
// companies without a mark render a monogram (the old data pointed three
// companies at other companies' logos).
//
// To add previews to a company page, drop files in
// public/media/<slug>/ and add a `media` array — the Media panel appears
// automatically and is omitted when absent:
//
//   media: [
//     { kind: "image", src: "/media/positron/board.jpg",
//       alt: "Positron accelerator board", caption: "Atlas board" },
//     { kind: "gif", src: "/media/positron/demo.gif", alt: "Throughput demo" },
//     { kind: "video", youtubeId: "dQw4w9WgXcQ", title: "Founder deep dive" },
//   ]

export const companies: Company[] = [
  {
    slug: "aravolta",
    name: "Aravolta",
    oneLiner: "Data center optimization.",
    body: "Leveraging advanced models and digital twins for datacenter hardware asset monitoring, energy optimization, layout planning, and more. Founded by ex-Microsoft team and part of the Y Combinator S25 cohort.",
    round: "Pre-seed",
    year: 2025,
    sector: "ai",
    domain: "datacenters",
    links: [{ label: "Site", url: "https://aravolta.com" }],
    affiliations: {
      universities: ["Georgia Tech"],
      companies: ["Microsoft"],
      investors: ["Y Combinator", "Augur VC"],
    },
  },
  {
    slug: "tensorstax",
    name: "TensorStax",
    oneLiner: "Autonomous data engineering.",
    body: "Self-healing data engineering agents handling pipeline maintenance, DB migrations, etc. Uses novel reinforcement learning techniques for minimal human hand-holding. Acquired by Snowflake in February 2026; the technology is being folded into Cortex Code, Snowflake's agentic AI developer platform.",
    round: "Seed",
    year: 2025,
    sector: "ai",
    domain: "agentic platforms",
    logo: "/portfolio/grayscale/tensorstax.png",
    status: {
      kind: "acquired",
      label: "Acquired by Snowflake",
      short: "Acquired",
      href: "https://www.snowflake.com/en/blog/tensorstax-acquisition-agentic-ai/",
    },
    links: [
      { label: "Site", url: "https://tensorstax.com" },
      {
        label: "Acquisition",
        url: "https://www.snowflake.com/en/blog/tensorstax-acquisition-agentic-ai/",
      },
    ],
    affiliations: {
      universities: ["University of Texas at Austin"],
      companies: ["Snowflake"],
      investors: ["Bee Partners", "Glasswing Ventures"],
    },
  },
  {
    slug: "inferx",
    name: "InferX",
    oneLiner: "Serverless inference for production AI.",
    body: "Runs large numbers of models under irregular real-world traffic without paying for idle GPUs. Sub-second cold starts via GPU snapshot restore — including 32B models — behind an OpenAI-compatible API, deployable to hosted endpoints, private infrastructure, or on-prem.",
    round: "Seed",
    year: 2025,
    sector: "ai",
    domain: "infra",
    links: [{ label: "Site", url: "https://inferx.net" }],
    affiliations: { investors: ["Augur VC"] },
  },
  {
    slug: "apical-intelligence",
    name: "Apical Intelligence",
    oneLiner: "Neuroscience-inspired efficient AI. Stealth.",
    body: "Building AI systems on neuroscience principles rather than scaled transformers, combining ML research with systems engineering to cut the power, latency, and cost of frontier-grade inference. Pre-product.",
    round: "Pre-seed",
    year: 2026,
    sector: "ai",
    domain: "new model architectures",
    links: [{ label: "Site", url: "https://www.apicalintelligence.io" }],
  },
  {
    slug: "fastino",
    name: "Fastino",
    oneLiner: "1000x faster LLM inference.",
    body: "Revolutionary inference approach that achieves OOM speedups and CPU compatibility. Early benchmarks show sub-millisecond response times. Inherently hallucination-resistant and optimal for sensitive enterprise workflows like structured outputs, PII masking, etc.",
    round: "Pre-seed",
    year: 2024,
    sector: "ai",
    domain: "new model architectures",
    logo: "/portfolio/grayscale/fastino.png",
    links: [
      { label: "Site", url: "https://fastino.ai" },
      {
        label: "VentureBeat",
        url: "https://venturebeat.com/ai/microsoft-backed-startup-debuts-task-optimized-enterprise-ai-models-that-run-on-cpus/",
      },
    ],
    affiliations: { investors: ["Microsoft M12", "Insight Venture Partners"] },
  },
  {
    slug: "positron",
    name: "Positron",
    oneLiner: "Inference ASICs. OOM improvements over Hopper / Blackwell.",
    body: "Custom silicon designed specifically for transformer architecture inference. Ex-Groq, NVIDIA, and Intel team. Currently in production with multiple customers.",
    round: "Seed",
    year: 2024,
    sector: "ai",
    domain: "infra",
    logo: "/portfolio/grayscale/positron.png",
    links: [
      { label: "Site", url: "https://positron.ai" },
      {
        label: "Deep Dive",
        url: "https://cerebralvalley.ai/blog/positron-is-pushing-the-boundaries-of-ai-hardware-2THN3t9OrS6n50HC3YyWPu",
      },
      {
        label: "Series A Announcement",
        url: "https://www.businesswire.com/news/home/20250728912387/en/Positron-AI-Secures-%2451.6-Million-in-Oversubscribed-Series-A-to-Accelerate-Inference-Optimized-Hardware",
      },
    ],
    affiliations: { companies: ["NVIDIA", "Intel", "Groq"] },
  },
  {
    slug: "alecto",
    name: "Alecto",
    oneLiner: "Identity infrastructure. Stealth.",
    body: "Consent layer for identity verification against non-consensual intimate imagery (NCII) on social media platforms. Combines biometrics and survivor-friendly alerting system to detect, flag, and remove possible NCII across multiple platforms. Co-authors of the Take It Down Act (TIDA).",
    round: "Angel",
    year: 2024,
    sector: "ai",
    domain: "app layer",
    logo: "/portfolio/grayscale/alecto.png",
    links: [{ label: "Site", url: "https://alectoai.com" }],
  },
  {
    slug: "cerebral-valley",
    name: "Cerebral Valley",
    oneLiner: "AI community and media platform.",
    body: "The definitive hub for hackers, founders, researchers, and investors. Platform includes exclusive events, deep dive content, and a curated network of AI professionals.",
    round: "Angel",
    year: 2023,
    sector: "ai",
    domain: "other",
    logo: "/portfolio/grayscale/cerebralvalley.png",
    links: [{ label: "Site", url: "https://cerebralvalley.ai" }],
  },
  {
    slug: "paradigm-robotics",
    name: "Paradigm Robotics",
    oneLiner: "Robotic first responders.",
    body: "Developing autonomous robotic systems for high-risk emergency response scenarios. Robots can navigate hazardous environments and perform complex rescue operations without putting human lives at risk.",
    round: "Seed",
    year: 2025,
    sector: "deep-tech",
    domain: "robotics",
    logo: "/portfolio/grayscale/paradigm_robotics.png",
    links: [{ label: "Site", url: "https://www.paradigmrobotics.tech/" }],
    affiliations: { universities: ["University of Texas at Austin"] },
  },
  {
    slug: "360-energy",
    name: "360 Energy",
    oneLiner: "Building the energy-compute asset class.",
    body: "Backed by Halliburton, off-grid gas offtake monetized via in-field computing.",
    round: "Seed",
    year: 2025,
    sector: "deep-tech",
    domain: "energy",
    links: [{ label: "Site", url: "https://www.360energyco.com/" }],
    affiliations: {
      universities: ["Southern Methodist University"],
      companies: ["Halliburton"],
    },
  },
  {
    slug: "springcycle-energy",
    name: "SpringCycle Energy",
    oneLiner: "Ultra-long-duration energy storage.",
    body: "New battery chemistry for long-duration energy storage.",
    round: "Pre-seed",
    year: 2025,
    sector: "deep-tech",
    domain: "energy",
    links: [{ label: "Site", url: "https://springcycleenergy.com/" }],
  },
  {
    slug: "deployable-energy",
    name: "Deployable Energy",
    oneLiner: "Factory-built nuclear, deployable anywhere.",
    body: "A 1 MWe / 3.5 MWt helium-cooled 'nuclear battery' built from off-the-shelf materials on standard 5% U235 fuel with a five-year refueling cycle. Houston-based, selected for the Department of Energy's Nuclear Energy Launch Pad, and driving its first module to Idaho for federal testing.",
    round: "Seed",
    year: 2026,
    sector: "deep-tech",
    domain: "energy",
    links: [{ label: "Site", url: "https://www.deployable.energy" }],
    affiliations: { companies: ["U.S. Department of Energy"] },
  },
  {
    slug: "fervo-energy",
    name: "Fervo Energy",
    oneLiner: "Enhanced geothermal for 24/7 clean power.",
    body: "Applies horizontal drilling and distributed fiber-optic sensing from oil and gas to unlock geothermal in places it was never economic, targeting dependable round-the-clock baseload. Listed on Nasdaq in May 2026 at $27 a share in an upsized 70M-share offering.",
    round: "Seed",
    year: 2024,
    sector: "deep-tech",
    domain: "energy",
    status: {
      kind: "public",
      label: "NASDAQ: FRVO",
      href: "https://ir.fervoenergy.com/",
    },
    links: [
      { label: "Site", url: "https://fervoenergy.com" },
      { label: "Investor Relations", url: "https://ir.fervoenergy.com/" },
    ],
  },
  {
    slug: "lunetronic",
    name: "Lunetronic",
    oneLiner: "Optical clocks for lunar navigation.",
    body: "Building an ultra-stable cryogenic optical clock to sit in a permanently shadowed crater near the lunar pole — foundational timing and navigation infrastructure for everything that operates on the Moon. Collaborating with NASA JPL and NIST on the Lunar Super-Laser project.",
    round: "Pre-seed",
    year: 2026,
    sector: "deep-tech",
    domain: "space",
    links: [{ label: "Site", url: "https://lunetronic.com" }],
    affiliations: { companies: ["NASA JPL", "NIST"] },
  },
  {
    slug: "alterego",
    name: "Alterego",
    oneLiner: "Silent speech for human <> AI interaction.",
    body: "An MIT Media Lab project. Novel neural interface technology enabling silent speech communication through subtle facial muscle detection.",
    round: "Pre-seed",
    year: 2025,
    sector: "deep-tech",
    domain: "BCI",
    links: [
      { label: "Site", url: "https://www.media.mit.edu/projects/alterego/overview/" },
    ],
    affiliations: { universities: ["Massachusetts Institute of Technology"] },
  },
  {
    slug: "hypr",
    name: "HYPR",
    oneLiner: "Radically different robotaxis with RL and consumer hardware.",
    body: "Reinventing autonomous vehicles using reinforcement learning and off-the-shelf sensors. Achieving L4/L5 autonomy at OOM lower costs compared to incumbents. Founder ex-Zoox.",
    round: "Seed",
    year: 2024,
    sector: "deep-tech",
    domain: "robotics",
    logo: "/portfolio/grayscale/hypr.png",
    links: [
      { label: "Site", url: "https://hypr.ai" },
      { label: "Investment Notes", url: "https://www.blackbird.vc/blog/investment-notes-hypr" },
    ],
    affiliations: { companies: ["Zoox"], investors: ["Blackbird VC"] },
  },
  {
    slug: "besxar",
    name: "Besxar",
    oneLiner: "Orbital manufacturing. Stealth.",
    body: "Pioneering space-based silicon manufacturing using novel microgravity crystallization processes. Founder ex-OpenAI.",
    round: "Pre-seed",
    year: 2024,
    sector: "deep-tech",
    domain: "hardware",
    links: [{ label: "Site", url: "https://www.besxar.com/" }],
    affiliations: { companies: ["OpenAI"] },
  },
  {
    slug: "glacier",
    name: "Glacier",
    oneLiner: "Ending waste with recycling robots.",
    body: "AI-powered recycling automation system achieving incredible sorting accuracy. Deployed in major waste management facilities, processing hundreds of tons of material daily.",
    round: "Seed",
    year: 2023,
    sector: "deep-tech",
    domain: "robotics",
    logo: "/portfolio/grayscale/glacier.png",
    links: [
      { label: "Site", url: "https://www.endwaste.io/" },
      {
        label: "TechCrunch",
        url: "https://techcrunch.com/2024/03/06/amazon-teams-with-recycling-robot-firm-to-track-package-waste/",
      },
    ],
    affiliations: {
      companies: ["Amazon"],
      investors: ["Amazon", "New Enterprise Associates"],
    },
  },
];

export const sectorLabels: Record<Sector, string> = {
  ai: "AI",
  "deep-tech": "Deep Tech",
};

/** Both outcomes are good news, so both use fixed semantic hues rather than
    the brand accent (which marks interaction, not meaning): emerald for an
    acquisition, sky for a listing — distinguishable at a glance, and both
    modifiers already ship light-theme contrast overrides in kiroshi.css,
    so neither needs new CSS. */
export function statusChip(kind: "acquired" | "public"): string {
  return kind === "acquired" ? "k-chip k-chip--good" : "k-chip k-chip--sky";
}

export function getCompany(slug: string): Company | undefined {
  return companies.find((c) => c.slug === slug);
}

export function bySector(sector: Sector): Company[] {
  return companies.filter((c) => c.sector === sector);
}
