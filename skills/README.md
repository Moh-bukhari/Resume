# Skills for this repository

The portable system begins at [START-HERE.md](../START-HERE.md). Use
[task workflows](../docs/WORKFLOWS.md) for tracking, preparation, and publishing;
this index selects the specialist methods used inside those workflows.
Any AI can read the skill Markdown directly; a vendor-specific skill loader
is optional. Current work is recorded in [the handoff](../docs/HANDOFF.md).

Start with [AGENTS.md](../AGENTS.md) and [Mohammed's combined application
workflow](application-workflow/SKILL.md), or [the resume subset](resume-workflow/SKILL.md)
when only a resume is needed. Read the relevant published original before using
its method; files and references are available offline.

## Contacts, letters, and full application packets

The combined workflow selects the strongest parts of established sources and
the earlier specialist picks. It includes role-specific bank evidence, current
contact checks, actual conversation history, before/after-application timing,
one useful ask, and editing. See the [dated comparison](../docs/SKILL-SELECTION.md).

| Task | Start here | Supporting skill |
| --- | --- | --- |
| Resume plus contacts and letters | [Combined application workflow](application-workflow/SKILL.md) | Adapted research-to-letter process, role recipes, and checks |
| Research the company/person | [Contact research](contact-research/SKILL.md) | [Anthropic Account Research](anthropic-sales/account-research/SKILL.md) |
| Find people and LinkedIn profiles | [Contact research](contact-research/SKILL.md) | [Exa Search](exa/search/SKILL.md) and its [people patterns](exa/search/references/patterns-people.md) |
| Find/verify professional emails | [Contact research](contact-research/SKILL.md) | [Daniela Ryplová's Verified Email Finder](apify/apify-verified-email-finder/SKILL.md) |
| Pre/post-application email, LinkedIn, referral, follow-up, thank-you, or reply | [Application letter writer](application-letter-writer/SKILL.md) | [Anthropic Draft Outreach](anthropic-sales/draft-outreach/SKILL.md) plus [Corey Haines Cold Email](marketingskills/cold-email/SKILL.md) |
| Polish a draft | [Application letter writer](application-letter-writer/SKILL.md) | [Copy Editing](marketingskills/copy-editing/SKILL.md) |
| Optional deeper context | [Contact research](contact-research/SKILL.md) | [Firecrawl Lead Research](firecrawl/firecrawl-lead-research/SKILL.md) |
| Formal cover letter | [Application letter writer](application-letter-writer/SKILL.md) | [Cover Letter Generator](resumeskills/skills/cover-letter-generator/SKILL.md) |

See [selection research](../docs/SKILL-SELECTION.md),
[contact guidance](../docs/CONTACT-RESEARCH.md), and
[letter routing/templates](../docs/LETTERS.md). The three selected marketing
skills include their references, evaluation cases, and [MIT license](marketingskills/LICENSE).
Their [pinned provenance](marketingskills/UPSTREAM.md) is separate from the
original ResumeSkills bundle below. Exa, Apify, and Firecrawl have separate
upstream provenance/licenses in their directories. Anthropic's two official
sales skills retain their originals and [Apache-2.0 provenance](anthropic-sales/UPSTREAM.md).
No live tool/provider access
is installed. These are original published skill files; local guides provide
the application-specific context.

Local guidance adapts Anthropic's research/history/intent structure and Corey's
natural voice and editing. Exa supplies targeted discovery; the optional email
finder contributes wrong-company and verification-status checks. Sales-volume
targets, sending domains, mailbox warm-up, automatic replies, and rigid
length/subject rules are not defaults for job applications. Contacts and event
state must be grounded in evidence.

## Default tailoring sequence

1. [Job description analyzer](resumeskills/skills/job-description-analyzer/SKILL.md): identify responsibilities, requirements, and evidence gaps.
2. [Resume tailor](resumeskills/skills/resume-tailor/SKILL.md): select supported experience for the target.
3. [Bullet writer](resumeskills/skills/resume-bullet-writer/SKILL.md): tighten action, scope, and outcome wording.
4. [Formatter](resumeskills/skills/resume-formatter/SKILL.md): readable layout, then compile and inspect the PDF.
5. [Version manager](resumeskills/skills/resume-version-manager/SKILL.md): preserve source facts and keep application versions distinct.

Use ATS optimization for clarity and keyword alignment, not a promise of an ATS
score. Use the quantifier to identify useful questions, not invent numbers.
Choose cover-letter, interview, LinkedIn, outreach, and other skills only for
that task. Their presence does not authorize sending, applying, or publishing.

## User preferences and factual priority

The bank and latest user instructions take precedence over generic examples.
Do not add a missing skill solely because a JD contains it, copy an example's
numbers, assume tool expertise from a code import, or substitute a long CV for
the requested one-page resume. Keep Tamara first and provide complete
standalone Overleaf LaTeX. Upstream suggested layouts, file names, and match
scores are optional; this repository's workflow is documented in AGENTS.md.

## Included upstream bundle

Source: [paramchoudhary/ResumeSkills](https://github.com/paramchoudhary/resumeskills),
pinned commit `74ae19e7c62b0516d1c298328e5544976c12da5d`.
The requested skill files are vendored unchanged under `resumeskills/`, with
[LICENSE](resumeskills/LICENSE), [README](resumeskills/README.md), and contributing
guidance. Upstream README links were adjusted for this nested location.
It contains 22 skills. No plugin installation or network fetch is
needed to read them. The local wrapper above is specific to this repository.

| Skill | Purpose |
| --- | --- |
| [academic-cv-builder](resumeskills/skills/academic-cv-builder/SKILL.md) | Format CVs for academic positions with publications, grants, and teaching |
| [application-form-filler](resumeskills/skills/application-form-filler/SKILL.md) | Fill out job application form fields with context-aware, tailored answers drawn from the candidate's CV and the job description |
| [career-changer-translator](resumeskills/skills/career-changer-translator/SKILL.md) | Translate skills from one industry to another, identify transferable skills |
| [cold-email-writer](resumeskills/skills/cold-email-writer/SKILL.md) | Write personalized cold outreach emails to hiring managers and founders — specific, human, not a pitch deck |
| [cover-letter-generator](resumeskills/skills/cover-letter-generator/SKILL.md) | Create personalized, compelling cover letters from resume and job description |
| [creative-portfolio-resume](resumeskills/skills/creative-portfolio-resume/SKILL.md) | Balance visual design with ATS compatibility for creative roles |
| [executive-resume-writer](resumeskills/skills/executive-resume-writer/SKILL.md) | Create C-suite and VP level resumes emphasizing strategic leadership |
| [interview-prep-generator](resumeskills/skills/interview-prep-generator/SKILL.md) | Generate STAR stories, practice questions, and talking points from resume |
| [job-description-analyzer](resumeskills/skills/job-description-analyzer/SKILL.md) | Analyze job postings, calculate match scores, identify gaps, and create application strategy |
| [linkedin-profile-optimizer](resumeskills/skills/linkedin-profile-optimizer/SKILL.md) | Optimize LinkedIn profile for searchability, recruiter visibility, and engagement |
| [offer-comparison-analyzer](resumeskills/skills/offer-comparison-analyzer/SKILL.md) | Compare multiple job offers side-by-side with total compensation analysis |
| [portfolio-case-study-writer](resumeskills/skills/portfolio-case-study-writer/SKILL.md) | Transform resume bullets into detailed portfolio case studies |
| [reference-list-builder](resumeskills/skills/reference-list-builder/SKILL.md) | Format professional references properly and prepare reference materials |
| [resume-ats-optimizer](resumeskills/skills/resume-ats-optimizer/SKILL.md) | Optimize resumes for Applicant Tracking Systems, check ATS compatibility, and analyze keyword match |
| [resume-bullet-writer](resumeskills/skills/resume-bullet-writer/SKILL.md) | Transform weak resume bullets into achievement-focused statements with metrics and impact |
| [resume-formatter](resumeskills/skills/resume-formatter/SKILL.md) | Ensure ATS-friendly formatting and create clean scannable layouts |
| [resume-quantifier](resumeskills/skills/resume-quantifier/SKILL.md) | Find opportunities to add metrics and estimate numbers when exact data unavailable |
| [resume-section-builder](resumeskills/skills/resume-section-builder/SKILL.md) | Create targeted resume sections optimized for different experience levels and roles |
| [resume-tailor](resumeskills/skills/resume-tailor/SKILL.md) | Customize resume for specific job postings while maintaining truthfulness |
| [resume-version-manager](resumeskills/skills/resume-version-manager/SKILL.md) | Track different resume versions, maintain master resume, manage tailored versions |
| [salary-negotiation-prep](resumeskills/skills/salary-negotiation-prep/SKILL.md) | Research market rates, build negotiation strategy, and create counter-offer scripts |
| [tech-resume-optimizer](resumeskills/skills/tech-resume-optimizer/SKILL.md) | Optimize resumes for software engineering, PM, and technical roles |
