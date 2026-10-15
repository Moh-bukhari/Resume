# Skills selected for job research and letters

Reviewed for this repository on 2026-10-15. Selection criteria: contact/source
quality, current-role verification, handling unknown email results, useful
writing guidance, dependencies, and an explicit redistributable license.
This is a task-specific selection, not a universal ranking or response-rate claim.

| Skill | Decision and purpose |
| --- | --- |
| [Corey Haines — Prospecting](../skills/marketingskills/prospecting/SKILL.md) | Included. Strong source/date/confidence records, identity cross-checks, contact enrichment, and distinction between no match and tool errors. Local wrapper adapts sales targeting to a job's function. |
| [Corey Haines — Cold Email](../skills/marketingskills/cold-email/SKILL.md) | Included. Concise writing, relevant personalization, one ask, follow-ups, and LinkedIn guidance. Local wrapper selects drafting guidance and excludes bulk-sales infrastructure/automatic reply assumptions. |
| [ResumeSkills — Cover Letter Generator](../skills/resumeskills/skills/cover-letter-generator/SKILL.md) | Already included. Useful for a formal role-specific letter using the factual bank. |
| [ResumeSkills — Cold Email Writer](../skills/resumeskills/skills/cold-email-writer/SKILL.md) | Retained as optional style guidance. Local defaults replace its long length minimum, fixed subject, and unnecessary disclosure blocks. |
| [Composio — Lead Research Assistant](https://github.com/ComposioHQ/awesome-claude-skills/blob/be2a406907dbc61b73e6827ded415c96139d13a2/lead-research-assistant/SKILL.md) | Reviewed, not copied. More generic company sales-lead research, with less detail on contact evidence for this need; overlaps the selected research skill. |
| [OpenAI — Playwright](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright) | Optional capability reference. Helps browser work when installed; provides neither web search nor contact data by itself. Not needed to read this toolkit or generate drafts. |

The two newly included upstream skills are pinned to commit
`365b412152b9542499ca1439426f7fc3cc92bb65` and copied with their references,
evaluation cases, and MIT license. See
[provenance](../skills/marketingskills/UPSTREAM.md).

## How they work together

1. [Application workflow](../skills/application-workflow/SKILL.md) coordinates
   the packet, application state, and output files.
2. [Resume workflow](../skills/resume-workflow/SKILL.md) selects bank facts and
   produces the one-page Overleaf resume.
3. [Contact research](../skills/contact-research/SKILL.md) finds relevant
   people, actual LinkedIn URLs, and professional email evidence.
4. [Application letter writer](../skills/application-letter-writer/SKILL.md)
   writes the right message for the confirmed stage and recipient.

Local wrappers take priority over generic sales examples, campaign benchmarks,
mandatory sending domains, or autonomous-message suggestions. No browser,
provider account, subscription, or API access is installed by copying a skill.
Public-source research is the default; available authorized tools can improve
coverage. Missing results remain missing rather than becoming guessed contacts.
