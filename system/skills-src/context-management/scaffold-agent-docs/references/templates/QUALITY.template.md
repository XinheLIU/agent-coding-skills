# Quality Standards

Last updated: {{YYYY-MM-DD}}

<!-- What "done" means here, concretely enough to check. -->

## Definition of done

A change is done when:

- [ ] It works when run locally.
- [ ] Tests cover the normal path and at least one failure path.
- [ ] `{{literal test command}}` passes.
- [ ] `{{literal lint / typecheck command}}` passes.
- [ ] The commit message states what changed and what was left undone.
- [ ] `docs/` is updated if architecture or conventions changed.
- [ ] {{Project-specific gate.}}

## Review checklist

**Correctness**

- [ ] {{Project-specific correctness check — e.g. tenant isolation, permission checks, input validation.}}

**Maintainability**

- [ ] Naming follows `docs/CONVENTIONS.md`.
- [ ] Logic sits in the right layer per `docs/ARCHITECTURE.md`.
- [ ] Duplication worth extracting has been extracted.

## Test requirements

{{Induced from the existing tests: what is expected, what is conventionally skipped, coverage expectations if any.}}

## Performance and reliability

<!-- Delete if the project has no stated targets. Do not invent numbers. -->

{{Budgets or benchmarks that a change must not regress.}}

## To be added

- [ ] {{Acceptance criterion that cannot be induced from the code.}}
