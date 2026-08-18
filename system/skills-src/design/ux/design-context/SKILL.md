---
name: design-context
description: "Establish the project's design context before any UX work. Detects or creates a DESIGN.md (Google's open format), imports brand specs from reference sites or template catalogs, resolves token authority, and writes docs/design/system.md — the single source of truth every downstream design skill reads. Entry point of the design/ux pipeline."
---

Last updated: 2026-08-17

# Design Context

Establish the design context every other UX skill depends on: a canonical `docs/design/system.md`, optionally backed by a `DESIGN.md` at the project root.

This skill makes the layer-⑤ ecosystem (Google's [DESIGN.md format](https://github.com/google-labs-code/design.md) and its tooling) executable inside the pipeline. It owns one question: **where do design tokens come from for this project?** See `design/ux/README.md` for the full external-tool catalog this skill dispatches to.

## When to Use

- Starting design work and no `docs/design/system.md` exists yet
- A `DESIGN.md` exists at the project root but nothing consumes it
- You have a reference site or brand ("make it look like Linear") and want it converted into project design tokens
- An existing system.md may have drifted from an updated DESIGN.md

Do NOT use when:

- `docs/design/system.md` exists and is current — downstream skills read it directly; re-run only to re-sync from a changed DESIGN.md
- You want to design user flows or screens — that's `/interaction-design`, which runs after this
- Only generating visual options on an existing structure — that's `/visual-design-variants`

## Inputs and Handoffs

**Upstream (all optional — skill decides from what exists):**
- `DESIGN.md` at project root (Google format, YAML frontmatter tokens + prose rationale)
- `docs/design/system.md` (existing system, possibly stale)
- `docs/product/<slug>/prd.md` Part 1 (persona, platform, product type)
- A user-supplied reference (site URL, brand name, screenshot) if offered in conversation

**Downstream:**
- `docs/design/system.md` (Human layer, git-tracked) → feeds `/interaction-design`, `/visual-design-variants`, `/design-implement`, and `spec`
- The `DESIGN.md` at root is **read, never written** by this skill — it is an input like the PRD. External lifecycle tools (e.g. Oh My Design) own its creation when the user chooses that path.

## Workflow

### Step 0: Detect Context State

```bash
# The three possible sources of design truth
[ -f DESIGN.md ] && echo "DESIGN_MD: found" || echo "DESIGN_MD: missing"
[ -f docs/design/system.md ] && echo "SYSTEM_MD: found" || echo "SYSTEM_MD: missing"
PRD_PATH=$(find docs/product -name "prd.md" -type f 2>/dev/null | head -1)
[ -n "$PRD_PATH" ] && echo "PRD: $PRD_PATH" || echo "PRD: missing"
```

Branch on the result:

| State | Route |
|---|---|
| DESIGN.md found | → Step 1 (adopt + merge) |
| No DESIGN.md, user has a reference site/brand | → Step 2 (extract or adopt ④) |
| No DESIGN.md, no reference | → Step 3 (create from scratch) |
| system.md found and no DESIGN.md and no new reference | Validate and STOP — nothing to do; report that downstream skills can proceed |

### Step 1: Adopt Existing DESIGN.md

1. Read the `DESIGN.md`. If a DESIGN.md linter or lifecycle skill is installed (layer ⑤, e.g. Oh My Design), run its validation; otherwise sanity-check manually: does it have YAML frontmatter with `colors` / `typography` / `spacing`, plus prose sections?
2. Extract the token set: colors, typography, spacing, radius, motion, principles.
3. If `docs/design/system.md` exists, diff the token values and surface every conflict.

**AskUserQuestion** when conflicts exist:

> DESIGN.md and docs/design/system.md disagree on these tokens:
> - [token]: DESIGN.md says [X], system.md says [Y]
>
> **A)** DESIGN.md wins for visual tokens; system.md keeps component foundations and rationale (Recommended)
> **B)** system.md wins — treat DESIGN.md as advisory only
> **C)** Review each conflict one by one

Default rule when the user has no preference: **DESIGN.md is authoritative for visual token values** (colors, fonts, spacing numbers, radii); **system.md remains authoritative for component foundations** (button variants, form patterns, card rules) and prose rationale.

→ Continue at Step 4.

### Step 2: Acquire a DESIGN.md from a Reference

The user has a reference — a site they like, a known brand, or a screenshot. Offer acquisition routes by what's installed (see `design/ux/README.md` layers ④⑤):

**Extraction (⑤) — reference URL → DESIGN.md:**
- Deterministic token extraction (e.g. BrandMD) → spec-valid DESIGN.md, best when the reference's CSS is the truth
- Vision-based extraction (e.g. DesignPull) → captures visual intent, imagery style, do/don't rules, best when the feel matters more than the hex codes
- Manual capture (e.g. TypeUI Chrome extension) → user drives, agent consumes the output

**Ready-made (④) — catalog → DESIGN.md:**
- Template catalogs (e.g. Awesome Design MD, Awesome Design Skills) ship DESIGN.md files for known products (Linear, Stripe, …) — find the closest brand, copy it in, adapt

**AskUserQuestion:**

