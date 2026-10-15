# Tracker reference for any AI

This is the implementation contract for maintaining the application tracker
without conversation history or a particular AI provider. Start with
[AGENTS.md](../AGENTS.md), then use [the tracker workflow](TRACKER.md) and
[common update commands](../tracker/HOW-TO-UPDATE.md). This reference explains
the data and edge cases those shorter guides leave out.

The source is [tracker/tracker.json](../tracker/tracker.json). Markdown explains
the system and presents its state; the JSON preserves typed values, stable IDs,
and event history. Any AI that can edit repository files can maintain it using
the contracts below. The Python helpers are the preferred way to validate and
render changes. Reading this guide does not give an AI GitHub write access,
shell access, browsing, or permission to send applications or messages.

## Contents

- [Read and write boundaries](#read-and-write-boundaries)
- [Root object and conventions](#root-object-and-conventions)
- [Job fields](#job-fields)
- [Event record and provenance](#event-record-and-provenance)
- [Event transitions](#event-transitions)
- [Company records and settings](#company-records-and-settings)
- [CLI contract](#cli-contract)
- [Packet linking and contact context](#packet-linking-and-contact-context)
- [Exact update contract without a shell](#exact-update-contract-without-a-shell)
- [Verify and publish](#verify-and-publish)

## Read and write boundaries

| Information | Editable source | Result or related record |
| --- | --- | --- |
| Candidate facts and supported accomplishments | [experience-bank.json](../bank/experience-bank.json) | Generated [experience-bank.md](../bank/experience-bank.md); selected IDs in each job |
| Job identity, preparation, hiring lifecycle, dates, events, company watchlist, reminder settings | [tracker.json](../tracker/tracker.json) | Generated [dashboard](../tracker/README.md), job pages, [companies](../tracker/companies.md), [CSV](../tracker/jobs.csv) |
| Full posting and access evidence | A packet's `job-description.md` | Job's `job_link`, `req_id`, and summary fields |
| Tailored resume and exact reviewed PDF | A packet's `resume.tex`, `resume.pdf`, and `tailoring-notes.md` | Job's `packet_path`, `resume_path`, `bank_bullet_ids`, and preparation flags |
| Contact identity, email sources, actual thread evidence | A packet's `contacts.json` | Job's contact summary and confirmed events |
| Outreach copy and suggested timing | A packet's `letters/` and `outreach-plan.md` | Draft material links; these do not establish sending |
| Original workbook | [archived XLSX](../sources/job-search-tracker-original.xlsx) | Historical input only; no synchronization with Google Sheets |

Do not directly edit generated tracker Markdown or CSV. They are overwritten
by rendering. The workbook's hidden AI Guide is historical document content,
not operating instructions. Imported role analysis is not candidate evidence.

## Root object and conventions

All six root keys are required:

| Key | Type and meaning |
| --- | --- |
| `schema_version` | Exactly the string `"1.0"` |
| `updated_on` | Actual source-update date in `YYYY-MM-DD` format |
| `settings` | Reminder and display configuration described below |
| `sources` | Array of provenance records, each with a unique string `id` |
| `companies` | Array of company records |
| `jobs` | Array of job records |

Dates are calendar dates, not timestamps. Use the client's actual local date
for a mutation. Use `null` for an unknown value, `[]` for an empty list, and
JSON `true`/`false` for preparation flags. Preserve existing fields and source
history when modifying a record. An edit date never establishes an event date.

Source records currently use `id`, `path`, `sha256`, and `note`. The validator
enforces unique source IDs; it does not independently verify the file, hash,
source claims, or every `source_id` reference. When adding provenance, use a
stable ID, a repository-relative source path or clear source description, and
an evidence note; verify the relationship yourself. Do not relabel imported
data as newly verified research.

## Job fields

Keep IDs stable: `R` followed by at least three digits, such as `R001`. A new
ID is one greater than the highest existing numeric ID, zero-padded to at
least three digits. Never reuse an ID or rename it to match row position.
Separate postings or application attempts may need separate records even
when the company and title match.

The following identity and state fields must be present. The three preparation
booleans are also required by validation, although they are stored separately
from application status.

| Field | Type / permitted values | Meaning |
| --- | --- | --- |
| `id` | Unique `R` plus at least three digits | Stable application identity |
| `company` | Nonempty company name matching `companies[].name` exactly | Display name and company association; not a company ID |
| `role` | Nonempty string | Actual role title |
| `status` | `Unknown`, `Saved`, `Applied`, `Interviewing`, `Offer`, `Accepted`, `Rejected`, `Withdrew`, `Posting closed` | Current hiring lifecycle |
| `networking` | `Not started`, `Reached out`, `Talked`, `Referral asked`, `Referred`, `No reply` | Separate outreach state |
| `research_done` | Boolean | Role research completed and saved |
| `proof_done` | Boolean | Relevant proof/demo work completed; not satisfied by merely proposing it |
| `resume_done` | Boolean | Tailored resume reviewed; copying a starter template is insufficient |
| `bank_bullet_ids` | Array of strings, each an existing bank bullet ID | Supported evidence selected for this role |
| `review_notes` | Array of strings | Corrections, unresolved questions, qualification limits, and review context |
| `events` | Array of event objects | Actual recorded events and local change history |

These additional fields are nullable. Existing records normally include them
explicitly. Keep that shape when creating a record rather than depending on
the validator's acceptance of absent optional fields.

| Field(s) | Type / constraint | Meaning |
| --- | --- | --- |
| `priority` | `High`, `Medium`, `Low`, or `null` | User's priority |
| `fit` | Integer 1–5 or `null` | Judgment about fit; not an externally measured score |
| `apply_by` | ISO date or `null` | Personal application target |
| `deadline` | ISO date or `null` | Posting deadline; retain source and verification limits |
| `applied_on` | ISO date or `null` | Confirmed application date; cannot exceed root `updated_on` |
| `interview_on` | ISO date or `null` | Next scheduled interview; does not record completion |
| `last_contact` | ISO date or `null` | Most recently recorded sent/reply date; cannot exceed root `updated_on` |
| `posted_on` | ISO date or `null` | Posting date when known |
| `added_on`, `updated_on` | ISO date or `null` | Record creation and latest source edit |
| `contact` | Text or `null` | Short confirmed contact summary; detailed identity remains in `contacts.json` |
| `log` | Text or `null` | Existing free-text activity log; preserve original history |
| `job_link` | HTTP(S) URL or `null`; no whitespace or embedded credentials | Posting reference; a URL alone does not prove it is live |
| `location`, `work_mode`, `job_type`, `team`, `pay` | Text or `null` | Role details from supplied/retrieved requirements |
| `start_date` | Text or `null` | Human-readable start timing; deliberately not restricted to an ISO date |
| `req_id` | Text or `null` | Employer's requisition identifier |
| `about_role`, `must_haves`, `nice_to_haves`, `keywords`, `interview_process` | Text or `null` | Role summaries; the full posting belongs in the packet |
| `strongest_proof`, `gaps`, `prep_plan`, `ai_notes` | Text or `null` | Historical/imported planning analysis; current renderer labels it for review |
| `source_id` | Text or `null` | Source provenance reference; maintain the corresponding root source record |
| `packet_path` | Repository-relative path under `applications/`, or `null` | Application folder |
| `resume_path` | Repository-relative path under `applications/`, or `null` | Exact reviewed resume artifact, conventionally a PDF |
| `letters_path` | Repository-relative path under `applications/`, or `null` | Draft letters folder |

Material paths cannot be absolute, contain `..` or backslashes, or escape
`applications/` through a symlink. A missing target produces a warning and no
clickable material link. Path validity does not establish document quality or
completion. The validator does not enforce a PDF extension for `resume_path`;
the workflow requires linking the actual reviewed artifact.

`update --set` supports the fields above except `id`, `events`, `source_id`,
and `added_on`. Lists `bank_bullet_ids` and `review_notes` are replaced as a
whole, so preserve existing entries unless deliberately correcting them.
`updated_on` is set from `--on` after processing assignments; supply the
mutation date through `--on` rather than trying to override it with `--set`.

## Event record and provenance

The helper appends events; it does not send a message or submit an application.
Each event uses these fields:

| Field | Contract |
| --- | --- |
| `id` | Unique within the job: job ID plus `-E` and at least three digits; use the highest existing suffix plus one |
| `type` | One of the types in the transition table below |
| `occurred_on` | Actual occurrence date or `null` when unknown |
| `recorded_on` | Actual local date the fact was recorded; helpers always supply it |
| `confirmed_by` | `user`, `tool`, or historical `imported_workbook`; CLI accepts only `user` or `tool` |
| `note` | Nonempty evidence/reason text; describe what the user or authorized tool actually established |
| `contact` | Optional actual contact summary supplied with the event |
| `history_only` | Boolean added by event projection; true means do not project this event into current tracker fields |
| `changes` | Optional object mapping changed fields to `{ "before": oldValue, "after": newValue }` |
| `source_id` | Optional provenance retained on imported events |

Use `tool` for a confirmed result of an authorized action, or for local
preparation/change records the AI actually completed. An AI's guess is not a
tool confirmation. A copied draft is not a `sent` event. The existence of an
application folder is not an `application` event.

The validator allows missing/null occurrence and record dates in historical
events, but new work must always record the known mutation date. It checks
types, dates, IDs, and notes; it does not verify whether the underlying action
really happened or reconcile all historical state automatically.

## Event transitions

For a current, nonhistorical event, the helper first sets `contact` if the
event supplies a nonempty contact value, then applies the rules below. It
records changed summary fields in `changes`. No event changes preparation
booleans or selected bank IDs.

| `type` | Current tracker projection |
| --- | --- |
| `application` | Changes `Unknown`/`Saved`/`Applied` to `Applied`; writes `applied_on` only when the occurrence date is known; does not regress `Interviewing` |
| `sent` | Sets networking to `Reached out`; sets `last_contact` to the actual date, including `null` if unknown |
| `reply` | Sets networking to `Talked`; sets `last_contact` to the actual date, including `null` if unknown |
| `interview_scheduled` | Sets status to `Interviewing`; replaces `interview_on` with the actual scheduled date, including `null` if unknown |
| `interview` | Sets status to `Interviewing`; clears `interview_on` only when it equals this known completed-interview date |
| `offer` | Sets status to `Offer` |
| `accepted` | Sets status to `Accepted` |
| `rejected` | Sets status to `Rejected` |
| `withdrawn` | Sets status to `Withdrew` |
| `posting_closed` | Sets status to `Posting closed` |
| `note` | No hiring/networking transition; a supplied contact can still update the contact summary |
| `tracker_update` | Written by field updates with their before/after values; unavailable as an `event --type` choice |

A terminal outcome is `Accepted`, `Rejected`, `Withdrew`, or `Posting closed`.
`Offer` is not terminal for all purposes, but earlier application/interview
events are prevented from reverting it.

### Dates, backfills, and corrections

- `--on` records today's edit; `--event-date` records when the action happened.
  Omitting `--event-date` keeps it unknown. Never fill it with `--on` by habit.
- Future occurrence dates are allowed only for `interview_scheduled` and
  `note`. Completed events cannot occur after their record date.
- A dated `sent` or `reply` earlier than any existing dated sent/reply event
  or `last_contact` is automatically history-only.
- A dated lifecycle event earlier than any existing dated lifecycle event is
  automatically history-only. That comparison includes `application`,
  `interview`, `offer`, `accepted`, `rejected`, `withdrawn`, and `posting_closed`.
  Scheduled interviews are excluded from this date comparison.
- Application and interview events, including scheduled interviews, are
  history-only while status is `Offer` or terminal. An offer is history-only
  while status is terminal.
- Equal dates do not establish ordering. Same-date events project in recording
  order. Unknown-date events cannot be ordered by their dates. Use
  `--history-only` whenever the evidence is historical and should not change
  the current summary, including backfilled interview appointments.
- A new undated sent/reply event clears `last_contact`, and a new undated
  appointment clears `interview_on`, so the old date cannot start a new timer.
  An undated application event preserves an already-known `applied_on`.
- History-only prevents tracker field projections, not recognition of the
  fact itself. Linked packet context can still recognize a confirmed past
  application or completed interview from that event.

For a mistaken current summary, use `update` with the correction, evidence,
and known dates. For an erroneously typed historical `application` or
`interview` event, a new note alone is insufficient: packet context would
still read the false event. Reconcile that event through a deliberate JSON
edit, preserve its original contents and the correction reason in a new
change/note record, then repair affected summary fields and packet context.
There is no event-delete or event-correction CLI. Never erase valid history
just to make the present state look simpler.

## Company records and settings

Company records require a unique `C` plus at least three digits in `id`, and
a nonempty unique `name`. Company matching is exact and case-sensitive.
Use the highest numeric company ID plus one when adding a company; preserve
IDs when changing a name. If renaming, update all referencing job `company`
values and reconcile linked packet identities together.

The current company schema also contains the following nullable fields:

| Fields | Intended values |
| --- | --- |
| `priority` | `High`, `Medium`, `Low`, or `null`, following job priority conventions |
| `what_they_do`, `industry`, `hq`, `bay_area_office`, `mena_office`, `stage_and_size` | Text or `null`; research, not candidate claims |
| `careers_page`, `job_board` | HTTP(S) URLs or `null` |
| `early_career_program`, `roles_to_search_for`, `why_it_fits`, `notes` | Text or `null`; include dated source/verification context |
| `added_on`, `updated_on` | ISO dates or `null` |
| `source_id` | Existing provenance ID or `null` |

The company validator currently checks identity and name uniqueness, not every
research field. Preserve these conventions yourself. The CLI creates a minimal
company automatically when adding a job for a new exact company name. It has
no standalone company-edit command: edit the company object in JSON, update
its and the root's `updated_on`, and render/check. Record a substantive research
change's source and date in company notes or a source record. Company edits do
not automatically create per-job events.

| Setting | Current value | Effect |
| --- | --- | --- |
| `timezone` | `America/Los_Angeles` | Displayed date context; the script does not convert or discover the current date |
| `contact_followup_days` | `5` | Nonnegative interval after a known latest contact |
| `contact_followup_unit` | `calendar` | `calendar` or `business`; business means Monday–Friday, with holidays counted as weekdays |
| `application_followup_days` | `14` | Nonnegative calendar-day interval after application |
| `lookahead_days` | `7` | Nonnegative calendar-day dashboard horizon; overdue items remain visible |
| `planning_offsets.research` | `10` | Calendar days before the target application date |
| `planning_offsets.networking` | `9` | Calendar days before the target application date |
| `planning_offsets.proof` | `4` | Calendar days before the target application date |
| `planning_offsets.resume` | `2` | Calendar days before the target application date |
| `fit1_decision_days` | `3` | Preserved and validated imported setting; currently not used by the scheduler |

All numeric settings must be nonnegative integers, not booleans. Settings
changes currently require a JSON edit: preserve other settings, record the
user's requested policy and date in an appropriate source note, update root
`updated_on`, and render/check. Do not claim that changing `timezone` schedules
a background job. Nothing here sends notifications or messages.

### How reminders are derived

The renderer uses the JSON's `updated_on` by default, or an explicit `--as-of`
date. It does not use the machine clock. Merely viewing GitHub changes nothing.

1. Terminal jobs have no schedule items.
2. Saved/Unknown jobs without `applied_on` use `apply_by` if present, otherwise
   `deadline`, as the target. Incomplete prep flags produce dated suggestions;
   `Not started` networking produces an outreach suggestion; the target is
   an application item. If both target and deadline exist, scheduling uses
   the target, so inspect a separate earlier deadline yourself.
3. An `Applied` job with `applied_on` gets an application follow-up suggestion.
   Other statuses do not get that reminder.
4. `Reached out` or `Referral asked` with `last_contact` gets a contact follow-up
   suggestion. `Talked`, `Referred`, and `No reply` do not.
5. A known `interview_on` creates an interview item unless the job is `Offer`
   or terminal. A past interview date never becomes a completion event.
6. The dashboard shows the earliest pending preparation suggestion for each
   job, plus other schedule items due on or before the horizon. Job detail
   pages retain the full derived schedule. Preparation progress counts the
   three actual booleans; applying does not mark them done.

Review actual replies, employer instructions, and relevance before following
a reminder. There is no per-job snooze or automated reply detection. Do not
change an actual event date to postpone a reminder; record the real timing
instruction in notes and plan from it.

## CLI contract

Run from the repository root with Python 3; tracker maintenance needs only the
standard library. The one-time XLSX importer has a separate optional dependency
and must not be rerun over the maintained tracker.

Global options must appear before the command:

| Option | Required? | Meaning |
| --- | --- | --- |
| `--tracker PATH` | No | Alternate source; default `tracker/tracker.json` |
| `--dry-run` | No | Print the proposed job record; write no tracker, packet, or views |

| Command | Required arguments | Optional arguments and behavior |
| --- | --- | --- |
| `check` | None | Validate structure/evidence references; print unresolved-data notes |
| `show ID` | Job ID | Print the whole source record; lookup is case-insensitive |
| `update ID` | One or more `--set field=value`, `--on DATE`, `--note TEXT` | `--confirmed-by user\|tool`; required for changes to actual dates, status beyond Saved/Unknown, or networking beyond Not started |
| `event ID` | `--type TYPE`, `--on DATE`, `--note TEXT`, `--confirmed-by user\|tool` | `--event-date DATE`, `--contact TEXT`, `--history-only` |
| `add` | `--company TEXT`, `--role TEXT`, `--on DATE`, `--note TEXT` | `--url URL`, `--confirmed-by user\|tool`; creates Saved / Not started, all prep false, empty selected IDs and history plus its initial note |

`--set` parses `null` as JSON null, boolean fields as exact `true`/`false`,
`fit` as an integer, list fields as JSON arrays, and other values as text.
Quote shell arguments correctly. Preserve whole existing lists when adding
an item. The CLI rejects an identical existing posting URL on `add`; also
check requisition IDs and URL variants yourself to avoid duplicates.

An update that changes no values writes nothing. A successful field update
appends a `tracker_update` event; an add appends a `note`. Both default to
`confirmed_by: tool` for local work when provenance is omitted. Every saved
mutation updates job/root edit dates and regenerates the views.

Actual date fields `applied_on`, `interview_on`, and `last_contact` require
confirmation even when clearing them. The CLI's weaker treatment of Saved,
Unknown, or Not started is not evidence that a completed action can be
silently erased; explain corrections and preserve history.

To refresh generated views without changing source records:

```bash
python3 scripts/render_tracker.py --as-of 2026-10-15
python3 scripts/render_tracker.py --check --as-of 2026-10-15
```

Use the actual desired snapshot date in both commands. `--check` defaults to
root `updated_on`; a different explicit snapshot date must also be supplied
when checking. Render-only refresh does not modify root/job update dates.
The renderer also accepts `--tracker PATH` and `--output-dir PATH`. Render
validation is narrower than tracker validation; run both after source edits.

## Packet linking and contact context

See [application files](../applications/README.md). For an existing tracked job:

```bash
python3 scripts/new_application.py --tracker-id R001 --date 2026-10-15
```

The helper creates a packet under `applications/` with an ID-prefixed slug,
an `application.json` manifest, a full-posting placeholder seeded with imported
role summaries, a resume starter, notes, contact data, and eight letter
templates. It sets `packet_path` and `letters_path`; it does not mark prep done
or set a reviewed `resume_path`. Existing folders and conflicting links are
rejected. These link changes do not currently append a tracker event; the
manifest and source diff record the linkage.

`new_application.py` accepts optional `--tracker`, `--slug`, `--stage`,
`--date`, and `--output-root`. Without `--tracker-id`, `--company` and `--role`
are required. With the ID, supplied company/role must match the tracker.
Use an exact uppercase tracker ID. Dates can be omitted but then stay unknown.
Output outside this repository's `applications/` leaves the tracker unchanged.

The manifest has `schema_version`, `application_id`, `tracker_path`, `company`,
`role`, `job_link`, `req_id`, and `created_on`. The default source reference is
`tracker/tracker.json`. This reference and ID prevent updates through an
alternate tracker copy from changing another tracker's packet.

Packet `application_stage` has a narrower purpose than tracker status:

| Evidence | Inferred packet stage |
| --- | --- |
| Confirmed `interview` event | `interview_completed`; date is the latest known actual interview occurrence |
| `applied_on`, confirmed `application` event, or status `Applied` | `after_application` |
| Status `Saved`, with neither preceding evidence | `before_application` |
| Other state without sufficient evidence | `unknown` on initialization |

An appointment or `Interviewing` label alone is insufficient for completed-
interview wording. The initializer can accept an explicitly known stage, but
rejects before-application if a real application or interview is already
recorded. It validates date/stage consistency.

After event/status/application-date updates, the tracker helper refreshes a
linked `contacts.json` when present and its identity matches. It derives
completion dates from occurrence dates, not append order. It sets a known
application date; unknown input does not automatically erase an already-known
packet date. Other unsupported state may retain the previous packet stage.
For corrections, inspect and reconcile both records rather than assuming the
helper clears every old value.

The helper does **not** append detailed `outreach_events`, research contact
identities, rewrite letter metadata or copy, or revise old submitted resumes.
After an actual event, update those relevant packet records using the same
evidence, then validate them. Tracker event provenance `tool` maps to contact
event provenance `tool_result`, not the literal string `tool`.

The [contact guide](CONTACT-RESEARCH.md) and
[contact validator](../scripts/check_contacts.py) define full identity evidence.
For a packet event, `event_type` is `draft`, `sent`, `reply`, `interview`, or
`application`; `occurred_at` is an ISO date/timestamp or `null`; `recipient_id`
is an existing contact ID or `null`; `confirmed_by` is `user`, `tool_result`,
or `none` for drafts; and `evidence_note` explains the source. Do not invent a
recipient just to populate the event. Scheduled interviews and hiring outcomes
remain in the tracker; the contact event enum does not support those types.

Changing company/role for a linked job is blocked by the update CLI. Reconcile
the tracker, company references, manifest, contacts identity, and packet notes
together through a deliberate edit. Do not create a second identity to avoid
correcting the original.

## Exact update contract without a shell

An AI with file or GitHub editing access can make the same source changes
without running the helpers. A chat-only AI can produce the exact proposed
edits for a file-capable environment; it must not claim they were saved.

1. Read the complete latest source record and relevant packet. Compare current
   content before writing so another session's updates are preserved. Resolve
   identity, evidence, known occurrence dates, and actual local mutation date.
2. For a field edit, capture each changed field's original and final value,
   apply only the intended fields, and append a `tracker_update` event. Its
   occurrence and record dates both equal the mutation date. Use the next
   event ID, actual provenance, nonempty reason, and a `changes` object with
   each changed field's `before` and `after` values. Do nothing if unchanged.
3. For an actual event, append the next-ID event with the actual type, record
   date, known occurrence date or `null`, provenance, evidence note, and
   optional confirmed contact. Apply the backfill guards above; record the
   resulting `history_only` boolean. If false, apply the transition table and
   record only the summary fields that changed in `changes`. If true, leave
   current tracker fields unchanged.
4. For a new job, check existing IDs, URLs, and requisitions first. Add or reuse
   the exact company name. Allocate the next R ID; populate all fields from
   the job tables, with unknown optional values `null`, status `Saved`,
   networking `Not started`, prep false, empty selected IDs/review notes/events,
   and creation/update dates equal to the mutation date. Append its first
   `note` event using that date for occurrence and recording and explain the
   source. New-company optional fields start `null` except creation/update dates.
5. For all job mutations, set the job's and root's `updated_on` to the mutation
   date. Preserve unrelated jobs, settings, source records, and historical
   events. For company/settings edits, follow their separate contracts above.
6. If linked, apply the packet-context rules and record the actual contact
   evidence. For a manual new packet, copy the same template files described
   in [application files](../applications/README.md), create the manifest,
   seed only supported stage/dates, and link only existing material paths.
   A template never completes preparation.
7. Review the full JSON syntax and these constraints, then obtain actual
   validator/render execution in a capable environment. Record whether the
   source was saved, packet reconciled, checks run, views regenerated, and
   GitHub updated. Do not describe manual inspection as a passed validator.

If scripts cannot run, keep the canonical edit reviewable and report that
generated views still need regeneration. Do not hand-edit generated pages
as an alternative source of truth. Any configured repository automation may
finish validation/rendering, but inspect its actual result before claiming
the dashboard is current.

## Verify and publish

After source or packet changes, run the applicable checks:

```bash
python3 scripts/tracker.py check
python3 scripts/render_tracker.py --check
python3 scripts/check_contacts.py applications/actual-packet/contacts.json
git diff --check
git diff --stat
```

The contact command applies only to an existing packet; replace its path.
Use matching `--as-of` when checking a separately refreshed snapshot. For code
changes, the tracker regression suite is:

```bash
python3 -m unittest discover -s tests -v
```

Check that only intended IDs changed, dates are evidence-based, state and
preparation remain separate, selected IDs exist, packet links resolve, and
no draft became a sent/submitted event. Validation checks recorded structure;
it does not verify live openings, identity, deliverability, or completed actions.

Review, commit, and push the source and generated views through the repository's
authorized Git workflow. GitHub reflects pushed commits, not unsaved edits.
Report a local-only result if pushing is unavailable. Preserve the archived
XLSX; this workflow does not update the original Google Sheet.

The helper saves tracker JSON atomically, then renders. If rendering fails,
the source may already be saved; fix the cause and rerun rendering rather
than replaying the event and duplicating history. Linked packet context is
written before tracker save, so inspect both after a partial failure.
Initializer failures after save begins can leave a created packet; reuse or
repair it after inspection instead of overwriting it.

Implementation references:
[tracker updater](../scripts/tracker.py),
[renderer](../scripts/render_tracker.py),
[packet initializer](../scripts/new_application.py), and
[regression checks](../tests/test_tracker.py).
