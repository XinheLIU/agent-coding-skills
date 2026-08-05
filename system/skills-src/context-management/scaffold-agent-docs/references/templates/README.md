# Human-Layer Templates

Last updated: 2026-08-04

Fill-in blueprints for the Human documentation layer. `scaffold-agent-docs` reads these in both init and update modes; `manage-context` Phase B uses them as the reference shape when orchestrating Human-layer repairs.

| Template | Becomes | Answers |
| --- | --- | --- |
| `AGENTS.template.md` | `AGENTS.md` | Where do I look for anything? |
| `ARCHITECTURE.template.md` | `docs/ARCHITECTURE.md` | How is it split, and why? |
| `CONVENTIONS.template.md` | `docs/CONVENTIONS.md` | How do we write code here? |
| `TECH_DECISIONS.template.md` | `docs/TECH_DECISIONS.md` | Why this technology? |
| `QUALITY.template.md` | `docs/QUALITY.md` | When is it done? |
| `backlog.template.md` | `docs/exec-plans/backlog.md` | What is not built yet? |
| `tech-debt-tracker.template.md` | `docs/exec-plans/tech-debt-tracker.md` | What is built badly? |

## Using them

Replace every `{{placeholder}}`. Delete the HTML guidance comments — they are instructions to whoever fills the template, not content for the finished file. Delete whole sections the project has not earned rather than leaving them empty; an empty heading reads as a gap, and the next agent tries to fill it.

Set `Last updated:` to the date you write the file.

## The rules that make these worth having

**Mark what you could not determine.** Every template carries a `To be added` section. An honest `TO BE ADDED — original rationale unknown` is more useful than an invented reason, because a plausible fabrication gets believed and repeated. The collected list of these markers is the most valuable output of a scaffolding pass — it is exactly the set of things only a human can answer.

**Verify relationships before asserting them.** `ARCHITECTURE.md` claims that module A depends on B must be backed by a real import. Same directory is not evidence. Where no import is found, use the `To be verified` section instead of asserting.

**Keep `AGENTS.md` an index.** Under 200 lines, literal commands rather than "see the docs", and every path in its table resolving to a file that exists. When it outgrows the ceiling, move detail into `docs/` and leave a pointer — `review-agent-instructions` owns that restructuring.

**Backlog and debt are different files on purpose.** Backlog is not built yet; debt is built badly. Merging them loses the distinction that decides whether you are writing new code or repairing old code.
