# How this system works

[Start here](../START-HERE.md) · [Task workflows](WORKFLOWS.md) ·
[Documentation index](README.md)

The repository holds instructions, candidate evidence, operational records,
and job-specific work. The AI supplies judgment and uses its available tools.
No hidden chat memory, particular model, external database, or running web
application is needed for local tracking and document work.

## File ownership

| Information | Edit here | Readable view / related guide |
| --- | --- | --- |
| Confirmed candidate facts, bullet variants, metric scope, preferences, answered questions | [bank/experience-bank.json](../bank/experience-bank.json) | [Experience bank](../bank/experience-bank.md); [maintenance](MAINTENANCE.md) |
| Target companies, jobs, status, preparation, dates, event history, material links | [tracker/tracker.json](../tracker/tracker.json) | [Dashboard](../tracker/README.md), job pages, companies, CSV; [tracking](TRACKER.md) |
| Full description, source/access limits, fit decisions | Job packet's `job-description.md` and `tailoring-notes.md` | [Packet layout](../applications/README.md) |
| Exact resume and letter versions | Job packet's `resume.tex`, reviewed `resume.pdf`, `letters/*.md` | [Tailoring](TAILORING.md), [letters](LETTERS.md) |
| Contact identity, LinkedIn/email evidence, prior threads | Job packet's `contacts.json` | [Contact research](CONTACT-RESEARCH.md) |
| Selected recipient, message intent, timing, employer instructions | Job packet's `outreach-plan.md` | [Outreach plan template](../templates/outreach-plan.md) |
| Unfinished session work, checks, continuation instructions | [HANDOFF.md](HANDOFF.md) | Work note; never overrides the bank or tracker |
| How future assistants should operate | [AGENTS.md](../AGENTS.md) and these guides | [Documentation index](README.md) |
| Historical inputs and source attribution | [sources/](../sources/README.md), upstream `UPSTREAM.md`/licenses | Evidence, not active user instructions |
| External startup ideas, variants, hypotheses, and next questions | [EXTERNAL-PROJECTS.md](../EXTERNAL-PROJECTS.md) | Editable Markdown concept record; not candidate accomplishments or application state |

Markdown is the instruction and review layer. JSON provides one editable record
for each kind of state, so separate views cannot quietly disagree. The scripts
are local helpers that implement the documented workflow. They never apply for
jobs, send messages, or synchronize the old Google Sheet.

External-project concepts are an exception to the JSON record pattern:
`EXTERNAL-PROJECTS.md` is their editable master and readable view. Idea-only
work does not require bank/tracker mutations or regeneration. Record actual
project accomplishments in the bank only when supported evidence is supplied.

The tracker owns hiring lifecycle. `contacts.json` owns detailed identity and
thread evidence; its narrower application stage is derived from confirmed
lifecycle facts. An old resume's submission note cannot override a newer tracker
event. Imported fit/proof notes must be checked against the factual bank.

## Start a session

1. Read the latest user task, [AGENTS.md](../AGENTS.md), and [HANDOFF.md](HANDOFF.md).
   Use the current checkout. Inspect `git status --short --branch`; preserve
   existing edits and do not create a worktree unless requested.
2. Read the relevant tracker record and linked packet. For new jobs, search by
   posting URL/requirement ID and company/title before adding. URLs can differ
   only by tracking parameters; the CLI's exact-URL check is not full deduplication.
3. Establish the current date from the user's environment. Keep that mutation
   date separate from when an event actually happened. Check the stored tracker
   timezone; do not substitute a server date or silently change the user's policy.
4. Check tools only for the task at hand. Continue work that does not depend on
   unavailable browsing, PDF tooling, credentials, or write access.
5. Follow [WORKFLOWS.md](WORKFLOWS.md). Save facts and decisions in files as work
   progresses so another model can continue.

## What an assistant needs

| Capability | Requirement | If unavailable |
| --- | --- | --- |
| Read instructions, evidence, and current state | Checkout/file reader, or repository browsing | Ask for the relevant files; do not assume prior chat context |
| Update records and generate GitHub views | File writing and Python 3.10+; standard library only | Supply exact proposed edits and mark regeneration/validation pending |
| Tailor LaTeX and write letters | Text/file editing | Return complete source/copyable text |
| Compile and inspect a PDF locally | pdfLaTeX and Poppler utilities; see [BUILD.md](BUILD.md) | Give complete Overleaf source; state that build/layout checks remain unrun |
| Find current people/postings | Available browser/search tools | Use supplied descriptions and dated sources; leave unsupported details unknown |
| Optional email enrichment | Existing authorized provider/tool access | Use published professional sources or a sourced LinkedIn route |
| Publish tracker/materials to GitHub | Git push or an equivalent authorized GitHub file-write API | Preserve changes locally or supply a patch; say they are unpublished |
| Apply or send a message externally | Suitable tool/access and the user's authorization for the action | Prepare drafts; record real events when confirmed |

