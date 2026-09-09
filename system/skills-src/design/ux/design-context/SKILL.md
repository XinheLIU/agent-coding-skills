---
name: design-context
description: "Establish or refresh this project's design authority — the root DESIGN.md that answers HOW the product looks. Adopt an existing DESIGN.md, import from a reference site or brand, fold in a legacy docs/design/system.md, or route to from-scratch creation. Run before any other UX skill; they all read DESIGN.md. Use when no design authority exists, when system.md needs migrating, or when DESIGN.md has drifted from its source."
---

Last updated: 2026-09-09

# Design Context

Establish the design authority every other UX skill depends on: a canonical `DESIGN.md` at the project root.

Shared design understanding is a triad — `product.html` is **why**, `DESIGN.md` is **how**, `docs/design/prototype.html` is **what** ([references/design-memory.md](references/design-memory.md)). This skill owns the **how**. It resolves design authority from whatever exists — a `DESIGN.md` already at the root, a reference site or brand, a legacy `docs/design/system.md`, or nothing — and leaves one canonical `DESIGN.md` behind. It does not design; it decides authority.

## When to Use

- Starting design work and no `DESIGN.md` exists at the project root
- A legacy `docs/design/system.md` exists and has not been folded into `DESIGN.md`
- You have a reference site or brand ("make it look like X") and want it converted into design authority
- An existing DESIGN.md may have drifted from its source, or an external ⑤ tool updated it and the prototype's tokens need re-syncing

Do NOT use when:

- `DESIGN.md` exists and is current — downstream skills read it directly; re-run only to re-sync or migrate
- You want to design user flows or screens — that's `/interaction-design`, which runs after this
- Only generating visual options on an existing structure — that's `/visual-design-variants`

## Inputs and Handoffs

**Upstream (all optional — skill decides from what exists):**
- `DESIGN.md` at project root (YAML frontmatter tokens + prose rationale)
- `docs/design/system.md` (legacy token source, if never migrated)
- the configured product document (`product.html#prd`, or a canonical legacy PRD) — the **why**: persona, platform, product type
- A user-supplied reference (site URL, brand name, screenshot) if offered in conversation

**Downstream:**
- `DESIGN.md` at project root (Human layer, git-tracked) — the canonical **how**; feeds `/interaction-design`, `/visual-design-variants`, `/design-implement`, `spec`, and the `:root` token block of `docs/design/prototype.html`
- When an external ⑤ tool owns the DESIGN.md lifecycle (accepted in `capabilities.md`), this skill routes writes through it and reconciles the result; the file is canonical either way.

## Workflow

### Step 0: Detect Context State

Resolve the product document from explicit user paths, `docs/agents/memory.md`, and active `state.md`. New product memory uses `product.html#prd`; follow its persona, capability, scope, and question links. Legacy `prd.md` remains readable when canonical. Do not pick the first file found across products. Read HTML source records directly, preserving evidence/commitment distinctions. When no product document exists at all, the why can be inferred from the repo via `map-current-product`; offer it before designing against guesses.

```bash
# The possible sources of design truth
[ -f DESIGN.md ] && echo "DESIGN_MD: found" || echo "DESIGN_MD: missing"
[ -f docs/design/system.md ] && echo "LEGACY_SYSTEM_MD: found" || echo "LEGACY_SYSTEM_MD: missing"
[ -f docs/design/prototype.html ] && echo "PROTOTYPE: found" || echo "PROTOTYPE: missing"
```

Branch on the result:

| State | Route |
|---|---|
| DESIGN.md found, current, no legacy system.md | Validate and STOP — report that downstream skills can proceed; re-sync the prototype token block if stale (Step 4) |
| DESIGN.md found, legacy system.md also present | → Step 1 (adopt + fold the legacy file in) |
| No DESIGN.md, legacy system.md present | → Step 1 (migrate: system.md content becomes the DESIGN.md draft) |
| No DESIGN.md, user has a reference site/brand | → Step 2 (import from the reference) |
| No DESIGN.md, no legacy file, no reference | → Step 3 (create from scratch) |

### Step 1: Adopt, Migrate, and Merge

1. Read whichever authority files exist. A `DESIGN.md` carries YAML frontmatter with `colors` / `typography` / `spacing`, plus prose sections; a legacy `system.md` carries the same facts in Markdown sections. If the project has a validator for the format, run it.
2. Extract the token set from each: colors, typography, spacing, radius, motion, principles, component foundations.
3. Diff the token values across sources and surface every conflict.

