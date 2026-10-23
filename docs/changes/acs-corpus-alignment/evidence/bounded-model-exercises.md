# B2/B3 bounded model exercises and B3–B5 review

Last updated: 2026-10-23

Model: my-api/gpt-6-astra. Run: 8d50dc74-9666-42e0-8f6b-e2dad92b80e1.

## Review

Reviewed the current working-tree diffs and source for the B2 code-quality interactive caller and B3/B4/B5, against their tickets. Ticket evidence claims were treated as context, not as independently verified test results.

- **Correct — B2 caller fix:** [acs-review-code-quality/SKILL.md:150](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/test/review/acs-review-code-quality/SKILL.md:150) now says: “Classify findings with confidence ≥ 7 under the questioning protocol,” then “ask only the user-owned frontier in prerequisite order.” The diff removes “Stop after each file” and “one issue, one” question interface. The rule at [line 327](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/test/review/acs-review-code-quality/SKILL.md:327) also delegates “classification, frontier rounds, and affirmative recommendations” to the canonical protocol. This fixes both the interactive-flow caller and its local rules. [test_questioning.py:84](/Users/xhl/GitHub/skills/agent-coding-skills/system/evals/tests/test_questioning.py:84) explicitly rejects the removed phrases.
- **Correct — B3 scope postures:** [acs-shape-solution/SKILL.md:333](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/plan/acs-shape-solution/SKILL.md:333) defines all four postures. HOLD says: “Do not surface expansions or silently remove scope.” The following rules require “explicit user opt-in” for every addition or removal and state that an unanswered choice “is pending, not approval.” The record contract includes posture, baseline, dispositions, approval evidence, and `NOT in scope`. [THIRD_PARTY_NOTICES.md:80](/Users/xhl/GitHub/skills/agent-coding-skills/system/THIRD_PARTY_NOTICES.md:80) names the pinned gstack source and the Phase C landing anchor.
- **Correct — B4 TDD boundaries:** [acs-tdd/SKILL.md:29](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/build/acs-tdd/SKILL.md:29) requires a seam “named in an accepted TST, or confirmed by the user when no TST exists,” and requires reconciliation when an existing TST does not accept it. Lines 35–37 name the three anti-patterns and require independent expected values. [Line 45](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/build/acs-tdd/SKILL.md:45) says “End this loop at green”; line 51 moves refactoring into review. The criterion → test/evidence → revision mapping remains at line 53.
- **Correct — B5 diagnosis limits:** [acs-diagnose-incident/SKILL.md:41](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/maintain/acs-diagnose-incident/SKILL.md:41) requires stopping after three falsified hypotheses and waiting for the user before a fourth probe or new instrumentation. The next three numbered rules specify the recorded directory boundary, aggregate five-file limit, and `[DEBUG-xxxx]` tags. The close requires instrumentation removal and a tag search. [runtime-debuggers.md:7](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/maintain/acs-diagnose-incident/references/runtime-debuggers.md:7) supplies Node and Python debugger recipes without bypassing those limits.
- **Fixed:** None applied; this was read-only.
- **Findings:** No issues found.
- **Merge verdict: OK with notes** for the named source review. Tests and generated-package parity were not executed or certified in this session.

I inspected the four focused test modules. They distinguish authored fixtures from model behavior; B4 additionally contains an executable red-to-green subprocess fixture. Their presence does not establish that they pass against the current integrated tree. The supervisor should run:

```text
python3 -m unittest discover -s system/evals/tests -p 'test_questioning.py' -v
python3 -m unittest discover -s system/evals/tests -p 'test_scope_postures.py' -v
python3 -m unittest discover -s system/evals/tests -p 'test_tdd_seams.py' -v
python3 -m unittest discover -s system/evals/tests -p 'test_diagnose_incident.py' -v
python3 system/evals/validate_suite.py
python3 scripts/validate-protocols.py
```

## Bounded exercise 1 — Actual `acs-validate-demand` first-round output

**Execution boundary:** I loaded `acs-validate-demand`, its diagnostic framework, and canonical `system/protocols/questioning.md`. The following is my actual response to the supplied consultancy scenario. It is not a fixture copied from the repository. No user replies are simulated.

Your brief establishes a shared client-feedback inbox for two consultants, no integrations yet, and a deliberate open choice about who submits feedback. You have delegated routine implementation decisions, but explicitly reserved the submitter choice for challenge.

I’ll treat this as pre-product demand validation. The request establishes interest in the idea; it does not yet establish recurring pain, client willingness to submit, or consultant willingness to maintain the inbox.

### Candidate classifications and routes

