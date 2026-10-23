# B7-review-seat: Put a reviewer between collect and done

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: B8-rulings, B19-evidence-binding
affects: `system/protocols/orchestration.md`; `system/skills-src/build/acs-implement/SKILL.md`; `state-schema.json`
Effort: M

## Scope

The loop dispatches, collects evidence and marks done. Nothing reviews a ticket before the whole-change review, and a failure waits for the user.

Add a review operation with two scheduler states, `in_review` and `fix_round`:

1. Record BASE before dispatch.
2. Hand the reviewer the diff plus the ticket's criteria and brief. Never pass the implementer's report.
3. The reviewer returns two ordered verdicts — spec compliance, then quality — plus "cannot verify from the diff" items.
4. Fix rounds: 1–3 resume the implementer; 4–5 use a fresh implementer; after that, a ruling (B8).
5. The coordinator never fixes code; workers do not spawn sub-agents.

Keep `acs-review-code-quality` as the whole-branch review; the per-ticket reviewer stays narrow.

## Inputs

- Analysis: §8.8 G3, §10 B7.
- Sources: Superpowers `subagent-driven-development` and `task-reviewer-prompt.md`; Addy `orchestration-patterns`; pstack `shipping`.
- Measured: reviewers given only a diff "produce confident spec verdicts that silently redefine 'spec'"; 0/5 flagged the missing brief (Vincent, 2026-06-15).

## Verification

- `grep -n "in_review\|fix_round" system/protocols/orchestration.md` shows both states and their transitions.
- A scratch run shows one ticket pass through `in_review` and return a fix round.
- A reviewer package without the brief is rejected by the orchestration rule.
- Evidence still validates the criterion → test → revision mapping.

## Blockers

B8 supplies the ruling taxonomy used after round 5; B19 supplies revision binding for BASE.

## Coordination proposal

`orchestration.md` is also edited by B8 and B19. Land B19, then B8, then B7. `state-schema.json` has one writer.

## Execution rulings

- Parent direction: B7 alone adds the per-ticket review seat; preserve accepted B8 operational retries and B19 source/evidence binding. Review fix rounds have their own persisted counter, never reset the operational retry budget, and grant no new authorization.
- Parent rulings recorded for coordination only: B23 is a stdlib Python CLI under `scripts/`, read-only by default, reusing B14/B19; B11 observability belongs in `acs-design-contracts`; B10 consumers declare verification commands and environments, unset values block execution, and checks stay local mock/scratch/dry-run without external PR/merge/deploy. These are outside B7 implementation scope.
- B17 trigger fixtures/configurable runner and B16/B17 model/budget selection remain separate work. The user-owned model/budget decision is pending; no live model result or prediction is claimed here.
- Keep shared protocol edits within B7 operation/lifecycle/review seams and necessary caller consistency. Use scratch generated output, preserve shared semantics/compaction/catalog budgets, and never edit upstream references.
- Deterministic authored traces exercise the review contract; they are not a live reviewer, host binding, or measured model-behavior evaluation. An unavailable independent review seat blocks acceptance; serial implementation remains available without authorizing delegation.

## Evidence

Implemented for independent review; `Status: in_progress` and `Readiness: needs-review` remain pending acceptance.

- Added `review(ticket, package)` between green collection and completion, with scheduler `in_review`/`fix_round` states, immutable BASE snapshot provenance, required brief/criteria/diff inputs, ordered spec/quality verdicts and explicit cannot-verify disposition. Implementer reports are excluded from initial and repeat review.
- Five persisted fix rounds resume the implementer for rounds 1–3 and use a fresh executor for 4–5, then route unresolved findings to B8 rulings. Operational retry counters remain separate; authorization, source freshness, independent review and B19 evidence checks still gate completion. Coordinator/worker role boundaries and whole-branch review remain explicit.
- Updated the scheduler schema and minimal caller/host documentation consistency seams. The historical herdr example remains unverified; no host adapter or executable scheduler was added.
- Six new `test_review_seat.py` tests cover readable positive packages; missing/blank/inaccessible/stale/report-contaminated negative packages; a scratch `in_review` → `fix_round` → `in_review` → `done` trace; ordered source contracts; five-round exhaustion and separate operational retries; stale source/input verdicts; B19 current/stale evidence; and standalone package closure. These are authored deterministic contract fixtures, not observed model behavior.
- Integrated dirty baseline copies, status, per-file hashes and contribution diff are under `.scratch/B7-review-seat/`. BASE source fingerprint: `sha256:2cefd6f2a372a4402dd09df0fdd43d986778328f290f444cec4c9dea22e5f1f9`. Tested completion fingerprint: `sha256:1a2c1e9db5cf51e013c2d4c936d03efd060384f2bebc2ceff22b67ee0fd9214e`. Scope: nonignored tracked/untracked `system/`, `scripts/`, `catalog/`, `.gitignore`, `LICENSE`; hash sorted JSON records of file bytes, symlink text and file-target bytes, or missing paths. Ticket/evidence and generated scratch are excluded. Exact commands, environment, timestamps and logs are in `verification.json`; seven passing rows validate via B19 in `evidence.json`. The failed full-suite row remains recorded separately, never relabeled green.
- Validation: focused B7 6/6 PASS; evidence regressions 19/19 PASS; suite inventory/catalog/declarations 43 skills PASS; scratch builder and `--check` PASS; protocol/package validator PASS; `git diff --check` PASS. Full source/package suite: 115/116 PASS, one preexisting B6 scope-posture text assertion failure (`Raise concerns about it once` versus compacted `Raise concerns once`). Both implicated files exactly match captured baseline and were preserved. Configured tokenizer compaction checks, shared semantics and catalog-budget tests passed in that run.
- An initial focused run found a test-only call to a nonexistent checker API; corrected to B19's `evidence_errors` and reran. No dependencies, subagents, commits, installs, pushes or publication. No staged files.
- Unverified: actual reviewer judgment, missing-brief rejection by a live host, resume/fresh-executor behavior and review-loop reliability under real model execution. Fixtures and prose do not establish runtime enforcement. B16/B17 model/budget selection is still pending outside B7. Next step: independent acceptance review of the contribution diff; reconcile the unrelated baseline assertion in its owning task.

## Parent acceptance

2026-10-23: integrated source accepted after 152 suite tests, build/check, both validators and [independent review](../evidence/fifth-batch-review.md). Acceptance is the source contract and explicitly described local scripted exercises. It does not certify live agent/host enforcement, real PR/release actions, or production telemetry. No external operation was performed.
