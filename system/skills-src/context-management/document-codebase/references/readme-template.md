# README Authoring Playbook

Last updated: 2026-08-02

The root `README.md` is the **face of the project** — the first and often only doc a visitor reads. It decides whether they try the project or close the tab. Treat it as a product surface, not a dumping ground.

This playbook governs **root** READMEs. Sub-package READMEs inherit the principles but can skip badges, screenshots, and governance sections.

## Seven guiding principles

Every section below must earn its place against these seven rules. If a section doesn't serve one of them, cut it.

### 1. Value First, Upfront

Lead with a **1-sentence pitch** immediately under the title. It must answer, in that single sentence:

- **What** the project is (noun).
- **Who** it is for (audience).
- **What pain** it removes (problem).
- **What makes it different** (differentiator).

Bad: *"A powerful, modern, flexible Python toolkit for data analysis."*
Good: *"A local-only CLI that turns raw bank CSVs into reconciled, double-entry ledgers for solo freelancers who don't want to hand their finances to a SaaS."*

No marketing adjectives ("powerful", "blazing-fast", "revolutionary"). No self-referential fluff ("the best project for…"). State facts.

### 2. Instant Credibility & Context

Below the pitch, place two credibility elements:

- **Badge row** — at-a-glance health: build status, latest version, license, downloads, test coverage. Use [shields.io](https://shields.io/). Cap at 4–6 badges; more becomes noise.
- **Visual proof** — a screenshot, terminal recording, or short GIF (≤10 s, ≤2 MB) showing the tool *actually working*. A GIF of the happy path is worth ten paragraphs. Host in `docs/assets/` or `.github/assets/`.

If the project has no UI and no interesting CLI output, substitute a minimal code example that produces a surprising result in five lines.

### 3. Frictionless Onboarding

Quick Start must get a first-time user to a **working result in 3 steps or fewer**. Every command must be:

- **Copy-pasteable** — no `<your-path-here>` placeholders mid-command; put placeholders in a variable at the top.
- **Verified** — you ran it yourself, from a clean checkout, within the last release cycle.
- **Terminated by a success signal** — one concrete line the user can compare against (`curl localhost:8000/health → {"ok": true}`).

Prerequisites are a bulleted list with exact version floors and a one-line `--version` check per tool. If the stack is exotic (non-standard Python version, uncommon DB), explain the *why* in one sentence.

### 4. Layered, Scannable Structure

A reader scans before they read. Structure must support three personas simultaneously:

- **Evaluator** — can they decide in 30 seconds? Pitch + badges + screenshot + features.
- **New user** — can they run it in 5 minutes? Quick Start + minimal example.
- **Contributor / power user** — can they find deep docs? Links to `docs/architecture/`, `docs/API.md`, `CONTRIBUTING.md`, roadmap.

Enforcement:

- Use `##` for top-level sections; no deeper than `###` in the README itself.
- Include a Table of Contents **only** if the README exceeds ~400 lines. Shorter READMEs navigate fine via the GitHub outline pane.
- Order matters: value → proof → run → learn → contribute → legal. Never make a contributor scroll past licensing to reach install steps.

### 5. Concise, Benefit-Driven Features

List **3–6** features. Not 12. Each bullet must be written from the *user's* perspective:

- Bad: *"Uses asyncio for concurrent HTTP requests."*
- Good: *"Fetches 100 URLs in parallel — drops batch sync time from 40 s to 2 s."*

If you cannot phrase a feature as a user outcome, it's an implementation detail — move it to `docs/architecture/`.

### 6. Guaranteed Reproducibility

Every snippet in the README is a **contract**. If it breaks, you have lied to the reader and lost them.

Rules:

- All commands run from a clean clone on a supported OS/version combination at release time.
- State the exact environment: `Tested on macOS 14.4 / Ubuntu 22.04, Python 3.11.8, uv 0.4.x`.
- Call out known pitfalls inline: *"On Windows, replace `source .venv/bin/activate` with `.venv\\Scripts\\activate`."*
- Pin versions in install examples when drift would break reproducibility (`uv add "fastapi==0.110.*"` when semver-majoring matters).

When in doubt: re-run the Quick Start section on a fresh VM before every release.

### 7. Clear Governance & Navigation

End with a navigation block that answers "where do I go next?". Include:

- **License** — SPDX identifier + one-line scope (`MIT — do what you want, keep the notice`). Link to `LICENSE`.
- **Contributing** — link to `CONTRIBUTING.md` or equivalent. If the project isn't accepting contributions, say so explicitly.
- **Roadmap** — link to `ROADMAP.md`, a GitHub Project, or a milestones view. If none exists, a three-bullet "Next up" list suffices.
- **Community** — Discord/Slack/Discussions link, or "Open an issue" if no community exists.
- **Full docs** — link to `docs/` index, hosted site, or API reference.
- **Contact / maintainer** — one name or handle, one channel.

Do not end the README with installation troubleshooting. End it with where to go next.

## Canonical section order

```
# Project Name
<1-sentence pitch, italicized>
<badge row>
<screenshot / demo GIF>

## About
<2–4 sentence expansion of the pitch: problem, solution, non-goals>
### Built With
<tech stack badges or bullet list>

## Quick Start
### Prerequisites
### Installation   ← 3 steps or fewer
### Verify         ← concrete success signal

## Usage
<minimal working example, then link to more>

## Features
<3–6 benefit-driven bullets>

## Documentation
<links to docs/architecture/, docs/API.md, etc.>

## Roadmap
<3–5 bullets or link to ROADMAP.md>

## Contributing
<link to CONTRIBUTING.md + 2-sentence summary>

## License
<SPDX + one line + link>

## Contact
<maintainer handle + channel>

## Acknowledgments
<optional; third-party credits, inspirations>
```

Omit any section the project doesn't need (e.g., no Acknowledgments for an internal repo, no Contributing for a solo project). Do **not** reorder — the order enforces principle 4.

## Annotated skeleton

The fill-in template lives at `assets/templates/README.template.md`. Use it as the starting point in Phase 3; this playbook is the *why* behind each section.

## Badges — reference set

Pick 3–6 from this set. Order: build → version → license → downloads → coverage → chat.

| Badge | Source | Notes |
|-------|--------|-------|
| Build status | GitHub Actions, CircleCI | Link to the workflow run, not a static image |
| Version | shields.io PyPI/npm/crates | Auto-updates from registry |
| License | shields.io license | Matches `LICENSE` file |
| Downloads | shields.io PyPI/npm | Monthly, not total |
| Coverage | Codecov, Coveralls | Only if CI actually runs coverage |
| Chat | Discord, Slack invite | Only if the channel is staffed |

Avoid: "Made with ❤️", "PRs welcome" (put in `CONTRIBUTING.md`), rainbow stacks of irrelevant tech badges.

## Screenshot / demo GIF guidance

- **Format**: GIF for motion, PNG/WebP for static. APNG and MP4 don't render reliably in GitHub previews.
- **Size**: ≤2 MB. Compress with `gifsicle -O3` or `ffmpeg`.
- **Content**: the happy path only. Show input → result, 5–10 seconds, no cursor wandering.
- **Location**: `docs/assets/` (or `.github/assets/` if you want them out of documentation search).
- **Accessibility**: every image needs descriptive alt text. `![demo](…)` is not enough.

For CLI tools, `asciinema` + [`agg`](https://github.com/asciinema/agg) produces small, crisp GIFs. For web UIs, [`peek`](https://github.com/phw/peek) or [`LICEcap`](https://www.cockos.com/licecap/) work well.

## Anti-patterns

| Anti-pattern | Why it fails | Do instead |
|---|---|---|
| Burying install under a 2-screen intro | Breaks principle 3; evaluators leave | Move pitch+screenshot above; install is next |
| "This project is the best…" | No credibility; adjectives aren't evidence | State the differentiator as a fact |
| 15 badges across 2 rows | Visual noise; hides the real signal | Cap at 4–6 |
| ASCII-art banner taking 20 lines | Steals vertical space above the fold | Use a small logo (≤200px) or none |
| Copy-paste of `--help` output | Duplicates code; rots instantly | Link to `docs/CLI.md` or regenerate via CI |
| Full API reference inline | Makes the README a book | Link to `docs/API.md` |
| "TODO: document this" left in | Signals abandonment | Either write it or cut the section |
| Screenshot of an IDE, not the tool | Shows your setup, not your product | Screenshot the tool's own output |

## Validation checklist

Before committing a README, every item must be true:

- [ ] `Last updated: YYYY-MM-DD` present directly under the `#` title.
- [ ] Pitch fits on one line, names audience + pain + differentiator, no marketing adjectives.
- [ ] 3–6 badges, all resolve, all link to something useful.
- [ ] Screenshot or demo GIF present (or a 5-line code example if there's no visual surface).
- [ ] Quick Start reaches a working result in ≤3 steps.
- [ ] Every command copy-pastes without editing and was run from a clean checkout.
- [ ] Success signal stated concretely after the install steps.
- [ ] 3–6 features, each written as a user benefit.
- [ ] Links to `docs/`, `CONTRIBUTING.md`, `LICENSE`, roadmap all resolve.
- [ ] No duplicated content already present in `docs/`, `AGENTS.md`, or `CONTRIBUTING.md` — links, not repetition.
- [ ] License section names the SPDX identifier and scope in one line.
- [ ] README length: evaluator can scan in under 60 seconds (target ≤250 lines; hard cap ≤400).

If any item fails, fix it before proposing the README as complete.
