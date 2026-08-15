# Agent Instructions

Last updated: 2026-08-04

## Repository boundary

- `system/` is the product being designed and maintained in this repository.
- `references/` is an optional local corpus of copied upstream skills. It is intentionally gitignored and may not exist in every clone.

## Local reference workspace

When comparing, evaluating, or adapting external skills, explicitly inspect `references/` through the filesystem. Do not rely on `git status`, `git ls-files`, or repository history to reveal it. Read `references/README.md` first when present.

Treat `references/` as read-only source material:

- Never stage, force-add, commit, or distribute anything under `references/`.
- Keep the root-anchored `/references/` rule in `.gitignore`.
- Do not edit a copied skill to implement the system.
- Extract the useful principle, then implement and document the adapted design under `system/`.
- Preserve provenance when a reference influences a system decision.

## Shared frontend

The public catalog frontend is owned by the sibling `../agent-skills` repository. This repository publishes only `catalog/skill-set.json`; do not recreate or maintain a separate frontend here.

When the user asks to launch, run, open, preview, or test the frontend locally from this repository:

1. Run `node scripts/build-catalog.mjs --local` in `../agent-skills`.
2. Start `python3 -m http.server 4174 -d docs` in `../agent-skills`. If port `4174` is occupied, choose the next available port without terminating an unknown process.
3. Verify the local catalog loads, then give the user the exact `http://127.0.0.1:<port>/` URL and keep the server running.