Bundled skills can be read as ordinary files even if the assistant has no skill
loader. They do not install providers or grant accounts. No model API key is
needed to run the tracker. The optional Excel importer requires `openpyxl` only
for a new import; never re-import over the maintained tracker.

## The update cycle

1. **Read:** resolve the stable job ID and inspect existing history and artifacts.
2. **Do the work:** save the requested research, document, or confirmed event.
   For new/revised application prose, complete
   [Professional Writing Review](../skills/professional-writing-review/SKILL.md)
   before delivery, preserving the bank evidence and company-fit brief.
3. **Update the owner:** bank for candidate facts; tracker for job progress;
   packet for actual materials/contact evidence. Preserve unknown dates and
   provenance. Use the tracker helper for normal mutations.
4. **Reconcile:** update the packet's relevant context and draft wording if
   the stage changed. The helper refreshes some stage/date fields; it does not
   rewrite letters or copy identity/thread evidence.
5. **Render and check:** helpers regenerate tracker views after mutations.
   After direct JSON edits, regenerate explicitly and validate. Run only checks
   relevant to the change; [WORKFLOWS.md](WORKFLOWS.md) lists them.
6. **Prepare the handoff:** record completed work, real check results, remaining
   unknowns, and the next concrete step in [HANDOFF.md](HANDOFF.md). For the
   commit being prepared, say it contains the handoff and that the reader
   should verify its remote status; do not claim a push that has not happened.
7. **Publish:** review the diff, preserve unrelated work, and commit/push the
   intended records, generated views, and handoff together. Check the remote
   result and report success or its exact limit. If publishing fails, keep that
   limit in the local handoff for the next assistant.

A draft, planned action, or past due date cannot create a completed event.
Before recording a report, inspect the history to avoid adding the same event
again after a retry or a handoff. The CLI does not deduplicate repeated events.
Use [the reference](TRACKER-REFERENCE.md) for backfills, corrections, and
the exact mapping from events to current fields.

## Publish without losing work

Inspect the branch, remote, and diff. Stage only files belonging to the current
task. Use a descriptive commit, then push through the repository's authorized
workflow. For this repository the dashboard is normally viewed on `main`.
Check the remote before pushing; a different default branch should be handled
explicitly. Example inspection commands:

```bash
git status --short --branch
git remote -v
git diff --check
git diff --stat
git ls-remote origin refs/heads/main
```

When publishing to `main` is authorized and the local branch contains the remote
history, `git push origin HEAD:main` publishes it. If rejected as non-fast-forward,
fetch and reconcile the changes without overwriting remote work. Resolve JSON
conflicts by stable record/event IDs; retain independent events, reconcile any
ID collision, and regenerate views. Do not force-push to make an update fit.
An assistant may instead create a requested branch/PR and clearly report that
the main dashboard has not changed yet.

If a helper failed, inspect the files before retrying. Tracker JSON may have
saved even when view rendering failed; linked contact context may have changed
before a later write failed. Repair and validate the existing state rather than
recording the event twice. Never report “published” on the basis of a local edit.

## Work without a shell

A repository-editing assistant can update the canonical JSON directly using
[TRACKER-REFERENCE.md](TRACKER-REFERENCE.md), preserving IDs, typed values,
event evidence, and packet consistency. If it cannot run Python, it must leave
validation and view generation explicitly pending. A chat-only assistant should
return a proposed change with the job ID, exact fields, evidence, event date,
and affected files; it must not claim the tracker was updated.

Record this in the handoff so an execution-capable assistant can complete the
same work without reconstructing the conversation. Do not edit rendered tables
as a substitute for changing the master record.

## End-of-session handoff

Keep [HANDOFF.md](HANDOFF.md) short and current using its existing headings.
Reference IDs and paths instead of copying the bank or whole tracker. Include
unfinished work, missing access/information, and which checks were actually run.
Update facts and events in their proper files first. Retain older session
history through Git; the current handoff is not another application ledger.
If nothing is pending, say so and name the next useful user-driven task.
