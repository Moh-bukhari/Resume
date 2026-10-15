# Application tracker

Open [the dashboard](../tracker/README.md) on GitHub to see application status,
preparation, suggested next actions, and links to each job. Use
[company research](../tracker/companies.md) for the wider company list and
[the CSV](../tracker/jobs.csv) for a table/export. The tracker works in GitHub;
it does not need Google Sheets, GitHub Pages, or a running server.

## What owns each kind of information

| Record | Source of truth |
| --- | --- |
| Candidate experience, metrics, and supported claims | `bank/experience-bank.json` |
| Companies, target jobs, application lifecycle, preparation, and tracker events | `tracker/tracker.json` |
| Full JD, exact resume version, letters, and tailoring decisions | `applications/<slug>/` |
| Contact identity/email sources, conversation context, and confirmed outreach evidence | The packet's `contacts.json` |
| Original imported workbook | `sources/job-search-tracker-original.xlsx`, an archived snapshot |

The JSON is the editable tracker master. Markdown pages and CSV are generated
views; editing those views will be overwritten. The original workbook and the
linked Google Sheet do not stay synchronized with this repository.

The import preserves 10 job IDs (`R001`–`R010`) and 41 company records. Keep IDs
stable when sorting or renaming; a row number or company/title is not an ID.
Do not merge separate postings or application attempts merely because their
titles match. Unknown dates, contacts, and posting URLs remain unknown.
Imported fit/proof notes are research leads, not new candidate facts: check
their claims against the bank before using them in a resume or letter.

## Read, update, and prepare a packet

Run commands from the repository root. The dates below are examples; use the
user's actual local mutation date. Inspect before changing a record:

```bash
python3 scripts/tracker.py show R010
python3 scripts/tracker.py check
```

The [update guide](../tracker/HOW-TO-UPDATE.md) covers field changes, confirmed
events, dry runs, new jobs, and publishing. A tracker update regenerates its
GitHub pages and CSV. Commit and push the changed files to publish them.

To start a tailored packet for an existing tracked job:

```bash
python3 scripts/new_application.py --tracker-id R010 --date 2026-10-15
```

The initializer uses the tracked company, role, and known application state;
it links a packet only after successfully creating it and refuses to overwrite
an existing folder. Reuse an existing packet when one is already linked.
Creating templates does not finish the resume, research a contact, submit an
application, or send a message. Preserve submitted resume versions when
preparing later revisions.

## Lifecycle, preparation, and outreach

Keep these separate: a reviewed resume can be ready while the job is still
saved; an applied job can have no outreach; a drafted letter is unsent.
Actual applications, messages, replies, interviews, and outcomes require user
confirmation or evidence from an authorized tool result. Do not advance their
status from a template, suggested task, inferred date, or generated file.

An interview scheduled or an `Interviewing` lifecycle status does not prove an
interview was completed. The packet's narrower `application_stage` is outreach
context, not a replacement for the tracker's full hiring lifecycle. When an
actual event affects both records, keep the tracker and packet consistent:

1. Record the confirmed lifecycle/event in the tracker with its evidence.
2. Record the same known contact/event facts in the packet's `contacts.json`,
   retaining identity sources, thread context, and unknown dates.
3. Refresh stage-dependent notes and drafts where needed. Do not rewrite an
   old submitted resume or describe a draft as sent.
4. Run tracker checks and the packet's contact validator.

If records disagree, inspect the evidence and ask for a material missing fact;
do not silently replace sourced details with a status label. Tracker lifecycle
is the operational master; detailed contact evidence remains in the packet.

## Dates and reminders

The dashboard is a dated snapshot, not a live clock or notification service.
Re-render for the user's local date after updates or a fresh review. Suggested
dates record a plan, not completed activity. Review actual replies and employer
instructions before acting.

The imported tracker settings use **5 calendar days after actual contact** and
**14 calendar days after an application** for follow-up suggestions. Those
explicit settings govern this tracker instead of the general outreach guide's
default. Change the settings if the user wants a different policy. Unknown
event dates cannot start a follow-up clock.

For manual JSON edits, update `updated_on`, preserve stable IDs and evidence,
then regenerate and validate:

```bash
python3 scripts/render_tracker.py --as-of 2026-10-15
python3 scripts/tracker.py check
python3 scripts/render_tracker.py --check
python3 scripts/check_contacts.py applications/company-role/contacts.json
```

The final command applies only to an existing packet. Repository visibility
also applies to tracker records; keep credentials outside the repository.

The tracker tools have functional regression checks for state, dates, imports,
and packet creation:

```bash
python3 -m unittest discover -s tests -v
```
