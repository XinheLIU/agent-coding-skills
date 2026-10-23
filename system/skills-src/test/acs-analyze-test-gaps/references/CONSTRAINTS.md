# Constraint floor

Last updated: 2026-10-23

Use this guide to draft or reconcile the target repository's root `CONSTRAINTS.md`
when constraint analysis is in scope. It is not an ACS-wide numeric quality policy.
Read existing constraints, accepted criteria, test commands and CI configuration
first. Preserve their authority; do not invent coverage or performance targets.
Resolve genuine missing decisions through [Questioning](../../../../protocols/questioning.md).
Missing thresholds do not prevent running the floor guard or independent analysis.

The analysis skill may write a proposed constraint record as an analysis artifact;
implementation owns adopting commands or changing source, tests, configuration and
CI. No checker installation or hook wiring is implied by this guide.

## Floor

- Thresholds: do not lower a minimum, raise a maximum, remove a check, or defer its required stage to claim success.
- Tests: do not skip, delete or weaken a valid test to make the result green.
- Suppressions: report new checker suppression comments rather than hiding their effect.
- Catches: report newly empty or stubbed error handlers and unimplemented error stubs.
- Exceptions: a new or changed exception is a review finding, never automatic permission to pass.

## Placement by cost

Put each required check at the cheapest stage that can observe its claim. Record
measured runtime and the acceptable budget; the labels below are placement tiers,
not new lifecycle rigor tiers. A cheap floor scan runs before expensive verification
and again against the final diff before a readiness claim. It cannot replace tests.

| Stage | Cost and scope | Evidence required |
| --- | --- | --- |
| Edit loop | Seconds; diff floor guard and existing fast type/lint checks | Exact command, scope, result and revision/diff fingerprint |
| Task end | Related tests and coverage from the same run; cost within the accepted task budget | Criteria/contracts mapped to tests and outcomes; skipped/not-run checks stay visible |
| CI or runtime | Costly integration, security, mutation, performance or accessibility checks where dependencies exist | Actual environment, scope, runtime and result; a deferred required check blocks its readiness claim |

Move a slow check out of the edit loop by an accepted placement decision, without
silently removing its task/CI obligation. Reuse coverage already produced by the
standard test run. Do not run the test suite a second time merely to get coverage.
For repeated mistakes prefer architecture, types, then existing static checks, then
behavior tests; prose alone is the fallback for judgment that cannot be automated.

A target record should contain stable rule IDs, reason/criterion, explicit direction
(`>=` for minimum, `<=` for maximum), accepted or measured baseline, exact command,
required stage, budget and owner. Distinguish measured-only metrics from enforced
checks. Commands in wrappers must agree with the record. Example shape only:

```markdown
# Constraints

Last updated: <YYYY-MM-DD>

## Enforced checks

| ID | Rule and rationale | Checked by | Stage | Budget | Owner |
| --- | --- | --- | --- | --- | --- |
| <stable ID> | <accepted rule, direction and criterion> | <existing command> | <edit/task/CI> | <accepted cost> | <owner> |

## Measured only

| ID | Metric and direction | Measured by | Revision |
| --- | --- | --- | --- |
| <stable ID> | <measured baseline; not an enforced target> | <command> | <fingerprint> |

## Exceptions

| ID | Rule | Path | Reason and approval record | Owner | Expires |
| --- | --- | --- | --- | --- | --- |
```

## Run the guard

Run the packaged [floor guard](../scripts/floor_guard.py) with Python 3.10+ and Git.
Resolve its path relative to this skill; pass the accepted base explicitly:

```sh
python3 <skill-directory>/scripts/floor_guard.py --repo <target-repository> --base <accepted-base-ref>
```

The guard reads the merge base with `HEAD` through the working tree: committed,
staged and unstaged final changes plus non-ignored untracked files. Starting in a
subdirectory still scans the entire repository. It neither executes project checks
nor writes, stages or fixes anything. Renames are treated as deletion plus addition
so a renamed test cannot conceal lost assertions. Deleted-line locations use the
old file; other locations use the new file, both one-based.

| Exit | Meaning | Effect on claims |
| --- | --- | --- |
| 0 | No supported silencing patterns found in this diff | Floor scan only; no overall green claim |
| 1 | Findings name file, line, side and one of the five moves | Refuse green until reviewed and resolved against canonical criteria |
| 2 | Input/merge base unavailable or unsupported | Incomplete verification; never interpret as clean |

JSON includes `merge_base`, `diff_sha256`, `files_scanned`, `status`, findings, and
`green_claim: false`. It omits matched source text and Git error output. Bind the
command, actual completion timestamp/timezone, environment, exit code and this
fingerprint to canonical [engineering evidence](../../../../protocols/engineering-memory.md).
Preserve the dispatch base and previous failures; a later run does not erase them.
A changed diff invalidates this scan's evidence.

This is a conservative textual detector, not a semantic verifier. Supported patterns
include common JS/Python/Go test skips, removed assertions in conventional test
paths, common suppression directives, JS empty catches, Python `except: pass`, and
unimplemented error stubs. Assertion replacements and renames may need review even
when legitimate. It does not prove replacement assertion equivalence or interpret
arbitrary languages or external checker configurations. Numeric ratchets apply to
stable rows/bullets in files named `CONSTRAINTS.md`; unknown numeric directions,
removed rules and nonnumeric command/stage edits are reported for review. New or
changed rows under `## Exceptions` remain findings even when approved; the approval
record supplies disposition, not a bypass switch. Removing an exception is silent.

Ordinary Markdown is documentation and is not scanned for code-like patterns.
Ignored files are outside scope. Binary changes, changed symlinks/submodules,
unreadable inputs and duplicate table rule IDs return unavailable instead of clean.
Record any language/configuration gaps as unassessed; review the actual diff and
run the required checks before deciding readiness. Fix valid violations in their
owning workflow; report false positives and accepted exceptions with evidence and
owner/expiry, without auto-fixing or suppressing the finding.

## Provenance

Adapted principles: Addy Osmani's `constraint-driven-development` and
`references/floor-guard.md` at `aeac41d` in
[agent-skills](https://github.com/addyosmani/agent-skills), and pstack `correct` at
`0b8e952` in [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack).
The guard is an ACS stdlib implementation, not a copied upstream runtime. ACS uses
canonical Questioning and evidence ownership instead of upstream interview and
installation procedures.
