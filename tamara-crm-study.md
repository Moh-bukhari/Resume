# Tamara CRM: evidence for resume framing

Later user clarification: 700K+ describes the historical applicant base, with
additional intake for event attendees and prospective applicants. The user
confirmed use by TA, Talent Brand/Partnerships, COO/Head of TA, and Strategy.
These are firsthand updates recorded in the master bank; the source inspection
below remains a static technical review.

Read-only inspection of `Moh-bukhari/CRM`, main commit
`a3822317d0920a797bc9a4691c12472665117f66`, folder `pre-ats-crm-main`.
No application, operational scripts, live APIs, candidate database, or
credentials were run or inspected. The CRM source was left unchanged.

The strongest story is translating executive and team workflows into an
implemented shared platform. This connects stakeholder discovery, product
design, full-stack implementation, integrations, and recruiting operations.
It supports both supplied Retell roles more directly than generic talent-brand
campaign language.

## Source-corroborated implementation

| Capability | Source evidence |
| --- | --- |
| Next.js/TypeScript recruiting CRM, Prisma and SQLite/Turso | `package.json`; `prisma/schema.prisma:7`; `src/lib/db.ts:57` |
| Applicant, prospect, event, and outreach data with shared context | `prisma/schema.prisma:37`; `src/lib/search-index-sql.ts:29` |
| Separate Talent Acquisition/Talent Brand owners and history | `prisma/schema.prisma:560`; `src/lib/warm/owners.ts:6` |
| Engagement timelines, next actions, stale/overdue follow-up tracking | `src/lib/warm/touchpoints.ts:42`; `src/app/tracking/page.tsx:19`; `src/app/api/candidates/[id]/warm/route.ts:10` |
| CSV/Excel import reconciliation and deduplication | `src/lib/warm/import-match.ts:67`; `src/lib/import-runner.ts:398`; `src/lib/dedupe.ts` |
| Greenhouse Harvest OAuth client, pagination and retries | `src/lib/greenhouse/harvest.ts` |
| Incremental sync with persisted checkpoints and worker leases | `src/lib/greenhouse/sync-run.ts:15`; `src/lib/greenhouse/sync.ts` |
| Signed webhook ingestion and processing/retry state | `src/lib/greenhouse/webhook.ts`; `src/app/api/greenhouse/webhook/route.ts` |
| Structured application/CV intake and conditional Job Board submission | `src/app/api/apply/[track]/route.ts:12`; `src/lib/early-careers/intake.ts:72`; `src/lib/greenhouse/job-board.ts` |
| Local deterministic resume parsing | `src/lib/resume/parse-resume.ts:2` |
| OpenAI structured translation to deterministic search filters | `src/lib/ai/nl-filters.ts:195`; `src/app/api/search/nl/route.ts:16` |
| Conversational search tools, live SQL counts and shared views | `src/app/api/danny/route.ts:100`; `:257`; `:385`; `:466` |
| FTS5 and trigger-maintained index across profile/application/event history | `src/lib/search-index-sql.ts:29`; `:80` |
| Preview, confirmation, outcome logging and specific reversal workflows | `src/lib/actions/preview.ts:7`; `src/lib/actions/runner.ts:51`; `:126`; `:341` |
| Consent-source metadata, do-not-contact controls, sensitive-field checks | `src/lib/warm/types.ts:23`; `src/app/api/candidates/[id]/warm/route.ts:57`; `src/lib/pdpl.ts` |

## User-provided facts

The user reports personally building the project and mapping COO and team
stakeholder workflows. The clarified scale is a 700K+ historical applicant
base, plus additional attendee/prospect intake. These are firsthand user
assertions; code cannot establish authorship, conversations, or current count.

Future resumes should use **700K+ historical applicants/applicant records**,
with further intake described separately. Source comments discuss roughly
520K candidates and 700K application rows in older cohorts; those separate
units cannot corroborate a current live count. The user's clarification has
resolved the intended historical-versus-future scope.

## Limits on framing

- Describe AI-assisted search and deterministic filtering, not AI resume
  ranking, fit prediction, or automated hiring decisions.
- Do not claim measured latency, uptime, sync throughput, hours saved, or
  hiring conversion; these were not measured.
- Do not describe local deterministic resume parsing as LLM parsing.
- Privacy controls are implemented, but no legal compliance or security
  certification is established. Selected-user identity is attribution, not
  enterprise per-user authentication.
- Avoid saying no candidate data ever reaches the LLM: the conversational
  route receives aggregate vocabulary and answer labels/counts from the data.
- Conditional Greenhouse application writes and guarded bulk actions should
  be described as implemented features, not proof that every write path is
  enabled in the deployed environment.

The table above preserves the relevant implementation evidence in this
repository. Its paths/line numbers refer to the
[pinned upstream snapshot](https://github.com/Moh-bukhari/CRM/tree/a3822317d0920a797bc9a4691c12472665117f66/pre-ats-crm-main).
No temporary checkout is required to use the resume bank. Current firsthand
clarifications and selectable technical bullets are in
[the master bank](bank/experience-bank.md).
