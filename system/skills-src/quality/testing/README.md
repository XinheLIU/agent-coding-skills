# Quality · Testing

Last updated: 2026-09-12

The skills from this sub-phase have been relocated.

| Skill | Moved to | New name |
| --- | --- | --- |
| `tdd` | `build/tdd` | `tdd` (unchanged) |
| `analyze-test-gaps` | `test/analyze-test-gaps` | `analyze-test-gaps` (unchanged) |

`tdd` moved to `build/` because test-driven development is part of the implementation loop, not a post-build quality step. `analyze-test-gaps` moved to `test/` because coverage audits and integration test gaps are addressed after build is complete.

See [`build/README.md`](../../build/README.md) and [`workflows/test.md`](../../../workflows/test.md).
