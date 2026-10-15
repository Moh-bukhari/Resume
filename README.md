# Mohammed Bukhari — application toolkit

A factual experience bank, one-page Overleaf resumes, professional contact
research, and tailored application letters in one place.
**AI assistants: start with [AGENTS.md](AGENTS.md).**

## Published specialist skills

The [comparison research](docs/SKILL-SELECTION.md) covers both the earlier
picks and better-known alternatives. The combined workflow uses Anthropic's
official research/outreach skills (about 29.8K repository stars) and Corey
Haines' specialist writing/editing skills (about 54.9K), alongside Exa for
people discovery. Counts were observed on October 15, 2026; they measure
repository popularity, not results for an individual skill.

| Task | Published skill |
| --- | --- |
| Research relevant company/person needs | [Anthropic — Account Research](skills/anthropic-sales/account-research/SKILL.md) |
| Find relevant people and LinkedIn profiles | [Exa Labs — Search](skills/exa/search/SKILL.md), including people-search patterns |
| Choose cold/warm intent and structure the message | [Anthropic — Draft Outreach](skills/anthropic-sales/draft-outreach/SKILL.md) |
| Write natural, concise outreach | [Corey Haines — Cold Email](skills/marketingskills/cold-email/SKILL.md) |
| Polish the writing | [Corey Haines — Copy Editing](skills/marketingskills/copy-editing/SKILL.md) |
| Optional email enrichment/verification | [Daniela Ryplová — Verified Email Finder](skills/apify/apify-verified-email-finder/SKILL.md), from Apify's community catalog |
| Optional deeper context | [Firecrawl — Lead Research](skills/firecrawl/firecrawl-lead-research/SKILL.md) |

