# Mohammed Bukhari — resume toolkit

A reusable experience bank, resume skills, and one-page LaTeX workflow for
tailoring applications. **AI assistants: start with [AGENTS.md](AGENTS.md).**

## Start here

1. Read the [experience bank](bank/experience-bank.md) and the full job description.
2. Follow the [tailoring guide](docs/TAILORING.md) and [skill router](skills/README.md).
3. Copy [the current template](templates/resume-base.tex) into a new
   [application folder](applications/README.md), then select relevant facts.
4. Build with `bash scripts/build_resume.sh applications/<company>-<role>/resume.tex`.
5. Provide the complete standalone LaTeX in chat for Overleaf. Downloads have
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
| [skills/resumeskills/](skills/resumeskills/) | Requested upstream ResumeSkills bundle and license |
| [docs/TAILORING.md](docs/TAILORING.md) | Positioning, layout choices, and role-family examples |
| [docs/EXAMPLE-PROMPTS.md](docs/EXAMPLE-PROMPTS.md) | Copyable prompts for tailoring, updates, reviews, and interview preparation |
| [docs/MAINTENANCE.md](docs/MAINTENANCE.md) | Updating facts and generated views |
| [docs/BUILD.md](docs/BUILD.md) | Local/Overleaf compilation and troubleshooting |
| [templates/](templates/) | Current resume starting point and application-notes template |
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
```

Build output goes under ignored `build/<source-stem>/`. See
[build instructions](docs/BUILD.md) for dependencies and PDF review. No web
server, database, API keys, or candidate data are needed.

To begin an application, paste the JD and say:

> Read AGENTS.md and tailor a one-page Overleaf resume for this role using my
> experience bank. Explain the selected evidence and give complete LaTeX.
