# Application versions

Store each tailored resume and its evidence in a separate folder. Start from the current `bank/experience-bank.json`, the guidance in `skills/README.md`, and `templates/resume-base.tex`. Existing application drafts and PDFs are prior versions, not the factual master or a record of submission.

Use lowercase, hyphen-separated company and role slugs:

```text
applications/
  company-role/
    resume.tex
    resume.pdf
    job-description.md
    tailoring-notes.md
    contacts.json
    outreach-plan.md
    letters/
```

For example, a new role could use `applications/example-company-growth-associate/`. Do not overwrite a different role's version. When two postings share a company and title, add a short location or posting identifier to distinguish them. If a submitted version must be preserved while a revision is prepared, create a distinct revision folder and record the relationship in the notes.

Start a packet from the repository root:

```bash
python3 scripts/new_application.py --company "Example Company" --role "Growth Associate"
```

Use `--stage before_application`, `--stage after_application`, or
`--stage interview_completed` only when known. Default: `unknown`. Optional
`--date YYYY-MM-DD` records the creation date, not an application/interview
date. `--slug` distinguishes similar postings; see `--help`. Existing folders
are never overwritten. The helper scaffolds drafts; research, tailoring,
finalizing letters, and PDF validation remain AI tasks.

- `resume.tex`: complete standalone Overleaf source, tailored from the current bank.
- `resume.pdf`: the locally built, inspected PDF corresponding to that exact source; create it only after validation.
- `job-description.md`: the full supplied or retrieved description, exact title, company, URL, source, retrieval/provision date in the user's timezone, and any access/status limits. Never invent a description from a role title or an inaccessible link.
- `tailoring-notes.md`: copy `templates/application-notes.md`; record selected bullet IDs, evidence, scope limits, gaps, positioning decisions, changes, validation and submission status.
- `contacts.json`: sourced identities, found LinkedIn URLs, professional email
  origin/verification, application stage, and separately confirmed events.
- `outreach-plan.md`: recipient/channel, evidence, stage, and suggested timing.
- `letters/`: eight unused template drafts initially; finalize the needed
  types and omit unused variants when presenting a finished packet.

Use [contact research](../docs/CONTACT-RESEARCH.md),
[letter guidance](../docs/LETTERS.md), or the
[complete workflow](../skills/application-workflow/SKILL.md). Current-state
records belong in `contacts.json`; draft/notes metadata should match that
state. Unknown dates stay unknown.

## Workflow

1. Read the current bank and relevant skills. Keep Tamara first by default. Select supported facts for this role; do not import superseded claims from old drafts.
2. Create the version folder and copy in the standalone base and notes template. Save the full job description and source details.
3. Tailor the content, recording selected bullet IDs and material gaps. Keep body text at 10pt on one A4 page; remove less relevant content before shrinking it.
4. If facts change, edit `bank/experience-bank.json`, regenerate the derived Markdown/CSV, and run the consistency check from the repository root:

   ```bash
   python3 scripts/render_bank.py
   python3 scripts/check_bank.py
   ```

5. Build the chosen source from the repository root. The following example assumes that application folder already exists:

   ```bash
   bash scripts/build_resume.sh applications/company-role/resume.tex
   ```

   Generated files go under ignored `build/<stem>/`; for this filename the PDF is `build/resume/resume.pdf`. Other application sources named `resume.tex` use the same output stem, so inspect and copy the correct successful build before building another version.

6. Review the source/text diff, compiler output, PDF page count and paper size, extracted text, and full-page appearance. Record the actual results in `tailoring-notes.md`; a successful compile alone does not establish one-page fit or correct content.
7. After validation, manually copy the reviewed artifact to the version folder:

   ```bash
   cp build/resume/resume.pdf applications/company-role/resume.pdf
   ```

8. Research the relevant contact and create stage-appropriate drafts using
   the guides above. Check the evidence record:

   ```bash
   python3 scripts/check_contacts.py applications/company-role/contacts.json
   ```

9. Deliver the source/PDF, requested copyable letters, sourced contacts, and
   important gaps. Provide complete Overleaf LaTeX in chat when downloads fail.

Leave generated `.aux`, `.log`, `.out` and related build files in ignored `build/`, outside application folders. The templates are starting points and contain no record of validation for a new version.

## Status

Documents start as **drafts**. Application status defaults to **unknown/no
submission recorded**, unless a known stage was supplied. File creation does
not mark a job applied to or an email sent. Record real events from user
confirmation or a confirmed result of a separately authorized action, with
dates when known. Drafting does not authorize applying or sending outreach.
