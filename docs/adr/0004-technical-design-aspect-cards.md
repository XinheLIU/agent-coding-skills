# Cut technical design into aspect cards that share one record

Last updated: 2026-09-29

Change: technical design reorganization
Status: accepted
Basis: review of the design/technical and test/review skill sets, 2026-09-29
affects: `system/skills-src/design/technical/**`, `system/skills-src/test/review/**`, `system/protocols/design-memory.md`, `system/protocols/skill-declarations.md`, `catalog/skill-set.json`

Technical design had been split by activity instead of by aspect. Four thin design skills (architecture, foundation, modules, validate-codebase) sat beside four thick review skills (review-architecture, audit-architecture, review-design-doc, review-implementation-gaps). Design and review of the same aspect lived in different skills and different phases. Each skill wrote its own file (`technical-design.md`, `AUDIT.md`, `eng-reviews/review-architecture-*`, `plan-review-*`, `gap-analysis-*`), and three per-skill HTML report contracts did not agree. Two skills traced design to code with near-identical status vocabularies. No skill designed a test strategy, contracts got a single sentence, and `system.invariants` had consumers but no producer.

The set is now five vertical aspect cards plus a thin router:

- `acs-design-architecture` (ARC)
- `acs-design-modules` (MOD)
- `acs-design-contracts` (CON)
- `acs-design-test-strategy` (TST)
- `acs-trace-requirements` (TRC)
- `acs-technical-design`, the router

Each card assesses the current state, designs the target, and reviews a proposal for its one aspect. Each writes its own section of `docs/design/technical-design.md` and its own rows in one findings ledger. One HTML view is derived from that record.

## Considered options

- **Keep the design/review split and share only an output format.** This fixes the scattered files but keeps each aspect's judgment in two places, with nothing to stop them drifting. Rejected.
- **One large technical-design skill.** This gives a single output, but it recreates the imbalance the review found and makes it impossible to run one aspect alone. Rejected.
- **Four cards, with test strategy folded into contracts.** Fewer skills, but verification planning would stay a subsection nobody owns, and that gap is the one the review found. Rejected in favor of five.
- **Keep a separate foundation skill.** Foundations are a decision (what to share, in which form), which belongs to ARC, and a contract shape, which belongs to MOD. A separate skill duplicated both. Folded in.

## Consequences

- Deleted with no compatibility stubs, following the phase reorganization in ADR-0001:
  - `acs-audit-architecture`, `acs-design-foundation` and `acs-validate-codebase`
  - `acs-review-architecture`, `acs-review-design-doc` and `acs-review-implementation-gaps`
- Their lenses moved to exactly one card each.
- `system/agents/` is deleted. Its 26 prompt files repeated lenses that belong to skills:
  - the 12 architecture explorer/reviewer prompts became ARC's deep-mode checklist, `acs-design-architecture/references/architecture-lenses.md`
  - the 13 domain and `code-reviewer` prompts became `acs-review-code-quality/references/domain-lenses.md`
  - `tdd-builder` repeated the `acs-implement` / `acs-tdd` delivery flow

  A lens runs inline, or as a delegated task whose instruction is its section of the reference, so delegation needs no separate agent file.
- `acs-review-code-quality`, `acs-refactor-code` and `acs-analyze-test-gaps` stay change- or code-level tools. They consume the record:
  - code quality reads `FND-ARC` and `TRC` rows
  - refactoring preserves `CON` invariants
  - test gaps start from `TST` critical paths
- `verification.trace_matrix` replaces `implementation_gap_map` and `implementation_alignment`.
- The design memory contract (v1.3.0) names the technical record next to the UX triad.
