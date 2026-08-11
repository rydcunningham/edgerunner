// Single source of truth for site identity, nav, socials, and the
// cross-property URLs. Nothing else hardcodes a hostname.

export const site = {
  name: "Edgerunner Ventures",
  nameZh: "锋行资本",
  tagline: "watt-to-bit capital.",
  url: "https://edgerunner.io",
  email: "rc@edgerunner.io",
};

// Product properties. Local ports in dev; subdomains in production via env.
export const properties = {
  cortex: process.env.NEXT_PUBLIC_CORTEX_URL ?? "http://localhost:3001",
  overclock: process.env.NEXT_PUBLIC_OVERCLOCK_URL ?? "http://localhost:3002",
  newsletter: "https://machineyearning.io",
};

// labelZh covers only this short nav chrome — see LangToggle's note on scope.
export const nav = [
  { label: "Home", labelZh: "首页", href: "/" },
  { label: "About", labelZh: "关于", href: "/about" },
  { label: "Portfolio", labelZh: "投资组合", href: "/portfolio" },
  { label: "Research", labelZh: "研究", href: "/research" },
  { label: "Machine Yearning", labelZh: "Machine Yearning", href: "/writing" },
] as const;

// Full list — About's own social row shows all of these.
export const socials = [
  { label: "x", url: "https://twitter.com/rydcunningham" },
  { label: "github", url: "https://github.com/rydcunningham" },
  { label: "linkedin", url: "https://linkedin.com/in/rydcunningham" },
  { label: "substack", url: properties.newsletter },
] as const;

// Footer shows a shorter row — github/substack are already reachable from
// nav (Machine Yearning) and the research pages, so the footer stays tighter.
export const footerSocials = socials.filter((s) => s.label === "x" || s.label === "linkedin");
