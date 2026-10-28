# Application tailoring notes

## Target and version

- Company: Sierra
- Exact role title: Strategist, Agent Development (Arabic speaking)
- Posting URL: https://jobs.ashbyhq.com/Sierra/034c2c56-357f-4ed2-9da7-f4d36a999385
- Location / work arrangement: London, UK · Full-time · On-site
- Job-description source: official Ashby posting, verified LIVE the morning of 2026-10-28; role facts supplied and confirmed by Mohammed in this chat
- Source obtained on: 2026-10-28, America/Los_Angeles
- Full description file: `./job-description.md`
- Description or posting-access limitations: none known; Ashby page is canonical
- Version created/updated: 2026-10-28
- Resume source: `./resume.tex`
- Reviewed PDF: `./resume.pdf` (copied 2026-10-28 after 1-page A4 verification; also at repo root as `Mohammed_Bukhari_Sierra_Strategist.pdf`)
- Document status: **draft**
- Submission status: **no submission recorded** — Mohammed asked for the resume only; do NOT submit or start outreach from this packet
- Submission evidence/date: not supplied

## Company mission and goals

- Company mission / customers / problem solved: Sierra builds AI agents for customer experience for enterprise customers; the Agent Strategist owns the Agent Development Life Cycle (scope, conversation design, tooling, evaluation, launch, continuous iteration in production) and acts as trusted strategic advisor to enterprise executives.
- Sources and observation/provision dates: Ashby posting (live 2026-10-28); tracker resources: sierra.ai/blog/agent-strategist-your-phd-in-applied-ai and sierra.ai/blog/agent-development-life-cycle
- Role/team goals: (1) own customer agents end to end in production; (2) advise executives and run working sessions with customer teams; (3) feed unmet customer needs back into product. All stated in the posting.
- Positioning: hands-on agent builder (Sitters voice agent; Tamara OpenAI conversational search) + customer-facing tooling adopted by stakeholders including the COO (Tamara CRM) + founder/operator proof (AynX) + native Arabic, the headline requirement.

| Company or team goal | Source / date / stated or inferred | Bank bullet IDs and relevant contribution | Scope or gap |
| --- | --- | --- | --- |
| Own the Agent Development Life Cycle in production | Posting, 2026-10-28, stated | SIT-01/02 (built + designed a voice agent), TAM-18/19 (OpenAI conversational search, deterministic filters, shared views) | No enterprise production-agent deployment; hackathon + internal tooling scale |
| Trusted advisor to executives; working sessions with customer teams | Posting, 2026-10-28, stated | TAM-08/25 (mapped COO/Talent Brand/recruiting workflows; system used by TA, Talent Brand/Partnerships, COO, Head of TA, Strategy) | Internal stakeholders, not external enterprise customers |
| Arabic-speaking strategist | Posting title, 2026-10-28, stated | Profile languages: Arabic — native | None |

- Alignment review/date: reviewed 2026-10-28 against the posting and bank; COO-sponsor claim from imported tracker proof NOT used (tracker review note flags it unconfirmed)
- Resume choices shaped by this brief: summary leads with native Arabic + agent building; Sitters elevated with conversation-design bullet; Tamara framed as customer-facing tooling + stakeholder trust; SCET kept for evaluation/prioritization scale (100K+ → 500)

## Requirements and selected evidence

| Job requirement | Selected bullet ID(s) | Relevant evidence / wording | Scope or gap |
| --- | --- | --- | --- |
| Arabic speaking (headline) | profile languages | "Arabic (native)" in Skills + "Native Arabic-speaking" in Summary | None |
| Production AI/LLM agent experience (even better) | SIT-01, SIT-02, SIT-04 | Built Next.js voice agent with Claude + ElevenLabs; designed personas separating sourced answers from labeled speculation; 1st place Anthropic hackathon Sep 2026 | Hackathon build, not enterprise production |
| Customer-facing tooling, stakeholder trust | TAM-08, TAM-18, TAM-19, TAM-25 | Mapped executive/recruiting workflows; OpenAI NL search → deterministic filters; system used by TA, Talent Brand/Partnerships, COO, Head of TA, Strategy | Internal users at one company |
| Evaluation / prioritization | SCP-06, SCP-02 | Filtered 100K+ leads to 500 priority targets via AI APIs + HubSpot API; $50K attribution → budget decisions | Marketing leads, not agent evals |
| Founder / operator background (even better) | AYN-01, AYN-03, AYN-04 | Founded AynX; ML-backed decision engine; DebriSolver finalist | Pre-revenue, competition stage |
| Technical degree (even better) | profile education | B.S. Aerospace Engineering, UC Berkeley, expected May 2027, GPA 3.5 | In progress |
| Partnerships / complex projects | TAM-02 | Evaluated 40+, engaged 20, secured 7 partnerships | Organizations, not customers/hires |

