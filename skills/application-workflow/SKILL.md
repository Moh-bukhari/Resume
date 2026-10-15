---
name: application-workflow
description: Build a complete per-job packet combining a tailored Overleaf resume, sourced contact research, stage-appropriate letters, and application notes.
---

# Complete application packet

Use when the user wants the resume and letters for one job, or wants to find
the right person to contact. Read `AGENTS.md` first.

1. Load the full JD, factual bank, existing application folder if any, and
   confirmed application state. Unknown status stays unknown.
2. For a new target, run `scripts/new_application.py --help`, then initialize
   a folder with company/role and known stage/date. This scaffolds drafts; it
   does not perform research, write tailored claims, apply, or send anything.
3. Use `resume-workflow` for the supported one-page LaTeX resume and optional
   formal cover letter. Build/review as documented.
4. Use `contact-research` to identify a relevant recipient, LinkedIn route,
   and professional email evidence. Public-source research is the default;
   tools that are unavailable stay unavailable.
5. Use `docs/LETTERS.md` to choose timing. For an open role, do not delay a
   required application waiting for a cold-email reply. A pre-application
   question/referral is useful when there is a real uncertainty or connection.
6. Use `application-letter-writer` for one primary outreach draft and a useful
   LinkedIn/follow-up variant. Save evidence and timing in `outreach-plan.md`.
7. Check bank/contact records, PDF, links, stage language, and consistency
   between resume and letters. Keep unsent drafts separate from confirmed
   sent/application/interview events.

Return the complete LaTeX and requested copyable letters, contact sources and
uncertainty, and the next recommended step. Keep all artifacts in
`applications/<company>-<role>/`. No sending or application submission is implied.
