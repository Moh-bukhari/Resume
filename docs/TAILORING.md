# Tailoring a resume

Use this repository to select and explain Mohammed Bukhari's documented work for
a particular role. A tailored resume is a selection from the bank, not a new
source of facts.

For every tailored version, follow [company alignment](COMPANY-ALIGNMENT.md).
Map the company's mission and current goals to this role and supported bank
evidence in `tailoring-notes.md`; use that map to choose the summary, bullets,
and projects. Review the connection before marking the resume ready.

Before the final build and delivery, apply
[Professional Writing Review](../skills/professional-writing-review/SKILL.md)
to the summary and bullets. Record the result in `tailoring-notes.md`. Keep
accurate action verbs, technical terms, metrics, and scope; then rebuild the
final LaTeX so the reviewed wording is the wording in the PDF.

## Start here

1. Read [AGENTS.md](../AGENTS.md) for repository instructions and
   [the skills guide](../skills/README.md) for the relevant bundled skills.
2. Read [the experience bank](../bank/experience-bank.md), especially the target
   role map, metric scope, bullet status, and unanswered questions. Edit
   [experience-bank.json](../bank/experience-bank.json) when facts change; the
   Markdown and CSV views are generated.
3. Obtain the actual job description. Save its URL and the text used in
   `applications/<company>-<role>/job-description.md`. A company name or posting
   URL alone does not establish the requirements. If a posting cannot be read,
   ask for its text or clearly label work as provisional.
4. Use [resume-base.tex](../templates/resume-base.tex) for the layout. Existing
   [Mercor](../mercor-growth-associate.tex) and Retell
   [deployment](../retell-deployment-strategist.tex) /
   [AI agents](../retell-founders-initiatives.tex) versions are examples of
   emphasis. **The current bank supersedes their older factual wording.**

For Tamara technical details, consult [the CRM study](../tamara-crm-study.md).
Its code review supports features, not a live database count or performance
benchmark. [The original fit notes](../retell-fit-notes.md) provide context for
the two supplied Retell descriptions; check the current posting for changes.

## What can change

| Choice | How to use it |
| --- | --- |
| Summary | Select or combine supported themes from the bank's `summaries`; keep it to roughly two or three short lines. Name the work that makes the positioning credible. |
| Bullet selection | Choose the most relevant evidence, usually two to four bullets for a major role. IDs are options: several variants can describe the same achievement. |
| Bullet merging | Combine compatible facts from one experience; preserve source IDs and metric scope in the notes. Do not add their counts together or repeat the same result as separate wins. |
| Emphasis | Change ordering, verbs, and selective bolding so the first lines answer the job's main requirements. Use job terminology only when it describes supported work. |
| Experience order | Keep **Tamara first** unless the user explicitly changes that preference. Reorder the remaining entries for relevance while retaining their real dates and titles. |
| Projects | Select the strongest two or three for this role. A shorter project section can make room for relevant professional work. Omitted projects remain in the bank. |
| Skills and coursework | Prioritize confirmed tools and applicable coursework; remove irrelevant items before shrinking text. A tool in a job description is not evidence the candidate used it. |
| Education placement | Keep expected May 2027 graduation visible. Education can move upward for student/engineering roles or downward when recent work better answers the job. |
| Layout | Keep A4, 10pt body text, a single column, and pdfLaTeX compatibility. Shorten content before tightening spacing. |

## Starting selections by role

These are evidence maps, not a checklist to fit on one page. Read each bullet's
scope note before using it; the bank's `role_maps` has broader alternatives.

| Target | Lead story and useful bullet IDs | Supporting choices and gaps |
| --- | --- | --- |
| **Mercor Growth Associate / sourcing** | Sales Navigator funnel, relationship-building, qualified pipeline, and shared CRM: `TAM-06`, `TAM-26`, `TAM-05`, `TAM-02`, `TAM-15`. Add SCET lead prioritization `SCP-06`. Start with `SUM-02` or the combined `SUM-01`. | Partnerships and outbound automation support the sourcing story. The personal job-search project (`PAI-08`, `PAI-09`) can demonstrate funnel operations if space permits. Early-career candidates are not established medical/domain experts; LinkedIn Recruiter use is unconfirmed. |
| **Retell Deployment Strategist / product or solutions** | Stakeholder discovery, workflow mapping, shared adoption, and implementation: `TAM-08`, `TAM-09`, `TAM-25`, `TAM-14`, `TAM-15`. Use `SUM-03`. | Embersafe discovery and feedback (`EMB-01`, `EMB-02`, `EMB-04`/`EMB-05`) and Sitters voice AI (`SIT-01`, `SIT-02`) add relevant examples. Internal CRM use and prototype demos do not establish external enterprise production deployments or measured customer ROI. |
| **Retell Founders Initiatives, AI Agents / internal tools** | Practical integration and automation: select a few from `TAM-10`–`TAM-13`, `TAM-18`, `TAM-19`, `TAM-21`, plus `SCP-06`/`SCP-07`. Use `SUM-04`. | Sitters and the job-search workflow show additional building. Explain systems and ownership clearly. The required professional SWE tenure and production LLM experience are not established merely by changing titles or counting student projects. |
| **Aerospace / simulation** | Keep Tamara first but concise; give space to propulsion/CAD/CFD/MATLAB (`SEB-01`–`SEB-03`), STAR design (`STR-01`–`STR-03`), and AynX (`AYN-01`–`AYN-04`). Use `SUM-06`. | Move education/coursework higher and prioritize engineering tools. Distinguish design and simulation from manufactured, tested, or flown hardware; substantial physical hardware results have not been supplied. |

