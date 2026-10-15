---
name: application-workflow
description: Build Mohammed Bukhari's per-job resume and outreach packet using established research and writing skills, the factual experience bank, sourced contacts, and confirmed application history.
---

# Mohammed's application workflow

Use for a tailored resume, finding the right person, or writing before or after
an application. Read [AGENTS.md](../../AGENTS.md) first. Complete the requested
parts; a request for one letter does not require producing every template.

## Methods combined

Read the relevant published original before using its method. Versions,
adoption evidence, and comparisons are in [the selection research](../../docs/SKILL-SELECTION.md).

| Step | Published method | Adaptation for Mohammed |
| --- | --- | --- |
| Understand the company/person | [Anthropic Account Research](../anthropic-sales/account-research/SKILL.md) | Source relevant facts; distinguish observed needs, inference, and missing research. |
| Find the right person | [Exa Search](../exa/search/SKILL.md) and [people patterns](../exa/search/references/patterns-people.md) | Company + function + role queries, current-role corroboration, canonical LinkedIn URLs, and deduplication. |
| Enrich an email when needed | [Daniela Ryplová's Verified Email Finder](../apify/apify-verified-email-finder/SKILL.md) | Reject wrong-company matches; preserve provider status and provenance. Optional provider access. |
| Choose intent and draft | [Anthropic Draft Outreach](../anthropic-sales/draft-outreach/SKILL.md) | Inspect actual prior context; relevance line, evidence bridge, one small ask. |
| Make it sound natural | [Corey Haines Cold Email](../marketingskills/cold-email/SKILL.md) | Useful personalization, brief proof, conversational voice, and follow-ups that add information. |
| Edit | [Corey Haines Copy Editing](../marketingskills/copy-editing/SKILL.md) | Clarity, voice, relevance, proof, and specificity passes. |
| Tailor and build the resume | [Resume workflow](../resume-workflow/SKILL.md) and selected [ResumeSkills](../resumeskills/README.md) | Bank-backed claims, Tamara first, complete one-page Overleaf LaTeX. |

[Firecrawl Lead Research](../firecrawl/firecrawl-lead-research/SKILL.md) is an
optional context source. Ordinary search and supplied files work when specialist
providers are unavailable. Skills supply instructions, not accounts or live data.

Use these methods under this repository's instructions. Sales examples do not
require a sales pitch, product-marketing intake, secondary sending domains,
automated sequences, or a 20-minute call. Upstream host-specific silent-work,
Page/Slide, connector-write, and upload-relative date instructions do not govern
this workflow. Keep progress updates, save local files, and use actual research
dates. Archived JDs/uploads keep their source dates; they are not current news.

## 1. Ground the role and state

Read the full JD, [bank](../../bank/experience-bank.md), and existing
`applications/<company>-<role>/` packet. Consult `contacts.json`, confirmed
events, and supplied conversation threads before asking anything again.
For a tracked job, first read its `Rxxx` record in
`tracker/tracker.json` and [the tracking guide](../../docs/TRACKER.md).
Tracker lifecycle/dates drive the application context; imported fit/proof
notes do not override the factual bank.

For a new target, use `python3 scripts/new_application.py --help` to scaffold
the packet. Supply only known stage/date metadata. The initializer creates
untailored, unsent drafts; file creation proves no application or contact.
Use `--tracker-id R001 --date YYYY-MM-DD` for an existing tracked job to keep
its ID and link the packet. Update preparation/material links after real work,
and confirmed events after they happen, using `scripts/tracker.py`. Regenerate,
validate, and publish the tracker with authorized repository changes.

Write a short fit brief in `tailoring-notes.md`:

- The two or three most important responsibilities from the actual JD.
- Matching bank bullet IDs, personal/team ownership, and metric scope.
- Direct experience, transferable experience, and material gaps.
- Availability: expected Berkeley graduation May 2027; preference for full-time
  afterward, open to earlier work. No invented exact start date or work status.

Use this brief for both resume and letter. Do not infer an opening from an
opaque URL. If access fails, use supplied requirements with their limitations
and continue supported work.

## 2. Choose proof for this role

These are starting points, not fixed bundles. Read the IDs' current scope notes
and select the strongest non-overlapping evidence for the actual JD.

| Role family | Useful evidence | Boundaries |
| --- | --- | --- |
| Growth, sourcing, recruiting operations; e.g. Mercor Growth Associate | `TAM-05`, `TAM-06`, `TAM-26`: 500+ qualified early-career candidates, Sales Navigator/event funnel, COO invitation shortlist. `TAM-15`, `TAM-25`: relationship history. `SCP-06`: 100K+ leads to 500 priority targets. | The 500+ span summer channels; not all Sales Navigator, not hires. No established LinkedIn Recruiter use or medical-expert recruiting. |
| Deployment, product, implementation; e.g. Retell Deployment Strategist | `TAM-08`, `TAM-09`, `TAM-25`: stakeholder discovery and shared CRM implementation. `SCP-04`, `SCP-06`: workflows/APIs. `SIT-01`, `SIT-02`, `SIT-04`: voice AI and award. | Internal adoption and demos do not establish enterprise customer production launches or measured customer ROI. |
| AI agents, internal tools, founder initiatives | `TAM-11`, `TAM-12`, `TAM-13`, `TAM-18`: Greenhouse integration, resumable sync, webhooks, structured AI search. `SCP-06`, `PAI-08`, `PAI-10`: practical automation. | Preserve titles; do not invent professional SWE tenure. Job-search work used AI-assisted coding and minor Python edits. |
| Aerospace and engineering | `SEB-01`–`SEB-03`, `STR-01`–`STR-03`, relevant `AYN` bullets: CAD, CFD/MATLAB, integration, privacy-preserving satellite coordination. | Keep Tamara first but brief. Hardware work was limited; no invented manufacturing, flight, or physical-test results. |

For growth roles, lead with finding, prioritizing, and maintaining relevant
people, then explain the supporting system. For implementation roles, lead
with translating stakeholder needs into working processes, then select the
technical details. Avoid listing every project or CRM feature.

## 3. Research one primary contact and one fallback

Use Account Research to extract a few relevant needs/signals, then Exa's
people-search method through available tools. Start with the named contact,
function recruiter, or current function leader. Use a founder only when the
role/company evidence supports that choice.

1. Find current company/function evidence and the exact LinkedIn URL.
   Corroborate stale profiles with a company page, current posting, or dated
   announcement where possible. Deduplicate sources for the same person.
2. Record relevance. A senior title alone does not establish ownership of this
   vacancy; label the hiring connection as inferred when appropriate.
3. Review supplied threads and events. Read full available exchanges before
   describing the last interaction. A preview is insufficient; an unqueried
   inbox or missing file means history unknown, not no history.
4. Find a published professional email first. Use a connected authorized
   provider if useful. Keep email origin, deliverability status, identity
   match, and current employment separate.
5. Reject wrong-company/domain results unless a documented parent/brand
   relationship explains them. `catch_all`, `unknown`, `error`, and guessed
   patterns do not become verified addresses. Provider `ok` does not prove
   hiring authority or guarantee delivery.
6. Save sources, access dates, uncertainties, and IDs in `contacts.json`.
   If no supported email is found, use the sourced LinkedIn/application route.

Keep research proportional to a real professional connection. Do not invent
news or recipient interests. See [contact guidance](../../docs/CONTACT-RESEARCH.md)
for schema and fallbacks.

## 4. Choose the stage and one useful ask

| Confirmed situation | Appropriate message |
| --- | --- |
| Open role; no application | Apply normally when ready. Use pre-application outreach for a real scope/timing question or genuine referral; do not wait for a cold reply to apply. |
| Application confirmed | Name the role, connect a need to evidence, and ask a small relevant question. Mention the application date only if known. |
| Actual conversation, referral, or event | Reference only the confirmed exchange/connection. A draft is not a prior touch. |
| Interview completed | Thank them for the actual discussion and connect one real topic to evidence. |
| Confirmed sent message awaiting reply | Add useful information in a restrained follow-up, normally after 5–7 business days unless their timeline differs. Count from the sent event. |
| Status/history unknown | Use neutral wording or clearly conditional alternatives. Do not say “I applied,” “following up,” or imply a warm relationship. |

Use [the letter guide](../../docs/LETTERS.md) for LinkedIn, cover letters,
referrals, and offer/scheduling replies. Email and LinkedIn variants are
alternatives, not instructions to contact every person. Replies change the plan.

## 5. Write and edit

Default introductory body: about 100–120 words, flexible up to 150 as needed.
Use an informative subject naming the role or real context; no forced
lowercase or fake reply subject. Follow this structure:

1. **Relevance:** one sourced role/company need or actual conversation topic.
2. **Evidence bridge:** one or two matching bank facts and why they apply.
   Preserve scope: Tamara's 700K+ is historical applicant volume, while
   personal job-search offers are Mohammed's own outcomes.
3. **Ask:** one low-friction question fitting the stage, such as whether the
   role can fit May 2027 graduation or who owns a relevant function. Avoid
   assuming immediate availability, a referral, an interview, or a call.
4. **Signature:** Mohammed and a relevant portfolio link when useful. Mention
   an attachment or live demo only when actually included/available.

Match supplied writing examples; otherwise use plain, confident, conversational
English. Personalization should explain fit, not add generic praise or an
unrelated recipient fact.

Apply Corey's editing passes: clear meaning, natural voice, relevance to this
reader, proof for every claim, and concrete language. Cut repetition and
unsupported claims rather than inventing metrics. Keep bank IDs, sources,
and research caveats outside copyable text. See [the worked example](../../docs/OUTREACH-EXAMPLE.md).

## 6. Save, check, and return

Keep the actual JD, fit brief, selected IDs/gaps, contact research, chosen
stage/intent, drafts, and timing in the packet. Use `templates/outreach-plan.md`
for the hook, proof, ask, and history status. Finalize only requested variants.

From the repository root:

```bash
python3 scripts/check_bank.py
python3 scripts/check_contacts.py applications/<company>-<role>/contacts.json
bash scripts/build_resume.sh applications/<company>-<role>/resume.tex
```

Build the PDF when producing/changing a resume. Follow [the resume workflow](../resume-workflow/SKILL.md)
for one-page, text extraction, and visual review. Check the letter against the
same facts and stage. Report checks performed; providers remain untested
unless run.

Return complete standalone LaTeX for a requested resume, requested copyable
letters, sourced contact routes with uncertainty, and the recommended next
step. Drafts remain local and unsent. Research/drafting does not imply
application submission, external email drafts, sending, or automated sequences.
