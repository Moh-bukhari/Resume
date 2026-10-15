# Use the experience bank

Start with [experience-bank.md](experience-bank.md), the complete master
reference for future tailoring. It contains 13 experience/project groups,
72 selectable bullet options, 21 numeric facts, four awards, skills,
coursework, summary options, role maps, source notes, and open questions.

Latest clarifications: 700K+ is the historical applicant base, with further
event/prospect intake; internal CRM users and COO-led invitation workflows are
recorded. SCET's custom AI/HubSpot API workflow filters 100K+ multi-source leads
into 500 priority targets. Embersafe has a five-person team, with personal
ownership of needs/compliance surveys and the resident frontend for household
intake, assistance checks, and contractor-discount access. City-council
engagement in the Sonoma area is `planned_only`, following the user's latest
correction that it is still planning. The $1M+
government-funding figure is problem context, not funding raised or managed.

Job search, OpenClaw/Raspberry Pi, and the personal assistant are separate
projects. The job-search workflow has concrete tasks: resume matching,
qualification scoring, a 75+ routing threshold, spreadsheet tracking,
application preparation, role-lead contact discovery, and outreach drafts.
Developed in 2025 with Claude/GPT-assisted coding and minor Python edits, it
processed 2,000+ jobs in one month. The personal search involved 221 applications,
interviews with 17 different companies, and seven distinct offers. Keep the
processing window separate from the full outcome timeline. The user continued
with Tamara; the tool's development year does not alter Tamara's start date.
OpenClaw and assistant capabilities remain `needs_detail`. Original bullet IDs
are retained across the separated entries.

The user identified Berkeley Big Ideas as Embersafe's date reference. Official
calendar lookup was blocked by the environment's network proxy (HTTP 403);
exact cycle and project dates remain unverified. Do not copy Rasma's dates.

- [experience-bank.json](experience-bank.json) is the editable factual master
  for AI tools and future updates; Markdown and CSV are generated views.
- [bullet-bank.csv](bullet-bank.csv) contains one bullet option per row for
  spreadsheet filtering by experience, role tags, status, and source.

The master bank is intentionally longer than a submitted resume. Choose a few
relevant bullet IDs, combine overlapping angles, and produce a separate
one-page version for each role. Never treat alternative wordings as additional
achievements or add their numbers together.

When new facts arrive, edit JSON and run `python3 scripts/render_bank.py` and
`python3 scripts/check_bank.py` from the repository root. Preserve stable
bullet IDs. New entries can use the next
available number for the relevant experience. Older application PDFs should
remain unchanged unless the user requests a revision.

Default preferences: Tamara first, readable 10pt text, a full standalone
Overleaf document, pdfLaTeX, and copyable code in chat. File downloads have
previously been unreliable for the user.

Use only supported facts. Keep approximate counts, shared credit, implementation
stage, system-record scope, and expected graduation accurate. The retired
SCET acquisition figures stay excluded. Existing Retell/Mercor draft submission
status remains unknown; the 221 applications refer to the prior personal search.

For a new job, supply its full description and say:

> Use my master experience bank to tailor a one-page resume for this role.
> Select the most relevant bullet IDs, explain any important evidence gaps,
> and provide complete Overleaf-ready LaTeX. Preserve titles, dates, metric
> scope, and personal versus team credit. Keep Tamara first unless I ask otherwise.