> You referenced [site/brand]. How should I turn it into design context?
>
> **A)** Extract tokens from the live site (deterministic) — best fidelity to their CSS
> **B)** Extract visual intent (vision-based) — best fidelity to their feel
> **C)** Adopt a ready-made spec from a template catalog — fastest, if a close brand exists
> **D)** Skip acquisition — create from scratch instead (→ Step 3)

Run the chosen external skill (per its own install/invoke convention), then place the result at `DESIGN.md` in the project root and continue at Step 1 (adopt + merge).

If no extraction/adoption skill is installed: report which capability is missing, link the README catalog entry, and offer Step 3 as the fallback.

### Step 3: No Reference — Create from Scratch

**AskUserQuestion:**

> No DESIGN.md or reference to import. How should the design system be created?
>
> **A)** Run `/design-system-create` — consultative from-scratch creation, native to this repo (Recommended)
> **B)** Initialize a DESIGN.md lifecycle tool (layer ⑤, e.g. Oh My Design `omd:init`) — external skill owns DESIGN.md creation and persistence, then I merge it (requires that skill installed)
> **C)** Cancel — I'll provide a reference or DESIGN.md myself

If A: invoke `/design-system-create`. When it completes, its output `docs/design/system.md` IS this skill's output — skip to Step 5.
If B: run the external lifecycle skill, then continue at Step 1.

### Step 4: Write Canonical system.md

Merge the resolved tokens into the system.md structure (the full template lives in `/design-system-create` Step 5 — use the same sections: Aesthetic Direction, Typography, Color Palette, Spacing Scale, Layout, Border Radius, Component Foundations, Accessibility, References).

Merge rules:

- **Visual tokens** (colors, type, spacing, radius) ← from DESIGN.md (or adopted ④ spec), translated into the system.md token naming (`--surface-page`, `--text-primary`, `--accent`, …)
- **Component foundations** ← keep from existing system.md if present; otherwise write minimal defaults and mark them `<!-- TODO: refine on first component -->`
- **Rationale** ← pull the DESIGN.md prose principles into `## Aesthetic Direction`; note the source
- **Provenance** ← add a `## References` line: `Tokens imported from DESIGN.md (<source>, <date>)`

Validate before writing:

- All text/background pairs pass WCAG AA (4.5:1 normal, 3:1 large)
- One decisive accent color
- 2–3 surface levels only

Show the merged result, then **AskUserQuestion**:

> Merged design system ready. Conflicts resolved: [N]. Source: [DESIGN.md / catalog / extraction].
>
> **A)** Approve — write docs/design/system.md
> **B)** Adjust [specific token] first
> **C)** Discard — keep existing system.md unchanged

Write on approval:

```bash
mkdir -p docs/design
```

### Step 5: Summary and Handoff

Report:

- **Design context source:** [existing DESIGN.md / extracted from <url> / adopted from <catalog> / created from scratch via /design-system-create]
- **Canonical output:** `docs/design/system.md` (Human layer)
- **Token authority:** [DESIGN.md visual tokens + system.md component patterns | system.md only]
- **Unresolved conflicts:** [none / list]

**AskUserQuestion** for next step:

> Design context established.
>
> **A)** Run `/interaction-design` — define user flows and states on this system (Recommended for new features)
> **B)** Run `/visual-design-variants` — interaction structure already exists, go straight to visuals
> **C)** Done — I'll continue manually

## Memory Layer Classification

**Human layer (git-tracked, outlives effort):**
- `docs/design/system.md` — canonical design system, written or updated by this skill

**External input (git-tracked by project convention, owned elsewhere):**
- `DESIGN.md` at project root — read by this skill, written by external lifecycle tools or the user

**Working layer:** none — this skill produces no scratch artifacts. Extraction intermediates live wherever the external tool puts them.

Durability test: if the work root were deleted, would the project lose a fact it needs? system.md YES (Human layer). A downloaded template's intermediate files NO.

## Quality Gates

Before writing `docs/design/system.md`:

- [ ] Token source is recorded in `## References` (provenance is mandatory)
- [ ] Conflicts between DESIGN.md and existing system.md were surfaced, not silently overwritten
- [ ] WCAG AA contrast validated for all text/background pairs
- [ ] ONE decisive accent color; 2–3 surface levels
- [ ] DESIGN.md at root was NOT modified by this skill
- [ ] Component foundations present (from existing system.md or TODO-marked defaults)

## Integration Points

**Reads from:**
- `DESIGN.md` (project root, layer-⑤ format)
- `docs/design/system.md` (existing system, for merge/validation)
- `docs/product/<slug>/prd.md` Part 1 (product context when creating from scratch)

**Writes to:**
- `docs/design/system.md` (Human layer)

**Feeds:**
- `/interaction-design` (structure design reads system.md constraints)
- `/visual-design-variants` (variant generation applies system.md tokens)
- `/design-implement` (production code uses system.md tokens)
- `spec` (design constraints cited as input)

**External skills (optional):** layer ⑤ DESIGN.md lifecycle and extractors, layer ④ template catalogs — dispatched per `design/ux/README.md`. When none are installed, the from-scratch native path (`/design-system-create`) is the fallback and nothing is blocked.
