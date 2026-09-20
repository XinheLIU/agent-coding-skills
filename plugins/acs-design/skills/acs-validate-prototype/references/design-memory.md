# Design Memory Contract

Last updated: 2026-09-17

Design skills contribute to one shared design understanding. A skill owns its reasoning method, not the understanding itself. Read this contract before reading or updating design memory. It also applies when a skill runs standalone.

## Lifecycle and authority

The [shared protocol](PROTOCOL.md) defines lifecycles, relationships, freshness, and the handoff envelope. Product records span North Star, Current State, and Change Context; applicable DESIGN.md rules are Current State; accepted prototype sections and consequential design decisions are Change Context. The prototype preserves accepted intent; code establishes actual behavior. Technical data/API/system/module contracts are separately addressable Change Context, linked to the same canonical change and requirement/criterion IDs.

At acceptance, retain consequential rationale beside the design or in the change's decision home (new local default `docs/changes/<change-id>/decisions/<decision-id>.md`). Record ID, status, scope, decision, basis/alternatives, consumed requirement/token/contract revisions, `depends_on`, `affects`, and `supersedes` when applicable. Keep previous decisions; mark applicability `needs review` when relevant premises change. Do this before implementation; component documentation is not a prerequisite. Minor visual choices need no new ADR, but consequential rationale must not live only in scratch.

## The triad

Shared design understanding is three durable documents, answering three different questions:

| Question | Document | What it holds | Owned by |
| --- | --- | --- | --- |
| **Why** | `<product-docs>/<product-slug>/product.html` | Product intent: personas, problems, capabilities, journeys, scope. See [product-memory.md](product-memory.md). | Product skills. When no product docs exist, `acs-map-current-product` infers the baseline from the repo. |
| **How** | `DESIGN.md` at the project root | Design authority: visual tokens in YAML frontmatter (colors, typography, spacing, radius, motion), plus prose — aesthetic rationale, component foundations, accessibility rules, provenance. | `acs-design-context` (native), or an accepted external ⑤ acs-design-context capability. |
| **What** | `docs/design/prototype.html` | The canonical prototype: rendered structure and visuals per surface, all five states switchable, fidelity and lock markers, links back to the why. | The pipeline stage whose gate the change passed through. |

A reader who opens these three files knows what the product is for, what its design rules are, and what the design actually looks like — without reconstructing any effort's working files. Separately linked accepted contracts and consequential decisions are also durable. Drafts, rejected variant files, and raw experiments remain Run Context after required rationale/evidence is retained.

## Documents and routing

- Run Context: `<work-root>/<effort>/design/` — wireframe drafts, variant HTMLs, the capability record (`capabilities.md`), draft decision notes, and throwaway prototypes under `prototypes/<slug>/`.
- Durable: the triad above, plus `docs/design/components/<name>.md` — the per-component implementation record (API, states, choices the code cannot show).
- Routing stays in `docs/agents/memory.md` and `<work-root>/<effort>/state.md`, exactly as for product memory. Resolve explicit user paths first, then memory configuration and active-state pointers. The work root defaults to `.scratch/`.

MECE guides the boundary, not a hard constraint: a fact needed after the effort ends must reach the triad or linked Change Context; analysis in progress stays in the work root. The durability test is unchanged — if the work root were deleted, would the project lose a fact it still needs?

**Legacy.** `docs/design/system.md` remains readable while it is still the canonical token source; `acs-design-context` folds it into `DESIGN.md` on its next run and leaves a one-line pointer behind. Older efforts' `interaction/state-table.md` and `visual/approved.html` remain readable as working intermediates; the canonical prototype supersedes them as the durable handoff.

## The canonical prototype

`docs/design/prototype.html` is one self-contained, git-tracked HTML file. It needs no build step and opens from `file://`. Format contract:

- **One `<section>` per surface** (a screen, page, or self-contained component), carrying:
  - `data-surface="<kebab-slug>"` — stable identity, preserved across edits
  - `data-capability="<relative-path>#<record-id>"` — link to the `product.html` capability or journey this surface serves (the why)
  - `data-fidelity="wireframe | styled | implemented"`
  - `data-structure="open | locked"`
  - `data-updated="YYYY-MM-DD"`
