# Third-Party Notices

Last updated: 2026-09-26

## Context and presentation architecture

The accepted [Context design](resources/docs/context-memory-presenter-proposal.md) adapts memory-scope separation from [LangGraph](https://docs.langchain.com/oss/python/concepts/memory), structured notes and selective retrieval from [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), and presentation/domain separation from [Martin Fowler's Presentation Model](https://martinfowler.com/eaaDev/PresentationModel.html). OpenSpec (`bae58cf`) informs current/change separation; Superpowers (`5bf4e78`) informs optional visual companions. These are design influences, not vendored runtime dependencies. The proposal records source details and the adapted boundaries.
## Reference clones (study material only)

Two upstream references are cloned under `references/` (source-checkout provenance: `references`) for study: [`obra/superpowers`](https://github.com/obra/superpowers) (MIT) and [`Fission-AI/OpenSpec`](https://github.com/Fission-AI/OpenSpec) (MIT). Their pinned commits are recorded in `references/README.md` (source-checkout provenance: `references/README.md`). These entries record the provenance of the study corpus — the same status as the gstack and Matt Pocock snapshots.

The `acs-brainstorm` skill cites the `superpowers` `brainstorming` Socratic pattern (see `skills-src/plan/acs-brainstorm/SKILL.md`). The existing-product lane adapts OpenSpec's brownfield-first and delta-spec principles in `acs-map-current-product` and `acs-define-outcomes`. Upstream names in these notices retain their original spelling; ACS adaptations use the `acs-` namespace.

## PM-Skills

The existing-product lane adapts selected principles from [`product-on-purpose/pm-skills`](https://github.com/product-on-purpose/pm-skills), licensed under Apache-2.0. The local study copy is under `references/pm-skills/` (source-checkout provenance: `references/pm-skills`), with license text at `references/pm-skills/LICENSE` (source-checkout provenance: `references/pm-skills/LICENSE`).

- `acs-map-current-product` adapts `deliver-user-stories` for persona/action/benefit story shape and story testability.
- `acs-define-outcomes` adapts `deliver-acceptance-criteria`, `deliver-edge-cases`, `measure-instrumentation-spec`, and `iterate-refinement-notes` for acceptance criteria, recovery-path coverage, analytics contracts, and refinement notes.

## Matt Pocock skills

The adapted skills listed in the organization report were influenced by [`mattpocock/skills`](https://github.com/mattpocock/skills), licensed under the MIT License.

- Revision `2ab958093e83e0ec752e6c1c5932da465bf23e0c`: `grill-me`, `grill-with-docs`, `grilling`, `to-spec`, `to-tickets`.
- Revision `ed37663cc5fbef691ddfecd080dff42f7e7e350d`: the other 17 audited skills.

`build/acs-plan-delivery` adapts the progressive decision mapping of `wayfinder` and independently verifiable slicing of `to-tickets`. It reuses upstream Product/Design decisions, keeps design blockers and delivery slices in one canonical graph, and integrates the suite's DAG renderer and execution handoffs. No upstream skill installation is required.

The locally copied `references/matt-pocock/skills/engineering/README.md` is a repository-local index and is not represented as upstream source.

The product-lane shared-understanding protocol (`skills-src/plan/acs-validate-demand/references/shared-understanding.md`) adapts two Matt Pocock mechanics: from `grilling`, the shared-understanding contract — do not act until the user confirms a shared understanding, provide a recommended answer with each question, and look up facts from the environment while putting decisions to the user; from `to-tickets` step 4 ("Quiz the user"), the batched numbered-question-and-iterate pattern. The protocol deliberately inverts `grilling`'s one-question-at-a-time rule in favor of blocks of 4–5 questions per message. The `acs-brainstorm` skill's superpowers-derived Socratic flow carries the same deliberate one-at-a-time → block substitution, noted in its Credit section.

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

## Product-ideation adaptations

`generate-product-ideas` adapts the constraint-driven generation approach from the skills-manager `ideation` skill by SHL0MS, declared MIT-licensed in its skill metadata.

`acs-validate-demand` adapts product reasoning from gstack `office-hours` and `plan-ceo-review` version 1.58.5.0. gstack is MIT-licensed, copyright (c) 2026 Garry Tan. The adaptations remove gstack-specific runtime behavior and integrate the shared memory protocol. The `plan-ceo-review` ambition-review and scope-posture adaptations were removed with the deprecated `scope-mvp` and `scope-product-increment` skills and have no current home.

## OpenSpec adaptations

`acs-map-current-product` and `acs-define-outcomes` adapt brownfield-first exploration and
`ADDED / MODIFIED / REMOVED` behavior-delta language from [`Fission-AI/OpenSpec`](https://github.com/Fission-AI/OpenSpec), licensed under the MIT License. No OpenSpec CLI code or runtime dependency is included.
