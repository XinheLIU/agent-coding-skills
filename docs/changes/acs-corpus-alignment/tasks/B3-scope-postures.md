# B3-scope-postures: Give the scope postures a home or delete the dangling reference

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: done
Readiness: ready
depends_on: none
affects: `system/skills-src/plan/acs-shape-solution/SKILL.md` Phase C (line 341); `system/THIRD_PARTY_NOTICES.md`
Effort: S

## Scope

`acs-shape-solution:341` says "When the Expand posture applies", but no posture is defined anywhere; `THIRD_PARTY_NOTICES:80` records that the scope-posture adaptations "have no current home".

Add the four postures from gstack (`plan-ceo-review:62-68, 291-356`) as a named section in Phase C: expansion, selective expansion, hold, reduction. Two rules: commit to the mode and raise concerns once; every scope change is an explicit opt-in that leaves a "NOT in scope" record. Drop the "Boil the Ocean" framing.

If the plan phase rejects postures as out of scope, delete the sentence instead and record the refusal.

## Inputs

- Analysis: §6.6, §8.8 G10, §10 B3.
- Source: gstack `plan-ceo-review` scope postures; `THIRD_PARTY_NOTICES.md:80`.

## Verification

- `grep -rn "Expand posture" system/` resolves to the new section, not an undefined term.
- A `acs-shape-solution` run records the chosen posture and a "NOT in scope" line.
- `THIRD_PARTY_NOTICES.md` names the source and its landing path.

## Blockers

none

## Coordination proposal

Only `acs-shape-solution` and the notices file. No shared write.

## Evidence

Implemented on 2026-10-23. Only Phase C and its document date changed in `acs-shape-solution`; only the product-ideation provenance paragraph and date changed in the notices. Added four postures, one-time posture concerns, explicit opt-in for additions and removals, pending-choice semantics, and a scope decision record with a `NOT in scope:` line. Existing approval is reused. The dangling `Expand posture` spelling is replaced by an anchored `Expansion posture` reference.

Baseline identity: HEAD `fbc81fd046ea0c2093e4516cc8dbdd289d473395`, including the pre-existing integrated B1/B2/B14/B19 working changes. Before edits, saved `.scratch/B3-scope-postures/baseline/git.diff`, `git-status.txt`, `HEAD.txt`, `file-hashes.json`, and copies of the two owned source files and this ticket. The 1,071-file baseline SHA-256 manifest has digest `a514e84ea9a2dd6b28f17404e01f0cb3e5d06b36ca447143bdd76e4a92115b0b`. This baseline, not plain `git diff HEAD`, identifies the B3 contribution.

| Criterion | Command | Result | Source identity |
| --- | --- | --- | --- |
| Defined posture reference | `rg -n 'Expand posture|Expansion posture|Scope postures' system/skills-src/plan/acs-shape-solution/SKILL.md` | PASS: section at line 333 and anchored reference at line 360; obsolete spelling absent | Skill SHA-256 `0d2069fd231e0e8b2a0a56c5944435501bca7500085e96021649d14c786e964a` |
| Chosen posture and exclusions; scope approval boundaries | `python3 -m unittest discover -s system/evals/tests -p test_scope_postures.py -v` | PASS: 5 tests, four authored posture cases, six invalid mutations, provenance and relocated standalone checks | Fixture SHA-256 `78a51b8876867c752694794e7bf872f4c3ca76b03c171a2fedbfece1c307bdb6`; test SHA-256 `95513720b36a621fd2aceb047135115ba271a837c260839c1186caef34816477` |
| Provenance source and landing path | Same focused test command, `test_notice_names_pinned_source_and_landing_anchor` | PASS: pinned template and Phase C anchor named | Notices SHA-256 `1ad8c522ccf8dfc47d09a282dc12b9772b5526d3d54247514c75e77e29d8f8d4`; upstream gstack `35dd014c580037d1c009776d8b0584587c1bd42c`, template SHA-256 `15574692617651adfb77080256a2a0493ad15565bd267b72fa73f8dcbe6f9416` |
| Generated package build | `python3 scripts/build-plugins.py --output .scratch/B3-scope-postures/plugins` | PASS: 10 packages materialized | Same source hashes; generated output isolated from tracked `plugins/` |
| Registry, links, package closure | `python3 scripts/validate-protocols.py --plugins .scratch/B3-scope-postures/plugins` | PASS | Generated packages from the preceding builder command |
| Suite integrity | `python3 system/evals/validate_suite.py` | PASS: 43 source skills; inventory, catalog budget, declarations, local links/anchors | Integrated baseline plus B3 files |
| Preserve catalog behavior | `python3 -m unittest discover -s system/evals/tests -p test_catalog_budget.py -v` | PASS: 11 tests | Existing B1 test unchanged; skill frontmatter unchanged |
| Preserve integrated baseline and separate generated edits | `python3 .scratch/B3-scope-postures/check-contribution.py` | PASS: exactly the five files below differ; no inherited files changed outside the two owned sections/dates | Baseline manifest above |
| Whitespace and index | `git diff --check`; `git diff --cached --name-only` | PASS; empty staged-file list | Current working tree |

Exact contribution files:

- `system/skills-src/plan/acs-shape-solution/SKILL.md`
- `system/THIRD_PARTY_NOTICES.md`
- `system/evals/fixtures/acs-shape-solution-scope-postures.json`
- `system/evals/tests/test_scope_postures.py`
- `docs/changes/acs-corpus-alignment/tasks/B3-scope-postures.md`

Logs, source hashes, contribution patch, and generated packages are under `.scratch/B3-scope-postures/`. The upstream source was read only at `/Users/xhl/GitHub/skills/agent-coding-skills/references/gstack/source/plan-ceo-review/SKILL.md.tmpl`; local `references/` remains a real directory and was not changed. No commits, staging, installs, publication, or subagents.

Limitations: the posture cases are authored acceptance fixtures, not model transcripts or observed `acs-shape-solution` runs. They verify the record contract and its negative cases, not model compliance or a full product-memory HTML workflow. The ticket's live-run criterion remains unverified. Independent review is pending; parent should regenerate final plugins from integrated canonical source.

## Parent acceptance

2026-10-23: canonical build and affected suite passed; independent review found no remaining issues. See [bounded model exercises and source review](../evidence/bounded-model-exercises.md). B2/B3 evidence is one actual bounded model turn each, not a reliability benchmark. B4 has real scripted red/green evidence; B5 requires an explicitly simulated transcript.
