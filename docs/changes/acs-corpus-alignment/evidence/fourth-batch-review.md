# Fourth batch acceptance review

Last updated: 2026-10-23

## Review

No issues found.

- **Correct — B21 greenfield routing is repaired.** [acs-shape-solution/SKILL.md:27](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/plan/acs-shape-solution/SKILL.md:27) explicitly says “greenfield uses problem/demand context” and restricts baseline mapping to “Existing-product work needing a missing/stale baseline.” The surrounding demand-validation gate, authorized exploratory exception, settled-solution routing, scope approvals, and persistence rules remain intact.

- **Correct — B21 dynamic announcements are restored.** [acs-design-interaction-flow/SKILL.md:32](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/design/ux/acs-design-interaction-flow/SKILL.md:32) now requires “live regions for dynamic state updates and error announcements.” Keyboard navigation, responsive breakpoints, touch targets, contrast, reduced motion, five-state coverage, and approved-surface boundaries remain present.

- **Correct — assertions cover both repairs and their packaged forms.** [test_compaction_safe_bodies.py:35](/Users/xhl/GitHub/skills/agent-coding-skills/system/evals/tests/test_compaction_safe_bodies.py:35) includes both restored contracts. Source, plugin, and relocated standalone checks enforce their presence inside the bounded prefix; negative checks reject removed rules and overflow. Generated plugin copies contain the corrected wording. The retained [focused test log](/Users/xhl/GitHub/skills/agent-coding-skills/.scratch/acs-corpus-alignment/review-fix-compaction.log:1) records all five tests passing without skips.

- **Correct — B21 evidence now distinguishes historical and integrated validation.** The [appended evidence:58](/Users/xhl/GitHub/skills/agent-coding-skills/docs/changes/acs-corpus-alignment/tasks/B21-compaction-safe-bodies.md:58) supersedes the initial byte-only account. It identifies the cached tokenizer by SHA-256, records **1,929 / 1,999 / 2,004 tokens** for source / standalone / plugin, describes missing configuration as unverified/skipped, and explicitly disclaims current-host certification or live compaction proof. Those counts match the saved configured test output.

- **Correct — previous B8/B13 findings remain valid.** [orchestration.md:55](/Users/xhl/GitHub/skills/agent-coding-skills/system/protocols/orchestration.md:55) retains the persisted two-retry limit, authorization stops, and unknown-side-effect protection; the implementation caller still routes through that policy. The [security rubric:40](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/test/review/acs-review-code-quality/SKILL.md:40) retains separate severity/confidence/evidence judgments, entrypoint/boundary/impact requirements, unknown-reachability treatment, candidate exclusions, and a conclusion-withholding independent challenge.

- **Correct — previous B24/B25 findings remain valid.** The [host-duty table:48](/Users/xhl/GitHub/skills/agent-coding-skills/system/docs/harness-architecture.md:48) retains all four duties, explicit unavailable bindings pending verification, and the distinction between manual approval and hook enforcement. Both [root README:9](/Users/xhl/GitHub/skills/agent-coding-skills/README.md:9) and [system README:7](/Users/xhl/GitHub/skills/agent-coding-skills/system/README.md:7) retain the audience, lighter alternative, Bounded default, approval reuse, and upward tier changes.

**Verification limits:** Read-only source, generated-output, test-code, prior-review, and saved-log inspection. No commands executed or files changed. Builder execution is supported by its saved log; post-fix validator passes remain parent-reported. This was a focused re-review of the corrections and named contracts, not a whole-repository audit.

**Merge verdict: OK** for the reviewed scope.

BLOCKERS: none