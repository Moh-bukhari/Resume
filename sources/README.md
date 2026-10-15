# Preserved sources

The [humanizer research record](skill-research/2026-10-15-humanizers.json)
preserves dated repository adoption, pinned revisions, source URLs, and selected
file hashes for the required writing review. See the
[comparison](../docs/HUMANIZER-SELECTION.md) for decisions and access limits.

- [user-supplied-resume.tex](user-supplied-resume.tex): original uploaded resume,
  preserved as received. It is historical input; current bank corrections win.
- Bank `SRC` records capture additional firsthand answers so the previous
  conversation is unnecessary.
- [CRM study](../tamara-crm-study.md): static implementation evidence at the
  named upstream commit, with explicit limits on live/runtime claims.
- [Known job requirements](../jobs/README.md): user-supplied target inputs,
  not proof of current vacancies or candidate skills.
- [Skill research snapshot](skill-research/2026-10-15-adoption.json): dated
  repository popularity, publisher, maintenance, and pinned-source observations
  for the [skill comparison](../docs/SKILL-SELECTION.md). These are repository
  counters, not skill-level installs or tested outreach results. Original
  skills and licenses are preserved separately under `skills/`.
- [Original job tracker](job-search-tracker-original.xlsx): unchanged uploaded
  workbook, retained as an archive. [Import provenance and limits](job-search-tracker-import.md)
  document the extraction. The current operational master is
  [tracker/tracker.json](../tracker/tracker.json); old workbook instructions and
  candidate-analysis cells do not override the bank or active instructions.

The original upload is not a fresh tailored deliverable and is not guaranteed
to compile unchanged. Start new work from `templates/resume-base.tex`.
Use relative paths for future documents. Never include credentials or real
applicant/candidate data.