| ID | Candidate | Classification | Route and reason |
|---|---|---|---|
| C1 | How many consultants, and are integrations required? | Lookup fact | Directly inspect the supplied brief: two consultants; no integrations yet. Settled; do not ask again. |
| C2 | Should consultants or clients submit feedback? | User challenge | Ask Q1. You expressly requested challenge on this consequential actor choice; delegated implementation discretion does not settle it. |
| C3 | What concrete problem currently justifies a shared inbox? | User challenge: user-held evidence | Ask Q2. Only your experience or supplied records can establish a recent incident and its consequences. No such evidence was supplied. |
| C4 | How long would manual capture take, and would either submitter complete it reliably? | Observable fact | Route to `acs-validate-prototype` once the actor and a representative task are settled. No prototype or observed run exists here; retain the unknown rather than asking you to guess. |
| C5 | Should routine technical choices become interview questions now? | Mechanical decision | Decide and record: no. They do not establish demand, and you delegated them. Choose them when implementation is authorized and its constraints are known. |
| C6 | Should the working language say “feedback” or “tickets”? | Taste decision | Provisionally use “feedback,” matching your brief and avoiding an unsupported support-ticket workflow. Show this terminology at the next existing review gate; do not add a gate. |

### Deferred premises

| Deferred item | Open prerequisite | Consequence |
|---|---|---|
| Client submission channel and access rules | Submitter choice, C2 | Do not assume a client form, account, or portal. |
| Consultant capture and handoff details | Submitter choice plus evidence about the current workflow | Do not ask how consultants will operate a workflow they have not selected. |
| Capture-time and completion-rate observation | Chosen actor and representative task | No efficiency or adoption claim can be graded Observed. |
| Narrowest useful wedge, pain score, and savings estimate | A specific incident, consequences, and frequency | Do not invent scores, choose a beachhead, or issue a demand verdict yet. |

### First frontier round

1. **Who submits** — Do you accept testing **consultant-entered feedback as the initial demand hypothesis**, while leaving client submission unresolved until evidence supports it?

   **Recommended answer:** Yes—test consultant entry first; this is a hypothesis to validate, not an approved product restriction.  
   **Reason:** Your brief names two consultants and no integrations, giving us a bounded group to investigate without assuming that clients will adopt a new submission habit.

   Your original direction leaves the submitter open. The alternative is to investigate client entry first, especially if direct, unfiltered feedback is the central problem. I do not yet know where feedback arrives or whether consultants distort or omit it. If my recommendation is wrong, consultant entry could add work and lose the client’s original meaning.

2. **Evidence of the problem** — Do you accept keeping “we need a shared feedback inbox” **unverified until it is grounded in one recent feedback episode and its consequence**?

   **Recommended answer:** Yes—use a real episode before treating the inbox as necessary. If one is available, describe where the feedback arrived, what happened next, and what it cost or put at risk; otherwise record that no example is available yet.  
   **Reason:** The brief states the desired tool but provides no current workflow, missed-feedback incident, or operational cost.

   This evidence question applies whichever actor submits. It does not assume your answer to Q1. A specific account could support **Reported** evidence; it would not become **Observed** merely because we discussed it.

### Unanswered findings and provisional close

- **Q1 — Who submits:** Unanswered. Consultant-first remains an **Inferred hypothesis**, not an accepted decision. Actor-dependent scope and observation stay blocked.
- **Q2 — Evidence of the problem:** Unanswered. Recurring pain and the need for a dedicated inbox remain **Inferred**; the expressed desire for the tool is **Stated interest**. No severity, frequency, or savings value has been supplied.

**Established:** Two-person consultancy; shared client-feedback inbox requested; no integrations yet; submitter choice open and explicitly subject to challenge; routine implementation choices delegated.

**Assumptions:** Pre-product stage and consultant-first investigation are provisional. Their consequences are limited to this diagnostic approach; neither authorizes building or excluding client submission.

**Disputed:** No disagreement has been expressed. The submitter question is unresolved, not a recorded disagreement.

**Open confirmation:** This reading remains unconfirmed because the bounded exercise contains no user reply. No demand verdict, approved scope, or downstream design handoff is issued.

## Bounded exercise 2 — Actual `acs-shape-solution` Phase C output

**Execution boundary:** I loaded Phase C and the product-memory record contract. This is a separate scenario with its own supplied accepted baseline; it does not inherit approval from the unanswered first exercise.

You explicitly chose **HOLD**. I will preserve manual feedback entry for two consultants and CSV export, with no integrations. The previously suggested AI summaries and client portal have no approval and remain outside accepted scope. There is no need to ask you to choose HOLD again or reconsider those additions.

