# Example prompts

Replace angle-bracket placeholders before using these. Read
[AGENTS.md](../AGENTS.md) and [the tailoring guide](TAILORING.md) first. These
prompts authorize local drafting and review; sending applications or outreach
requires a separate explicit instruction.

## Complete application packet

> Read AGENTS.md and use application-workflow for `<company> — <role>`.
> Here is the full JD: `<text and URL>`. My application status is `<not applied /
> applied, date if known / interviewed / unknown>`. Tailor a one-page Overleaf
> resume, find one relevant contact and one fallback, source their LinkedIn and
> professional email where available, and recommend before/after-application
> timing. Draft the useful cover letter, email, and LinkedIn variant for this
> stage. Save sources, bank claim IDs, uncertainty, and timing notes. Give me
> full LaTeX and copyable messages. Keep everything as drafts.

`application-workflow` combines Anthropic's research/context methods, Exa's
people discovery, Corey's outreach/editing, and optional email verification
with this bank. It selects role-specific proof and timing rather than reusing
the same letter for every company. See the [comparison research](SKILL-SELECTION.md).

## Find the right person

> For `<company, role, JD>`, find the relevant recruiter or function leader
> and one fallback. Use contact-research. Explain their hiring connection and
> show source URLs/dates for current role, LinkedIn, and professional email.
> Separate published/provider addresses, guesses, and delivery checks. If no
> supported email is found, give the best sourced route. Save contacts.json.

## Write before applying

> I have not applied to `<role/company>`. Decide whether a pre-application note
> would answer a useful question or whether I should apply normally first.
> Draft a concise message to the sourced recipient with one clear ask, using
> relevant bank evidence and the JD. Do not invent an application or referral.

## Write after applying

> I applied to `<exact role/company>` on `<date or unknown>`. Use the saved JD,
> resume, and contact research to draft a short email and LinkedIn alternative.
> Connect their needs to my work; keep claim/source IDs outside the copyable
> text. Leave both as drafts.

## Follow up or thank an interviewer

> Here is the actual sent thread/interview context: `<text, dates, details>`.
> Write the appropriate follow-up or thank-you using application-letter-writer.
> Respect stated timelines, add useful context, and do not invent a topic or
> earlier message. Suggest timing in my timezone; leave the message as a draft.

## Offers and other hiring replies

> Draft a `<scheduling / clarification / negotiation / acceptance / decline /
> withdrawal / reference>` reply. Here are the real terms, thread, dates, and
> my decision: `<details>`. Use event-response. Ask about missing material
> terms instead of inventing commitments or current competing offers.

## Tailor a new application

> Tailor a one-page Overleaf resume for `<company> — <role>`. The posting is
> `<URL>`; here is the description: `<paste full text>`. Use the current bank,
> relevant bundled skills, and repository instructions. Keep Tamara first.
> Match the key requirements to bank IDs, select the strongest evidence, and
> identify unsupported requirements. Save the standalone source, job text,
> notes, and checked PDF under `applications/<company>-<role>/`. Return the full
> copyable LaTeX and a brief explanation of the choices. Ask only questions
> whose answers would materially change the draft.

## Change the emphasis

**Mercor / growth and sourcing**

> Using this Mercor Growth Associate description, lead with my Sales Navigator
> sourcing, COO-led invitation funnel, candidate relationships, 500+ qualified
> candidates, and shared CRM. Add the SCET 100K+-to-500 lead workflow where
> useful. Compare the personal job-search project with the other projects and
> include whichever best supports the role within one page. Do not claim
> LinkedIn Recruiter experience or a direct Sales Navigator API. Use the bank
> over factual wording in old drafts. Description: `<text and URL>`.

**Retell / deployment and product**

> Build a Deployment Strategist version around stakeholder discovery,
> workflow design, cross-team coordination, internal implementation, and voice
> AI. Consider Tamara, SCET, Embersafe, and Sitters; select the strongest
> evidence rather than fitting everything. Preserve Embersafe's planning stage
> and distinguish demos from production customer delivery. Description:
> `<text and URL>`.

**Retell / AI agents and internal systems**

> Build a Founders Initiatives / AI Agents version emphasizing Greenhouse
> integration, resumable synchronization, AI-assisted structured search,
> HubSpot/AI workflows, and practical building. Keep the technical details
> selective and readable. Explain any professional SWE or production-experience
> gap honestly; do not rename my roles to imply that experience. Description:
> `<text and URL>`.

**Aerospace / engineering**

> Tailor for this aerospace role. Keep Tamara first but brief, and give more
> room to Space Enterprise, STAR, AynX, engineering coursework, CAD, CFD, and
> MATLAB where the description supports it. Use design/simulation wording
> accurately and do not invent physical testing results. Description:
> `<text and URL>`.

## Add facts to the bank

> Add these new facts: `<facts, dates, ownership, tools, and measurable results>`.
> Compare them with the current bank and record whether they extend or correct
> existing claims. Preserve stable IDs, source attribution, metric scope, and
> answered clarifications. Ask about any material ambiguity. Update the JSON,
> generate the Markdown/CSV views, and run the bank checks. Show the new or
> changed resume-ready bullets; do not silently rewrite old application drafts.

## Compare jobs or resume choices

> Compare `<job A description and URL>` with `<job B description and URL>` using
> the current bank. Map requirements to specific evidence, distinguish direct
> matches from transferable experience and gaps, and recommend a resume
> selection for each. Suggest questions only where new information could change
> the assessment. Do not infer requirements from company reputation.

## Fix or review LaTeX

> Review `<path to resume.tex>` for factual consistency with the current bank,
> one-page A4 layout, readable 10pt body text, and pdfLaTeX compatibility.
> Compile it, inspect extracted text and layout where tools permit, and fix
> errors or overflow. Preserve supported content; shorten weaker material
> before shrinking text. Return the complete standalone LaTeX, not a fragment,
> and report exactly what was verified.

## Prepare for interviews

> Use `<saved job-description.md>` and `<saved resume.tex>` to run a mock
> interview. Ask one question at a time about the role's most important
> responsibilities and my selected projects. Build follow-ups from the bank,
> probing ownership, tradeoffs, and evidence. Help me develop concise answers
> using real examples; flag missing details rather than inventing a story.

## Draft outreach for review

> Draft a short message to `<person/role>` about `<job and URL>`, using only
> supported achievements from the bank. Explain why each selected achievement
> is relevant and provide two concise options. Save the drafts for my review;
> do not send them or infer contact details.
