# Hosting Plan — Cortex + Overclock → edgerunner.io

> **Living document.** Any agent working on Cortex, Overclock, Kiroshi, Corpus,
> or the deployment pipeline should read this first and update task status as
> they go. Source of truth for the hosting workstream; supersedes the "instruments
> stay local" framing in `README.md` until §3 + §4 land, at which point the
> README itself gets rewritten.
>
> **Status legend:** `[ ]` pending · `[~]` in-progress (owner noted) · `[!]`
> blocked (see note) · `[x]` done.

## Locked decisions

| # | Decision | Rationale |
|---|---|---|
| D1 | **Kiroshi becomes its own repo** (separate from this monorepo) | The design sandbox at `~/edgeos/kiroshi` graduates to a real source-of-truth repo; `packages/tokens/kiroshi.css` and any future consumers import from it as a published package. |
| D2 | **Pre-build Cortex data on corpus change** (option b in §3) | Preserves Cortex's "no write path" contract; deploy builds stay deterministic and don't depend on `~/edgeos/engine` python agents at deploy time. |
| D3 | **Shared `@edgerunner/corpus-data` artifact package** (option A) | The §3.1 CI job already emits versioned JSON — wrapping it as a private package buys clean runtime decoupling, schema coordination via `@edgerunner/corpus-types`, and trivial local dev for Overclock and any future consumer. Outperforms runtime fetch (B) because Overclock's "interactive digital twins" want local data not network calls, and outperforms snapshots (C/C′) because drift is the default and C′ degenerates to A within a quarter anyway. |

## Open decisions

| # | Decision | Options |
|---|---|---|
| D4 | Initial hosting tier for Cortex/Overclock | invite-only (Vercel Password Protection) vs Phase-5 public freemium gate (`apps/cortex/docs/cortex.md` §11) |
| D5 | Cortex dev port | 3001 (root README) vs 4318 (Cortex README/CLAUDE.md). Pick one. |

---

## Stream 1 — Kiroshi graduates to its own repo

**Goal:** single source of truth for the design system, consumed identically by
edgerunner-web, Cortex, Overclock. Unblocks Cortex's `aleph-ii` migration and
Overclock's visual alignment.

- [x] **1.1** ~~Create `edgerunner/kiroshi` repo.~~ **Repo already exists at
  `github.com/rydcunningham/kiroshi` (private, 43 commits, last push
  2026-08-06).** The `~/edgeos/kiroshi` working tree is its checkout — it IS
  the canonical home. Namespace note: existing repos in this stack use
  `rydcunningham/*` (cortex, corpus, edgerunner), not `edgerunner/*`. The npm
  *scope* stays `@edgerunner/*` (matches existing workspace packages) — only
  the GitHub owner differs.