The following is the scope decision record produced in this response. It is an HTML record fragment for `discovery.html`, not a claim that a file was written.

```html
<section id="scope-decisions">
  <h2>Scope decisions</h2>

  <article id="decision-feedback-inbox-hold" data-kind="decision">
    <h3>Feedback inbox: preserve the accepted scope</h3>

    <p><strong>Scope posture: HOLD</strong></p>
    <p>
      Basis: the user explicitly selected HOLD in the supplied scenario.
      Reuse that choice without requesting approval again.
      The posture authorizes analysis within the accepted boundary;
      it does not approve additions or removals.
    </p>

    <h4>Accepted baseline</h4>
    <ul>
      <li>Manual feedback entry.</li>
      <li>Use by two consultants.</li>
      <li>CSV export.</li>
      <li>No integrations.</li>
    </ul>
    <p>
      Approval evidence: the scenario explicitly identifies these items
      as accepted scope. This record introduces no new scope approval.
    </p>

    <h4>Existing suggestions and opt-in states</h4>
    <table>
      <thead>
        <tr>
          <th>Item</th>
          <th>Disposition</th>
          <th>Explicit opt-in</th>
          <th>Scope effect</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>AI summaries</td>
          <td>Pending; not rejected</td>
          <td>Absent: the user has not approved this suggestion</td>
          <td>Outside accepted scope; no implementation authorized</td>
        </tr>
        <tr>
          <td>Client portal</td>
          <td>Pending; not rejected</td>
          <td>Absent: the user has not approved this suggestion</td>
          <td>Outside accepted scope; no implementation authorized</td>
        </tr>
        <tr>
          <td>Integrations</td>
          <td>Excluded by the accepted baseline</td>
          <td>No opt-in to add integrations</td>
          <td>Remain outside accepted scope</td>
        </tr>
      </tbody>
    </table>

    <p>
      No additions or cuts are approved by this record.
      CSV export remains in scope.
      The prior suggestions are recorded for boundary clarity,
      not presented again as expansion recommendations.
    </p>

    <p>
      <strong>NOT in scope:</strong>
      integrations, because the accepted baseline excludes them;
      AI summaries and a client portal, because explicit opt-in is absent.
      The two suggestions remain pending, not rejected.
    </p>

    <p>
      Apply HOLD by checking the coherence and failure coverage of manual
      entry and CSV export within the two-consultant baseline.
      No evidence supplied here warrants a posture objection.
      A later scope change requires its own explicit approval.
    </p>
  </article>
</section>
```

Record anchor for a later authorized insertion: `discovery.html#decision-feedback-inbox-hold`. No discovery file or full solution proposal was created in this read-only exercise.

## Assessment of the observed outputs

| Criterion | Observed result |
|---|---|
| B2: classification before asking | **Met in this turn.** C1–C6 record classes, routes, and reasons; Q1 and Q2 trace to C2 and C3. |
| B2: no more than five questions | **Met.** Two numbered recommendation-positive questions. |
| B2: prerequisite frontier | **Met.** The incident-evidence question applies to either submitter. Submission channels, operational details, and prototype observations are deferred. |
| B2: always ask the explicit user challenge | **Met.** Submitter choice is asked, with a recommendation, alternative, missing evidence, and cost of being wrong. It is not classified as a routine implementation choice. |
| B2: affirmative recommendation wording | **Met.** “Yes” accepts the stated recommendation in both questions. |
| B2: unresolved answers remain findings | **Met for the no-reply boundary.** Both unanswered questions are named, and neither is treated as approval. Handling an actual partial reply was not exercised. |
| B3: record chosen posture | **Met.** The record reuses explicit HOLD and names its basis. |
| B3: explicit opt-in governs changes | **Met.** Both suggestions remain pending with absent opt-in; neither enters accepted scope. |
| B3: preserve exclusions and accepted scope | **Met.** `NOT in scope` names integrations and both unapproved additions; manual entry, two consultants, and CSV export remain accepted. |
| B3: commit to HOLD | **Met.** The output neither recommends expansions nor silently cuts CSV export. |
| B3: record identity | **Met at fragment level.** A `decision` article sits under `scope-decisions` with a proposed discovery anchor. File insertion and HTML validation were not exercised. |

These are **two actual, one-turn bounded model exercises in this review session**. They demonstrate the outputs above after loading the relevant instructions. They do not establish full-workflow completion, multi-turn compliance, live prototype behavior, durable-memory correctness, or population reliability. The self-assessment is separate from the independent source review and does not substitute for executed repository tests.