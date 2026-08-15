# Frontend Design

Last updated: 2026-08-02

## Frontend Design Skills

| Skill                             | What it is                                                                                                                                                                  | How it works                                                                                                                                                                                                                                                                                                                                 | Best use                                                                                                                                                                                                                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Taste Skill**                   | An opinionated **AI art director / anti-slop skill**. Primarily for landing pages, portfolios and visual redesigns.                                                         | Reads the brief, declares a “Design Read,” then adjusts three dials: **variance, motion and density**. It contains detailed rules against common AI clichés and offers variants for minimalist, brutalist, premium, image-first and GPT/Codex workflows. ([GitHub][2])                                                                       | Strong visual personality and anti-slop rules. Best when an agent produces technically correct but **generic-looking websites**. The default v2 is experimental and explicitly not targeted at dashboards, tables or complex product workflows. ([GitHub][3])                    |
| **UI/UX Pro Max**                 | A **searchable UI/UX knowledge base and recommendation engine** covering many industries and technology stacks.                                                             | Uses a local Python search engine, BM25 ranking and JSON reasoning rules to search 84 styles, 192 palettes, 74 font pairs, 192 product types, UX rules, charts, icons and motion presets. It generates a design system and can persist a global `MASTER.md` plus page-level overrides. ([GitHub][4])                                         | Searchable styles, palettes and industry references. Best for **broad coverage and cross-stack guidance**, especially mobile, dashboards and unfamiliar industries. Less opinionated than Taste, less workflow-oriented than Impeccable.                                        |
| **Impeccable**                    | A **full frontend design operating system** for coding agents. Covers landing pages, dashboards, product UI, audits, polishing, responsive design and production hardening. | Initializes persistent `PRODUCT.md` and `DESIGN.md`; distinguishes **brand surfaces** from **product surfaces**; provides 23 commands such as `shape`, `craft`, `critique`, `audit`, `polish`, `harden` and `live`. It also has 46 deterministic detectors and editor hooks that catch design anti-patterns during code edits. ([GitHub][1]) | End-to-end design workflow, auditing and polishing. Best when you want a **repeatable design-development workflow**, not merely a better prompt. Strongest choice for serious projects and continuous iteration.                                                                 |
| **Frontend Design — Anthropic**   | A compact, official **design philosophy skill** that prevents generic AI interfaces.                                                                                        | Grounds design in the product’s subject matter, defines typography, palette, layout and one memorable “signature,” critiques the direction, then implements responsive code. It is framework-agnostic and relatively flexible. Philosophy: *understand the subject, develop a distinctive direction, critique it, then build.* ([GitHub][5]) | Lightweight, high-quality default. Good balance of creativity, reasoning and implementation without excessive process. Anthropic and Antigravity are the same philosophy at different strictness. Anthropic asks you to *understand → diverge → critique → build*; Antigravity asks you to *declare → score → satisfy rules → build*.                                                                                                                                             |
| **Frontend Design — Antigravity** | A larger, more prescriptive community reinterpretation of the same philosophy.                                                                                              | Requires a named aesthetic, a memorable differentiation anchor, design-system snapshot, accessibility checks and a **DFII score** covering impact, context fit, feasibility, performance and consistency risk. Philosophy: *declare the direction, score it, satisfy explicit rules, then build.* ([GitHub][6])                              | Strict creative gate before implementation. Best when agents produce inconsistent results and you want a **mandatory design preflight and checklist**.                                                                                                                        |

## Simple mental model

* **Taste Skill:** gives the agent **taste**.
* **UI/UX Pro Max:** gives it a **design reference library**.
* **Impeccable:** gives it a **design process, tools and quality-control loop**.
* **Frontend Design (Anthropic / Antigravity):** gives it a **design philosophy** — flexible or strict.

## Basic installation

```bash
# Impeccable
npx impeccable install
# Then inside the agent:
/impeccable init
```

```bash
# Taste Skill
npx skills add https://github.com/Leonxlnx/taste-skill \
  --skill design-taste-frontend
```

```bash
# UI/UX Pro Max
npm install -g ui-ux-pro-max-cli
uipro init --ai codex       # or claude, cursor, opencode, etc.
```

These are the repositories’ current recommended installation paths. ([GitHub][1])

## Recommendation

Use **Anthropic Frontend Design as the base**, **Impeccable as the workflow**, and **UI/UX Pro Max as reference material**. Use Taste or Antigravity only for visually expressive pages; do not activate both simultaneously because their overlapping aesthetic rules may conflict.

Avoid making all skills simultaneous authorities: their typography, icon, color and layout rules can conflict. One should govern; the others should advise.

[1]: https://github.com/pbakaus/impeccable "GitHub - pbakaus/impeccable: The design language that makes your AI harness better at design. · GitHub"
[2]: https://raw.githubusercontent.com/Leonxlnx/taste-skill/main/skills/taste-skill/SKILL.md "raw.githubusercontent.com"
[3]: https://github.com/leonxlnx/taste-skill "GitHub - Leonxlnx/taste-skill: Taste-Skill - gives your AI good taste. stops the AI from generating boring, generic slop · GitHub"
[4]: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill "GitHub - nextlevelbuilder/ui-ux-pro-max-skill: An AI SKILL that provide design intelligence for building professional UI/UX multiple platforms · GitHub"
[5]: https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md "skills/skills/frontend-design/SKILL.md at main · anthropics/skills · GitHub"
[6]: https://github.com/sickn33/antigravity-awesome-skills/blob/main/skills/frontend-design/SKILL.md?plain=1 "agentic-awesome-skills/skills/frontend-design/SKILL.md at main · sickn33/agentic-awesome-skills · GitHub"
