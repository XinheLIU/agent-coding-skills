---
name: design-context
description: "Establish or refresh this project's design authority — the root DESIGN.md that answers HOW the product looks. Adopt an existing DESIGN.md, import from a reference site or brand, fold in a legacy docs/design/system.md, or route to from-scratch creation. Run before any other UX skill; they all read DESIGN.md. Use when no design authority exists, when system.md needs migrating, or when DESIGN.md has drifted from its source."
---

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [design.authority_question]
  retrieves: [product.relevant_context, design.existing_authority]
  produces: [design.authority_decision]
  updates: [design.applicable_rules, design.accepted_decisions]
  invalidates: [design.token_dependents, verification.visual_evidence]
  handoff_to: [interaction_design, visual_design]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


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
- `DESIGN.md` at project root (Current State, git-tracked) — the canonical **how**; feeds `/interaction-design`, `/visual-design-variants`, `/design-implement`, `spec`, and the `:root` token block of `docs/design/prototype.html`
- When an external ⑤ tool owns the DESIGN.md lifecycle (accepted in `capabilities.md`), this skill routes writes through it and reconciles the result; the file is canonical either way.

## Workflow

### Step 0: Detect Context State

Use the coordinator-resolved product/spec and relevant records. Preserve canonical requirement/criterion IDs and distinguish observed behavior from accepted intent.

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

**Ask through the coordinator** when conflicts exist:

> DESIGN.md and the legacy docs/design/system.md disagree on these tokens:
> - [token]: DESIGN.md says [X], system.md says [Y]
>
> **A)** DESIGN.md wins for visual tokens; keep system.md's component foundations and rationale in the merged prose (Recommended)
> **B)** system.md wins — its values overwrite the DESIGN.md frontmatter
> **C)** Review each conflict one by one

Default rule when the user has no preference: **existing DESIGN.md frontmatter is authoritative for visual token values** (colors, fonts, spacing numbers, radii); **legacy system.md content survives as prose** (component foundations, aesthetic rationale) inside the merged DESIGN.md.

→ Continue at Step 4.

### Step 2: Acquire Design Authority from a Reference

Request optional ④ templates or ⑤ design-context results through the coordinator. Preserve DESIGN.md authority and reconcile provenance/tokens before acceptance. Native adoption/extraction/creation remains available.

**the coordinator’s question interface:**

> You referenced [site/brand]. How should I turn it into design context?
>
> **A)** Extract exact tokens from the live site — best fidelity to their CSS
> **B)** Extract visual intent from the rendered design — best fidelity to their feel
> **C)** Adopt a published spec for a close brand — fastest, when one exists
> **D)** Skip the import — create from scratch instead (→ Step 3)

Carry out the chosen method, draft the result as `DESIGN.md` content, and continue at Step 1 (adopt + merge with anything already present). Use a capability recorded in `capabilities.md` for the chosen method only when the user accepted it; otherwise do the extraction directly from the fetched page. When neither is possible, say so and offer Step 3.

### Step 3: No Reference — Create from Scratch

**the coordinator’s question interface:**

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

Show the merged result, then **Ask through the coordinator**:

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
- **Canonical output:** `DESIGN.md` at project root (Current State) — the triad's **how**
- **Legacy migration:** [system.md folded in and pointered / none present]
- **Prototype token sync:** [re-synced / no prototype yet]
- **Unresolved conflicts:** [none / list]

**Ask through the coordinator** for next step:

> Design authority established.
>
> **A)** Run `/interaction-design` — define structure and states in the canonical prototype (Recommended for new features)
> **B)** Run `/visual-design-variants` — structure already locked, go straight to visuals
> **C)** Done — I'll continue manually

## Accepted decision handoff

At acceptance, retain consequential decision IDs, rationale, alternatives, affected surfaces/criteria, and consumed requirement/token/contract revisions beside the accepted design or in linked Change Context, following [the Design contract](references/design-memory.md). Do not wait for component documentation. Draft notes and rejected variant files may remain in Run Context after this reconciliation. Return accepted references, delta, unresolved questions/blocking effects, and next action to the coordinator.

## Shared Memory Contract

Full contract: [references/design-memory.md](references/design-memory.md).


Use coordinator-supplied paths and the active change identity; do not repeat path discovery.

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
- `DESIGN.md` at project root (Current State)
- `docs/design/prototype.html` `:root` token block (sync only)

**Feeds:**
- `/interaction-design` (reads DESIGN.md constraints)
- `/visual-design-variants` (applies DESIGN.md tokens)
- `/design-implement` (production code uses DESIGN.md tokens)
- `spec` (design constraints cited as input)

**When no import tool is available:** the from-scratch path (`/design-system-create`) is the fallback and nothing is blocked.
