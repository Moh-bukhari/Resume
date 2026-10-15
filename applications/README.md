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
```

For example, a new role could use `applications/example-company-growth-associate/`. Do not overwrite a different role's version. When two postings share a company and title, add a short location or posting identifier to distinguish them. If a submitted version must be preserved while a revision is prepared, create a distinct revision folder and record the relationship in the notes.

- `resume.tex`: complete standalone Overleaf source, tailored from the current bank.
- `resume.pdf`: the locally built, inspected PDF corresponding to that exact source; create it only after validation.
- `job-description.md`: the full supplied or retrieved description, exact title, company, URL, source, retrieval/provision date in the user's timezone, and any access/status limits. Never invent a description from a role title or an inaccessible link.
- `tailoring-notes.md`: copy `templates/application-notes.md`; record selected bullet IDs, evidence, scope limits, gaps, positioning decisions, changes, validation and submission status.

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

8. Deliver the source/PDF and any material limitations. For Overleaf use the complete `resume.tex` with pdfLaTeX. Provide the complete LaTeX in chat when downloads are unavailable.

Leave generated `.aux`, `.log`, `.out` and related build files in ignored `build/`, outside application folders. The templates are starting points and contain no record of validation for a new version.

## Status

Every new version starts as **draft**, with **no submission recorded**. Creating a folder, compiling a PDF, or reviewing a resume does not mark a job applied to. Drafting alone does not authorize submitting applications or sending emails, LinkedIn messages or other outreach; follow explicit user instructions for any such action. Record an actual submission only when the user explicitly confirms it, with its date and the confirmed action.
