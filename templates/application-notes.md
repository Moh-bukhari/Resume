# Application tailoring notes

Copy this file into `applications/<company>-<role>/tailoring-notes.md` and replace the placeholders. Record completed work and observed evidence; leave unperformed checks marked pending. A resume draft does not record a submitted application.

## Target and version

- Company: [company]
- Exact role title: [title from the supplied/official description]
- Posting URL: [URL; do not infer a title from a URL identifier]
- Location / work arrangement: [as stated in the description]
- Job-description source: [user-supplied / official posting / other identified source]
- Source obtained on: [YYYY-MM-DD, user/client timezone]
- Full description file: `./job-description.md`
- Description or posting-access limitations: [none known / describe]
- Version created/updated: [YYYY-MM-DD, user/client timezone]
- Resume source: `./resume.tex`
- Reviewed PDF: `./resume.pdf` [pending until a checked artifact is copied here]
- Document status: **draft**
- Submission status: **no submission recorded**
- Submission evidence/date, only if explicitly confirmed by the user: [not supplied]

## Requirements and selected evidence

Use `bank/experience-bank.json` as the factual source. Consult `skills/README.md` for the relevant bundled resume skills, then select a few strong, non-overlapping bullets. Preserve each bullet's metric units, ownership, dates, and scope notes. Job requirements are not evidence of candidate experience.

| Job requirement | Selected bullet ID(s) | Relevant evidence / wording | Scope or gap |
| --- | --- | --- | --- |
| [requirement] | [TAM-09, etc.] | [supported wording] | [limit or missing evidence] |

- Selected summary or rewritten summary: [bank summary ID / supported draft]
- Selected experience and project order: [Tamara first by default]
- Selected skills: [only skills supported in the bank]
- Source IDs for new or changed factual claims: [SRC identifiers]
- Facts updated from a new explicit user correction: [none / exact correction and source]
- Details intentionally omitted for relevance or space: [items]
- Material fit gaps: [missing required experience, availability constraints, etc.]
- Questions that materially affect this draft: [none / concise questions; continue independent work]

When changing shared facts, edit the JSON first, preserve source/status/scope metadata, then regenerate and check the bank from the repository root:

```bash
python3 scripts/render_bank.py
python3 scripts/check_bank.py
```

Do not revive retired SCET ROAS/CPL/conversion-value claims or ask for those figures again. Keep planned work distinct from completed work, historical applicant volume distinct from new intake, and personal job-search outcomes distinct from customer or recruiting outcomes. The job-search tool's 75+ threshold is not a percentage or accuracy result.

## Changes and review

- Baseline compared: [template path or prior application version]
- Changes to positioning: [what changed and why it fits the description]
- Changes to selected evidence: [bullet IDs added/removed/combined]
- Changes to LaTeX/layout: [content/order/spacing changes]
- Factual review: [pending / findings and correction]
- Scope/ownership/date review: [pending / findings and correction]
- Text diff reviewed: [pending / files and result]
- LaTeX diff reviewed: [pending / files and result]

Keep the complete standalone LaTeX document. Preserve legacy drafts unless the user explicitly asks to replace one. If using a prior application as the baseline, refresh its claims from the current bank rather than treating that old resume as authoritative.

## Build and validation record

Commands below are examples from the repository root; substitute the actual application folder. They are not a record of completed validation.

```bash
python3 scripts/check_bank.py
bash scripts/build_resume.sh applications/company-role/resume.tex
pdfinfo build/resume/resume.pdf
pdftotext -layout build/resume/resume.pdf -
```

The helper puts generated files under ignored `build/<stem>/`. Verify the output associated with this successful build before copying its PDF into the application folder. In the example above the stem is `resume`.

- [ ] Bank consistency check passed. Command/date/result: [pending]
- [ ] pdfLaTeX build succeeded. Command/date/result: [pending]
- [ ] Page count is **1** and paper is **A4**. Evidence: [pending]
- [ ] Body text remains readable **10pt**; shorten content before reducing font size.
- [ ] Extracted PDF text has the correct order, contact details, dates, titles, metrics and characters. Evidence: [pending]
- [ ] Full-page visual review found no clipping, overlapping text, crowded headings or unreadable links. Evidence: [pending]
- [ ] Compiler warnings affecting layout were resolved or documented. Evidence: [pending]
- [ ] Final `.tex` and PDF contain the same selected wording and facts. Evidence: [pending]
- [ ] Reviewed PDF copied to `./resume.pdf`. Build artifact/date: [pending]
- [ ] Application notes and full description are saved beside the resume.

Overleaf delivery: upload the complete standalone `resume.tex`, select it as the main document, and use **pdfLaTeX**. If the user cannot download files, provide the complete source in chat. Only mark checks completed when they were actually run and inspected.

## Submission record

Preparing these files does not authorize or establish an application, email, LinkedIn message, or other outreach. Update submission status only from explicit user confirmation; record the date and confirmed action rather than inferring it from file creation.

## Contacts and letters

- Current-state/evidence record: `contacts.json`
- Selected recipient ID, relevance, and fallback: [researched choices]
- LinkedIn source and current-role confidence: [source/date/limits]
- Professional email origin and verification: [record separately]
- Outreach plan: `outreach-plan.md`
- Needed letter type, chosen stage, and draft file(s): [under `letters/`]
- Company/recipient sources and candidate bank IDs: [outside copyable text]
- Contact validation: [pending / actual result]
- Actual sent/reply/application/interview events: [confirmed events only]

Follow `docs/CONTACT-RESEARCH.md` and `docs/LETTERS.md`. The starter helper
creates unused drafts; finalize the variants fitting the actual stage. Keep
inferred addresses labeled and unknown dates unknown. Drafts start no timers.
