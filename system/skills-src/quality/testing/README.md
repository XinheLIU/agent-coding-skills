# Quality · Testing

Last updated: 2026-09-09

Ensuring code does what it claims through automated verification and test coverage analysis.

| Skill | Owns |
| --- | --- |
| `tdd` | Test-driven development workflow — write the failing test first, then make it pass; routes spec and quality review to `review-implementation-gaps` / `review-code-quality` rather than embedding its own |
| `analyze-test-gaps` | Audit existing test coverage; identify untested paths and missing edge cases |

`tdd` drives criterion-based behavior slices and returns evidence and proposed reviews to the coordinator. Canonical ticket status stays in its tracker; final verification retains criteria, revision, environment, failures, and omissions in Change Context. `analyze-test-gaps` is a review tool used after the fact or before a large refactor.
