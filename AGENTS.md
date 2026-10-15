# Instructions for AI assistants

This is Mohammed Bukhari's application toolkit. Maintain the factual bank,
produce one-page Overleaf resumes, research relevant professional contacts,
and write stage-appropriate letters. No prior chat or files outside this
checkout are needed.

## Read in this order

1. This file.
2. `bank/experience-bank.md` for profile, bullets, metrics, summaries, sources,
   role maps, and gaps. Edit facts in `bank/experience-bank.json`.
3. `skills/README.md` and the task guide: `docs/TAILORING.md` for resumes,
   `docs/CONTACT-RESEARCH.md` for people, `docs/LETTERS.md` for letters.
4. The full target JD. Known user-supplied requirements are under `jobs/`;
   these are historical inputs, not verified current openings.
5. `templates/resume-base.tex` for the current standalone layout.
6. `tamara-crm-study.md` for detailed Tamara implementation claims.

Use `skills/application-workflow/SKILL.md` for a complete packet,
`docs/EXAMPLE-PROMPTS.md` for tasks, `docs/MAINTENANCE.md` for bank updates,
and `docs/BUILD.md` for compilation. New versions follow `applications/README.md`.

## Source priority

- The latest explicit user correction wins. Save new facts in the bank before
  using them in a new version.
- JSON is the editable factual master; Markdown and CSV are generated views.
  Edit JSON, then run the renderer.
- Sources distinguish firsthand assertions, static code inspection, intended
  functionality, and planned work. `ready` means usable user-supplied evidence,
  not independent employment verification.
- Root `.tex`/PDF versions, `resume-facts.md`, original sources, and
  `retell-fit-notes.md` are historical. They do not override bank corrections.
  Preserve them unless asked to revise them.
- A JD, research, skill example, code comment, or planned use is not evidence
  of a new candidate accomplishment. Add keywords only for supported work.

## Defaults and preferences

- **Tamara first**, above SCET, unless the user explicitly changes this.
- One page; A4; 10pt body; simple single column; pdfLaTeX; text-based PDF.
  Template margins are 0.58 inches. Cut weaker content before shrinking text,
  using tiny margins, or overlapping elements.
- Supply **complete standalone LaTeX in chat**, from `\documentclass` through
  `\end{document}`. Downloads have been unreliable and section-only snippets
  previously caused invalid LaTeX.
- Letters are copyable text/Markdown by default. Use a concrete subject, a
  sourced role/company connection, one or two relevant bank facts, and one
  clear ask. Introductory emails are usually 90–150 words; use the letter guide
  for other formats. Generic upstream length/subject rules are optional.
- Expected graduation is May 2027. Full-time preference is after graduation,
  open to earlier work. Do not infer exact availability, current residence,
  citizenship, work authorization, or sponsorship needs.
- Preserve titles/dates: Tamara internship June–August 2026 then consulting
  (exact consulting start unspecified); SCET internship/PM dates overlap.
- Ask focused questions when useful; do not repeat answered clarifications.
  Continue with supported facts while optional answers are pending.
- Use the existing checkout; no separate worktree unless explicitly requested.

## Facts easy to misstate

Read selected bullets' scope notes, especially these distinctions:

| Fact | Correct scope |
| --- | --- |
| Tamara 700K+ | Historical applicant base, with further attendee/prospect intake. Not active users or personally sourced leads; no live DB count performed. |
| Tamara 500+ | Qualified early-career candidates added across summer 2026 channels; not hires or all from Sales Navigator. |
| Tamara stakeholders | TA, Talent Brand/Partnerships, COO, Head of TA, and Strategy used the system; active-user count unknown. |
| Tamara sourcing | Sales Navigator shortlist, COO LinkedIn invitations, follow-ups. No direct LinkedIn API or LinkedIn Recruiter usage established. |
| Tamara AI | OpenAI natural-language search translated to deterministic filters, not resume ranking or automated hiring. |
| SCET 100K+ → 500 | Multi-source leads filtered to priority outreach targets using AI APIs and HubSpot's API; not conversions or paid enrollments. |
| SCET money | $50K ad-spend scope; $100K+ shared-project payments across approximately 12 partnerships. Not personal sales or owned budget. |
| Retired SCET figures | Exclude ROAS, CPL, and converted-lead-value figures. User said to skip them; do not resurrect or re-request them. |
| Job-search development | 2025, Claude/GPT-assisted coding with minor Python edits. No claim of independently handwritten end-to-end code or unconfirmed runtime APIs. |
| Job-search results | 2,000+ postings processed in one month; personal search: 221 applications, interviews with 17 distinct companies, seven distinct offers. Month only confirmed for processing. |
| Applications/outreach | Prepared application details and outreach drafts; automatic submission/sending not established. Development year does not change Tamara's 2026 start. |
| Embersafe | Five-person team; personally built fire-department needs/compliance surveys and resident frontend. Sonoma-area council engagement is **still planning**. |
| Embersafe $1M+ | Government-funding problem context, not project funding raised, managed, recovered, or saved. Exact Big Ideas cycle/project dates unverified. |
| Other projects | Demos, awards, intended customers, and algorithms do not establish live customers, clinical validation, measured performance, or production deployments. |
| Aerospace | CAD, simulation, integration; physical hardware involvement limited. No invented manufacturing, firing, flight, or test outcomes. |

