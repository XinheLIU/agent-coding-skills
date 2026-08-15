# Third-Party Notices

Last updated: 2026-08-03

## Matt Pocock skills

The adapted skills listed in [the organization report](docs/organization-report.md) were influenced by [`mattpocock/skills`](https://github.com/mattpocock/skills), licensed under the MIT License.

- Revision `2ab958093e83e0ec752e6c1c5932da465bf23e0c`: `grill-me`, `grill-with-docs`, `grilling`, `to-spec`, `to-tickets`.
- Revision `ed37663cc5fbef691ddfecd080dff42f7e7e350d`: the other 17 audited skills.

The locally copied `references/matt-pocock/skills/engineering/README.md` is a repository-local index and is not represented as upstream source.

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

Existing skill packages may contain their own licenses or metadata. Their provenance needs a complete normalization audit before a release; see [`TODO.md`](TODO.md).

## Wiki-layer

The prose wiki capability (`llm-wiki-init`, `llm-wiki-ingest`, `llm-wiki-lint`) now lives in [learning-os](https://github.com/XinheLIU/learning-os). Those skills adapt the LLM Wiki discipline from Andrej Karpathy's LLM Wiki approach (MIT). This system routes to them rather than maintaining a local copy.

`index-codebase` wraps the external indexers documented in [`skills-src/context-management/index-codebase/references/external-tools.md`](skills-src/context-management/index-codebase/references/external-tools.md) without vendoring their code: [`codemap`](https://github.com/JordanCoin/codemap), [`codegraph`](https://github.com/colbymchenry/codegraph), `graphify` (published as `graphifyy`), and [`GitNexus`](https://github.com/abhigyanpatwari/GitNexus). Each remains under its own upstream license and is invoked as an installed tool.

## Product-ideation adaptations

`generate-product-ideas` adapts the constraint-driven generation approach from the skills-manager `ideation` skill by SHL0MS, declared MIT-licensed in its skill metadata.

`validate-demand` and `scope-mvp` adapt product reasoning from gstack `office-hours` and `plan-ceo-review` version 1.58.5.0. gstack is MIT-licensed, copyright (c) 2026 Garry Tan. The adaptations remove gstack-specific runtime behavior and integrate the shared memory protocol.
