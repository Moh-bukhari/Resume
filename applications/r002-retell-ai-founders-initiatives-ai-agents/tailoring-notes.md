# Application tailoring notes

## Target and version

- Company: Retell AI
- Exact role title: Founders Initiatives, AI Agents
- Posting URL: https://jobs.ashbyhq.com/retell-ai/21cf0117-6b44-40df-96ea-0fb2d1d0892f
- Location / work arrangement: Redwood City, CA (relocation provided)
- Job-description source: official Ashby posting (full text read), cross-checked against tracker record R002
- Source obtained on: 2026-10-23 (posting verified live; published 2026-06-11)
- Full description file: `./job-description.md`
- Description or posting-access limitations: none known
- Version created/updated: 2026-10-23 (America/Los_Angeles)
- Resume source: `./resume.tex`
- Reviewed PDF: `./resume.pdf` (built and verified locally; binary not pushed —
  the GitHub write channel used accepts UTF-8 text only; the PDF lives with the
  local packet and in the workspace copy)
- Document status: **final (ready for submission)**
- Submission status: **no submission recorded**
- Submission evidence/date: none — the parent agent submits separately; this
  packet only prepares the application.

## Company mission and goals

- Company mission / customers / problem solved: Retell AI provides a voice-AI
  platform for building AI phone agents for enterprise customer experience
  (customers named in the posting include CVS/Aetna, American Airlines,
  Lenovo, and Grab). Founders Initiatives is the founders' own
  cross-functional team for the company's highest-priority opportunities,
  shipping core company infrastructure across product, engineering, GTM,
  operations, and AI systems.
- Sources and observation/provision dates: Ashby posting for this role, read
  2026-10-23; tracker R002 record (imported 2026-10-15, re-verified since).
- Role/team goals (stated in the posting): (1) internal and external AI
  systems that power how Retell hires, sells, operates, and scales —
  production-grade AI workflows, automations, and agent systems; (2)
  API-based integrations connecting systems across the company (CRMs, LLM
  providers); (3) GTM engineering and growth automation.
- Positioning: Mohammed could contribute through this role via the Tamara
  pre-ATS recruiting CRM — a Greenhouse-integrated recruiting system with
  resume parsing, API synchronization, and OpenAI search, adopted across TA,
  Talent Brand/Partnerships, and leadership — plus HubSpot/API automation at
  SCET and shipped LLM products (Sitters). The posting's 2+ years of
  professional software engineering and CS/CE degree asks are not met
  literally and are not claimed (see gaps).

| Company or team goal | Source / date / stated or inferred | Bank bullet IDs and relevant contribution | Scope or gap |
| --- | --- | --- | --- |
| HR & Recruiting AI: structured signals from resumes; AI recruiter screening/qualification workflows | Posting, stated, 2026-10-23 | TAM-09, TAM-17, TAM-20 (structured intake + local PDF/DOCX resume parsing into searchable candidate records; FTS5 full-text search); TAM-18, TAM-19 (OpenAI conversational search → validated deterministic filters, live counts, shared views) | No AI-based candidate ranking or interview-success scoring is claimed — the CRM's search is natural-language to deterministic filters, not ranking (bank rule) |
| API integrations across the company (CRMs, LLM systems) | Posting, stated | TAM-11, TAM-12, TAM-13 (Greenhouse Harvest API: OAuth, cursor pagination, retries; incremental sync with checkpoints/leases/resumable processing; signed webhooks); SCP-04, SCP-06 (HubSpot API automation; AI APIs + HubSpot API filtering) | Integrations evidenced are Greenhouse and HubSpot; Salesforce/GoHighLevel and Zapier/n8n/Make are bank-listed as unconfirmed tools and are not claimed |
| GTM engineering & growth automation; outbound pipelines | Posting, stated | SCP-06 (AI APIs + HubSpot API: 100K+ leads → 500 priority outreach targets); SCP-03, SCP-04 (LLM-powered personalized outbound email sequences; HubSpot lead/email workflow automation) | Lead targets are outreach priorities, not conversions or pipeline outcomes |
| Production-grade AI workflows / automations that reduce manual operations | Posting, stated | TAM-10 (CRM web app and data workflows, Next.js/TypeScript/Prisma, SQLite/Turso); TAM-21 (guarded bulk actions: previews, confirmation gates, outcome logs, reversals); SIT-01, SIT-02 (personally built Claude + ElevenLabs voice app with sourced-vs-speculation persona guardrails) | Systems are real and in organizational use at a fintech's talent org, but built by a student-stage founder/PM, not a professional SWE team; no production benchmarks claimed |

