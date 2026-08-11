import type { ArchiveProject, Product } from "./types";

// The research banner: the two live products plus retired projects.
// Product access URLs come from lib/site.ts properties, not from here.

export const products: Product[] = [
  {
    slug: "cortex",
    name: "CORTEX",
    tagline: "The Edgerunner Research knowledge base.",
    status: "Private beta",
    year: 2026,
    body: [
      "An encyclopedia of the energy-compute stack: organizations, people, hardware, models, places, and events across energy, silicon, compute, robotics, and intelligence — kept current by a fleet of research daemons.",
      "Every entity is linked into a navigable graph: registry, connectome, atlases, and supply-chain flows, with bilingual coverage of the China energy-compute buildout.",
    ],
    media: [
      {
        kind: "image",
        src: "/media/cortex/registry.jpg",
        alt: "Cortex entity registry, grouped by section",
        caption: "Registry · 3,856 entities, faceted",
      },
      {
        kind: "image",
        src: "/media/cortex/entity.jpg",
        alt: "Cortex entity dossier for NVIDIA",
        caption: "Entity dossier",
      },
      {
        kind: "image",
        src: "/media/cortex/connectome.jpg",
        alt: "Cortex connectome force graph",
        caption: "Connectome",
      },
    ],
  },
  {
    slug: "overclock",
    name: "OVERCLOCK",
    tagline: "Energy-compute digital twins.",
    status: "Private beta",
    year: 2026,
    body: [
      "A simulation platform for composing energy-compute stacks — generation, conversion, transmission, storage, and compute — and running the Sovereign Equation over them.",
      "The kernel is dual-language (Python and JavaScript, held to 1e-9 parity on golden vectors), so full simulations run client-side: token cost, NPV, IRR, and the electron-chain waterfall from fuel to floating point.",
    ],
    media: [
      {
        kind: "image",
        src: "/media/overclock/dynamo.jpg",
        alt: "Overclock Dynamo assembly view with Leviathan spec readout",
        caption: "Dynamo · Colossus 1 as-built, 1.02 Gtok/s",
      },
    ],
  },
];

export const archive: ArchiveProject[] = [
  {
    name: "ARMADA",
    description:
      "Delivery network simulator that tells you where things will break before they do. Optimize costs and throughput by testing assumptions in silico.",
    year: 2024,
    status: "retired",
  },
];

export function getProduct(slug: string): Product | undefined {
  return products.find((p) => p.slug === slug);
}
