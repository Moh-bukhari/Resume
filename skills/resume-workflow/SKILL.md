---
name: resume-workflow
description: Tailor and maintain Mohammed Bukhari's factual one-page Overleaf resumes using this repository's bank, skills, source notes, and validation tools.
---

# Resume workflow

Use for tailored resumes, bank updates, comparisons, or Overleaf repairs.
Read `AGENTS.md` first. Paths below are relative to the repository root.

1. Load `bank/experience-bank.json` or its generated Markdown. Select supported
   bullet IDs and scopes; current user corrections override older drafts.
2. Read the full target JD. Use `skills/README.md` to select upstream
   `job-description-analyzer`, `resume-tailor`, `resume-bullet-writer`, and
   `resume-formatter` as needed. Examples are not candidate facts.
3. Follow `docs/TAILORING.md`: Tamara first, readable 10pt body, A4, one page,
   pdfLaTeX. Reframe evidence; never invent missing tenure, outcomes, or tools.
4. Copy `templates/resume-base.tex` into a new application folder according to
   `applications/README.md`. Record JD, selected IDs, gaps, and status in
   `tailoring-notes.md` using `templates/application-notes.md`.
5. Run `python3 scripts/check_bank.py` and
   `bash scripts/build_resume.sh <path-to-resume.tex>`. Review extracted text
   and PDF layout; record actual checks and remaining limitations.
6. Provide complete standalone LaTeX in chat, including preamble and body,
   because prior downloads and snippets failed for the user.

For new facts, follow `docs/MAINTENANCE.md`, edit JSON, then regenerate Markdown
and CSV. Never maintain a competing factstore in a tailored resume.

Submitting applications, sending outreach, and editing external profiles are
separate actions governed by the user's request, not by the existence of a skill.