- Alignment review/date: reviewed 2026-10-23 against the posting text and the bank.
- Resume choices shaped by this brief: SUM-04 summary; Tamara CRM engineering
  bullets lead (recruiting AI + integrations are the role's core brief); SCET
  automation retained (SCP-06, SCP-03/SCP-04); AynX compressed to two bullets
  for founder ownership; Sitters and SkipLab retained; Operations Intern line
  and PAI personal job-search project omitted for one-page fit (see below).

## Requirements and selected evidence

Source: `bank/experience-bank.json`. Role family used: "Applied AI / internal
tools / GTM engineering" role map.

| Job requirement | Selected bullet ID(s) | Relevant evidence / wording | Scope or gap |
| --- | --- | --- | --- |
| HR & Recruiting AI systems (resume signals, screening workflows) | TAM-09, TAM-17, TAM-18, TAM-19, TAM-20, TAM-25 | Greenhouse-integrated CRM around 700K+ historical applicant records; structured intake + local resume parsing; OpenAI conversational search to deterministic filters; used by TA, Talent Brand/Partnerships, COO/Head of TA/Strategy | Search is not resume ranking; no interview-success lead scoring claimed |
| API-based integrations; CRM integrations (HubSpot named) | TAM-11, TAM-12, TAM-13, SCP-04, SCP-06 | Greenhouse Harvest API (OAuth, pagination, retries, checkpoints, webhooks); HubSpot API workflows and automation | Salesforce, GoHighLevel, Zapier, n8n, Make: unconfirmed in the bank — not claimed |
| LLM-powered systems (OpenAI, Claude named) | TAM-18, TAM-19, SIT-01, SCP-03 | OpenAI search assistant; Claude + ElevenLabs voice app; LLM-powered outbound email sequences | Gemini not used in bank evidence — not claimed |
| Strong software engineering skills (full-stack) | TAM-10, TAM-12, TAM-20, AYN-02, AYN-03 | Next.js/TypeScript/Prisma app and data workflows; resumable synchronization design; FTS5 indexing; cryptographic identity system + ML decision engine at AynX | Project-based engineering by a founder/PM; depth is real but not professional-SWE tenure (see gaps) |
| GTM engineering & growth automation | SCP-06, SCP-03, SCP-04 | AI/HubSpot API lead filtering (100K+ → 500 targets); LLM outbound sequences; HubSpot automation | No lifecycle/retention automation or ad-generation systems claimed |
| Founder mindset; high ownership; cross-functional work | AYN-01, TAM-25, SCP-05 | Founded AynX; built a system adopted across teams and leadership; ~12 partnerships / $100K+ shared-project payments at SCET | AynX has no confirmed customers; partnership figures are shared-project scope |
| Security & compliance automation | TAM-21 (partial only) | Guarded bulk actions with previews, confirmation gates, outcome logs, reversals — adjacent operational-safety evidence | No BAA/DPA, security-questionnaire, or audit-tooling experience — honest gap, not papered over |
| Bachelor's in CS/CE or closely related field | Education section | B.S. Aerospace Engineering, UC Berkeley, expected May 2027, GPA 3.5/4.0 | Aerospace, not CS/CE — not reworded or hidden |
| 2+ years professional software engineering | — | No bullet selected; the resume shows what he has built instead (Tamara CRM stack, AynX systems, Sitters) | **Not met and not claimed.** Engineering experience is founder/PM project work (2025–present), not 2+ years of professional SWE employment |
| 1+ year startup experience | AYN-01, TAM-09 | Founder of AynX since Oct 2025; consultant-built production system at Tamara (a startup-scale fintech) | Startup experience is founder/consulting-based |

- Selected summary: SUM-04 (ai_internal_tools), used verbatim.
- Selected experience and project order: Tamara → SCET (PM) → AynX; Projects: Sitters → SkipLab.
- Selected skills: bank-evidenced only — user-stated tools (TypeScript, Next.js, Python, SQL, OpenAI, Claude, ElevenLabs) plus owned-project implementation evidence (React, Prisma, SQLite/Turso, Greenhouse Harvest APIs/OAuth, webhooks, FTS5). Salesforce, Zapier, n8n, and Make are bank-listed as unconfirmed and excluded.
- Source IDs for new or changed factual claims: none — all wording drawn from existing bank bullets.
- Facts updated from a new explicit user correction: none in this pass. (AynX body uses the bank's AYN-01 "Founded" wording; the scaffold base's "Co-founded" line was not carried over.)
- Details intentionally omitted for relevance or space: SCET Operations Intern entry (SCO-01/SCO-03 — process evidence, cut at the one-page fitting pass); PAI personal job-search automation project (PAI-01/PAI-08/PAI-09 — personal workflow, tangential on a resume for this role despite its fit-scoring theme); Tamara partnerships bullet (TAM-02) and the SAR 100,000 competition line (prize pool; tangential); SCP-02 attribution bullet; Embersafe.
- Material fit gaps: **the posting asks for 2+ years of professional software engineering experience and a CS/CE (or closely related) degree; Mohammed is an Aerospace Engineering senior whose engineering is founder/PM project work. Neither gap is claimed or disguised in the resume** — the application leads with shipped systems in the role's exact domains instead. Also: no security/compliance automation (BAA/DPA/questionnaire) experience; no Salesforce/GoHighLevel or Zapier/n8n/Make experience (unconfirmed tools); full-time availability follows May 2027 graduation (bank availability note).
- Questions that materially affect this draft: none.
- Combined workflow and selected original methods: application-workflow; professional-writing-review (below); company-alignment brief (above).
- Shared resume/outreach positioning: "I already built the recruiting-AI system this role describes" — Tamara CRM (parsing, Greenhouse sync, OpenAI search) + SCET HubSpot/AI automation + shipped LLM product (Sitters).

## Changes and review

- Baseline compared: scaffold base copied by `scripts/new_application.py` for R002, and the submitted R001 resume (`applications/r001-retell-ai-deployment-strategist/resume.tex`).
- Changes to positioning: summary replaced with bank SUM-04 (AI/internal tools); engineering implementation leads instead of deployment/strategy framing.
- Changes to selected evidence: added the CRM engineering bullets the R001 version did not use — TAM-10 (stack), TAM-11/TAM-12/TAM-13 (Harvest API, sync, webhooks), TAM-17 + TAM-20 (resume parsing, FTS5) — and SCP-03 (LLM outbound sequences); combined AynX into two bullets; dropped TAM-02/TAM-08/TAM-14/TAM-15, SCP-02, the Operations Intern line, and PAI for fit/relevance; corrected AynX "Co-founded" → bank AYN-01 "Founded."
- Changes to LaTeX/layout: same template/preamble as the base (A4, 10pt, 0.58in margins); bullet-ID comments added per line.
- Factual review: every bullet traced to bank IDs above; scope notes checked (700K+ historical applicant records; 500 priority targets are not conversions; $100K+ shared-project payments; no ROAS/CPL/conversion figures; no ranking claim for the CRM search; no unconfirmed tools listed as skills).
- Scope/ownership/date review: titles/dates match bank experiences (Tamara Jun 2026–Present intern→consultant; SCET PM Sep 2025–Present; AynX Founder Oct 2025–Present; Sitters Sep 2026; SkipLab Jan 2025–Present, $7,000 team prize Jun 2025).

## Final writing review

- Artifact/version reviewed: `applications/r002-retell-ai-founders-initiatives-ai-agents/resume.tex`, 2026-10-23 version.
- Methods: Blader Humanizer + Corey Haines Copy Editing + final evidence comparison.
- Natural phrasing and professional voice: reviewed — bank bullet wording kept close to source; stacked bolding limited to system names and headline figures; no not-X-but-Y contrasts, no inflated verbs.
- Strong verbs, specific terms, and company fit retained: built/implemented/designed; role vocabulary (structured signals, integrations, synchronization, outbound) mirrors the posting where the bank evidence supports it, without keyword stuffing.
- Numbers, scope, attribution, dates, and project maturity preserved: yes — see factual review above.
- Writing review status/date: reviewed 2026-10-23.
- Remaining issues: none known.

## Build and validation record

- [x] Bank consistency check passed. Command/date/result: `python3 scripts/check_bank.py`, 2026-10-23 — "Bank valid: 13 entries, 72 bullets, 21 numeric facts; Markdown and CSV are synchronized." (Run in a local working copy of the repo; `sources/` and `tamara-crm-study.md` fetched so the bank's local source links resolve.)
- [x] pdfLaTeX build succeeded. Command: `bash scripts/build_resume.sh applications/r002-retell-ai-founders-initiatives-ai-agents/resume.tex`, 2026-10-23 — "Verified one page with extractable text."
- [x] Page count is **1** and paper is **A4** (verified with pdfinfo: 595.276 x 841.89 pts).
- [x] Body text remains readable **10pt** (template default unchanged).
- [x] Extracted PDF text checked (pdftotext): order, contact details, dates, titles, metrics verified.
- [x] Visual review via pdftoppm render: no clipping/overlap found; no Overfull boxes in the build log.
- [x] Reviewed PDF copied to `./resume.pdf` (local packet; see version note above) and to the workspace deliverables folder as `Mohammed_Bukhari_Retell_Founders_Initiatives.pdf`.

## Submission record

No submission recorded. Preparing this packet does not submit the
application; the parent agent handles submission separately.

## Contacts and letters

- Contact research for this role has not been run separately; the R001
  packet's researched contacts (`applications/r001-retell-ai-deployment-strategist/contacts.json`,
  research completed 2026-10-23) are the starting set for this company and
  role family. This packet's `contacts.json` remains the scaffold (empty,
  research not started) until that research is adapted or rerun.
- The scaffold's letter templates under `letters/` remain unused drafts in
  this packet.
- Actual sent/reply/application/interview events: none.
