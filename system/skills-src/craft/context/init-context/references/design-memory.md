# Design Memory Contract

Last updated: 2026-09-09

Design skills contribute to one shared design understanding. A skill owns its reasoning method, not the understanding itself. Read this contract before reading or updating design memory. It also applies when a skill runs standalone.

## The triad

Shared design understanding is three durable documents, answering three different questions:

| Question | Document | What it holds | Owned by |
| --- | --- | --- | --- |
| **Why** | `<product-docs>/<product-slug>/product.html` | Product intent: personas, problems, capabilities, journeys, scope. See [product-memory.md](product-memory.md). | Product skills. When no product docs exist, `map-current-product` infers the baseline from the repo. |
| **How** | `DESIGN.md` at the project root | Design authority: visual tokens in YAML frontmatter (colors, typography, spacing, radius, motion), plus prose — aesthetic rationale, component foundations, accessibility rules, provenance. | `design-context` (native), or an accepted external ⑤ design-context capability. |
| **What** | `docs/design/prototype.html` | The canonical prototype: rendered structure and visuals per surface, all five states switchable, fidelity and lock markers, links back to the why. | The pipeline stage whose gate the change passed through. |

A reader who opens these three files knows what the product is for, what its design rules are, and what the design actually looks like — without reconstructing any effort's working files. Everything else design skills produce is working memory and dies with the effort.

## Documents and routing

- Working: `<work-root>/<effort>/design/` — wireframe drafts, variant HTMLs, the capability record (`capabilities.md`), decision notes, and throwaway prototypes under `prototypes/<slug>/`.
- Human: the triad above, plus `docs/design/components/<name>.md` — the per-component implementation record (API, states, choices the code cannot show).
- Routing stays in `docs/agents/memory.md` and `<work-root>/<effort>/state.md`, exactly as for product memory. Resolve explicit user paths first, then memory configuration and active-state pointers. The work root defaults to `.scratch/`.

MECE guides the boundary, not a hard constraint: a fact needed after the effort ends must reach the triad; analysis in progress stays in the work root. The durability test is unchanged — if the work root were deleted, would the project lose a fact it still needs?

**Legacy.** `docs/design/system.md` remains readable while it is still the canonical token source; `design-context` folds it into `DESIGN.md` on its next run and leaves a one-line pointer behind. Older efforts' `interaction/state-table.md` and `visual/approved.html` remain readable as working intermediates; the canonical prototype supersedes them as the durable handoff.

## The canonical prototype

`docs/design/prototype.html` is one self-contained, git-tracked HTML file. It needs no build step and opens from `file://`. Format contract:

- **One `<section>` per surface** (a screen, page, or self-contained component), carrying:
  - `data-surface="<kebab-slug>"` — stable identity, preserved across edits
  - `data-capability="<relative-path>#<record-id>"` — link to the `product.html` capability or journey this surface serves (the why)
  - `data-fidelity="wireframe | styled | implemented"`
  - `data-structure="open | locked"`
  - `data-updated="YYYY-MM-DD"`
- **All five states rendered** inside each section as `data-state="loading | empty | error | success | partial"` blocks, driven by one shared state switcher (floating control, keyboard-accessible). Five-state coverage is checked by the presence of the five blocks, not by prose.
- **Every visual value is a CSS custom property** declared at `:root` with a provenance comment naming `DESIGN.md` and the date it was last synced. At `wireframe` fidelity, sections use only the grayscale wireframe palette; token properties apply from `styled` onward.
- **Implemented sections** additionally carry `data-component="<source-path>"` and `data-component-doc="docs/design/components/<name>.md"`.

Do not invent additional lifecycle attributes; if a section genuinely needs one, add a `data-attr-reason` stating why so review flags it.

## Fidelity and locking

The pipeline's two invariants are markers in the prototype, so they are checkable rather than prose:

1. **Structure before visuals.** A section enters at `wireframe` fidelity — grayscale boxes, labels, all five states, no brand styling. Approval of structure sets `data-structure="locked"`. From then on, styled passes may vary only token-governed visual properties; any change to layout, navigation, or state transitions reopens the section (`data-structure="open"`, back to `wireframe`) and routes through `interaction-design`.
2. **One canonical how.** Every visual value in a `styled` or `implemented` section traces to `DESIGN.md`. Engine- or tool-invented values are reconciled into `DESIGN.md` tokens or rejected. If a variant choice reveals the authority itself is wrong — a missing token, an accent that cannot carry the hierarchy — that is a `DESIGN.md` change through `design-context`, not a local override.

Stage transitions:

| Stage | Transition it owns |
| --- | --- |
| `interaction-design` | Creates or reopens sections at `wireframe`; sets `data-structure="locked"` at its approval gate |
| `visual-design-variants` | Explores variants in the working layer; at approval merges the winner into the section, `wireframe → styled` |
| `design-implement` | Ships code; marks the section `implemented` with component pointers |
| `prototype` (utility) | None — its outputs are throwaway and never merge directly; the stage that raised the question folds the decision in through its own gate |

## Supersession

Shipped code is canonical **behavior**; the prototype is canonical **intent**. When they diverge, report the divergence rather than silently editing either. Small drift: regenerate the section from the shipped component and keep `implemented`. Deliberate redesign: reopen the section through the pipeline. A component doc records which prototype section it supersedes, so the trace survives either way.

## Coordination and the capability record

`state.md` is updated at every approval gate with what settled, a pointer into the triad (a `data-surface` anchor, a `DESIGN.md` section, a `product.html` record), and the next stage. `<work-root>/<effort>/design/capabilities.md` keeps its existing contract — disjoint rows per capability slot, contributor mode per [PROTOCOL.md](PROTOCOL.md) — it is dispatch memory, not shared understanding, and is unchanged by this contract.

## Promotion

| Working fact | Promotes to | Via |
| --- | --- | --- |
| Accepted state definitions and flows | `product.html` capability records | `write-prd` |
| Contested token-authority decision | an ADR | `domain-modeling` |
| Reusable component conventions | `docs/conventions` | `sync-context` |
| Approved structure or visual treatment | the canonical prototype section | the owning stage's approval gate |
| Visual variant choice among permitted directions | nothing further — the merged styled section plus `DESIGN.md` are the record | — |

## External ⑤ tools

When an accepted `⑤ design context` capability (per the ux dispatch contract) owns the `DESIGN.md` lifecycle, native skills read `DESIGN.md` as canonical regardless of who maintains it, route writes through the tool where the user accepted that, and reconcile its output against this contract. `DESIGN.md`'s format — YAML frontmatter tokens plus prose — is the ecosystem convention those tools already maintain; the native path writes the same shape.
