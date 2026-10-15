# Start here — Mohammed's job application system

This repository is the portable memory and workspace for Mohammed Bukhari's
job search. An AI assistant can use it to tailor resumes, research contacts,
write letters, and maintain the application tracker without the original chat.
All instructions are ordinary Markdown; no particular AI provider is required.

## Give a new AI this instruction

> Open this repository and read START-HERE.md, then AGENTS.md. Follow the
> relevant workflow in docs/WORKFLOWS.md. Use the factual bank for my experience
> and tracker/tracker.json for application state. Complete the requested work,
> update the tracker when supported, validate the changed files, and publish
> the repository changes. Save a handoff so another assistant can continue.
> My task: [what you want done].

Give the assistant the whole checkout, or repository access that lets it read
the linked files. A URL alone is insufficient for a chat that cannot browse.
Writing back to GitHub requires repository write access. It can still draft
materials and describe a precise proposed update when that access is absent.

## Reading order

1. [AGENTS.md](AGENTS.md): Mohammed's preferences, facts to handle carefully,
   and operating rules. Some coding assistants discover this automatically;
   every other assistant should open it explicitly.
2. [System guide](docs/SYSTEM.md): where information lives, tool requirements,
   the update cycle, and how to continue without prior conversation.
3. [Handoff](docs/HANDOFF.md): unfinished work and the last session's checks.
   Confirm current state in the underlying records; a handoff is a work note.
4. [Workflows](docs/WORKFLOWS.md): select the procedure matching the request.
   Read the relevant specialist guide/skill from that procedure.
5. For a particular job, read its record in [the tracker](tracker/tracker.json),
   its [detail page](tracker/README.md), and its linked application packet.
   For resume or letter claims, also read the [experience bank](bank/experience-bank.md).

Do not read every vendored skill on every task. The [skill index](skills/README.md)
routes to the relevant methods, including their source and license.

## Open what you need

| Need | File |
| --- | --- |
| View jobs, reminders, and materials | [Tracker dashboard](tracker/README.md) |
| View the spreadsheet-style table | [Jobs CSV](tracker/jobs.csv) |
| View target companies | [Company watchlist](tracker/companies.md) |
| Understand all available experience | [Experience bank](bank/experience-bank.md) |
| Run a task from start to finish | [Workflows](docs/WORKFLOWS.md) |
| Update the tracker | [Quick update guide](tracker/HOW-TO-UPDATE.md) |
| Understand every tracking field and event | [Tracker reference](docs/TRACKER-REFERENCE.md) |
| Find all documentation | [Documentation index](docs/README.md) |

## The essential tracking rule

Use an existing `Rxxx` job ID whenever possible. Work readiness, an application,
and a sent message are separate facts. Creating a resume or letter only creates
an artifact. Record an actual submission/message/interview/outcome when the
user confirms it or an authorized tool provides the result.

The editable records are JSON; the instructions and browsable views are
Markdown. Update the records, regenerate the views, validate, then commit and
push. This keeps the dashboard, job pages, and CSV consistent. Editing a rendered
table alone will be overwritten. The original Google Sheet and Excel upload are
historical inputs and do not synchronize with this tracker.

## Example requests

- “Show what needs attention today and refresh the dashboard.”
- “Prepare R001: one-page resume, relevant contacts, and a letter.”
- “I applied to R004 today. Record it and suggest the next step.”
- “I sent R001's LinkedIn message to [name] on [date]. Update the history.”
- “They replied to R010: [paste]. Record it and draft my response.”
- “Add this job and prepare a packet: [posting/full description].”
- “Continue from docs/HANDOFF.md and tell me what is still missing.”

The assistant uses the user's current date for updates, preserves actual event
dates, and leaves unknown information unknown. GitHub displays the last
published snapshot; opening a page does not run a daily job or send reminders.
