import type { Update } from "./types";

// The updates feed. Newest first — one row each.
// Home shows HOME_LIMIT; /updates shows the full archive.
// Dates are YYYY.MM: precise enough to order, no invented day-of-month.

export const HOME_LIMIT = 5;

export const updates: Update[] = [
  {
    date: "2026.08",
    kind: "product",
    title: "Overclock enters private beta",
    href: "/research/overclock",
  },
  {
    date: "2026.08",
    kind: "product",
    title: "Cortex enters private beta",
    href: "/research/cortex",
  },
  {
    date: "2025.07",
    kind: "press",
    title: "Positron raises $51.6M Series A for inference-optimized hardware",
    href: "https://www.businesswire.com/news/home/20250728912387/en/Positron-AI-Secures-%2451.6-Million-in-Oversubscribed-Series-A-to-Accelerate-Inference-Optimized-Hardware",
    external: true,
  },
  {
    date: "2025.06",
    kind: "investment",
    title: "Invested in Aravolta — datacenter digital twins, YC S25",
    href: "/portfolio/aravolta",
  },
  {
    date: "2025.03",
    kind: "investment",
    title: "Invested in 360 Energy — building the energy-compute asset class",
    href: "/portfolio/360-energy",
  },
  {
    date: "2024.11",
    kind: "press",
    title: "Fastino debuts task-optimized enterprise models that run on CPUs",
    href: "https://venturebeat.com/ai/microsoft-backed-startup-debuts-task-optimized-enterprise-ai-models-that-run-on-cpus/",
    external: true,
  },
  {
    date: "2024.03",
    kind: "press",
    title: "Amazon teams with Glacier to track package waste",
    href: "https://techcrunch.com/2024/03/06/amazon-teams-with-recycling-robot-firm-to-track-package-waste/",
    external: true,
  },
];

export const kindLabels: Record<Update["kind"], string> = {
  product: "Product",
  investment: "Investment",
  press: "Press",
};