**AskUserQuestion** when conflicts exist:

> DESIGN.md and the legacy docs/design/system.md disagree on these tokens:
> - [token]: DESIGN.md says [X], system.md says [Y]
>
> **A)** DESIGN.md wins for visual tokens; keep system.md's component foundations and rationale in the merged prose (Recommended)
> **B)** system.md wins — its values overwrite the DESIGN.md frontmatter
> **C)** Review each conflict one by one

Default rule when the user has no preference: **existing DESIGN.md frontmatter is authoritative for visual token values** (colors, fonts, spacing numbers, radii); **legacy system.md content survives as prose** (component foundations, aesthetic rationale) inside the merged DESIGN.md.

→ Continue at Step 4.

### Step 2: Acquire Design Authority from a Reference

Read `<work-root>/<effort>/design/capabilities.md`. If it carries `④ templates` and `⑤ design context` rows, follow their decisions. Otherwise scan the skills available in this session for either:

- **④ templates** — a skill that ships finished design systems or brand specs to adopt wholesale. It carries no process and makes no judgment.
- **⑤ design context** — a skill that creates, extracts, or maintains a root `DESIGN.md` as a durable file across sessions.

Append one row per slot recording what was found, or `none`. Rows are `| slot | found or none | decision | this skill |`; create the file with that header when absent. A found capability is named with what it would change and offered against the native path below; it is never used without asking.

The user has a reference — a site they like, a known brand, or a screenshot. Three ways to turn it into a `DESIGN.md`, differing in what they are faithful to:

| Method | Faithful to | Best when |
|---|---|---|
| Read the live site's CSS | Their exact token values | The reference's stylesheet is the truth you want |
| Read the rendered design | Their visual intent — imagery, density, do/don't rules | The feel matters more than the hex codes |
| Adopt a published spec | Whatever the spec's author captured | A close-enough brand already has one written |

**AskUserQuestion:**

> You referenced [site/brand]. How should I turn it into design context?
>
> **A)** Extract exact tokens from the live site — best fidelity to their CSS
> **B)** Extract visual intent from the rendered design — best fidelity to their feel
> **C)** Adopt a published spec for a close brand — fastest, when one exists
> **D)** Skip the import — create from scratch instead (→ Step 3)

Carry out the chosen method, draft the result as `DESIGN.md` content, and continue at Step 1 (adopt + merge with anything already present). Use a capability recorded in `capabilities.md` for the chosen method only when the user accepted it; otherwise do the extraction directly from the fetched page. When neither is possible, say so and offer Step 3.

### Step 3: No Reference — Create from Scratch

**AskUserQuestion:**

> No DESIGN.md or reference to import. How should design authority be created?
>
> **A)** Run `/design-system-create` — consultative from-scratch creation, native to this repo (Recommended)
> **B)** Initialize a root `DESIGN.md` with the `⑤ design context` capability recorded in `capabilities.md`, when one was found — it owns the file, this skill reconciles the result
> **C)** Cancel — I'll provide a reference or DESIGN.md myself

If A: invoke `/design-system-create`. When it completes, its output `DESIGN.md` IS this skill's output — skip to Step 5.
If B: run that tool, then continue at Step 1.

### Step 4: Write Canonical DESIGN.md

Merge the resolved authority into the DESIGN.md shape: YAML frontmatter carrying the machine-readable tokens, prose carrying the judgment (the full section template lives in `/design-system-create` Step 5 — Aesthetic Direction, Typography, Color Palette, Spacing Scale, Layout, Border Radius, Component Foundations, Accessibility, References).

Merge rules:

- **Frontmatter tokens** (colors, type, spacing, radius, motion) ← the winning source per Step 1, in the shared token naming (`--surface-page`, `--text-primary`, `--accent`, …)
- **Component foundations** ← keep from existing prose if present; otherwise write minimal defaults and mark them `<!-- TODO: refine on first component -->`
- **Rationale** ← keep or write `## Aesthetic Direction` prose; note the source
- **Provenance** ← a `## References` line: `Tokens from <source>, <date>` (mandatory)

Validate before writing:

- All text/background pairs pass WCAG AA (4.5:1 normal, 3:1 large)
- One decisive accent color
- 2–3 surface levels only

