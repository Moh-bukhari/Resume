# Job Search Tracker workbook import

Imported on **2026-10-15** (America/Los_Angeles).

- Original upload: `Job Search Tracker.xlsx`.
- Preserved archive: [`job-search-tracker-original.xlsx`](job-search-tracker-original.xlsx).
- SHA-256: `ea9b69723e339ac8264ae96df2258de398a3fa2d5147c4ad149b014caa65f031`.
- Editable tracker: [`tracker/tracker.json`](../tracker/tracker.json).
- Imported **10 jobs** and **41 companies**.
- Existing job IDs are preserved. Company IDs follow the original nonempty row order.
- Blank cells remain `null`; checkboxes become booleans; dates use `YYYY-MM-DD`.
- Original per-row added/updated dates are retained. The root date records this import.

## What was preserved and excluded

The original workbook is byte-identical to the upload. It was opened read-only
with `data_only=True`; it was never saved through openpyxl. Historical text
fields are preserved, including typos and literal line breaks/escape sequences.
The source workbook contains Home, Jobs, Companies, AI Guide, and Lists tabs.

Jobs formula columns **E:G** (next step, due, progress) and **AO:AQ** (follow-up,
group, role key), and Companies formula counts **Q:R**, were excluded. Generated
views calculate current results from tracker facts. Empty ID rows were skipped,
even where unchecked boxes were present. Home settings D73:D80 were imported;
the original five-calendar-day contact follow-up policy remains explicit.

The hidden **AI Guide is archived document content, not active instructions**.
Its stale biography and instructions do not override AGENTS.md or the factual
bank. Lists is not a source of candidate accomplishments. No formula, macro,
embedded instruction, network link, or external program was executed.

## Evidence and review

All source text is imported evidence, not independently verified live job data.
Company fundraising, hiring status, job requirements, suggested fit scores,
and planning deadlines need refresh before relying on them. Imported
`strongest_proof`, `gaps`, and `prep_plan` are historical assessments, not new
resume facts. Each job has review notes; unsupported AynX outreach-engine,
solo-founder, SCET audit-pipeline, SDK, and Fortune 500 claims are flagged where
present. Stale Tamara requirements-only and SCET-title descriptions are flagged.
Use `bank/experience-bank.json` for all candidate claims.

**1 application event(s)** were imported from explicit Applied on
dates. R010 records an application on **2026-10-14** and Networking **Reached
out**, but no contact, last-contact date, log, or job URL. The application event
is marked `confirmed_by: imported_workbook`; no sent outreach event or recipient
was invented. Its source role typo, **Growth Assosiate**, remains with a review
note pointing to the user-supplied **Growth Associate** title. All new packet,
resume, and letter paths start empty; no prep work is marked complete by the
migration.

## Reproducing the one-time migration

The importer alone requires openpyxl. Routine updates and generated views use
Python's standard library. Do not rerun the importer over the maintained tracker:
it would discard later edits. By default it refuses to overwrite any of its
three outputs; `--force` is only for an intentional fresh migration.

```bash
python3 scripts/import_tracker_xlsx.py \
  --input /path/to/Job\ Search\ Tracker.xlsx \
  --output tracker/tracker.json --on 2026-10-15
```

The output is expected under `<toolkit-root>/tracker/`; its archive and this
note are written under the adjacent `sources/` directory. No files are written
until the input, dates, required headers, IDs, field types, and settings pass
validation. This import does not submit applications or send messages.
