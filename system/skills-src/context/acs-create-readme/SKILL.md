---
name: acs-create-readme
description: Create or revamp a project's README.md after auditing its implementation, manifests, and existing documentation. Use for README authoring; agent instructions belong to acs-review-agent-instructions and repository-wide document organization belongs to acs-sync-context.
---

# Create README

Last updated: 2026-10-04

Write for a human arriving with zero project context. The README should answer
what problem this solves, how to run it, and where to go next in under a minute.

## Context contract

```yaml
context:
  requires: [repository.implementation]
  retrieves: [context.configuration, repository.manifests, repository.documentation]
  produces: [context.readme_draft, context.readme_verification]
  updates: [context.readme]
  invalidates: [context.readme_dependents]
  handoff_to: [coordinator]
```

Shared semantics: [shared protocol](../../../protocols/skill-declarations.md#skill-declarations);
shared execution: [Coordination](../../../protocols/context-coordination.md).
Existing authorization persists. This skill owns human-facing README content;
`acs-review-agent-instructions` owns `AGENTS.md`/`CLAUDE.md`, and `acs-sync-context`
owns repository-wide document classification and reorganization.

## 1. Audit before drafting

Inspect the implementation and project conventions:

- Manifests, entry points, scripts and dependency declarations: actual behavior,
  runtime, package manager and runnable commands.
- Existing README: useful content, stale claims, missing first-run instructions.
- `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md`: authoritative documents to link.
- Assets and CI: existing screenshots, logo and verifiable badge facts.
- Directory layout: boundaries a newcomer needs to understand.

Ask only for consequential facts the repository and task do not establish,
such as an unclear audience or a license choice. Do not invent demo URLs,
installation sources, supported versions or contact details.

## 2. Choose the smallest useful structure

| Tier | Project | Sections |
| --- | --- | --- |
| Minimal | Script, small library, internal tool | About, Getting Started, Usage |
| Standard | Typical application or library | Add Built With, Project Structure, relevant pointers |
| Full | Public project seeking contributors | Add verified badges, TOC, contribution and credit pointers |

Use [the README template](references/readme-template.md) as an adaptable
blueprint. Keep only sections that serve this project; replace every placeholder.

## 3. Draft from evidence

- Lead with the problem and intended reader; explain what the project does plainly.
- Make Getting Started copyable. Check commands, paths and package names against
  manifests and documented tooling, including prerequisites and first success.
- Show actual usage examples and available output. Explain unfamiliar flags,
  abbreviations, environment variables and units when the reader meets them.
- Link dedicated license, contribution and changelog files instead of duplicating them.
- Use screenshots or badges only when the assets or underlying facts exist.
- Match the project's language and conventions. Keep formatting readable and avoid filler.
- Include `Last updated: YYYY-MM-DD` near the top of the resulting README.

For a revamp, explain which sections are kept, rewritten, added or removed and why.
Reuse the user's authorization to apply a requested revamp; a review-only request
produces findings or a proposed draft without modifying the README.

## 4. Verify and deliver

Check every introduced command against the project, resolve local links and assets,
and match TOC anchors to retained headings. Run an existing documentation check when
available. Avoid installation, deployment or other side effects merely to test an
example; identify any commands not executed and the evidence used to check them.

Complete when the requested README or review draft answers the three entry questions,
contains no unresolved placeholders or unsupported claims, and links to current
authoritative documentation. Report the path, substantive changes and verification.
Keep unrelated documents and repository structure unchanged.

## Sources

Recovered from the managed `create-readme` skill after its local source path disappeared.
The adaptation retains its repository audit, size-based structure and template, while
using ACS context ownership and current skill IDs.

- [awesome-copilot / create-readme](https://www.skills.sh/github/awesome-copilot/create-readme)
- [Dryad: What's in a README?](https://blog.datadryad.org/2025/09/09/whats-in-a-readme-why-your-readme-matters-and-how-to-create-the-best-one-possible/)
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template) (MIT)
