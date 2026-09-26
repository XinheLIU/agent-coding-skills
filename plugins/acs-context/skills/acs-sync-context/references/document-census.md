# Document Census

Last updated: 2026-09-26

Procedure for the census, effort verdicts, and why-extraction steps of [`acs-sync-context`](../SKILL.md). Classification vocabulary and the two axes live in [the layout guide](../../acs-init-context/references/canonical-doc-layout.md); retention law lives in [the protocol](../../../resources/protocols/skill-declarations.md).

## Boundary

```bash
git ls-files '*.md' '*.html'
```

Report untracked candidates from a separate named scan. Do not walk the filesystem for the boundary: a bare `find` descends into vendored corpora that repository instructions forbid touching, inflating the count with files no disposition applies to.

Read the configured `## Not context` rules from memory configuration before deriving any. They are a reviewed repository fact; re-deriving them each run invites disagreement between runs.

Narrow the boundary to changed paths in Fast mode. Fast mode then reports a scoped finding list and claims no completeness.

## Accounting

Each document lands in exactly one classification row, or inside one named exclusion rule carrying its file count. Classified rows plus excluded counts equal the scan count. State that arithmetic; it is what makes the census reviewable, and "etc." breaks it.

Exclusion rules name a path pattern, its reason code, and its count:

| Rule | Reason | Files |
| --- | --- | --- |

Classified rows carry evidence and destination:

| Path | Class | Disposition | Basis | Why destination | Owner |
| --- | --- | --- | --- | --- | --- |

`Basis` carries evidence and age together — a revision or tag plus the commit-measured age, for example `v0.4.0 / 17c3eb2 · untouched 4d`. `Why destination` is `—` for every row except `PROMOTE` and `EXPIRE`.

## Effort state

Decide each `WORKING` row from repository evidence. First match wins:

| Evidence | Verdict |
| --- | --- |
| A tag, release, or merged commit whose message or scope names the effort | `COMPLETE` |
| The effort's target structure exists at the paths it states | `COMPLETE` |
| Target structure partial, named absent items still absent, the document or its ticket touched inside the window | `PARTIAL` |
| Target structure partial, an open ticket, branch, or recent commit references the effort | `ONGOING` |
| No target structure, nothing referencing it, untouched past the window | `ABANDONED` |

A document's own checklist is not evidence of its state. Unchecked boxes in a shipped effort show the checklist was abandoned, not the work. Measure age with `git log -1 --format=%ad -- <path>`, never a `Last updated` line.

`PARTIAL` and `ONGOING` rows keep their documents. Name what remains and route it to its owner instead of expiring the record that tracks it.

## Extract the why

For each `PROMOTE` or `EXPIRE` row:

1. **Separate.** Split the document into rationale — why this shape, what was rejected, what constraint forced it, what was deliberately left out — and procedure: steps, task assignments, file manifests, checkboxes, estimates. Procedure is what the shipped diff already encodes.
2. **Test each rationale item** against the three conditions in [the ADR bar](../../acs-init-context/references/ADR-FORMAT.md#when-to-offer-an-adr). Items that pass become one ADR per decision at the configured decision-record home, `Status: accepted`, `Basis:` naming the tag or commit that shipped it. Items that are durable but fail the bar go to the relevant Persistent Current document or change record.
3. **Write one changelog line** under the shipping version heading, or under the unreleased heading when no tag exists yet, to be backfilled at release. It says what changed, why in a subordinate clause, and links the ADR and the release reference. The tag carries the how and the what.
4. **Verify with the source unavailable.** A reader with only the ADRs and the changelog line must be able to answer why the repository is shaped this way, and every link must resolve. Incomplete extraction leaves the row unexpired.

One ADR per decision, not one per document. A long plan may yield two ADRs and one changelog line, or zero ADRs and one changelog line when nothing meets the bar. An ADR that compacts a document's contents recreates that document under a new name.

This skill may write an ADR whose content is historical: accepted, with its basis being the revision that shipped it, and no open question. An ADR that decides anything still open belongs to the design owner; route it there and keep the source document until the decision lands.

## Present and confirm

Persist the census to the configured recovery entry's run directory as `context-census.md` before presenting. The confirmation is a review decision, and [the Presenter contract](../../../resources/protocols/presenter.md) requires reviewed content stay retrievable.

Present one message in this order:

1. **Scope** — one line: mode, baseline, and counts, including how many were classified and how many excluded by how many rules.
2. **Exclusions** — the rule table, a line per rule. It answers "did you look at everything" before the reader wonders.
3. **Classified rows grouped by disposition**, least destructive first. Collapse `OK` to a count. Expand `DELETE` and `EXPIRE` last and in full, every path spelled out with its basis and why destination.
4. **The close** — state what is established from tag, commit, or shipped-structure evidence; what rests on age alone, named as an assumption with its consequence; and where repository evidence and a document's own claims disagree, with the observation that settles it.
5. **One question per disposition group** — confirm, amend named rows, or decline. Not one question per file: a retention sweep is a batch decision, and twenty sequential prompts is the same defect in another costume. Declining ends the run with the census as the deliverable.

The table is a view. The classification is the domain result; layout carries no conclusion the census record lacks. Markdown in conversation suffices; add an HTML companion under [the visual report template](../../../resources/skills-src/authoring/references/visual-report.md) only when the census exceeds roughly thirty classified rows.

Record the retention outcome as a Persistent Changes entry — usually the same changelog line from step 3 above — naming what was removed and on what basis. Without it a run removes durable records and then removes the only account of why.