- Selected summary: rewritten draft from SUM-01/SUM-04 angles (agent building + Arabic lead)
- Selected experience and project order: Tamara → SCET → AynX; Sitters first under Projects & Awards
- Selected skills: TypeScript, Next.js, Python, SQL, OpenAI, Claude, ElevenLabs, Greenhouse APIs, HubSpot API; Languages line with Arabic native
- Source IDs for new or changed factual claims: none — all claims from existing bank bullets/profile
- Facts updated from a new explicit user correction: none
- Details intentionally omitted for relevance or space: SCET Operations Intern entry; Tamara CRM implementation depth (sync/webhooks detail compressed to one line); SkipLab second bullet; Embersafe
- Material fit gaps: no enterprise customer delivery; no production agent at enterprise scale; London role — posting silent on visa sponsorship (flagged in tracker; ask early if applying)
- Questions that materially affect this draft: none
- Combined workflow and selected original methods: application-workflow; professional-writing-review (humanizer pass done 2026-10-28)
- Shared resume/outreach positioning: agent builder who ships customer-facing AI tooling stakeholders actually adopt; native Arabic

## Changes and review

- Baseline compared: templates/resume-base.tex layout (same as R001/R002 packets)
- Changes to positioning: Sierra-specific summary; Arabic in first line
- Changes to selected evidence: Sitters promoted; Tamara bullets recombined (TAM-08+25, TAM-09/11/12/20 compressed, TAM-18+19, TAM-02+05)
- Changes to LaTeX/layout: none to template geometry
- Factual review: done 2026-10-28 — every claim traced to bank bullet IDs above; 700K+ stated as historical applicant base; CRM described as NL search → deterministic filters, never ranking
- Scope/ownership/date review: done 2026-10-28 — titles/dates match bank (Tamara Jun 2026–Present intern→consultant; SCET Sep 2025–Present; AynX Oct 2025–Present)
- Text diff reviewed: pending (single new file)
- LaTeX diff reviewed: pending

## Final writing review

- Artifact/version reviewed: resume.tex, 2026-10-28 draft
- Methods: Blader Humanizer + Corey Haines Copy Editing + final evidence comparison
- Natural phrasing and professional voice: reviewed 2026-10-28 — plain, direct wording; no inflated claims
- Strong verbs, specific terms, and company fit retained: yes — "conversation design," "deterministic filters," "Agent Development Life Cycle" adjacency via Sitters/Tamara bullets
- Numbers, scope, attribution, dates, and project maturity preserved: yes — verified against bank scope notes
- Writing review status/date: reviewed 2026-10-28
- Remaining issues: none

## Build and validation record

- [x] Bank consistency check passed. Command/date/result: `python3 scripts/check_bank.py`, 2026-10-28 — "Bank valid: 13 entries, 72 bullets, 21 numeric facts; Markdown and CSV are synchronized."
- [x] pdfLaTeX build succeeded. Command/date/result: `bash scripts/build_resume.sh applications/r005-sierra-strategist-agent-development-arabic-speaking/resume.tex`, 2026-10-28 — 1 page, 121,125 bytes (local TeX installed on this host for the build).
- [x] Page count is **1** and paper is **A4**. Evidence: pdfinfo — Pages: 1; Page size: 595.276 x 841.89 pts (A4).
- [x] Body text remains readable **10pt**; template defaults unchanged.
- [x] Extracted PDF text verified 2026-10-28: correct order, contact details, dates, titles, metrics (700K+ historical base, 100K+ → 500, $50K, $7,000) and "Arabic (native)" present in Summary and Languages.
- [x] Full-page visual review 2026-10-28 (rendered PNG): no clipping, overlap, or crowding; comfortable bottom margin.
- [x] Compiler warnings: zero Overfull box warnings in build log.
- [x] Final `.tex` and PDF contain the same selected wording and facts (built directly from this `.tex`).
- [x] Reviewed PDF copied to `./resume.pdf` and to repo root as `Mohammed_Bukhari_Sierra_Strategist.pdf`, 2026-10-28.
- [x] Application notes and full description are saved beside the resume.

## Submission record

No submission. Resume-only task per Mohammed's instruction 2026-10-28. Tracker R005 stays **Saved** with `resume_done: true`.

## Contacts and letters

- Not started — outreach explicitly out of scope for this task.
- Contacts file: `contacts.json` (scaffold only)
- Outreach plan: `outreach-plan.md` (scaffold only)

## Initializer context

- Application stage inferred from confirmed tracker context: `before_application`
- Workspace creation date supplied by the user: 2026-10-28
- Files scaffolded by `scripts/new_application.py --tracker-id R005 --date 2026-10-28`.
