# @edgerunner/kiroshi

The Kiroshi v2 design system as a `workspace:*` package — the consumer surface
for `apps/web`, `apps/cortex`, and `apps/overclock`.

## Upstream

Source of truth: **`github.com/rydcunningham/kiroshi`** (private), checked out
at `~/edgeos/kiroshi`. That repo is the design sandbox where the HTML
references live (`v2/registry.html`, `v2/entity.html`, etc.) and where design
iteration happens. This package holds only the artifacts downstream apps
actually consume.

## Contents

| File | Upstream | Notes |
|---|---|---|
| `tokens.css` | `v2/tokens.css` | The `--k-*` contract — colorways, themes, fonts, the `.k-page` ground. 380 lines verbatim. |
| `shared/reset.css` | `shared/reset.css` | The single shared reset. 11 lines verbatim. |
| `shared/entity-views.mjs` | `shared/entity-views.js` | ESM wrapper of the `renderStructure` SVG renderer. Upstream is an IIFE that sets `window.KIROSHI_renderStructure`; this export is `import { renderStructure } from "@edgerunner/kiroshi/shared/entity-views"`. |

## Not yet synced (deferred)

`page-grammar/<surface>.css` — the `<style>` blocks from `v2/*.html` (registry,
entity, frontier, board, mxa, connectome, china-board, flow, geo, map, huawei).
These are Cortex-page-specific grammars; they'll be extracted into this package
when Cortex un-gitignores (HOSTING-PLAN §3.6) and the `aleph-ii` R1 refactor
(`apps/cortex/docs/refactor-r1.md` §0) starts landing.

## Sync

When the upstream design system changes:

```sh
cp ~/edgeos/kiroshi/v2/tokens.css packages/kiroshi/tokens.css
cp ~/edgeos/kiroshi/shared/reset.css packages/kiroshi/shared/reset.css
# entity-views.mjs is a hand-maintained ESM wrapper — port any meaningful
# changes to renderStructure() from shared/entity-views.js upstream.
```

This is the same sync model `packages/tokens/kiroshi.css` has used for months;
versioning is this repo's git history.

## Consumers

- `apps/web` — imports via `@edgerunner/tokens/kiroshi.css`, which re-exports
  this package's `tokens.css`. The `edgerunner.css` colorway layers on top.
- `apps/cortex` (future, currently gitignored) — will swap its vendored
  `app/tokens.css` for a direct `@edgerunner/kiroshi/tokens.css` import as part
  of the `aleph-ii` R1 refactor.
- `apps/overclock` — imports via `@edgerunner/tokens/kiroshi.css` today.
