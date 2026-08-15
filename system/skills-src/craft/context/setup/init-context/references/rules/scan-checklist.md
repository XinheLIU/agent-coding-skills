# Scan Checklist — 10 Categories

Last updated: 2026-08-02

Loaded by extract-rules Step 2. For each category, sample 3–5 representative files. Don't exhaustively read.

For every category, report: **Status** (`Established` / `Partial` / `Missing`), **current convention** (one line), **evidence** (2–3 `file:line`), **constraint type** (static / dynamic / implicit).

## 1. File & Directory Structure

What to look for:
- Folder layout: `src/` vs flat? `tests/` vs co-located? `lib/` vs `pkg/`?
- Module separation: by feature, by layer, or mixed?
- File naming: `kebab-case.ts`, `snake_case.py`, `PascalCase.java`, `camelCase.js`?
- Index/barrel files: `index.ts` re-exports? `__init__.py` populated?

Where to find evidence: top-level `ls`, sample files in each major directory.

Constraint type: usually **static** (path conventions are global).

## 2. API Endpoint Conventions

What to look for:
- URL paths: `/api/v1/users`, `/users`, `/v1/api/users`?
- HTTP method usage: PUT for full updates, PATCH for partial? POST for actions?
- Query param naming: `?user_id=` or `?userId=`?
- Response envelope: `{data: ..., error: ...}`, `{result: ...}`, raw?
- Error format: HTTP status + JSON body? Custom error codes?

Where to find evidence: route files (`routes/`, `controllers/`, `api/`), OpenAPI spec if present.

Constraint type: **static**, path-scoped to api directory.

## 3. Code Formatting

What to look for:
- Indentation: tabs vs spaces, 2 vs 4?
- Line length: 80, 100, 120?
- Brace style: K&R, Allman, none (Python)?
- Trailing commas, semicolons (JS/TS)?
- Formatter in use: prettier, ruff, gofmt, rustfmt, black, clang-format?

Where to find evidence: `.editorconfig`, `prettier.config.js`, `pyproject.toml [tool.black]`, `[tool.ruff]`, `.clang-format`, `Makefile`/`package.json` `format` script.

Constraint type: **static**, global. Prefer linter config over prose rule.

**Language notes:**
- Python: ruff or black + isort. Check `pyproject.toml`.
- JS/TS: prettier. Check `prettier.config.*` or `.prettierrc`.
- Go: gofmt is canonical (no config).
- Rust: rustfmt with `rustfmt.toml`.

## 4. Naming Conventions

What to look for:
- Variable/function casing: `snake_case`, `camelCase`?
- Class casing: `PascalCase` is near-universal but verify.
- Constants: `UPPER_SNAKE_CASE` or just module-level `camelCase`?
- File naming (cross-check with category 1).
- Boolean prefixes: `is_`, `has_`, `should_`?
- Abbreviation rules: `URL` or `Url`? `ID` or `Id`?

Where to find evidence: 5 random source files across the codebase.

Constraint type: **static**, global.

## 5. Database Conventions

What to look for:
- Table naming: singular (`user`) or plural (`users`)? `snake_case`?
- Column naming: `created_at` vs `createdAt`? `user_id` vs `userId`?
- Primary keys: `id` vs `<table>_id`?
- Foreign keys: `<other_table>_id` or `fk_<table>_<other>`?
- Indexes: `idx_<table>_<column>` or `<table>_<column>_idx`?
- Timestamps: `created_at` / `updated_at` always present?
- Soft delete: `deleted_at` column? `is_deleted` flag? hard delete only?
- Enums: stored as strings, ints, or DB-native enum types?

Where to find evidence: migrations directory, ORM model files, schema files.

Constraint type: **static**, path-scoped to models / migrations.

## 6. Logging Standards

What to look for:
- Log levels in use: which of TRACE/DEBUG/INFO/WARN/ERROR?
- Format: structured JSON, key-value, plain text?
- Logger library: `logging` (Python), `winston`/`pino` (Node), `slog` (Go)?
- Mandatory fields: timestamp, module, trace ID, request ID, user ID?
- Where: at entry points only, every function, on errors only?

Where to find evidence: any 5 files with logging calls; logger config file.

Constraint type: **static**, global.

## 7. Security Practices

What to look for:
- Input validation: framework validator, manual, schemas (zod/pydantic)?
- SQL injection: parameterized queries everywhere? ORM-only?
- XSS prevention: framework auto-escape? manual encoding?
- Auth/authz: middleware-based? per-handler decorator? token type (JWT, session)?
- Secret management: env vars, vault, encrypted config file?
- CORS: allow-all, allow-list, configurable?
- Rate limiting: present? per-endpoint or global?

Where to find evidence: middleware files, validators, config loader, auth module.

Constraint type: **static**, global. Often elevates to AGENTS.md cross-runtime.

## 8. Version Control Conventions

What to look for:
- Commit message format: Conventional Commits (`feat:`, `fix:`)? Prefixed (`[bugfix]`)? Free-form?
- Branch naming: `feature/`, `fix/`, `chore/`? main vs master?
- PR/MR requirements: required reviewers, required CI checks?
- `.gitignore` completeness: env files, build artifacts, IDE configs?
- Hooks: husky, pre-commit, lefthook?

Where to find evidence: `git log --oneline -20`, `.git/hooks/`, `.husky/`, `.pre-commit-config.yaml`, `CONTRIBUTING.md`.

Constraint type: **static**, low-enforcement. Document in `docs/spec.md` rather than `.claude/rules/`.

## 9. Comments & Documentation

What to look for:
- Docstring style: JSDoc, Google, NumPy, reST, none?
- Required locations: public APIs only, all functions, none?
- Inline comments: convention for TODO/FIXME/HACK/XXX?
- Changelog: `CHANGELOG.md` maintained? auto-generated?

Where to find evidence: 5 source files; check `CHANGELOG.md` last commit date.

Constraint type: **static**, global. Often handed off to `codebase-documenter`.

## 10. Environment & Configuration

What to look for:
- Config file format: `.env`, YAML, TOML, JSON, Python module?
- Secret handling: env vars, vault, encrypted file?
- Config loading: env-loaded at startup? hot-reload? layered (default → env → CLI)?
- Environment separation: dev/staging/prod files? single file with env switches?
- Hardcoded values: any URLs, paths, magic numbers in source?

Where to find evidence: `.env.example`, `config/`, `Settings`/`Config` class, `os.getenv` calls.

Constraint type: **static**, global.

## Sampling tactics

- **Top-down:** start from project root, descend into the 2–3 largest directories.
- **Test files first:** test conventions often surface naming and structure rules clearly.
- **Recent commits:** `git log --oneline -50` shows commit format and recent patterns.
- **Config-first:** linter and formatter configs answer Categories 3, 4, 9 instantly — read them before sampling source.

## Constraint type quick reference

- **Static** — applies to all code, all the time. Default classification for categories 1–10.
- **Dynamic** — only mentioned in some files (e.g. "limit edits to these files this task"). Surface as a meta-pattern in `docs/spec.md` §Workflow Norms, not as a category 1–10 rule.
- **Implicit** — embedded in HTML comments, sidebar notes, or non-obvious markers. Discover via grep for `<!-- DO NOT`, `# DO NOT`, `// DO NOT`, "PARTNER", "EXTERNAL CONSUMER".
