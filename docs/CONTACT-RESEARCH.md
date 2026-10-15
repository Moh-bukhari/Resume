# Find the right person and contact route

Use [contact-research](../skills/contact-research/SKILL.md) and the bundled
[Prospecting skill](../skills/marketingskills/prospecting/SKILL.md). The target
is a small, useful hiring shortlist for a particular job, not a sales lead list.

## Start with the job

Read the company domain, exact role, function, location if relevant, and any
named contact. Default to one primary person and one fallback:

1. A recruiter/contact explicitly associated with the posting or team.
2. A likely hiring manager or function leader, with evidence of responsibility
   for that work.
3. At a small company, a founder or generalist leader when their scope fits.

An impressive title alone does not establish hiring authority. Explain why
each person is relevant and label the connection confirmed, likely, or unknown.

## Research sequence

1. Read the official posting, careers/team pages, and named hiring posts.
2. Use available web search/browser tools to discover current professional
   profiles and relevant work. Useful search patterns include:
   - `"Company" "role or function" recruiter`
   - `site:linkedin.com/in "Company" "function"`
   - `site:company-domain "person name"`
   - `"person name" "Company" hiring`
3. Open the original sources when possible. Match employer, role, identity,
   and function; distinguish present employment from old bios or former roles.
   Search snippets are discovery leads, not proof of current details.
4. Save the exact LinkedIn profile URL actually found. If access is limited,
   record the limit and cross-check public company pages or professional work.
   Never manufacture a LinkedIn slug or treat a same-name match as confirmed.
5. Look for a published professional email on company/person professional
   pages or an authorized provider result. Cross-check that the result belongs
   to this person/company. Leave the address blank when unsupported.
6. Keep a short sourced reason for contact and one relevant personalization
   fact. Gather facts first; write the angle afterward.

If browsing/search is unavailable, say what could not be checked. Draft from
the supplied JD and bank with recipient placeholders. A skill file does not
install a browser or grant access to LinkedIn or a contact database.

## Email evidence is separate from deliverability

| Record | Meaning |
| --- | --- |
| `published` | Exact address appears in a professional source; save URL and date. |
| `provider_returned` | A connected provider returned the address for the matching person; record provider result/source and limits. |
| `user_provided` | The user supplied/confirmed the professional address, including an actual thread. Record provenance; no new web lookup is required. |
| `inferred` | An address pattern was guessed; keep it explicitly inferred, not a confirmed destination. |
| `unknown` | No supported address found; use a sourced profile or official hiring channel. |

A separate verification record can hold the provider, actual result, check
date, and limitations. `valid`, `catch_all`, `unknown`, and `not_checked` are
different results. Syntax checks, an MX record, or SMTP acceptance do not prove
that the address belongs to this person or that a message will be delivered.
Do not use a live email as a test probe.

## Tools: useful options, no paid dependency

- Start with public company pages, professional profiles, and the user's
  existing search/browser tools.
- LinkedIn Sales Navigator can help map the function when the user has it.
- Existing Hunter, Apollo, Clay, or similar connections can assist discovery
  and verification. Use current provider documentation and existing authorized
  access. Record lookup errors separately from a genuine no-match response.
- Check costs/credits before an unspecified paid lookup. Do not buy a service
  to complete a draft. Keep credentials in the supported environment.
- Browser automation can read individual accessible pages if the assistant
  has that capability; [OpenAI's Playwright skill](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright)
  is an optional capability reference, not a dependency installed here.

Only relevant professional information is needed. No bulk scraper, private
contact extraction, unrelated personal details, or access-wall workaround is
part of this workflow.

## Save evidence

Start from [contacts.json](../templates/contacts.json) in the application folder.
Use these fields for each entry:

| Field | Content |
| --- | --- |
| `id`, `name`, `employer`, `title` | Stable local ID and observed current identity |
| `linkedin_url` | Exact found profile URL, or null |
| `identity_sources` | Objects with `url`, `accessed_date`, `supporting_detail`; optional local source `id` and evidence `source_type` |
| `relevance_reason` | Why this person fits this specific role |
| `hiring_connection_status` | `confirmed`, `likely`, or `unknown`; identify the supporting evidence |
| `professional_email` | Sourced/provider-returned address, inferred address clearly labeled, or null |
| `email_source_type`, `email_sources` | Origin category and source objects, kept separate from verification |
| `verification` | `provider`, `result`, `checked_at`, `limitations`; null/`not_checked` when not run |
| `preferred_channel` | `email`, `linkedin`, `official_channel`, or `unknown` |
| `unresolved_questions` | Optional uncertainties instead of invented answers |

Store company/recipient facts here; candidate accomplishments remain in the
bank. Drafts can reference local contact-source IDs and bank bullet IDs in
their notes. Do not put uncertainty notes inside the copyable message.

For a user-provided contact, confirmed thread, or actual provider response, a
source object's `url` can be null if `source_type` is `user_provided`,
`confirmed_thread`, or `provider_result`. Describe the evidence in
`supporting_detail`. Do not invent a public URL for a thread or provider
record. Assess relevance without repeatedly requesting details already supplied.

`outreach_events` records actual events separately from drafts: `draft`,
`sent`, `reply`, `interview`, or `application`, with `recipient_id` where
applicable, `occurred_at`, `confirmed_by`, and `evidence_note`. Use actual
dates/timestamps when known; record unknown dates as unknown rather than
inventing them. A sent/application/interview event needs real user/tool
confirmation, not the existence of a file.

```bash
python3 scripts/check_contacts.py applications/company-role/contacts.json
```

Return the shortlist with name, current role, relevance, LinkedIn, professional
email and origin/verification state, source links, and remaining uncertainty.
Recommend one channel and keep the packet ready for drafting.
