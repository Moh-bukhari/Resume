---
name: contact-research
description: Find a small, sourced shortlist of job-relevant recruiters, likely hiring managers, or team leaders with current professional LinkedIn and email evidence.
---

# Job contact research

Use for “find the right person,” “find their LinkedIn/email,” and recipient
research for an application. Read `AGENTS.md` and `docs/CONTACT-RESEARCH.md`.
For a full packet, use `skills/application-workflow/SKILL.md` as the combined
workflow. Read Anthropic's original
`skills/anthropic-sales/account-research/SKILL.md` for sourced company/person
facts, dated signals, and explicitly inferred priorities.
Start with the original published skills selected in `docs/SKILL-SELECTION.md`:
Exa Search/people patterns, Daniela Ryplová's Apify Verified Email Finder, or
Firecrawl Lead Research, according to available tools and the task. Read their
files under `skills/exa/`, `skills/apify/`, and `skills/firecrawl/`. This local
file carries the candidate/project context; use upstream specialist methods.
Use the bundled `skills/marketingskills/prospecting/SKILL.md` for its research,
cross-checking, provenance, and enrichment techniques. This local workflow
replaces the upstream sales ICP, volume, campaign, and sending assumptions.
Host-specific silent work, Page/Slide output, and upload-date substitution
instructions do not apply; follow the actual host and repository context.

1. Read the actual JD, application context, existing contacts, and supplied
   prior threads. Open the full available thread before characterizing its
   latest exchange. Distinguish confirmed prior contact, no history found in
   the sources checked, and history not checked/unavailable. Unqueried history
   does not establish a cold contact. Reuse an established contact instead of
   repeating discovery. Identify the team/function,
   location if relevant, and any named hiring contact. Do not ask for a sales
   ICP; the job and company define relevance.
2. Find one primary contact and one fallback by default. Prefer a named role
   contact, team recruiter, or leader with evidence connecting them to the
   function. Label hiring authority as confirmed, likely, or unknown.
3. Research public company/team pages, current professional profiles, hiring
   posts, and professional work. Use available search/browser tools and source
   the original page. A search snippet is a discovery lead, not proof of a
   current job, contact address, or personalized claim.
4. Cross-check name, employer, function, and profile identity. Record LinkedIn
   URLs only when actually found. If LinkedIn is inaccessible, use other
   sources and record that limit; never invent a profile slug.
5. Prefer a published professional email with a source, or an authorized
   provider result tied to the matching person. Keep email origin separate
   from deliverability checks. An inferred pattern stays inferred; a catch-all
   result or SMTP-valid response is not proof of ownership or delivery.
6. Save `contacts.json` using `templates/contacts.json`, source URLs/access
   dates, relevance, uncertainty, and provider results. No match and a tool
   error are different outcomes. Leave unknown fields empty. In the outreach
   notes, separate observed needs from inferred priorities and connect the
   relevant requirement to supported bank proof; do not invent a personal hook.
7. Return a compact sourced shortlist and recommended channel. If no email
   is supported, offer a sourced LinkedIn profile or the official hiring
   channel. Continue letter drafting with a clear recipient placeholder.

Optional Hunter/Apollo/Clay or other tools may help when already connected.
Do not buy subscriptions or spend unspecified credits just because a skill
names a provider. Credentials belong in the environment, never in this repo.
Use the current host's available browser/search tools as the provider-free
fallback. Current official host/OpenAI plugin documentation can guide optional
browser setup; archived `openai/skills` browser copies are not a fresh-install
recommendation. The default public-source workflow needs no paid account. No bulk LinkedIn
scraper, login bypass, private contact database, or real-mail probe is needed.

No external mailbox drafts, sends, sales sequences, scheduling, or application
submissions are authorized by contact research. Drafting and recording contacts do not
establish an application or outreach event. Run
`python3 scripts/check_contacts.py <application-folder>/contacts.json`.
