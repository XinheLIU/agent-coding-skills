<!--
Fill-in skeleton for a root README. The authoritative guidance — principles,
anti-patterns, validation checklist — lives in
`.claude/skills/document-codebase/references/readme-template.md`.

Rules while filling this in:
  1. Replace every [placeholder]. Do not ship with them.
  2. Keep the section order. It enforces the "layered, scannable" principle.
  3. Delete sections the project does not need (e.g. Acknowledgments,
     Contributing for a solo project). Never reorder.
  4. Every code block must be copy-pasteable and verified from a clean clone.
-->

# [Project Name]

Last updated: 2026-08-02

Last updated: [YYYY-MM-DD]

*[One-sentence pitch: what it is, who it's for, the pain it removes, the differentiator. No marketing adjectives.]*

<!-- Example:
*A local-only CLI that turns raw bank CSVs into reconciled double-entry
ledgers for solo freelancers who don't want their finances in a SaaS.*
-->

[![Build][build-shield]][build-url]
[![Version][version-shield]][version-url]
[![License][license-shield]][license-url]
[![Downloads][downloads-shield]][downloads-url]

![Demo](docs/assets/demo.gif)

<!-- Replace with a real screenshot or ≤10s GIF showing the happy path.
     If there is no visual surface, delete the image and put a 5-line code
     example here that produces a surprising result. -->

## About

[2–4 sentences expanding the pitch: the problem, the solution shape, and one or two non-goals. Link to `AGENTS.md` or a design doc for deeper context.]

### Built With

- [Language + version floor]
- [Key framework / runtime]
- [Primary external dependency worth naming]

## Quick Start

### Prerequisites

- [Tool] [version floor] — check with `[tool] --version`
- [Tool] [version floor] — check with `[tool] --version`

### Installation

```bash
git clone [repo-url]
cd [project]
[one-command install — e.g. uv sync]
```

### Verify

```bash
[one command that exercises the happy path]
```

Expected output: `[one concrete, verifiable line — e.g. "server listens on :8000; curl /health → {\"ok\":true}"]`.

Tested on: [OS + version], [language + version], [package manager + version].

## Usage

Minimal working example:

```bash
[the smallest command that demonstrates value]
```

```text
[the output that command produces]
```

More examples: [`docs/USAGE.md`](./docs/USAGE.md) · [`docs/API.md`](./docs/API.md)

## Features

- **[Benefit headline]** — [one-line user outcome, not an implementation note]
- **[Benefit headline]** — […]
- **[Benefit headline]** — […]
<!-- 3–6 bullets. Each must be phrased as a user gain, not a code fact.
     Bad: "Uses asyncio."  Good: "Fetches 100 URLs in parallel — batch time
     drops from 40 s to 2 s." -->

## Documentation

- [`docs/architecture/c4-context.md`](./docs/architecture/c4-context.md) — System context
- [`docs/architecture/c4-containers.md`](./docs/architecture/c4-containers.md) — Containers
- [`docs/API.md`](./docs/API.md) — API reference
- [`AGENTS.md`](./AGENTS.md) — Contribution rules, coding conventions

## Roadmap

- [ ] [Next milestone — one line]
- [ ] [Next milestone — one line]
- [ ] [Next milestone — one line]

Full roadmap: [`ROADMAP.md`](./ROADMAP.md) <!-- or a GitHub Project link -->

## Contributing

Contributions are welcome. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for setup, branch naming, and review expectations.

<!-- If the project does not accept outside contributions, say so explicitly:
     "This is a solo project; issues are welcome, PRs are not accepted." -->

## License

[SPDX identifier] — [one-line scope, e.g. "do what you want, keep the notice"]. See [`LICENSE`](./LICENSE).

## Contact

[Maintainer name or handle] — [channel: issue tracker, email, or Discord]

## Acknowledgments

- [Third-party project or person worth crediting]
- [Inspiration / prior art]

<!-- Badge definitions. Replace placeholders with real URLs before shipping. -->
[build-shield]: https://img.shields.io/github/actions/workflow/status/[owner]/[repo]/ci.yml?branch=main
[build-url]: https://github.com/[owner]/[repo]/actions
[version-shield]: https://img.shields.io/github/v/release/[owner]/[repo]
[version-url]: https://github.com/[owner]/[repo]/releases
[license-shield]: https://img.shields.io/github/license/[owner]/[repo]
[license-url]: ./LICENSE
[downloads-shield]: https://img.shields.io/github/downloads/[owner]/[repo]/total
[downloads-url]: https://github.com/[owner]/[repo]/releases
