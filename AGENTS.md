# edgerunner-web

The public site at **edgerunner.io** (`apps/web`) plus the shared design packages
it builds on. Cortex (`apps/cortex`) and Overclock (`apps/overclock`) live here
as gitignored siblings until they have their own deploys — see `README.md` and
`HOSTING-PLAN.md`.

This file is the canonical instructions file for agents working in this repo
(following the `AGENTS.md` convention used across the `rydcunningham/*` and
`~/edgeos/*` projects; `CLAUDE.md` would be a thin pointer for Claude Code if
added later).

## Version control

- Commits follow the prior-commit style in this repo: descriptive subject,
  multi-paragraph body explaining what + why. No Conventional Commit prefix.
- **No AI co-author trailers.** Do not add `Co-Authored-By:` lines for opencode,
  Claude, or any other AI tool. The commit author is the operator; the tool is
  not credited. This rule is enforced across the edgerunner and edgeos projects
  (see `~/edgeos/AGENTS.md` §Version Control for the workspace-wide statement).
  The historical `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>` trailer
  on commit `504ec66` is the last occurrence — abandoned 2026-08-12.
- Do not commit unless explicitly asked. Inspect `git status`, `git diff`, and
  `git log` first; stage only intended files.

## Working in this repo

- `HOSTING-PLAN.md` is the tracked checklist for the hosting workstream
  (Kiroshi package, Corpus repo, Cortex + Overclock hostable, cross-app
  interaction). Read it before touching anything in `packages/kiroshi` or
  the build pipeline; update task status (`[ ]` / `[~]` / `[!]` / `[x]`) as
  you go.
- `packages/kiroshi/README.md` documents the sync model from upstream
  `rydcunningham/kiroshi` (the design sandbox).
- Cortex and Overclock are gitignored. The canonical Cortex lives at
  `~/edgeos/cortex` (see its own `AGENTS.md`); changes to Cortex's Kiroshi
  migration happen there, not here.
