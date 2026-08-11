// Tailwind preset bridging the --k-* token contract into utilities
// (bg-k-bg, border-k-line, text-k-dim, font-display…). Values resolve
// per-property at runtime via the colorway on <html>, so the same
// component classes render red on the site and cyan on cortex/overclock.
//
// Colors are FUNCTIONS so Tailwind opacity modifiers (text-k-accent/50)
// compose against runtime var() colors via color-mix — plain string values
// would make Tailwind silently drop any class with a modifier.
const k = (name) => (params) => {
  const o = params && params.opacityValue;
  if (o === undefined || o === null || o === "1" || o === 1) return `var(${name})`;
  return `color-mix(in srgb, var(${name}) calc(${o} * 100%), transparent)`;
};

module.exports = {
  theme: {
    extend: {
      colors: {
        "k-bg": k("--k-bg"),
        "k-panel": k("--k-bg-panel"),
        "k-raise": k("--k-bg-raise"),
        "k-sel": k("--k-bg-sel"),
        "k-line": k("--k-line"),
        "k-line-strong": k("--k-line-strong"),
        "k-tick": k("--k-tick"),
        "k-text": k("--k-text"),
        "k-dim": k("--k-dim"),
        "k-faint": k("--k-faint"),
        "k-accent": k("--k-accent"),
        "k-sunken": k("--k-sunken"),
        "k-edge": k("--k-edge"),
        "k-good": k("--k-good"),
        "k-warn": k("--k-warn"),
        "k-bad": k("--k-bad"),
        "k-up": k("--k-up"),
        "k-down": k("--k-down"),
      },
      fontFamily: {
        display: ["Rajdhani", "Noto Sans SC", "sans-serif"],
        text: ["Source Sans 3", "Noto Sans SC", "sans-serif"],
        mono: ["JetBrains Mono", "Noto Sans SC", "monospace"],
        rajdhani: ["Rajdhani", "sans-serif"],
      },
    },
  },
};
