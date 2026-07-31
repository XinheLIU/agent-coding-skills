# Doc-Types Playbook

Last updated: 2026-05-16

How to write each doc type for a technical audience. This is the prose-and-structure companion to the C4 reference files — it covers architecture-narrative, API, and inline-comment conventions. **Root READMEs have their own dedicated playbook at `references/readme-template.md` — read that, not this section.** Assume the reader is a programmer. Do not simplify for beginners unless the project genuinely targets them.

## Writing Conventions

### Voice, tense, directness

- Active voice, present tense, imperative mood for instructions.
  - Good: `The parser returns a ParsedReceipt.`  `Run migrations before starting the app.`
  - Bad: `A ParsedReceipt will be returned by the parser.`  `You will need to run migrations.`
- Cut hedges ("simply", "just", "basically") and filler ("in order to", "you can").
- Lead with the fact, then the qualifier. `Returns None when the file is empty; raises ParseError otherwise.` beats the reverse.

### Formatting

- Backticks for identifiers, file paths, commands, env vars: `parse_receipt`, `src/csv_parser.py`, `uv sync`, `DATABASE_URL`.
- Fenced code blocks with a language tag (` ```python `, ` ```bash `, ` ```mermaid `).
- Sentence-case headings: `## Data flow`, not `## Data Flow`.
- ISO dates everywhere: `2026-04-19`.
- Tables for anything that has ≥3 parallel fields (parameters, env vars, error codes, file-type mappings).

### Layering

Progressive disclosure — simple path up top, edge cases below:

```
## Install & run     ← 3–5 lines that get a working instance
## Usage             ← common operations, copy-pasteable
## Key concepts      ← abstractions a reader must hold before diving deeper
## Reference         ← exhaustive, alphabetical or structured
## Troubleshooting   ← failure modes, symptom → cause → fix
```

## README

See `references/readme-template.md`. That file owns the seven principles, section order, badge guidance, screenshot/GIF rules, anti-patterns, and the pre-commit validation checklist. Do not duplicate its guidance here.

Sub-package READMEs that live alongside standalone libraries within a monorepo inherit the principles but can omit badges, screenshots, Roadmap, and Contributing — they serve oriented readers, not evaluators.

### Annotated file tree (shared helper)

Used in the README's project-structure section and in some architecture narratives:

```text
src/
├── csv_parser.py          # Parses bank/platform CSVs → normalized rows
├── data_validator.py      # Schema + semantic validation, fail-fast
├── financial_calculator.py# Cents-only arithmetic, period rollups
└── ...
```

Rules: cluster by responsibility (never by filesystem order if that differs), keep the rightmost column to one line, show only directories a contributor must know about.

## Architecture narrative

Architecture documentation is *mostly* diagrams — see `references/c4-syntax.md` and `references/c4-anti-patterns.md`. The narrative around those diagrams is thin but essential.

Write structure before implementation:

1. **Model** — concepts, business nouns, states, lifecycle, and the problem they solve.
2. **Interface** — how those concepts are exposed through REST resources, commands, events, public APIs, SDK calls, scheduled jobs, or developer tools.
3. **Implementation** — databases, queues, caches, storage, framework glue, concurrency model, deployment shape, external services, and key technologies.

Architecture docs must answer **what, how, and why**: what exists, how it interacts, and why the boundaries or technologies were chosen.

### Per C4 file, include

- **Title** (`# System Context — Personal Accountant`).
- **Last updated** line.
- **One paragraph** framing the diagram: what it shows, what it deliberately omits.
- **The Mermaid block.**
- **Element notes** — bullet list, one line per container/component, explaining each element's responsibility and *why it exists as its own box*.
- **Links** to sibling diagrams (Context → Containers → Components) and to any ADR that justifies a non-obvious shape.

### Key design decisions (ADR-lite)

Inside `docs/architecture/` or a dedicated `docs/decisions/` folder. One decision per file:

```markdown
# ADR-00X: <decision>

Last updated: YYYY-MM-DD
Status: Accepted | Superseded by ADR-00Y

## Context
<what pressure forced the decision>

## Decision
<what was chosen>

## Consequences
<trade-offs accepted, including what becomes hard>
```

## API documentation

### When to write one

Any HTTP surface, SDK, or public library interface. If the project has ≥3 endpoints or ≥1 third-party consumer, it needs `docs/API.md`.

### API shape analysis

Before documenting endpoints, classify the public interface:

- **Resource-oriented** — stable nouns with standard HTTP semantics (`GET /plans`, `POST /plans`).
- **Action-oriented** — verbs or RPC-like operations (`POST /plans/consume`).
- **Event-oriented** — messages, topics, webhooks, callbacks, or streams.
- **Command-oriented** — explicit commands, jobs, or SDK calls that request work.

Then answer:

- Are names consistent across routes, DTOs, tables, UI labels, and tests?
- Does the project prefer explicit command objects, thin controllers, fat models, service layers, generated clients, or repository interfaces?
- Are errors shaped consistently?
- Are public interfaces hiding implementation details, or leaking internal table names, queue names, framework types, and storage concerns?
- Do developer-facing commands encode good practice, such as migrations, tests, scaffolding, or local setup?

### Per-endpoint structure

```markdown
### POST /api/v1/expenses

Records a new expense. Idempotent on (user_id, external_id).

**Auth**: Bearer token.
**Request**: JSON body
| Field        | Type     | Required | Notes                                |
|--------------|----------|----------|--------------------------------------|
| amount_cents | integer  | yes      | > 0                                  |
| category     | string   | yes      | One of `categories` config           |
| external_id  | string   | no       | Idempotency key                      |

**Response 201**: `{"id": "...", "created_at": "..."}`
**Errors**:
- 400 `INVALID_CATEGORY` — category not in `categories.csv`
- 409 `DUPLICATE_EXTERNAL_ID` — already recorded

**Implementation trace**:
| Concern | Source |
|---|---|
| Handler | `path/to/routes.py:42` |
| Request model | `path/to/models.py:12` |
| Response model | `path/to/models.py:33` |
| Validation | `path/to/models.py:18` |
| Domain decision | `path/to/service.py:51` |
| Persistence / side effect | `path/to/repository.py:77` |

**Example**:
```bash
curl -X POST https://host/api/v1/expenses \
  -H 'Authorization: Bearer $TOKEN' \
  -d '{"amount_cents":1299,"category":"groceries"}'
```
```

Rules:
- Show the full curl, not a schema diagram substitute.
- Document *every* error code the endpoint can emit. A reader should never hit a 5xx they can't triage from your docs.
- Call out idempotency, rate-limit class, and auth scope for each endpoint — don't hide these in a shared section alone.
- List method, path, one-sentence description, main request parameters, response structure, and handler source for every REST route.
- Cite the implementation points that matter: handler, request/response DTO, validation, domain decision, persistence/side effect, and external calls.
- Group endpoints by owning module/router. Filesystem order is less useful than model/interface ownership.

## Inline code documentation

### Principle

Comments explain **why** and **what's non-obvious**. Names explain *what*. If a comment restates the code, delete it.

Default: no comments. Add one when it names a hidden constraint, a subtle invariant, a workaround for a specific bug, or behavior that would surprise a reader.

### Docstrings

For this project, defer to `src/AGENTS.md` and `tests/AGENTS.md` for docstring rules — they are the authoritative source. For projects without explicit rules, use the language's standard:

- **Python**: Google-style or NumPy-style docstrings. Always type-hint the signature; don't re-state types in the docstring.
- **TypeScript/JavaScript**: JSDoc, but only for exported / public-API symbols. Type signatures come from TypeScript, not from JSDoc `@param {Type}`.
- **Go**: `// FuncName does X.` — full-sentence, starts with the symbol name.

### Patterns worth the ink

**Invariant**:
```python
# INVARIANT: amounts are always cents (integer). Float-valued inputs
# from upstream CSVs are rejected in data_validator.py before reaching here.
def sum_expenses(rows: list[Row]) -> int:
    return sum(r.amount_cents for r in rows)
```

**Why-this-check**:
```python
# The API returns None for deleted users and "" for users who never
# set a name. We must distinguish: deletion triggers an audit event;
# empty is skippable.
if user_name is None:
    log_deletion_event(user_id)
elif user_name == "":
    continue
```

**Workaround with a trigger for removal**:
```python
# WORKAROUND: openpyxl v3.1 raises on empty sheets. Remove this
# try/except once we upgrade past the fix in 3.2.
# Upstream issue: https://foss.example/openpyxl/issues/2345
try:
    ...
except EmptySheetError:
    return []
```

### Patterns to avoid

- Restating the code: `# increment counter` next to `counter += 1`.
- Commented-out code: delete it; git remembers.
- Change logs in comments: `# Modified by alice on 2025-03-02 to fix bug #42`. Git blame is better.
- Task-flavored comments referencing a PR or issue that will soon be closed: `# handles the case from #7812`.

## Visual-aid conventions

### File trees

ASCII, `├── `, `│   `, `└── ` characters, one-line annotations aligned on a single column. Keep under ~20 lines; split by directory if larger.

### Diagrams

**Default to Mermaid.** Use C4-flavored Mermaid (`C4Context`, `C4Container`, etc.) for architecture — see `references/c4-syntax.md`. Use plain `flowchart` or `sequenceDiagram` for non-architecture flows (algorithms, CI pipelines, state machines).

ASCII diagrams are acceptable only for tiny (3–5 box) flows embedded in prose. Anything larger becomes unreadable and unmaintainable — convert to Mermaid.

### Tables

- ≥3 parallel fields → table.
- Left column is the key, subsequent columns are attributes.
- Don't render long prose as table cells — if a cell needs a paragraph, pull it into the text below.

## Review checklist

Before declaring a doc ready:

- [ ] `Last updated:` is today.
- [ ] Every command is copy-pasteable and was actually run.
- [ ] Every code citation uses `path:line` or a named anchor — no paraphrase.
- [ ] Every Mermaid block renders (no unmatched braces, no undefined aliases).
- [ ] Every internal link resolves.
- [ ] Non-obvious constraints are stated as invariants, not implied.
- [ ] Beginner-only fluff is absent (no "in 5 minutes!", no "don't worry if...").
- [ ] The doc doesn't duplicate content that exists elsewhere — it links instead.

## Anti-patterns

| Pattern | Why it's bad | Do instead |
|---|---|---|
| "Simply run `foo`" | "Simply" implies the reader is dumb if it fails | `Run foo. Expected output: X.` |
| Full-project ASCII architecture diagram | Drifts from code within a week | Mermaid C4, diff-reviewable |
| Marketing intro paragraph | Wastes the first screen | Start with what the project *does*, one sentence |
| `// TODO: fix this` | Unattributed, unscoped, eternal | `# TODO(xhl, 2026-04-19): replace with X once Y lands — blocked by #123` |
| Docstring paragraphs that repeat the signature | Noise | One-line summary + `Args`/`Returns` only where the name isn't enough |
| "See the code for details" | The docs are the map; don't send readers back to the territory | Either include the detail or link to a specific file:line |