- **Visible reference links per section** identify the canonical change, relevant requirement/criterion IDs, accepted decision references and consumed revisions. Use ordinary links and text rather than a parallel metadata store.
- **All five states rendered** inside each section as `data-state="loading | empty | error | success | partial"` blocks, driven by one shared state switcher (floating control, keyboard-accessible). Five-state coverage is checked by the presence of the five blocks, not by prose.
- **Every visual value is a CSS custom property** declared at `:root` with a provenance comment naming `DESIGN.md` and the consumed token revision plus the date it was last synced; the date alone does not prove freshness. At `wireframe` fidelity, sections use only the grayscale wireframe palette; token properties apply from `styled` onward.
- **Implemented sections** additionally carry `data-component="<source-path>"` and `data-component-doc="docs/design/components/<name>.md"`.

Do not invent additional lifecycle attributes; if a section genuinely needs one, add a `data-attr-reason` stating why so review flags it.

## Fidelity and locking

The pipeline's two invariants are markers in the prototype, so they are checkable rather than prose:

1. **Structure before visuals.** A section enters at `wireframe` fidelity — grayscale boxes, labels, all five states, no brand styling. Approval of structure sets `data-structure="locked"`. From then on, styled passes may vary only token-governed visual properties; any change to layout, navigation, or state transitions reopens the section (`data-structure="open"`, back to `wireframe`) and routes through `interaction-design`.
2. **One canonical how.** Every visual value in a `styled` or `implemented` section traces to `DESIGN.md`. Engine- or tool-invented values are reconciled into `DESIGN.md` tokens or rejected. If a variant choice reveals the authority itself is wrong — a missing token, an accent that cannot carry the hierarchy — that is a `DESIGN.md` change through `acs-design-context`, not a local override.

Stage transitions:

| Stage | Transition it owns |
| --- | --- |
| `interaction-design` | Creates or reopens sections at `wireframe`; sets `data-structure="locked"` at its approval gate |
| `acs-visual-design-variants` | Explores variants in the working layer; at approval merges the winner into the section, `wireframe → styled` |
| `acs-design-implement` | Ships code; marks the section `implemented` with component pointers |
| `prototype` (utility) | None — its outputs are throwaway and never merge directly; the stage that raised the question folds the decision in through its own gate |

## Supersession

Shipped code is canonical **behavior**; the prototype is canonical **intent**. When they diverge, report the divergence rather than silently editing either. Record the affected intent/behavior and route reassessment to the design owner. Reopen a section only for an accepted design change. Do not require a synchronized second implementation of the UI; an `implemented` marker and source/component-doc pointers provide traceability, not proof that the prototype reproduces every shipped behavior.

## Coordination and the capability record

At a gate, the design skill returns accepted decision/contract and surface references, consumed revisions, delta, questions, and next action. The coordinator applies run-state updates, capability discovery/dispatch, and serialized writes under [workflow coordination](../../../../../protocols/context-coordination.md). Capability rows are Run Context; disjoint rows do not permit concurrent file writes.

## Promotion

| Working fact | Promotes to | Via |
| --- | --- | --- |
| Accepted state definitions and flows | canonical change spec/criteria; product records link them | `acs-write-prd` reconciles product scope |
| Contested token-authority decision | an ADR | `domain-modeling` |
| Reusable component conventions | `docs/conventions` | `acs-sync-context` |
| Approved structure or visual treatment | the canonical prototype section | the owning stage's approval gate |
| Consequential variant or interaction choice | accepted design/change decision with basis, alternatives, and revisions | owning stage at acceptance |

## External ⑤ tools

When an accepted `⑤ design context` capability (per the ux dispatch contract) owns the `DESIGN.md` lifecycle, native skills read `DESIGN.md` as canonical regardless of who maintains it, route writes through the tool where the user accepted that, and reconcile its output against this contract. `DESIGN.md`'s format — YAML frontmatter tokens plus prose — is the ecosystem convention those tools already maintain; the native path writes the same shape.
