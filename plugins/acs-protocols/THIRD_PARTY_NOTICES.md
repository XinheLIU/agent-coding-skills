# Third-Party Notices

Last updated: 2026-10-23

## Context and presentation architecture

The accepted [Context design](resources/docs/context-memory-presenter-proposal.md) adapts memory-scope separation from [LangGraph](https://docs.langchain.com/oss/python/concepts/memory), structured notes and selective retrieval from [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), and presentation/domain separation from [Martin Fowler's Presentation Model](https://martinfowler.com/eaaDev/PresentationModel.html). OpenSpec (`bae58cf`) informs current/change separation; Superpowers (`5bf4e78`) informs optional visual companions. These are design influences, not vendored runtime dependencies. The proposal records source details and the adapted boundaries.
## Reference clones (study material only)

Two upstream references are cloned under `references/` for study: [`obra/superpowers`](https://github.com/obra/superpowers) (MIT) and [`Fission-AI/OpenSpec`](https://github.com/Fission-AI/OpenSpec) (MIT). Their pinned commits are recorded in `references/README.md`. These entries record the provenance of the study corpus — the same status as the gstack and Matt Pocock snapshots.

The `acs-brainstorm` skill cites the `superpowers` `brainstorming` Socratic pattern (see `skills-src/plan/acs-brainstorm/SKILL.md`). The existing-product lane adapts OpenSpec's brownfield-first and delta-spec principles in `acs-map-current-product` and `acs-define-outcomes`. Upstream names in these notices retain their original spelling; ACS adaptations use the `acs-` namespace.

## Rigor-tier adaptations

The [workflow rigor tiers](workflows/README.md#rigor-tiers) adapt the three paths, one-way ratchet, and stage-specific approval from [Superpowers brainstorming](https://github.com/obra/superpowers/blob/5bf4e78/skills/brainstorming/SKILL.md) (MIT); proportional artifacts from [OpenSpec concepts](https://github.com/Fission-AI/OpenSpec/blob/bae58cf/docs/concepts.md#keep-it-lightweight-progressive-rigor) (MIT); and the risk-sensitive lightweight-path principle from [Addy Osmani's ship command](https://github.com/addyosmani/agent-skills/blob/aeac41d/commands/ship.toml) (MIT, rule 5). ACS uses its own one-ticket Bounded route, canonical questioning, and revision-bound evidence; it does not copy upstream command code, fixed fan-out thresholds, or single-question cadence. The model-tier sensor note follows the harness-cost analysis in [Are Harnesses Worth the Cost?](https://martinfowler.com/articles/are-harnesses-worth-the-cost.html).

## PM-Skills

The existing-product lane adapts selected principles from [`product-on-purpose/pm-skills`](https://github.com/product-on-purpose/pm-skills), licensed under Apache-2.0. The local study copy is under `references/pm-skills/`, with license text at `references/pm-skills/LICENSE`.

- `acs-map-current-product` adapts `deliver-user-stories` for persona/action/benefit story shape and story testability.
- `acs-define-outcomes` adapts `deliver-acceptance-criteria`, `deliver-edge-cases`, `measure-instrumentation-spec`, and `iterate-refinement-notes` for acceptance criteria, recovery-path coverage, analytics contracts, and refinement notes.

## Matt Pocock skills

The adapted skills listed in the organization report were influenced by [`mattpocock/skills`](https://github.com/mattpocock/skills), licensed under the MIT License.

- Revision `2ab958093e83e0ec752e6c1c5932da465bf23e0c`: `grill-me`, `grill-with-docs`, `grilling`, `to-spec`, `to-tickets`.
- Revision `ed37663cc5fbef691ddfecd080dff42f7e7e350d`: the other 17 audited skills.

The study copy under `references/matt-pocock/` has since been refreshed to the upstream tree at `49dd158` (2026-10-09). The adaptations above were made against the older revisions. The corpus-alignment changes additionally adapt questioning and TDD seam principles from `49dd158`, with provenance recorded in `protocols/questioning.md` and `skills-src/build/acs-tdd/SKILL.md`.

`build/acs-plan-delivery` adapts the progressive decision mapping of `wayfinder` and independently verifiable slicing of `to-tickets`. It reuses upstream Product/Design decisions, keeps design blockers and delivery slices in one canonical graph, and integrates the suite's DAG renderer and execution handoffs. No upstream skill installation is required.

The locally copied `references/matt-pocock/skills/engineering/README.md` is an upstream index file, and `references/matt-pocock/README.md` is repository-local; neither is represented as upstream skill source.

The canonical questioning protocol (`protocols/questioning.md`, with the former shared-understanding path retained as an alias) adapts Matt Pocock's recommended answers, shared-understanding close, fact lookup, and numbered question rounds. ACS classifies candidates before asking and presents only questions with settled prerequisites, at most five per round. It also adapts pstack's affirmative recommendation wording and gstack's execution-time decision classification; source revisions are recorded in the protocol. Product planning and code review use this shared contract.

```text
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Existing skill packages may contain their own licenses or metadata. Their provenance needs a complete normalization audit before a release.

## Wiki-layer

The prose wiki capability (`llm-wiki-init`, `llm-wiki-ingest`, `llm-wiki-lint`) now lives in [learning-os](https://github.com/XinheLIU/learning-os). Those skills adapt the LLM Wiki discipline from Andrej Karpathy's LLM Wiki approach (MIT). This system routes to them rather than maintaining a local copy.

`acs-init-context` documents and invokes the external indexers listed in its `references/index-tools/external-tools.md` without vendoring their code: [`codemap`](https://github.com/JordanCoin/codemap), [`codegraph`](https://github.com/colbymchenry/codegraph), `graphify` (published as `graphifyy`), and [`GitNexus`](https://github.com/abhigyanpatwari/GitNexus). Each remains under its own upstream license and is invoked as an installed tool.

## Addy Osmani agent-skills

[`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) is copied under `references/addy-osmani/` at `aeac41d` (2026-10-13), MIT-licensed. `acs-analyze-test-gaps` adapts the cost-based constraint placement and five-move diff floor from `constraint-driven-development` and its `references/floor-guard.md`. `acs-design-contracts` adapts question-first instrumentation, signal-to-question mapping, three-line alert runbooks, test-firing, and telemetry-only failure diagnosis from [`observability-and-instrumentation`](https://github.com/addyosmani/agent-skills/blob/aeac41d/skills/observability-and-instrumentation/SKILL.md). ACS keeps requirements in CON, routes verification through TST/implementation, and uses a local mock exercise without external notifications. The risk-sensitive lightweight-path principle is also adapted into the workflow rigor tiers above. Its Python guard is an ACS implementation; no upstream runtime is vendored. The companion constraint guide also adapts the architecture → types → checks → tests preference from pstack `correct` in [`cursor/plugins`](https://github.com/cursor/plugins/tree/main/pstack) at `0b8e952`. The guide records provenance and retains ACS questioning and engineering-evidence contracts. The study corpus is indexed by two repository-local maps: `references/README.md` for the collections, and `references/ANALYSIS.md` for how the packs differ and what the system borrows.

## pstack

[`cursor/plugins` → `pstack/`](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan is copied under `references/pstack/` at `0b8e952` (2026-10-18, v0.15.26), MIT-licensed. The corpus remains read-only study material. ACS adapts affirmative recommendation wording into `protocols/questioning.md` and revision-keyed evidence into `protocols/orchestration.md`; these are documented adaptations, not vendored runtime dependencies. Its guide images (2.2 MB) are part of the upstream docs and are copied as-is.

## Product-ideation adaptations

`generate-product-ideas` adapts the constraint-driven generation approach from the skills-manager `ideation` skill by SHL0MS, declared MIT-licensed in its skill metadata.

`acs-validate-demand` adapts product reasoning from gstack `office-hours` and `plan-ceo-review` version 1.58.5.0. gstack is MIT-licensed, copyright (c) 2026 Garry Tan. The adaptations remove gstack-specific runtime behavior and integrate the shared memory protocol. The earlier `plan-ceo-review` ambition-review and scope-posture adaptations were removed with the deprecated `scope-mvp` and `scope-product-increment` skills. The four scope postures now have a home in [`acs-shape-solution` Phase C](resources/skills-src/plan/acs-shape-solution/SKILL.md#scope-postures) (reference procedure; capability not installed), adapted from [`garrytan/gstack`](https://github.com/garrytan/gstack) `plan-ceo-review/SKILL.md.tmpl` at `35dd014c580037d1c009776d8b0584587c1bd42c` (lines 62–68 and 291–356). This adaptation retains commitment to the chosen mode, raising posture concerns once, explicit opt-in for each scope change, and a `NOT in scope` record. It uses ACS shared questioning and product-memory records, without gstack runtime behavior or its completeness-at-any-cost framing.

## Review evidence adaptations

The [review evidence gate](protocols/engineering-memory.md#review-evidence-gate), consumed by `acs-review-code-quality` and `acs-trace-requirements`, adapts the quotation gate in `review/SKILL.md` (lines 720–735) and artifact-completion honesty in `ship/sections/plan-completion.md` (line 90) from [`garrytan/gstack`](https://github.com/garrytan/gstack) at `35dd014c580037d1c009776d8b0584587c1bd42c` (MIT, copyright (c) 2026 Garry Tan). ACS keeps unquoted findings unverified at confidence ≤ 5/10, separates static wiring from delivery, and uses its existing evidence identity and traceability records. No gstack runtime is included.

## Release-tail adaptations

`acs-ship` and `acs-release` adapt rerun-verification/action-idempotency, PR evidence, first-use dry runs, merge-error state reads and consecutive canary checks from [`garrytan/gstack`](https://github.com/garrytan/gstack) `ship`, `land-and-deploy` and `canary` at `35dd014c580037d1c009776d8b0584587c1bd42c` (MIT, copyright (c) 2026 Garry Tan). Staged rollout, rollback thresholds and error-budget gating also draw on [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) `shipping-and-launch` at `aeac41d` (MIT). ACS requires consumer-declared commands/environments, keeps existing authorization and artifact-bound evidence, and uses local fixtures without upstream runtime code or provider defaults.

## OpenSpec adaptations

`acs-map-current-product` and `acs-define-outcomes` adapt brownfield-first exploration and
`ADDED / MODIFIED / REMOVED` behavior-delta language from [`Fission-AI/OpenSpec`](https://github.com/Fission-AI/OpenSpec), licensed under the MIT License. No OpenSpec CLI code or runtime dependency is included.