Show the merged result, then **AskUserQuestion**:

> Merged design authority ready. Conflicts resolved: [N]. Source: [existing DESIGN.md / legacy system.md / extraction / catalog].
>
> **A)** Approve — write DESIGN.md at the project root
> **B)** Adjust [specific token] first
> **C)** Discard — keep the existing files unchanged

Write on approval. When an accepted ⑤ tool owns the DESIGN.md lifecycle, route the write through it and verify the result matches the approved merge. Then:

1. **Retire the legacy file.** If `docs/design/system.md` was folded in, replace its body with a one-line pointer: `Superseded by /DESIGN.md (<date>). Kept for link stability.` Do not delete it; downstream links may still resolve through it.
2. **Re-sync the prototype.** If `docs/design/prototype.html` exists, regenerate its `:root` token block from the new frontmatter and update the provenance comment. Report any styled section whose rendered values no longer match — that is drift to fix through the pipeline, not silently.

### Step 5: Summary and Handoff

Report:

- **Design authority source:** [existing DESIGN.md / migrated from system.md / extracted from <url> / adopted from <catalog> / created via /design-system-create]
- **Canonical output:** `DESIGN.md` at project root (Human layer) — the triad's **how**
- **Legacy migration:** [system.md folded in and pointered / none present]
- **Prototype token sync:** [re-synced / no prototype yet]
- **Unresolved conflicts:** [none / list]

**AskUserQuestion** for next step:

> Design authority established.
>
> **A)** Run `/interaction-design` — define structure and states in the canonical prototype (Recommended for new features)
> **B)** Run `/visual-design-variants` — structure already locked, go straight to visuals
> **C)** Done — I'll continue manually

## Shared Memory Contract

Full contract: [references/design-memory.md](references/design-memory.md).

```text
Triad role:  HOW — this skill owns the canonical DESIGN.md at the project root
Layer:       human — design authority outlives the effort
Owns:        DESIGN.md (directly, or reconciled through an accepted ⑤ lifecycle tool)
Maintains:   the :root token block of docs/design/prototype.html (sync only, never sections)
Retires:     docs/design/system.md — folded into DESIGN.md, left as a pointer
Contributes: <work-root>/<effort>/design/capabilities.md — the `④ templates` and `⑤ design context` rows only
Coordinates: state.md — records the authority source and the next design stage
Promotes:    a contested token-authority decision → an ADR, via domain-modeling
```

Resolve the work root and the active effort from `docs/agents/memory.md`, defaulting to `.scratch/` when nothing is configured. The only working artifact this skill writes is its two rows in `capabilities.md`; extraction intermediates stay wherever the tool that produced them put them.

Durability test: if the work root were deleted, would the project lose a fact it still needs? `DESIGN.md` yes — it is the only record of which tokens won and why. A downloaded template's intermediates no.

Which design authority won is a decision someone would otherwise re-litigate, so it promotes. Record provenance in `## References` on the way through (Step 4), and when the choice was contested — an imported brand overriding a hand-built system, say — route the rationale to an ADR rather than leaving it in the conversation.

## Quality Gates

Before writing `DESIGN.md`:

- [ ] Token source is recorded in `## References` (provenance is mandatory)
- [ ] Conflicts between sources were surfaced, not silently overwritten
- [ ] WCAG AA contrast validated for all text/background pairs
- [ ] ONE decisive accent color; 2–3 surface levels
- [ ] Frontmatter tokens and prose sections both present (tokens without rationale is half an authority)
- [ ] Legacy `system.md`, if present, was folded in and pointered — not left as a second authority
- [ ] Prototype `:root` block re-synced when a prototype exists

## Integration Points

**Reads from:**
- `DESIGN.md` (project root, when present)
- `docs/design/system.md` (legacy, for migration)
- the configured product document — the why (product context when creating from scratch)

**Writes to:**
- `DESIGN.md` at project root (Human layer)
- `docs/design/prototype.html` `:root` token block (sync only)

**Feeds:**
- `/interaction-design` (reads DESIGN.md constraints)
- `/visual-design-variants` (applies DESIGN.md tokens)
- `/design-implement` (production code uses DESIGN.md tokens)
- `spec` (design constraints cited as input)

**When no import tool is available:** the from-scratch path (`/design-system-create`) is the fallback and nothing is blocked.
