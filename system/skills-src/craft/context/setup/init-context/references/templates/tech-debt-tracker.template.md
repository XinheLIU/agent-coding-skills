# Technical Debt

Last updated: {{YYYY-MM-DD}}

<!-- Code that exists but was built badly. Not unbuilt features — those go in backlog.md. -->

Format: `[high|medium|low] Problem — blast radius`

## Open

- {{[high] Problem — what it affects, and what it blocks}}
- {{[medium] Problem — what it affects}}

<!-- If the scan found nothing concrete, keep it empty and say so:

     None recorded yet. Add items as they surface.

     An honest empty list is more useful than invented debt, which sends people
     to refactor code that is fine. -->

## Signals worth recording

When scanning, these usually indicate real debt:

- The same logic duplicated across several places.
- One concept with several names.
- `TODO` / `FIXME` / `HACK` comments.
- Files large enough that nobody reads them end to end.
- Core modules with no tests.
- Dependencies pinned to a version nobody dares to bump.

## Resolved

<!-- Kept as a record of what was paid down and when. -->

- {{Problem — resolved {{YYYY-MM-DD}} by {{what changed}}}}