- [x] **1.2** Added `packages/kiroshi/` as a `workspace:*` package. No publish
  step — Kiroshi consumes the same pattern as `@edgerunner/tokens`/`brand`/
  `sim`: copy artifacts in from upstream `rydcunningham/kiroshi`, version them
  via this repo's git history. Package contents:
  `tokens.css` (verbatim from `v2/tokens.css`) · `shared/entity-views.mjs`
  (ESM wrapper around the upstream IIFE so it's `import`-able) ·
  `shared/reset.css` · `page-grammar/<surface>.css` (extracted from v2
  `<style>` blocks — deferred until Cortex un-gitignores, only tokens.css +
  shared have current consumers).
  - *Done (vigil, 2026-08-12):* package created. Upstream changes to
    `renderStructure` are now opt-in via `window.KIROSHI.pageFor` /
    `window.KIROSHI.navigate` (consumer-side navigation routing) — preserves
    the original `window.location` fallback for static consumers.
- [x] **1.3** ~~CI: version + publish on tag.~~ **Struck** — workspace
  packages don't publish. Versioning is git-history of this repo.
- [x] **1.4** Replaced `packages/tokens/kiroshi.css` with a re-export
  (`@import "@edgerunner/kiroshi/tokens.css";`). Added
  `@edgerunner/kiroshi` as a `workspace:*` dep of `packages/tokens` so the
  dependency graph is explicit. `pnpm build` verified: tokens land in the
  built CSS (3 `--k-bg` values for cyan/crimson/light, 3 `--k-accent` values
  for cyan/crimson/edgerunner-red). Existing `apps/web` import path
  unchanged.
- [ ] **1.5** In Cortex, swap the vendored `app/tokens.css` (`aleph-ii`
  branch) for the package import. **Happens in `~/edgeos/cortex`, not this
  repo** (Cortex is gitignored here until Stream 3.6). Finish the R1 phases
  from `apps/cortex/docs/refactor-r1.md` that depend on the token bridge.
- [ ] **1.6** ~~In `~/edgeos/kiroshi/` (local sandbox), add README notice…~~
  **Reframed.** `rydcunningham/kiroshi` stays the design sandbox (where the
  HTML files live as references and design iteration happens); this repo's
  `packages/kiroshi/` is the downstream consumer surface, synced by copy.
  No README notice needed upstream — the relationship is the same as
  `packages/tokens/kiroshi.css` has had for months.
- [x] **1.7** Verified `apps/web` builds against the new workspace package.
  (Cortex + Overclock verification happens when those land in Stream 3/4.)

## Stream 2 — Corpus → private repo, contract for downstream consumers

**Goal:** Cortex and engine read Corpus from a real repo URL, not
`${EDGEOS_DIR:-$HOME/edgeos}/corpus`. Wiki-link filename-uniqueness invariant
holds.

*Partially in flight in another session per operator — coordinate before
duplicating work.*

- [ ] **2.1** Confirm Corpus repo is `github.com/rydcunningham/cortex-corpus`
  (per `~/edgeos/AGENTS.md` §Version Control). Document access pattern for
  CI: deploy-token clone vs git submodule vs published tarball.
- [ ] **2.2** Audit every `${EDGEOS_DIR:-$HOME/edgeos}/corpus` reference in
  `apps/cortex/loader/*.mjs` and `apps/cortex/package.json`. Replace with
  `CORPUS_DIR` env, no implicit default in hosted build.
- [ ] **2.3** Publish `@edgerunner/corpus-types` (TS types mirroring corpus
  frontmatter 1:1, per `apps/cortex/README.md` §Principles). Both Cortex
  and Overclock depend on it for schema validation.
- [ ] **2.4** CI step on Corpus push: run schema validation, filename-uniqueness
  check (the `[[Foo 汉字]]` → filename-stem invariant), and trigger the
  downstream data-build (Stream 3 §3.1).

## Stream 3 — Cortex hostable + pre-build pipeline (decision D2)

**Goal:** `cortex.edgerunner.io` deploys from this repo without `~/edgeos`
present. Data artifacts are produced in CI on corpus change, not at deploy.

- [ ] **3.1** Stand up the **data-build pipeline**: CI workflow (GitHub
  Actions, separate from Vercel) that (a) clones Corpus, (b) clones engine,
  (c) runs the loader chain (`graph` · `datasets` · `value-chains` ·
  `leviathans` · `china-atlas` · `sim-catalog` · `sim-parity` · `reports` ·
  `usage` — see `apps/cortex/package.json` `data:build`), (d) publishes the
  resulting `data/*.json` as the private `@edgerunner/corpus-data` package
  (per D3) plus a Cortex-local artifact for the 22 MB `graph.json` (Cortex-only,
  not part of the shared package). This pipeline is the single producer;
  Cortex and Overclock are both consumers.
- [ ] **3.2** Decide private npm registry (depends on D6): GitHub Packages vs
  npm org vs Vercel private-package support. Document auth setup for both the
  CI publisher and the consumer builds (Cortex, Overclock). Choose a
  versioning scheme (semantic-release, or manual tags aligned with Corpus
  commits).
- [ ] **3.3** Resolve the 22 MB `graph.json` size question. It's Cortex-only
  (not in `@edgerunner/corpus-data`), but still ships with the Cortex deploy.
  Verify Vercel accepts it as a static asset; if it risks function/asset
  limits, split into per-section chunks loaded on demand.
- [ ] **3.4** Cortex build: remove `~/edgeos/engine` python (`uv`) dependency
  from the deploy build. The deploy only runs `next build`; all data is
  pre-built.
- [ ] **3.5** Promote Cortex to its own Vercel project: root `apps/cortex`,
  output `cortex.edgerunner.io`. Same pnpm workspace resolution as `apps/web`.
- [ ] **3.6** Un-gitelist `apps/cortex/` from `.gitignore` once 3.1–3.4 land
  and the build is reproducible without `~/edgeos`.
- [ ] **3.7** Decide D4 (invite-only vs public gate). If invite-only initially,
  apply Vercel Password Protection. If public, wire the one-filter publishable
  loader gate promised in `apps/cortex/README.md` §Roadmap Phase 5.
- [ ] **3.8** Reconcile dev port (D5): pick 3001 or 4318, update both
  `package.json` and `README.md`/`CLAUDE.md`.
- [ ] **3.9** Wire the three URL envs in Vercel project config:
  `NEXT_PUBLIC_CORTEX_URL` · `NEXT_PUBLIC_OVERCLOCK_URL` · `NEXT_PUBLIC_SITE_URL`.
  Add the same set to Cortex's env (currently only `apps/web` reads them).

## Stream 4 — Overclock hostable

**Goal:** `overclock.edgerunner.io` deploys from this repo without `~/edgeos`
or local-only `packages/sim`.

- [ ] **4.1** Audit `packages/sim/` (currently gitignored). Document what it
  contains, what Overclock actually imports from it, and whether it can be
  published as a workspace package or should be inlined into `apps/overclock`.
- [ ] **4.2** Add `@edgerunner/corpus-data` as a workspace dep of Overclock.
  Replace static `apps/overclock/data/{sim-catalog,leviathans,vendors}.json`
  with package imports. Verify shape matches what
  `apps/overclock/scripts/build-vendors.mjs` produces today — if the build
  script adds value beyond what the §3.1 pipeline emits, fold that logic into
  the data-build CI rather than keeping a second pipeline alive.
- [ ] **4.3** Promote Overclock to its own Vercel project: root
  `apps/overclock`, output `overclock.edgerunner.io`.
- [ ] **4.4** Un-gitelist `apps/overclock/` and `packages/sim/` from
  `.gitignore` once 4.1–4.2 land.
- [ ] **4.5** Apply the same auth/URL-env pattern as Cortex §3.7 + §3.9.

## Stream 5 — Seamless cross-app interaction

**Goal:** a user moving between CORTEX ⇄ OVERCLOCK ⇄ edgerunner.io loses no
context. URLs do the heavy lifting; chrome feels continuous.

- [ ] **5.1** Define the deep-link contract. Use the corpus filename-stem as
  the cross-app key (`overclock.edgerunner.io/sim/<slug>` ⇄
  `cortex.edgerunner.io/entity/<slug>#<view>`). Document in this file once
  agreed.
- [ ] **5.2** Share the nav primitive. Add a `@edgerunner/brand` component
  (or extend the existing rail) that renders the CORTEX ⇄ OVERCLOCK ⇄ SITE
  switcher consistently across all three apps. Kiroshi `.k-chrome` grammar.
- [ ] **5.3** Shared auth model (depends on D4). If invite-only: one IdP or
  Vercel IdP config across all three subdomains. Document session behavior
  (subdomain cookies, etc.).
- [ ] **5.4** Screenshot parity: same Kiroshi tokens render identically across
  the three apps in dark + light (Cortex light audit is
  `apps/cortex/docs/refactor-r1.md` Phase V open item).

## Stream 6 — Rewrite root README

**Goal:** the "instruments stay local" framing in `README.md` is obsolete once
§3 + §4 ship.

- [ ] **6.1** Update root `README.md` to reflect the three deployed properties.
- [ ] **6.2** Update `apps/cortex/README.md` to drop the `../corpus` sibling
  language and point at the data-build pipeline.
- [ ] **6.3** Remove the "instruments stay local" block from `.gitignore`
  once §3.6 and §4.5 land.

---

## Sequencing

```
Stream 1 (Kiroshi repo)   ─┐
                          ├─→ Stream 3 (Cortex hostable)  ─┐
Stream 2 (Corpus repo)    ─┘                                ├─→ Stream 5 (interaction)
                          ┌──→ Stream 4 (Overclock)        ─┘
                          └──→ Stream 6 (README)
```

Streams 1 and 2 are the leverage: 3, 4, and 5 all unblock on them. Stream 6 is
the last cleanup.

## Updating this file

- Check the box when a task completes. No ceremony.
- If you start a task, mark `[~]` and add your name/date inline:
  `[~] (vigil, 2026-08-12)`.
- If you're blocked, mark `[!]` and add a one-line note pointing at the
  blocker (file path, decision number, external dep).
- New decisions go in **Open decisions** with the options enumerated; promoted
  to **Locked decisions** when the operator calls it.
- Keep the wiki-link / filename-uniqueness convention from `~/edgeos/AGENTS.md`
  in mind for any cross-repo references.
