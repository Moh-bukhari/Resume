# Current work handoff

This is a continuation note for any AI, not a second tracker. Read
[START-HERE.md](../START-HERE.md) and the canonical records before acting.
Replace this note at the end of a session; Git keeps prior versions.

## Last task

- Date: 2026-10-23 (America/Los_Angeles).
- Request: build a tailored resume for the Retell AI Deployment Strategist
  application (tracker R001) using the repo workflow.
- Work: created the packet
  [applications/r001-retell-ai-deployment-strategist](../applications/r001-retell-ai-deployment-strategist/)
  with the full Ashby job description, a company-alignment tailoring brief,
  and a bank-sourced tailored resume (SUM-03 summary; Tamara CRM, SCET,
  AynX, Sitters, SkipLab evidence). The historical root
  `retell-deployment-strategist.tex` was the starting draft; its claims were
  refreshed from the bank (notably SCP-06 added, AynX "Co-founded" corrected
  to the bank's "Founded", 700K+ scoped as historical applicant records).
  Writing review (Humanizer + copy edit + evidence comparison) completed.
- Tracker: R001 `resume_done` and `research_done` set with an evidence note;
  status remains "Saved" — nothing was submitted to Ashby and no outreach
  was sent.

## Current records

- Application state: [tracker/tracker.json](../tracker/tracker.json).
- Candidate facts and answered clarifications: [bank](../bank/experience-bank.md).
- No new application or sent-message events were reported in this task.
- Existing unresolved tracker details remain in each job's review notes.
  Read those before asking for more information or reusing imported proof claims.

## Checks and publication

- `python3 scripts/check_bank.py` passed; `python3 scripts/tracker.py check`
  and `python3 scripts/render_tracker.py --check` passed.
- `bash scripts/build_resume.sh applications/r001-retell-ai-deployment-strategist/resume.tex`
  verified one page, A4, extractable text; extracted text and a rendered
  page image were reviewed (order, contact details, titles, metrics, no
  clipping/overlap). Reviewed PDF saved as the packet's `resume.pdf`.
- Remaining: the user submits on Ashby himself; outreach drafts for Carlo
  Porcelli / Sylvie Liu remain held for his approval (nothing sent).
- No bank/tracker data, application materials, or runtime code was changed;
  their rendering, PDF builds, and application tests are outside this task.
- External platform/competitor references are historical notes and were not
  freshly verified. No prototype or market validation was performed.
- Publication: the commit containing this handoff is intended for `origin/main`.
  On continuation, compare the commit with the actual remote; the file itself
  does not establish publication. No runtime configuration is required.

## Continue here

- For this idea, start at [the latest concept](../EXTERNAL-PROJECTS.md#latest-concept)
  and its [open questions](../EXTERNAL-PROJECTS.md#decisions-and-open-questions).
  First buyer, build scope, platform, and commercial model are unresolved.
- Documentation is the requested deliverable. The user has not requested
  prototype implementation, partner outreach, or recording a workplace in
  this task. The earlier laundry request was explicitly explanation-only.
- For job-search work, use the existing application workflows and canonical
  records. Do not promote this proposed startup into a resume accomplishment.

## Handoff maintenance

Keep the headings above. For an unfinished job task, include its stable ID,
linked packet, completed work, exact pending action, missing fact/access, and
checks actually run. Keep real events and facts in their canonical files first.
