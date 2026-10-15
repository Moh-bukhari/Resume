# Maintain the factual master

Edit `bank/experience-bank.json`. Markdown and CSV are generated views. Never
update only a tailored resume and assume future AIs will discover that fact.

## Update process

1. Read affected experience, bullets, metrics, sources, rules, and answered
   clarifications. The latest explicit user correction wins.
2. Append a source with a stable `SRC` ID and what the user confirmed or the
   inspection established. Online research needs a URL and access/status
   context. A failed lookup is not evidence of the information sought.
3. Update affected context, ownership, status, and all bullet variants.
   Preserve IDs even if wording or project grouping changes. New IDs use the
   next available number; do not recycle IDs for unrelated claims.
4. Update numerical facts with value, unit, period, population, team credit,
   and scope. Keep approximations and thresholds distinct. Do not derive
   conversion rates without comparable cohorts and confirmed periods.
5. Resolve answered questions and contradictory rules/role maps. Record the
   clarification so another AI does not ask the same question again.
6. Use the user's local date for `updated_client_date` when available. Old
   sources retain their historical dates.
7. Regenerate and validate:

   ```bash
   python3 scripts/render_bank.py
   python3 scripts/check_bank.py
   ```

Review changed JSON, Markdown, and CSV. Update supporting docs if needed.
Existing application drafts remain snapshots unless asked to revise them.

## JSON map

| Section | Content |
| --- | --- |
| `profile` | Contact, education, availability, language, preferences, positioning |
| `sources` | Stable provenance IDs, descriptions, and links |
| `experiences` | Role/project title, dates, context, ownership, scope metadata |
| `bullets` | ID, experience ID, text, tags, source IDs, status, scope note |
| `metrics` | Number, meaning, confirmation, attribution limits |
| `awards` | Project, recognition, date, team/project prize scope |
| `skills`, `coursework` | Stated tools, implementation evidence, uncertainty, coursework |
| `summaries`, `role_maps` | Optional positioning and relevant bullet selections |
| `questions`, `answered_clarifications` | Missing details and corrections already recorded |
| `tailoring_rules`, `submission_status` | Preferences, factual safeguards, draft/submission distinctions |

Statuses communicate maturity: `ready`, `needs_detail`, `planned_only`.
An in-progress status can describe future confirmed implementation; it must
never turn planning into completed work. Follow the validator's accepted schema.

## Portable sources

Store relevant sources under `sources/` with repository-relative paths. The
original upload can contain older claims; current bank corrections win.
`tamara-crm-study.md` includes upstream commit/path citations and review limits.

Do not depend on a scratch builder, temporary CRM checkout, prior chat,
credentials, or applicant database. Do not copy candidate files or environment
secrets into the repository. Skill examples, employer requirements, and intended
functionality are not new accomplishments.

Keep unverified details unverified, including Embersafe's exact competition
cycle/dates, undescribed implementation stacks, and external production/customer
outcomes. Do not make a blank field look complete by guessing.