Use [Mohammed's combined workflow](skills/application-workflow/SKILL.md) for
role-specific proof selection, recipient research, message timing, and drafting.
Original sources, licenses, and pins are retained separately. It adapts the
methods to your bank and May 2027 graduation, with examples for growth,
deployment, AI systems, and engineering roles.
Exa/Apify/Firecrawl execution needs the relevant tool access;
copying the skills does not configure an account or spend credits.

## Start here

1. Read the [experience bank](bank/experience-bank.md) and the full job description.
2. Follow the [combined application workflow](skills/application-workflow/SKILL.md)
   and [skill router](skills/README.md); use the [tailoring guide](docs/TAILORING.md)
   for the resume layout and selection.
3. Create an [application packet](applications/README.md) with the helper below.
4. Tailor the [resume](templates/resume-base.tex),
   [research relevant people](docs/CONTACT-RESEARCH.md), and
   [choose the right letter](docs/LETTERS.md) for the actual stage.
5. Build/check the resume and contacts. Provide complete LaTeX and copyable
   letters in chat. Downloads have
   previously been unreliable.

The default is one A4 page, readable 10pt text, pdfLaTeX, and Tamara first.

## Repository map

| Path | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Main instructions and navigation for any AI assistant |
| [CLAUDE.md](CLAUDE.md) | Claude entry point pointing to the same instructions |
| [bank/experience-bank.json](bank/experience-bank.json) | Editable factual master: profile, experiences, bullets, metrics, skills, summaries, sources, gaps, role maps |
| [bank/experience-bank.md](bank/experience-bank.md) | Generated human-readable master bank |
| [bank/bullet-bank.csv](bank/bullet-bank.csv) | Generated spreadsheet of selectable bullet variants |
| [skills/README.md](skills/README.md) | How to choose bundled skills |
| [skills/resume-workflow/SKILL.md](skills/resume-workflow/SKILL.md) | Repository-specific resume workflow |
| [skills/application-workflow/SKILL.md](skills/application-workflow/SKILL.md) | Complete resume/contact/letter packet |
| [skills/resumeskills/](skills/resumeskills/) | Requested upstream ResumeSkills bundle and license |
| [skills/marketingskills/](skills/marketingskills/UPSTREAM.md) | Selected Prospecting, Cold Email, and Copy Editing skills with references/license |
| [skills/anthropic-sales/](skills/anthropic-sales/UPSTREAM.md) | Official Account Research and Draft Outreach originals, license, and pinned provenance |
| [docs/SKILL-SELECTION.md](docs/SKILL-SELECTION.md) | Earlier vs established alternatives, adoption evidence, and selection decisions |
| [sources/skill-research/](sources/skill-research/2026-10-15-adoption.json) | Dated repository adoption, maintenance, publisher, and source observations |
| [docs/CONTACT-RESEARCH.md](docs/CONTACT-RESEARCH.md) | Find relevant people, LinkedIn URLs, and sourced professional emails |
| [docs/LETTERS.md](docs/LETTERS.md) | Before/after-application messages, cover letters, referrals, follow-ups, and hiring replies |
| [docs/TAILORING.md](docs/TAILORING.md) | Positioning, layout choices, and role-family examples |
| [docs/EXAMPLE-PROMPTS.md](docs/EXAMPLE-PROMPTS.md) | Copyable prompts for tailoring, updates, reviews, and interview preparation |
| [docs/MAINTENANCE.md](docs/MAINTENANCE.md) | Updating facts and generated views |
| [docs/BUILD.md](docs/BUILD.md) | Local/Overleaf compilation and troubleshooting |
| [templates/](templates/) | Resume, contact record, outreach plan, notes, and letter templates |
| [applications/](applications/README.md) | Future job-specific versions and evidence notes |
| [jobs/README.md](jobs/README.md) | User-supplied target requirements; live postings unverified |
| [tamara-crm-study.md](tamara-crm-study.md) | Source-cited implementation evidence and limits |
| [sources/README.md](sources/README.md) | Original upload and provenance guidance |
| [resume-facts.md](resume-facts.md) | Historical working notes; bank corrections take priority |
| [retell-fit-notes.md](retell-fit-notes.md) | Earlier fit analysis; some details later clarified |
| `scripts/` | Bank rendering, consistency checks, and PDF build helpers |

## Existing resume versions

These are preserved prior drafts. They predate some bank updates, including
the historical 700K+ applicant scope, SCET lead filtering, and personal
job-search results. Use the bank and current template for new work. A draft
is not evidence that an application was submitted.

| Version | Standalone LaTeX | PDF |
| --- | --- | --- |
| General base | [main.tex](main.tex) | [PDF](Mohammed_Bukhari_Resume.pdf) |
| Retell Deployment Strategist | [LaTeX](retell-deployment-strategist.tex) | [PDF](Mohammed_Bukhari_Retell_Deployment_Strategist.pdf) |
| Retell Founders Initiatives, AI Agents | [LaTeX](retell-founders-initiatives.tex) | [PDF](Mohammed_Bukhari_Retell_Founders_Initiatives.pdf) |
| Mercor Growth Associate | [LaTeX](mercor-growth-associate.tex) | [PDF](Mohammed_Bukhari_Mercor_Growth_Associate.pdf) |

## Commands

Run from the repository root. Python helpers use only the standard library.

```bash
python3 scripts/render_bank.py
python3 scripts/check_bank.py
bash scripts/build_resume.sh templates/resume-base.tex

# Start an unsent draft packet; see --help for stage/date options:
python3 scripts/new_application.py --company "Example Company" --role "Growth Associate"
python3 scripts/check_contacts.py applications/example-company-growth-associate/contacts.json
```

Build output goes under ignored `build/<source-stem>/`. See
[build instructions](docs/BUILD.md) for dependencies and PDF review. No web
server, database, API keys, or candidate data are needed for local drafting.
Live contact research uses the assistant's search/browser tools; enrichment
providers are optional. Skills supply instructions, not database/API access.

To begin an application, paste the JD and say:

> Read AGENTS.md and prepare my application packet for this job. Tailor a
> one-page Overleaf resume, find the most relevant person and source their
> LinkedIn/professional email, and draft the right message for my application
> stage. Keep contact uncertainty explicit and give complete LaTeX and
> copyable letters. Job description: [paste]. Application status: [state].
