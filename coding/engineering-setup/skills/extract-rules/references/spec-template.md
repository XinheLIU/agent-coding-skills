# `docs/spec.md` Template

Last updated: 2026-07-18

Loaded by extract-rules Step 5 when authoring or updating `docs/spec.md`. If the file already exists, **diff don't overwrite** — change only what's new or revised.

## Authoring rules

- **DRY.** If a convention is documented elsewhere (`docs/database-schema.md`, OpenAPI spec), link to it. Do not duplicate.
- **Reference, don't restate.** For Tier 1 rules in `.claude/rules/<topic>.md`, the spec section body is a single link line.
- **Concise.** One spec entry = one rule. No essays. Use tables when listing many rules.
- **Mark deferred items.** Use `<!-- TODO: decide on X -->` so deferred categories are easy to find later.
- **Status markers.** For each section, optionally tag `[Established]`, `[Partial]`, `[Deferred]` next to the heading.

## Skeleton

```markdown
# Technical Specifications

Last updated: YYYY-MM-DD

> Auto-maintained by `extract-rules`. This document indexes the project's technical
> conventions. All contributors (human and AI) should follow these rules.
> For active enforcement, see `.claude/rules/`.

## 1. File & Directory Structure

→ See [`.claude/rules/structure.md`](../.claude/rules/structure.md)

(or, if no rules file exists yet:)

[Established] Modules are organized by feature under `src/<feature>/`. Tests
live alongside source as `<name>_test.py`. See `src/api/` for the canonical example.

## 2. API Endpoint Conventions

→ See [`.claude/rules/api.md`](../.claude/rules/api.md)

## 3. Code Formatting

→ Enforced by `ruff` (config in `pyproject.toml [tool.ruff]`). Run `make format`.

## 4. Naming Conventions

→ See [`.claude/rules/naming.md`](../.claude/rules/naming.md)

## 5. Database Conventions

→ See [`.claude/rules/database.md`](../.claude/rules/database.md). Schema reference: [`docs/database-schema.md`](./database-schema.md).

## 6. Logging Standards

→ See [`.claude/rules/logging.md`](../.claude/rules/logging.md)

## 7. Security Practices

→ See [`.claude/rules/security.md`](../.claude/rules/security.md). Cross-runtime requirements also in [`AGENTS.md`](../AGENTS.md).

## 8. Version Control Conventions

[Established] Conventional Commits format (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`).

[Established] Branch naming: `feature/<short-desc>`, `fix/<issue-id>`, `chore/<short-desc>`.

[Partial] PR template exists at `.github/pull_request_template.md` but is not enforced.

## 9. Comments & Documentation

[Established] Public functions use Google-style docstrings. Private helpers may omit docstrings if the name is self-evident.

<!-- TODO: decide on changelog format — currently maintained inconsistently -->

## 10. Environment & Configuration

[Established] Config loaded from environment variables via `src/config.py`. `.env.example` is the canonical reference; production secrets are managed in [redacted vault].

## Workflow Norms

Dynamic per-task patterns this team follows. These are *not* statically enforced — they describe how the team typically wants the agent to behave.

- This team typically narrows edit scope per task. If a task doesn't name specific files, ask before broadening.
- Plan confirmation is the default for changes spanning more than ~3 files. Surface a plan and wait for approval.
- Prefer pause-and-ask over best-guess when requirements are ambiguous.

## Implicit Conventions

Hidden norms surfaced from comments and sidebar notes. Update when adding similar markers.

| Location | Marker | Convention |
|---|---|---|
| `docs/onboarding.md:42` | `<!-- Do not delete -->` | Section is referenced by onboarding flow |
| `src/api/partner.py:12` | `# NOTE: Consumed by Partner A` | Signature must remain stable |
| `scripts/cron.py:1` | `# DO NOT MOVE` | Path is hardcoded in external CI |
```

## Update-don't-overwrite checklist

When `docs/spec.md` already exists:

1. Read the existing file.
2. For each section, classify the new content as: **identical** (skip), **revised** (replace section body), **new** (add section), **removed** (only if the user explicitly approved removal).
3. Preserve `Last updated:` only if the file genuinely didn't change. Otherwise bump to today's date.
4. Preserve manually-added narrative the user wrote in between standard sections — do not overwrite it.
5. Re-run cross-link checks: every `→ See [...]` should resolve.

## DRY checks

Before saving:

- Search the file for the same fact twice. Resolve to one canonical home.
- Confirm every `→ See [...]` link resolves.
- If a rule body appears in `docs/spec.md` and also in `.claude/rules/<topic>.md`, remove it from `docs/spec.md` and link instead.
