---
name: create-readme
description: >
  Create or revamp a project's README.md. Audits the codebase first, then drafts
  a README scaled to project size using a proven template. Use when the user asks
  to "create a README", "write a README", "revamp the README", "improve the
  README", or "make the README more appealing". Owns README authoring only —
  CLAUDE.md/AGENTS.md shape belongs to `review-agent-instructions`/`review-agent-instructions`,
  and repo-wide codebase doc reorganization belongs to `scaffold-agent-docs` (update mode).
---

# Create README

Last updated: 2026-08-04

**Announce at start:** "I'm using the create-readme skill to draft/revamp your README."

## Layer

Human layer of the context-management collection. Owner of `README.md` only.

The README addresses a human arriving with zero context; `AGENTS.md` addresses an agent that needs routing. They are different audiences, so do not merge them or duplicate one into the other — link instead. `review-agent-instructions` owns those files, and repo-wide reorganization belongs to `scaffold-agent-docs` (update mode).

## Role

You are a senior software engineer with extensive open-source experience. The READMEs you write are appealing, informative, and easy to read — for someone arriving with **zero prior context**.

## Goal

Produce (or revamp) a `README.md` that lets a stranger answer three questions in under a minute:

1. **What is this?** — one-sentence definition + why it exists
2. **How do I run it?** — prerequisites, install, first success
3. **Where do I go next?** — usage, structure, links

## Guiding Principle: The Five-Year Hiatus Test

Write for someone coming to the project with no prior knowledge — including yourself after a five-year hiatus. What would you need to get back up to speed? That belongs in the README. When in doubt about context (what abbreviations mean, why two similar files differ, what tooling is needed), err on the side of detail. Insufficient context is the #1 reason readers abandon a project.

---

## Workflow

### Phase 1 — Audit the project

You MUST review the project before writing a word:

- Manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, ...) → name, description, scripts, dependencies
- Entry points and directory layout → what the project actually does
- Existing `README.md` (revamp mode) → what to keep, what's stale, what's missing
- `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md` → what NOT to duplicate
- Logo or icon assets (`assets/`, `docs/`, `public/`) → use in the header if found
- CI config, badges-worthy facts (test coverage, package registry, versions)

### Phase 2 — Classify and scope

Pick a tier based on the project; do NOT pad a small project to look big:

| Tier | Project | Sections |
|---|---|---|
| **Minimal** | Script, small lib, internal tool | About, Getting Started, Usage |
| **Standard** | Typical app or library | + Built With, Project Structure, Roadmap-link, Contact |
| **Full** | Open-source project seeking contributors | + badges, logo, ToC, Contributing pointer, Acknowledgments |

Ask the user ONLY for facts you cannot derive from the repo (target audience, hosted demo URL, contact/social handles, license choice if no LICENSE file). Do not ask about anything discoverable in Phase 1.

### Phase 3 — Draft

Use `references/readme-template.md` as the structural blueprint (adapted from [Best-README-Template](https://github.com/othneildrew/Best-README-Template)). Trim sections that don't apply to the chosen tier; never leave placeholder text like `project_title` in the output.

Content rules — you MUST follow all of these:

- **Concise and to the point.** Do not overuse emojis. No marketing fluff.
- **Lead with why.** The About section states the problem the project solves before describing features.
- **Copy-pasteable Getting Started.** Every command must actually work in this repo — verify script names against the manifest, don't invent them.
- **Show, don't tell, in Usage.** Real code examples and real output beat prose. Screenshots/demos where they exist.
- **Explain the non-obvious.** File/folder overview for non-trivial layouts; a key for abbreviations, env vars, config values, and units a newcomer couldn't guess.
- **Do NOT inline** LICENSE, CONTRIBUTING, or CHANGELOG content — link to the dedicated files instead. One-line pointers only.
- **GFM formatting.** Use tables, task lists, and [GitHub admonitions](https://github.com/orgs/community/discussions/16925) (`> [!NOTE]`, `> [!WARNING]`) where appropriate.
- **Header polish** (Standard/Full tier): logo if one exists, shields.io badges only for facts that are true (build status, package version, license), back-to-top links on long READMEs.

### Phase 4 — Review before writing

Self-check the draft against this list; fix failures before presenting:

- [ ] A stranger can answer *what / how to run / where next* in under a minute
- [ ] Every command verified against the repo (scripts, paths, package names)
- [ ] No placeholder text, no dead links, no sections duplicating LICENSE/CONTRIBUTING/CHANGELOG
- [ ] Every acronym, env var, and config value a newcomer would meet is explained
- [ ] ToC anchors match headings (Full tier)
- [ ] Tone: informative, minimal emoji, no filler

**Revamp mode:** present a section-by-section diff summary (keep / rewrite / add / drop with one-line reasons) and get user confirmation before overwriting the existing README.

---

## Output

Write to `README.md` at the project root (or the path the user specifies). For revamps, apply only after the Phase 4 confirmation.

## Sources

- [awesome-copilot / create-readme](https://www.skills.sh/github/awesome-copilot/create-readme) — role, tone, and formatting rules
- [Dryad: What's in a README?](https://blog.datadryad.org/2025/09/09/whats-in-a-readme-why-your-readme-matters-and-how-to-create-the-best-one-possible/) — zero-context reader principle, five-year hiatus test, err-on-detail
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) — structural template (see `references/readme-template.md`)
