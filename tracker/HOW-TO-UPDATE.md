# Update the tracker

New AI session: [START-HERE.md](../START-HERE.md). For complete procedures use
[WORKFLOWS.md](../docs/WORKFLOWS.md); for every field, event, correction, and
manual edit use [TRACKER-REFERENCE.md](../docs/TRACKER-REFERENCE.md).

Read [the dashboard](README.md), choose the stable job ID, and use
[the tracker guide](../docs/TRACKER.md) for ownership and evidence rules.
Commands run from the repository root. Example dates and notes below are
illustrative; replace them with the actual date and supported facts.

## Ask an AI

> Show R010 and its linked packet. Prepare the next useful resume or letter
> using the current bank and application workflow. Update preparation only
> after completing the work. Keep applications, sent messages, and outcomes
> unchanged unless I confirm them. Regenerate, validate, and publish the tracker.

For an actual event, give the ID, what happened, the date if known, and the
contact/channel if relevant. For example: “I sent R001's LinkedIn message to
[name] on [date]. Record that and suggest the next step.” An unknown date stays
unknown; the date the AI edits the tracker is not automatically the event date.

## Inspect and change fields

```bash
python3 scripts/tracker.py show R001
python3 scripts/tracker.py check
python3 scripts/tracker.py --dry-run update R001 --on 2026-10-15 --set research_done=true --note "Reviewed the official description and saved the sourced role research."
```

Remove `--dry-run` to apply a reviewed change. Repeat `--set field=value` for
multiple fields. Mark preparation complete only after the work is actually
done. Use `--confirmed-by user` or `--confirmed-by tool` when changing actual
application status/dates or networking activity; the note must explain the
confirmation. Prefer an event for a new application, conversation, or outcome
so its history is preserved.

## Record a confirmed event

```bash
python3 scripts/tracker.py --dry-run event R001 --type sent --on 2026-10-15 --event-date 2026-10-15 --confirmed-by user --contact "Recipient name" --note "User confirmed sending the LinkedIn message to this person on this date."
```

Only run that example for a real confirmed message. `--on` is the mutation
date; `--event-date` is when the event occurred. Omit the latter when unknown.
Supported event types are `application`, `sent`, `reply`, `interview_scheduled`,
`interview`, `offer`, `accepted`, `rejected`, `withdrawn`, `posting_closed`, and
`note`. Scheduling an interview does not record its completion.
Use `--history-only` when backfilling an older event that should not change
current status or reminder dates. Clearly older contact events and earlier
pipeline stages are also prevented from regressing current state. A new
undated contact or interview appointment leaves its reminder undated rather
than reusing the previous event's date.

When a packet exists, also update its `contacts.json` with the same supported
facts and evidence. Do not infer a recipient, a date, or a sent message from
the tracker's summary. Validate the contact file after editing it.

## Add a job or create its packet

```bash
python3 scripts/tracker.py --dry-run add --company "Example Company" --role "Growth Associate" --url "https://example.com/careers/growth-associate" --on 2026-10-15 --note "New target supplied by the user; posting still needs review."
python3 scripts/new_application.py --tracker-id R010 --date 2026-10-15
```

Replace the example job with a real target, review the dry run, then remove
`--dry-run`. Keep the assigned ID. Use an existing ID for an existing target;
never change IDs to match display order. The packet helper creates unreviewed
drafts and refuses to overwrite existing folders.

## Publish and refresh

Mutations regenerate the Markdown and CSV views automatically. Review the
diff, run checks, then commit and push through the repository's normal Git
workflow. The hosted dashboard changes after the commit is pushed.

```bash
python3 scripts/tracker.py check
git diff --stat
git diff -- tracker/tracker.json
```

For direct edits with GitHub's pencil button, edit **`tracker/tracker.json`**,
not the generated pages. Ask an AI to validate and regenerate after the edit:

```bash
python3 scripts/render_tracker.py --as-of 2026-10-15
python3 scripts/tracker.py check
```

Commit and push those generated changes too. The “as of” date is explicit:
GitHub does not recalculate reminders daily. Re-render for a fresh daily view;
do not change historical event dates to refresh the dashboard.

Advanced: `--tracker PATH` is a global option, placed before the command, for
working with another tracker file. The default is `tracker/tracker.json`.
