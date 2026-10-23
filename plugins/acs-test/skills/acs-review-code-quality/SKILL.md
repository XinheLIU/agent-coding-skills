---
name: acs-review-code-quality
description: Use when code or a PR needs production-readiness review, spec or standards checks, or investigation of open architecture findings.
---

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [source.review_scope]
  retrieves: [change.requirements, design.contracts, design.architecture_findings, verification.trace_matrix, repository.standards, verification.latest_evidence]
  produces: [verification.standards_findings, verification.spec_findings]
  updates: [change.review_evidence]
  invalidates: [verification.unsupported_readiness]
  handoff_to: [implementation, testing, operations]
```

Shared semantics: [shared protocol](../../resources/protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../resources/protocols/presenter.md); source records retain authority.

# Code Quality Review

## Procedure

0. Mode/scope: A recent diff (default; explicit path/range or active+WIP); B whole/spec (requested; root/local AGENTS.md/rules); C open FND-ARC files. Ambiguous → ask; invalid/empty → stop; no B rules → fallback/abort; no C findings → ask/A; too large → narrow. Canonical criteria/design/revisions, never newest report; match TRC identity/revisions. Keep omissions/deviations; no criteria → Spec unassessed.
1. api/db/auth/reliability/performance/security/code [lenses](references/domain-lenses.md), unless narrowed. Delegate if allowed, else inline; failures inline/unassessed. Pass scope/revisions/criteria/environment/parent findings/omissions.
2. Always inline: DRY/boundaries/errors/empty/max/timeouts/retries/over/under-engineering/naming/state/comments/diagrams. Fowler smells are judgments; repo overrides; skip tool checks. Spec: missing/partial/wrong/extra, cite lines/TRC; never narrow criteria. Note issue-free files.

**Interactive flow.** Apply [review evidence gate](../../resources/protocols/engineering-memory.md#review-evidence-gate) before confidence ≥ 7 enters [questioning](../../resources/protocols/questioning.md): mechanical recorded, taste at gate, user frontier in order. file:line; 2–3 one-sentence options (do nothing if reasonable), recommendation/reason. No answer → UNRESOLVED.

## Evidence identity

Retain task/criteria/contract/code/diff revisions, environment/failures/skips/omissions; reassess changes. A static code review cannot stand in for executed acceptance evidence.

**If you cannot quote the motivating line, the finding is unverified**: inspected file:line/quote/revision; never invent. Cap 5/10, never raise lower; appendix only. Quote necessary, insufficient. **Code that handles a deliverable is not the deliverable**: inspect artifact; unavailable → `UNVERIFIABLE`, not `DONE`, exact next check. Handler tests prove no delivery.

3. Diagram added/modified function branches/guards/errors/returns: tests/gaps, ★★★ behavior+edges+errors / ★★ happy / ★ smoke. Untested changed behavior → CRITICAL regression test, no question; prompts need evals.
4. Performance ≥7: N+1/unbounded loops/hot sync I/O/leaks/repeated costs. Scan added lines: secrets/shell injection/eval/exec/pickle/formatted SQL ([commands](references/review-formats.md#security-scans)); inspect, no automatic Critical.
### Security evidence rubric

Apply to security claims from every lens, including auth and db. Scanner matches are candidates; inspect surrounding code.


Keep these fields separate; neither severity, a scanner warning, nor reviewer agreement proves a claim. The existing review evidence gate still applies.

| Field | Required judgment |
| --- | --- |
| Severity | P0/P1/P2 with concrete impact and realistic attacker prerequisites; label hypothetical impact as conditional. A pattern or advisory score alone is insufficient. |
| Confidence | N/10 with rationale, unknowns and counterevidence; do not raise confidence merely because severity is high. Unquoted claims remain unverified at ≤ 5/10. |
| Evidence state | `candidate`, `supported-static`, `supported-reproduced`, or `disproved`, under the rules below. Static tracing never proves runtime execution or a tested repair. |

Every security finding, including an unresolved candidate, records all three evidence parts with source revisions and inspected quotes, or explicitly records `unknown` and the next check:

1. **Entrypoint:** the attacker-controlled input, caller and prerequisites. Trust follows who wrote a value, including environment, job and model inputs.
2. **Boundary crossing:** the concrete path from that input across the intended security boundary, its invariant and relevant protective controls (callers, middleware, configuration, validation and legitimate behavior).
3. **Demonstrated impact:** the specific unauthorized effect and its evidence. A complete static trace can demonstrate the effect logically; an executed reproduction must additionally cite the actual command, environment and observed security assertion with a legitimate control. Keep missing evidence explicit.

`candidate` means one or more parts or relevant control checks remain unresolved. `supported-static` requires all three parts and inspection of relevant controls; `supported-reproduced` additionally requires recorded execution evidence. `disproved` requires concrete counterevidence defeating the scoped claim; retain it as disposition evidence, not a vulnerability. **Unknown reachability remains unknown, not unreachable.** Record reachability separately as `reachable`, `unknown`, or `unreachable`; only inspected evidence ruling out the path in the stated scope permits `unreachable`. Missing hardening alone needs a concrete failure scenario.

Keep candidates and disproved claims in separate appendix subsections, outside supported totals, priorities and blocking verdicts. Supported findings still obey the quote gate and existing confidence/axis rules; `supported` never means a repair passed or the review is complete.

**Independent challenge.** When an authorized independent reviewer is available, give it only a neutral ID, scope/revision, locations and source evidence, boundary invariant, environment assumptions and this rubric. Withhold the producer's conclusion, severity, confidence, evidence-state label and proposed fix until the challenger records its own assessment. Have it inspect callers, middleware, configuration, validation, legitimate behavior and mitigations. Preserve the exact input and response, dissent, assumptions and reconciliation; reconcile against evidence, never by vote. If independence is unavailable, label the separate skeptical pass `sequential challenge; independent reviewer unavailable` and retain that limitation. Do not expand access or claim an independent transcript from a self-review or authored example.


## Consolidation

5. Dedupe file:line/lenses/axis. Standards and Spec separate, never reranked together. Route design-level issues to separate ARC/MOD/CON/TST cross-references, never code findings; authn/authz architecture → ARC/CON ([routing](references/review-formats.md#design-routing)). Per axis: CRITICAL bugs/regressions/security/data loss/missing regression tests; IMPORTANT gaps/P1/perf; NICE-TO-HAVE style/refactors/P2. Dependency order; what/why/files/deps/human+AI effort.
6. Either axis HIGH/MEDIUM Critical → NOT-READY; warnings → READY-WITH-FIXES; suggestions only → READY. Code Criticals (>21 complexity, changed logic zero tests, ice-cream-cone pyramid) block. Return report path/mode/lenses/findings/coverage/priorities/verdict.

## Completion criteria and hard rules

Findings: `[P0|P1|P2] [Standards|Spec] (confidence: N/10) file:line`; `Evidence: <verbatim motivating line(s), source revision>`; Verification quoted/unverified, missing/next check. Quoted ≠ executed.

Confidence rules (the [review evidence gate](#evidence-identity) takes precedence):
- Unquoted: `unverified`, ≤5, appendix only; excluded from main findings, priorities, and blocking verdicts.
- Quoted 9–10 code-verified; 7–8 strong pattern; 5–6 medium confidence, verify; ≤4 appendix only.

Write `docs/eng-reviews/next-steps-{branch}-{YYYYMMDD-HHMM}.md`: verdict/scope/revisions/spec/summary/strengths, axis priorities, appendix/unverified entries, coverage/domains ([format and provenance](references/review-formats.md)). Missing lenses never pass. Apply blast radius/on-call/complexity/reversibility.

<!-- compaction-core:end -->
