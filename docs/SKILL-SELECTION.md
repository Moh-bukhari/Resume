# Published specialist skills

The user wants existing online skills from practitioners and specialist tool
publishers. These are original external `SKILL.md` sources. The local workflow
files provide bank facts, application state, and output preferences.

Reviewed on 2026-10-15 by reading the published skill files, their references,
publisher information, dependencies, and licenses. Quality was assessed from
the methods; response rates and hiring results were not independently tested.

| Need | Published source | Why selected | Runtime needed |
| --- | --- | --- | --- |
| Find relevant people / LinkedIn | [Exa Labs — Search](https://github.com/exa-labs/exa-mcp-server/blob/e9c3b0126a3373eb1aeaca162e84d0791ff4c7f7/skills/search/SKILL.md) | Official search-provider skill; [people patterns](https://github.com/exa-labs/exa-mcp-server/blob/e9c3b0126a3373eb1aeaca162e84d0791ff4c7f7/skills/search/references/patterns-people.md) cover role/company queries, LinkedIn-weighted results, team-page checks, and profile deduplication. | Connected Exa search/fetch tools; account/access as documented upstream. |
| Find and verify business emails | [Daniela Ryplová — Verified Email Finder](https://github.com/apify/awesome-skills/blob/1eb0cd0c12e35a0d0a17c23f0f462d7062fd5813/skills/apify-verified-email-finder/SKILL.md) | Community-authored skill in Apify's official community catalog. Department filters, verification status handling, wrong-company filtering based on an observed error, and run/source provenance. | Authenticated Apify MCP/Actor access and credits, or the optional documented CLI route. |
| Write personalized email / LinkedIn outreach | [Corey Haines — Cold Email](https://github.com/coreyhaines31/marketingskills/blob/365b412152b9542499ca1439426f7fc3cc92bb65/skills/cold-email/SKILL.md) | Practitioner-authored guidance for concise writing, relevant personalization, proof, one clear ask, follow-ups, and channel-specific wording. | An AI with the job, candidate evidence, and recipient context. |
| Edit and sharpen the letter | [Corey Haines — Copy Editing](https://github.com/coreyhaines31/marketingskills/blob/365b412152b9542499ca1439426f7fc3cc92bb65/skills/copy-editing/SKILL.md) | Focused clarity, voice, relevance, evidence, and specificity passes; supports small edits instead of rewriting every draft. | An AI and the draft. |
| Research the person/company for a real hook | [Firecrawl — Lead Research](https://github.com/firecrawl/skills/blob/5348e9ed68062cff515f741eb61de92eeb509d12/skills/workflows/firecrawl-lead-research/SKILL.md) | Official web-research-provider skill for sourced company/person briefs and talking points; separates observations from inferred pain points. | Firecrawl search/scrape capability and API access. |

## Why these publishers

- **Exa Labs** publishes the skill in its own MCP-server repository. Its
  people-search instructions are specific to its search tools.
- **Daniela Ryplová** is explicitly credited in the email-finder skill. Apify
  hosts the community catalog; this is community authorship, not a claim that
  every instruction was written by Apify's core team.
- **Corey Haines** identifies himself in the [repository](https://github.com/coreyhaines31/marketingskills)
  and [profile](https://github.com/coreyhaines31/coreyhaines31) as founder of
  Conversion Factory and publisher of Swipe Files. This is relevant marketing
  practitioner provenance, not a verified guarantee of job-outreach results.
- **Firecrawl** publishes its research skill in its own skills repository.

## Local copies and provenance

| Source | Local files | License / version record |
| --- | --- | --- |
| Exa | [Search](../skills/exa/search/SKILL.md), including all references | [Provenance](../skills/exa/UPSTREAM.md), MIT |
| Apify community | [Verified Email Finder](../skills/apify/apify-verified-email-finder/SKILL.md), references, examples, optional CLI files | [Provenance](../skills/apify/UPSTREAM.md), Apache 2.0 |
| Corey Haines | [Cold Email](../skills/marketingskills/cold-email/SKILL.md), [Copy Editing](../skills/marketingskills/copy-editing/SKILL.md), existing [Prospecting](../skills/marketingskills/prospecting/SKILL.md) | [Provenance](../skills/marketingskills/UPSTREAM.md), MIT |
| Firecrawl | [Lead Research](../skills/firecrawl/firecrawl-lead-research/SKILL.md) | [Provenance](../skills/firecrawl/UPSTREAM.md), ISC |

Original skill files are preserved with licenses. Runtime services are not
installed or authenticated by copying instructions. No provider runs or paid
lookups were performed during curation. Optional scripts are retained as
upstream source, not executed or operationally validated.

## Recommended combination

Use Exa to find the relevant person, Verified Email Finder when email enrichment
is needed and authorized, Cold Email to write the message, and Copy Editing for
a final pass. Use Firecrawl when deeper person/company context is useful.
Existing Prospecting remains useful when working from ordinary public research.

Use current role/source evidence and the resume bank throughout. A provider
verification result does not establish current employment or hiring authority.
For job applications, preserve the actual before/after-application stage and
the user's preferred tone; sales-campaign settings and generic example numbers
do not become requirements or candidate facts.

Also reviewed [Felix Lee's Cold Message Writer](https://github.com/felixleezd/cold-message-writer),
which contains a job-seeking playbook, and
[Move's TA Hiring Stack](https://github.com/we-are-move/claude-ta-hiring-stack),
published by an embedded recruiting/sourcing consultancy. These are useful
additional references; the former uses several rigid style tactics and the
latter primarily addresses recruiters contacting candidates. They are not
defaults for this candidate-side toolkit.

Hunter's official MCP repository is a tool integration rather than a published
`SKILL.md`; third-party Hunter wrappers should not be described as Hunter-authored
expert playbooks. Keep the existing ResumeSkills bundle for resume/cover-letter
tasks without implying independent proof of its marketing outcome claims.
