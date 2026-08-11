# edgerunner-web

The public site at **edgerunner.io** (`apps/web`) plus the two shared design
packages it builds on.

| Path | Port | Property | Palette |
|---|---|---|---|
| `apps/web` | 3000 | edgerunner.io | Edgerunner black/red (`data-colorway="edgerunner"`) |

> **Instruments are not in this repo.** Cortex (`cortex.edgerunner.io`) and
> Overclock (`overclock.edgerunner.io`) are invite-only desktop instruments and
> stay on the local workspace until they get their own deploy — see
> `.gitignore`. Cortex in particular cannot build here: `lib/graph.ts` imports a
> 22 MB `graph.json` generated from the local corpus, which is never committed.
> The site links out to both by URL only, so it builds and deploys without them.

newsletter.edgerunner.io → 301 → machineyearning.io (Vercel domain config, no app).

## Packages

- `packages/tokens` — the `--k-*` contract. `kiroshi.css` is the cyan instrument
  system verbatim (source of truth: `edgeos/kiroshi/v2/tokens.css`);
  `edgerunner.css` re-grounds the atmosphere for the site; `preset.cjs` bridges
  the vars into Tailwind utilities (alpha-capable via color-mix).
- `packages/brand` — glyph/rail as currentColor React components (red on the
  site, cyan on the instruments, one file), plus woff2 faces with plain
  `@font-face`.

## Run

```sh
npx pnpm install
npx pnpm dev
```

Cross-property links read env with localhost defaults:
`NEXT_PUBLIC_CORTEX_URL`, `NEXT_PUBLIC_OVERCLOCK_URL`, `NEXT_PUBLIC_SITE_URL`.
In production these point at the subdomains.

## Deploy

Vercel, **root directory `apps/web`** — this is a pnpm workspace, so the build
must resolve `@edgerunner/tokens` and `@edgerunner/brand` from the repo root.
`packageManager` in the root `package.json` pins pnpm via corepack.

Fonts are vendored (`packages/brand/fonts.css`) and Cortex-side faces use
`next/font/local`. Do not reintroduce `next/font/google` — the network fetch
fails builds on constrained connections and degrades silently in dev.

## Content

All site content is typed TS modules in `apps/web/lib/content/`:
`portfolio.ts` (18 companies), `research.ts` (Cortex + Overclock front doors),
`updates.ts`, `about.ts`, `posts.ts` (markdown archive in `content/writing/`).

`updates.ts` feeds two places from one array: the home page shows the newest
`HOME_LIMIT` (5) in the right-hand column, and `/updates` shows the full
archive. `/updates` is deliberately absent from the nav (`lib/site.ts`) —
it's reached from the "ALL →" link on the home feed.

Two-column pages (company + product) share their geometry from `lib/layout.ts`,
so the 60:40 split and gutter stay in step across both.

## Adding media previews

Company and product pages render a **Media rail** in the right column when the
content entry has a `media` array; without one the page falls back to a single
column. Drop files in `apps/web/public/media/<slug>/` and add entries:

```ts
media: [
  { kind: "image", src: "/media/positron/board.jpg", alt: "…", caption: "…" },
  { kind: "gif",   src: "/media/positron/demo.gif",  alt: "…" },
  { kind: "video", youtubeId: "…", title: "Founder deep dive" },
]
```

Videos are click-to-load facades — no third-party JS until played. GIFs bypass
the image optimizer automatically. `fit: "contain"` letterboxes art that
shouldn't be cropped; the default covers and anchors to the top, which is right
for UI screenshots.

Cortex/Overclock previews are real screenshots of the running instruments,
captured with headless Chrome and downscaled to 1400px JPEG:

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --window-size=1600,1000 --virtual-time-budget=6000 \
  --screenshot=out.png http://localhost:3001/
```
