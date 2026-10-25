# Task runbooks

Start with [START-HERE](../START-HERE.md) and [the system map](SYSTEM.md).
These runbooks work with any AI that can read and edit this checkout. The
scripts provide local validation and rendering; the AI performs research,
judgment, drafting, and evidence review. Read [the tracker reference](TRACKER-REFERENCE.md)
for field definitions, event effects, and the manual-edit alternative.

All commands run from the repository root. **Dates, recipients, notes, and
paths in examples are illustrative.** Substitute the actual job ID, linked
packet path, supported facts, and user's local record date. An event's date
is separate from the date you record it. Do not execute sample events against
real records. `--dry-run` previews a mutation; remove it after reviewing the
actual authorized update.

| User's task | Runbook |
| --- | --- |
| “What should I do today?” | [Daily review](#1-review-the-day) |
| “Add this job” | [Add a role](#2-add-a-role) |
| “Prepare R001” | [Prepare a packet](#3-prepare-a-tracked-application) |
| “Find the right person / write a letter” | [Contacts and letters](#4-research-contacts-and-write-letters) |
| “I applied / sent it / got a reply” | [Record an event](#5-record-real-activity) |
| “Here is a correction to my experience” | [Update facts](#6-update-candidate-facts) |
| “Continue where the other AI stopped” | [Resume work](#7-resume-after-a-handoff) |
| “Update GitHub so I can see it” | [Finish and publish](#8-finish-and-publish) |
| “Document or continue my startup idea” | [External projects](#9-document-an-external-project) |

## 1. Review the day

1. Read [AGENTS.md](../AGENTS.md), inspect `git status --short`, and preserve
   existing unfinished changes. Establish today's date in the user's timezone;
   do not copy a historical example date or assume the host's date is local.
2. Validate the tracker, then refresh its dated view:

   ```bash
   python3 scripts/tracker.py check
   python3 scripts/render_tracker.py --as-of 2026-10-15
   ```

3. Read [the dashboard](../tracker/README.md). For each relevant ID, read its
   detail page and source record. Prioritize confirmed interviews/deadlines,
   overdue tasks, and the user's priorities. Distinguish `apply_by` (personal
   target) from `deadline` (recorded employer deadline).
4. Check the current posting and latest available conversation before acting
   on an old plan. Say when these sources could not be checked. The dashboard
   reflects recorded evidence; it does not check email or job boards itself.
5. Return a short list of next actions with IDs and reasons. Do the work the
   user requested, then use the relevant runbooks below. A reminder becoming
   due does not establish that anything was sent or submitted.

**Done when:** the dashboard has the intended as-of date, important uncertainty
is visible, and suggested actions match known history. Publish refreshed views
using runbook 8 when GitHub should reflect the review. No daily scheduler is
required or currently installed.

## 2. Add a role

1. Search `tracker/tracker.json` for the URL, requisition ID, company, and title.
   Reuse an existing `Rxxx` record for the same application. Check similar URLs
   manually; exact-URL duplicate rejection does not identify every duplicate.
2. Save the actual title and posting source. Use supplied text if retrieval
   fails and keep that limitation visible. A URL identifier alone is not a JD.
3. Preview the new record:

   ```bash
   python3 scripts/tracker.py --dry-run add --company "Example Company" --role "Growth Associate" --url "https://example.com/careers/growth-associate" --on 2026-10-15 --note "Target supplied by the user; full posting still needs review."
   ```

4. Run the real command with the actual inputs. Retain the assigned ID; the
   helper allocates the next one and adds a minimal company record if needed.
   Add known role details, priority, fit rationale, and dates using `update`
   or the reference's manual-edit procedure. Unknown fields stay null.
5. Start a packet only when useful for the task. New targets start `Saved`;
   recording a job does not record an application.

**Done when:** one stable ID identifies the opportunity, the source and limits
are recorded, and the dashboard contains the new job. Separate postings or
application attempts must remain distinguishable even when titles match.

## 3. Prepare a tracked application

1. Inspect the ID and follow `packet_path` if one is already present:

   ```bash
   python3 scripts/tracker.py show R001
   ```

   Read the packet's manifest, full JD, notes, contacts, and letters before
   editing. Reuse existing work. If no packet exists, create one:

   ```bash
   python3 scripts/new_application.py --tracker-id R001 --date 2026-10-15
   ```

   This creates templates and links their folder; it does not complete prep.
   The default folder for this example is
   `applications/r001-retell-ai-deployment-strategist/`. Use the actual returned
   path in subsequent commands.
2. Follow [the combined workflow](../skills/application-workflow/SKILL.md) and
   [tailoring guide](TAILORING.md). Save the full JD and its source/date in
   `job-description.md`. Match requirements to supported bank bullet IDs and
   preserve scope/ownership limits in `tailoring-notes.md`.
   Complete [company alignment](COMPANY-ALIGNMENT.md): save the sourced mission,
   role/team goals, evidence map, and positioning in those notes before drafting.
3. Tailor `resume.tex` from the current bank: Tamara first, one A4 page, 10pt
   body, standalone pdfLaTeX. For uncertain facts, use supported wording and
   record the gap. Imported tracker proof notes do not override the bank.
4. Build and inspect the exact version:

   First apply [Professional Writing Review](../skills/professional-writing-review/SKILL.md)
   to the final resume prose. Record its naturalness, strength, factual scope,
   and company-fit review in `tailoring-notes.md`, then build that exact wording:

   ```bash
   python3 scripts/check_bank.py
   bash scripts/build_resume.sh applications/r001-retell-ai-deployment-strategist/resume.tex
   pdfinfo build/resume/resume.pdf
   pdftotext -layout build/resume/resume.pdf -
   ```

   Review the PDF visually where available, including wrapping, clipping,
   links, reading order, and page count. Record checks actually performed.
   Copy the inspected PDF before building another `resume.tex`, since that
   output stem is shared:

   ```bash
   cp build/resume/resume.pdf applications/r001-retell-ai-deployment-strategist/resume.pdf
   ```

5. Update only completed preparation and real material paths. For example,
   after finishing the corresponding work:

   ```bash
   python3 scripts/tracker.py --dry-run update R001 --on 2026-10-15 --set research_done=true --set resume_done=true --set resume_path=applications/r001-retell-ai-deployment-strategist/resume.pdf --set 'bank_bullet_ids=["TAM-08","TAM-14"]' --note "Saved sourced role research and reviewed this resume; selected evidence is documented in the packet."
   ```

   Use the actual selected IDs. Mark `proof_done` only when the chosen proof
   artifact or evidence preparation is complete and documented; merely copying
   templates does not complete it. A drafted outreach letter does not change
   `networking` to `Reached out`.

**Done when:** the requested material is ready or clearly marked provisional;
its evidence, limits, and actual validation are saved; tracker links and prep
match the work. Deliver the full standalone LaTeX when producing a resume.
Record an application only after a confirmed submission, using runbook 5.

## 4. Research contacts and write letters

1. Read the exact job's tracker events, packet, and available prior threads.
   Choose wording for the confirmed stage. A scheduled interview is not a
   completed conversation; an existing draft is not prior outreach.
2. Follow [contact research](CONTACT-RESEARCH.md) and [letter guidance](LETTERS.md).
   Usually identify one primary contact and one fallback. Save current-role
   sources, exact found LinkedIn URLs, professional email provenance, and
   uncertainty in `contacts.json`. A guessed pattern is not a verified email.
3. Use the full available conversation for a reply or follow-up. If history
   was unavailable, record that. Do not assume no history because no connector
   was queried. Research can use available search tools; bundled skills do not
   provide accounts, paid credits, or credentials.
4. Draft only the relevant letter type under `letters/`. Connect sourced
   company/role needs to one or two bank facts and one clear ask. Keep claim
   IDs, sources, timing, and unresolved questions outside the copyable text in
   `outreach-plan.md` and letter metadata.
   Apply [company alignment](COMPANY-ALIGNMENT.md) and record the selected
   goal/proof and review date in the plan. Review the exact final text again
   before an authorized send; a logistical reply should address its actual task.
5. Validate the contact record, then link the completed drafts if useful:

   Before finalizing, run [Professional Writing Review](../skills/professional-writing-review/SKILL.md)
   on every drafted/revised message, including brief replies. Record the actual
   result in `outreach-plan.md` and letter metadata. Recheck changed text before
   any authorized send; preserve the version actually sent.

   ```bash
   python3 scripts/check_contacts.py applications/r001-retell-ai-deployment-strategist/contacts.json
   python3 scripts/tracker.py --dry-run update R001 --on 2026-10-15 --set letters_path=applications/r001-retell-ai-deployment-strategist/letters --note "Prepared the stage-appropriate letter; it remains unsent."
   ```

**Done when:** the user has copyable text, recipient evidence, an appropriate
next step, and clear uncertainties. No sent event or follow-up clock is created
by drafting. Existing user authorization governs external actions; the local
tools do not send messages or submit applications.

## 5. Record real activity

1. Resolve the stable job ID. Read its events first: replaying the same event
   command appends another event, so do not repeat an event already recorded.
2. Establish what happened from user confirmation or the result of an
   authorized tool action. Preserve the actual date if known; omit
   `--event-date` if unknown. `--on` is today's record date. Use
   `--confirmed-by user` or `tool` according to the actual evidence.
3. Choose the event that describes the confirmed action:

   | Confirmed action | Event type | Follow-through |
   | --- | --- | --- |
   | Application submitted | `application` | Preserve the exact submitted resume/version and submission evidence. |
   | Message sent | `sent` | Preserve recipient, channel, sent text, and source/thread reference. |
   | Reply received | `reply` | Read the reply, update the outreach plan, and replace obsolete follow-up drafts. |
   | Interview appointment agreed | `interview_scheduled` | `--event-date` is the appointment date; keep time/timezone and logistics in packet notes. |
   | Interview actually completed | `interview` | Record known discussion details before writing a thank-you. |
   | Offer / acceptance / rejection / withdrawal / posting closed | `offer` / `accepted` / `rejected` / `withdrawn` / `posting_closed` | Record the actual outcome and source; an acceptance draft is not an acceptance. |

   Example previews, **not events to assume occurred**:

   ```bash
   python3 scripts/tracker.py --dry-run event R001 --type application --on 2026-10-15 --event-date 2026-10-14 --confirmed-by user --note "User confirmed submitting this exact role on October 14; submitted version recorded in packet notes."
   python3 scripts/tracker.py --dry-run event R001 --type sent --on 2026-10-15 --event-date 2026-10-15 --confirmed-by user --contact "Confirmed recipient" --note "User confirmed sending the LinkedIn message; exact text and evidence saved in the packet."
   python3 scripts/tracker.py --dry-run event R001 --type interview_scheduled --on 2026-10-15 --event-date 2026-10-20 --confirmed-by user --note "User confirmed an interview scheduled for October 20; completion is not recorded."
   ```

4. Apply the supported event once. Use `--history-only` for an older event
   that should be recorded without replacing current status/contact dates.
   For correcting a mistaken field or event, use the correction procedure in
   [the tracker reference](TRACKER-REFERENCE.md), retaining a reason and history.
5. The updater refreshes linked `contacts.json` stage/date context. It does
   **not** copy conversation evidence or rewrite letter text and notes.
   Add the actual contact/thread evidence to `contacts.json`; reconcile
   `outreach-plan.md`, letter metadata, and tailoring/submission notes manually.
   Keep previously sent text and submitted versions identifiable.
6. Inspect the resulting job and validate the packet. Follow-up suggestions
   use the tracker's settings: currently five calendar days after contact and
   fourteen after application. Unknown dates cannot start a timer. Actual
   replies and employer/user instructions take priority over suggestions.

**Done when:** evidence and dates agree across the tracker and packet, the
correct next step is visible, and the real event is recorded once. Preparation
flags remain independent of application/outreach status. Runbook 8 publishes
the update.

## 6. Update candidate facts

Follow [bank maintenance](MAINTENANCE.md). Save the explicit correction or new
evidence as a source in `bank/experience-bank.json`, preserve stable IDs, update
affected bullet variants and metric scope, and record answered questions.
Keep planned work and implementation limits visible. A JD or tracker fit note
does not establish a candidate achievement.

```bash
python3 scripts/render_bank.py
python3 scripts/check_bank.py
```

**Done when:** the bank and generated views agree, corrections will survive a
new AI session, and affected drafts are identified. Revise requested drafts
from the bank while preserving submitted/sent versions and their history.

## 7. Resume after a handoff

1. Read [START-HERE](../START-HERE.md), [the system map](SYSTEM.md), and this
   runbook. Read [HANDOFF.md](HANDOFF.md) for pending work, then inspect
   `git status --short` and recent commits before changing anything.
2. Resolve the user's job ID, then read `tracker/tracker.json`, its detail page,
   the linked `application.json`, notes, contacts, outreach plan, and letters.
   Use current bank facts for candidate claims. No prior chat is required.
3. Separate completed work from templates and pending checks. Compare source
   records with generated views. If the tracker was saved but rendering failed,
   regenerate views; do not replay an event to repair the rendering.
4. Reconcile contradictions using sources and the latest explicit user
   correction. Preserve unknowns. Ask only for information that materially
   affects the task and is not already recorded.
5. Continue the next authorized action. At handoff, write what changed, checks
   actually completed, unresolved facts, and the next concrete action into the
   relevant packet's notes/outreach plan. Store shared fact corrections in the
   bank and operational events in the tracker, not only in a chat summary.
   Update [HANDOFF.md](HANDOFF.md) with the relevant IDs/paths and next step.

**Done when:** another AI can identify the current state, find its evidence,
and continue without inventing events or repeating completed work.

## 8. Finish and publish

CLI mutations regenerate tracker views using the source update date. After
manual source edits or a daily refresh, render explicitly for the intended
as-of date. Validate using that same date (the example below is illustrative):

```bash
python3 scripts/tracker.py check
python3 scripts/render_tracker.py --check --as-of 2026-10-15
git diff --check
git status --short
git diff --stat
```

Also run the bank or contact checks for records changed, and the PDF checks for
resumes produced. Run tracker regression tests when changing tracker code or
behavior: `python3 -m unittest discover -s tests -v`.

Without `--as-of`, the check uses the source's `updated_on`, which can be older
than a daily snapshot. Do not change historical source/event dates to satisfy
that check; pass the intended snapshot date.

Review the actual source and generated diff. Stage only the intended files,
commit, and push through the repository's authorized Git workflow. Inspect the
current branch and remote before choosing the push target; preserve unrelated
work. If publishing is unavailable, clearly identify what remains local.
Save actual checks, remaining work, and publication state in
[HANDOFF.md](HANDOFF.md); include it in the published changes. After pushing,
verify the result before reporting success.

**Done when:** the requested outputs and current tracker agree, appropriate
checks pass or their limits are disclosed, and the user knows whether GitHub
contains the update. GitHub displays committed Markdown/CSV; it does not edit
the original workbook, sync Google Sheets, or run an AI automatically.

## 9. Document an external project

Startup work has moved to [wearable-project](https://github.com/Moh-bukhari/wearable-project). Read its START-HERE.md
and AGENTS.md, then continue in that repository. This repository's
[external-project page](../EXTERNAL-PROJECTS.md) is a navigation pointer.
Do not recreate startup content in the application tracker or experience bank.