## Preserve the meaning of the evidence

The bank's `tailoring_rules` and per-item notes are the detailed authority. These
are recurring distinctions that affect wording:

- **Tamara:** 700K+ is the historical applicant base, with attendee/prospect
  intake additional. It is not 700K+ personally sourced people or active users.
  The 500+ qualified candidates came through summer channels, not necessarily
  Sales Navigator alone. Search uses AI-assisted structured filters; do not
  replace that with AI resume ranking. Sales Navigator connects to the sourcing
  workflow; a direct LinkedIn/Sales Navigator API integration is not established.
- **SCET:** 100K+ leads filtered to 500 targets describes selection scope, not
  enrollments or conversion. $100K+ is shared-project payments; $50K is ad spend.
  Retired ROAS/CPL/lead-value claims must stay excluded and need not be requested
  again.
- **Job-search project:** the 2025 build used Claude/GPT-assisted coding and
  minor Python edits. Processing 2,000+ jobs took one month; the full period for
  221 applications, 17 companies interviewing, and seven offers is not supplied.
  These are personal-search results, not a demonstrated causal lift. The 75+
  threshold has no confirmed denominator. Preparation and drafts do not imply
  autonomous application submission or message sending.
- **Embersafe:** the user owned surveys and the resident frontend within a
  five-person team. Sonoma-area council engagement is **planning**, not a live
  deployment. The $1M+ funding figure describes the coordination problem, not
  funding raised, managed, or saved. Exact Big Ideas cycle/project dates remain
  unverified; another project's dates or a competition calendar do not prove them.
- **Project maturity:** `ready` permits the scoped wording supplied; it is not
  independent verification. `needs_detail` entries require more detail before
  expansion. `planned_only` is prospective context, never a completed outcome.
  OpenClaw and the personal assistant remain separate, lightly documented
  projects. Do not invent capabilities or transfer another project's stack.

## Draft, verify, and save

1. Extract the job's main responsibilities and requirements. Match each to
   specific bank IDs; identify material gaps rather than inventing a match.
   Ask only questions that materially affect the draft and are not already
   answered in `answered_clarifications`.
2. Select a small evidence set and rewrite it for relevance. Preserve individual
   versus team credit, approximation, dates, units, and project maturity. Keep
   the summary consistent with the selected evidence.
3. Create a separate directory under `applications/<company>-<role>/` with
   `resume.tex`, `job-description.md`, and `tailoring-notes.md`. In the notes,
   record target/URL, source text, selected bullet and metric IDs, wording
   decisions, material gaps, and verification results. Submission status is
   taken from confirmed tracker/packet evidence; otherwise use “unknown / no
   submission recorded.” Mark submitted only when the user confirms an actual
   submission or an authorized tool returns evidence that it succeeded.
   Permission to apply does not establish that the application happened.
4. Produce a **complete standalone LaTeX document** with the preamble and
   `\begin{document}` / `\end{document}`. Escape LaTeX special characters in
   prose. Do not give only a section fragment for replacing an Overleaf document.
5. From the repository root, run:

   ```bash
   python3 scripts/check_bank.py
   bash scripts/build_resume.sh applications/<company>-<role>/resume.tex
   ```

   Read the build script's output for the generated PDF path. Verify one A4
   page, readable 10pt body text, clean text extraction, working contact links,
   and no clipped/overlapping text. Inspect the PDF visually when a viewer is
   available; compilation alone does not prove good layout. If compiling is
   unavailable, state what remains unverified.
6. Save the reviewed PDF as `applications/<company>-<role>/resume.pdf`. Return a
   short explanation of the emphasis and any material gap, plus the **full
   copyable LaTeX in chat**: downloads have previously failed for this user.

New user corrections should update the JSON bank first, then regenerate its
views with `python3 scripts/render_bank.py` and run the bank checks. Existing
application snapshots should remain recognizable; identify any revision you
make rather than treating a saved draft as a new fact source.