OpenClaw/Raspberry Pi and the personal assistant are separate projects from job
search; their concrete capabilities remain `needs_detail`.

## Tailor a resume

1. Read the full JD. Identify main responsibilities, evidence needs, and gaps.
   Research if useful/available; keep URLs and distinguish verified live data
   from user-pasted requirements. Never guess a role from an opaque URL. If
   access fails, say so and use available text or ask for the missing JD.
2. Choose bullet IDs and a summary using role maps and `docs/TAILORING.md`.
   Merge overlapping variants; they are not separate achievements.
3. Create `applications/<company>-<role>/` containing `job-description.md`,
   `tailoring-notes.md`, and `resume.tex`. Use `templates/application-notes.md`
   to record selected IDs, scopes, gaps, and checks. Default status: `draft`.
4. Adapt the current template with concrete verbs and readable bullets.
   Preserve facts and personal/team credit. Do not fill gaps with invented
   tools, tenure, revenue, customer outcomes, or keyword stuffing.
5. Run `python3 scripts/check_bank.py` and
   `bash scripts/build_resume.sh applications/<company>-<role>/resume.tex`.
   Output: `build/resume/resume.pdf`; copy a reviewed PDF to the application
   folder if needed. Build/copy different `resume.tex` versions sequentially
   because each source stem shares an output folder.
6. Review extracted text and visually inspect PDF layout when possible.
   One page alone does not establish correct wrapping, reading order, or
   contact links. Check for overlap, clipping, and escaped characters.
7. Give complete LaTeX and brief selections/gaps. Report checks actually run.
   Do not describe unrun checks as passed.

## Research people and write letters

1. Read the role and confirmed application state. Use
   `python3 scripts/new_application.py --help` to scaffold a new packet when
   useful; it creates drafts, not researched/sent materials. Reuse existing
   packets without overwriting prior work.
2. Use `skills/contact-research/SKILL.md` and `docs/CONTACT-RESEARCH.md`.
   Default to one primary contact and one fallback: a current recruiter,
   named role contact, or likely function leader with evidence of relevance.
   Label hiring authority instead of assuming it from a title.
3. Save exact found LinkedIn URLs and professional email evidence in
   `contacts.json`, with sources/access dates. Published address, provider
   result, inferred pattern, and deliverability check are separate concepts.
   Leave unknown details blank; do not call guesses verified.
4. Use `skills/application-letter-writer/SKILL.md` and `docs/LETTERS.md` to
   select before/after-application, referral, follow-up, LinkedIn, cover letter,
   thank-you, or event-response wording. Unknown status cannot become
   “I applied”; a draft cannot become a sent-message event.
5. Personalize company/recipient details from sourced facts and candidate
   claims from the bank. No invented prior meetings, referrals, news, product
   experience, current competing offers, or recipient addresses.
6. Save needed drafts under `letters/` and timing/evidence in `outreach-plan.md`.
   Keep notes/claim IDs outside the copyable text. Run
   `python3 scripts/check_contacts.py <application-folder>/contacts.json`.
7. Return contact sources/uncertainty and requested letters with the resume.
   If web access is unavailable, continue drafting from known facts with clear
   recipient placeholders; skills do not create live access.

For an open role, do not wait for a cold reply and miss a required application.
Use pre-application outreach for a useful scope/timing question or genuine
referral. Follow-up timing starts from a confirmed sent event, normally around
5–7 business days; employer/user timelines take priority. Replies change the plan.

Drafting and research do not authorize submitting applications, sending messages,
editing profiles, buying tools, or scheduling outreach. Follow the user's request;
do not ask again for already requested research or local drafting.

## Update facts

Follow `docs/MAINTENANCE.md`: edit JSON; append a source; update affected
bullets, metrics, context, questions, and rules. Preserve stable IDs and metric
scope. Record superseded claims as history. Use the user's local date for
`updated_client_date` when available.

```bash
python3 scripts/render_bank.py
python3 scripts/check_bank.py
```

Do not depend on the old scratch builder or attachments directory. The
preserved original upload is `sources/user-supplied-resume.tex`.

## Skills and environment

Choose the local resume, contact-research, letter-writing, or complete-packet
workflow through `skills/README.md`, then read relevant upstream skills.
Generic sales examples, sending infrastructure, autonomous replies, and
campaign benchmarks do not override job-application scope or user facts.

Python 3 supports the bank tools. PDF builds need `pdflatex`, `pdfinfo`, and
`pdftotext`; `pdftoppm` helps visual review. No server, production CRM, database,
real candidate data, model credentials, or API calls are needed for bank/resume
work. Live contact research needs search/browser access; authorized enrichment
tools are optional and are not installed by copying skills. Generated
artifacts belong in ignored `build/`; source `.tex`, selected PDFs, and notes
may be versioned. Never include credentials or raw applicant data.
