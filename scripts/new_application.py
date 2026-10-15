#!/usr/bin/env python3
"""Create a local application workspace of untailored, unsent draft templates."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import unicodedata

from check_contacts import validate_contacts


REPO_ROOT = Path(__file__).resolve().parents[1]
STAGES = ("unknown", "before_application", "after_application", "interview_completed")


def iso_date(value: str) -> str:
    try:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError
    except ValueError as error:
        raise argparse.ArgumentTypeError("Use an ISO date: YYYY-MM-DD.") from error
    return value


def metadata_value(value: str) -> str:
    value = value.strip()
    if not value or any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise argparse.ArgumentTypeError("Use a nonempty, single-line company or role name.")
    return value


def valid_slug(value: str) -> str:
    if len(value) > 120 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError("Slug must be 1–120 lowercase letters/numbers separated by hyphens.")
    return value


def default_slug(company: str, role: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", company + " " + role).encode("ascii", "ignore").decode()
    return valid_slug(re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-"))


def replace_metadata_lines(text: str, replacements: dict[str, str]) -> str:
    """Replace exact metadata lines; never change claims or message body placeholders."""
    return "\n".join(replacements.get(line, line) for line in text.splitlines()) + "\n"


def letter_metadata(text: str, company: str, role: str, stage: str, created_on: str) -> str:
    # A template for a post-application message is not itself a submission record.
    # Only the explicitly supplied stage may establish application status.
    application_status = {
        "unknown": "unconfirmed",
        "before_application": "not_submitted",
        "after_application": "submitted_user_confirmed",
        "interview_completed": "unconfirmed",
    }[stage]
    values = {
        "company": company, "role": role, "draft_date": created_on,
        "application_status": application_status, "application_stage": stage,
    }
    lines: list[str] = []
    in_yaml = False
    saw_stage = False
    for line in text.splitlines():
        if line.strip() == "```yaml":
            in_yaml = True
            saw_stage = False
        elif in_yaml and line.strip() == "```":
            if not saw_stage:
                lines.append("application_stage: " + json.dumps(stage))
            in_yaml = False
        elif in_yaml and ":" in line and not line[:1].isspace():
            key = line.split(":", 1)[0]
            if key in values:
                line = key + ": " + json.dumps(values[key], ensure_ascii=False)
                saw_stage = saw_stage or key == "application_stage"
        lines.append(line)
    return "\n".join(lines) + "\n"


def prepare_files(company: str, role: str, stage: str, created_on: str) -> dict[str, str]:
    templates = REPO_ROOT / "templates"
    required = {
        "resume.tex": templates / "resume-base.tex",
        "tailoring-notes.md": templates / "application-notes.md",
        "outreach-plan.md": templates / "outreach-plan.md",
    }
    files = {name: path.read_text(encoding="utf-8") for name, path in required.items()}
    contact_template = json.loads((templates / "contacts.json").read_text(encoding="utf-8"))
    if not isinstance(contact_template, dict):
        raise ValueError("templates/contacts.json must contain an object")
    if contact_template.get("contacts") or contact_template.get("outreach_events"):
        raise ValueError("contacts template must have empty contacts and outreach_events lists")
    contact_template.update({
        "company": company, "role": role, "application_stage": stage,
        "created_on": created_on or None, "application_date": None, "interview_date": None,
        "research_status": "not_started", "contacts": [], "outreach_events": [],
    })
    contact_errors, _ = validate_contacts(contact_template)
    if contact_errors:
        raise ValueError("Invalid contacts template: " + "; ".join(contact_errors))
    files["contacts.json"] = json.dumps(contact_template, ensure_ascii=False, indent=2) + "\n"
    common = {
        "- Company: [company]": f"- Company: {company}",
        "- Role: [role]": f"- Role: {role}",
        "- Exact role title: [title from the supplied/official description]": f"- Exact role title: {role}",
        "- Application stage: [stage]": f"- Application stage: {stage}",
        "- Created on: [date]": f"- Created on: {created_on}",
        "- Version created/updated: [YYYY-MM-DD, user/client timezone]": f"- Version created/updated: {created_on}",
    }
    for name in ("tailoring-notes.md", "outreach-plan.md"):
        files[name] = replace_metadata_lines(files[name], common)
    if stage == "after_application":
        files["tailoring-notes.md"] = replace_metadata_lines(files["tailoring-notes.md"], {
            "- Submission status: **no submission recorded**":
                "- Submission status: **submitted — explicitly supplied application stage; date unknown**",
            "- Submission evidence/date, only if explicitly confirmed by the user: [not supplied]":
                "- Submission evidence/date, only if explicitly confirmed by the user: "
                "initializer stage `after_application`; exact submission date not supplied",
        })
    # Preserve the supplied template's document/submission records as pending.
    # Record explicit CLI stage separately so an interview does not imply an application date.
    files["tailoring-notes.md"] += (
        "\n## Initializer context\n\n"
        f"- Application stage explicitly supplied to initializer: `{stage}`\n"
        f"- Workspace creation date supplied by the user: {created_on}\n"
        "- Application and interview dates: not supplied by the initializer.\n"
        "- Files are unreviewed templates; no tailoring, contact research, submission, or sending performed.\n"
    )
    files["job-description.md"] = (
        "# Job description — pending\n\n"
        f"- Company: {company}\n"
        f"- Role supplied to initializer: {role}\n"
        "- Official posting URL: [pending]\n"
        "- Source: [pending — supplied text or accessible official posting]\n"
        "- Source obtained on: \n\n"
        "Paste the actual full job description here before tailoring. The company/role above are user inputs, "
        "not verification of an opening. No job research has been performed.\n"
    )
    letters = sorted(path for path in (templates / "letters").glob("*.md")
                     if path.name.lower() != "readme.md")
    if not letters:
        raise ValueError("No Markdown templates found under templates/letters/")
    for path in letters:
        files["letters/" + path.name] = letter_metadata(
            path.read_text(encoding="utf-8"), company, role, stage, created_on,
        )
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--company", required=True, type=metadata_value)
    parser.add_argument("--role", required=True, type=metadata_value)
    parser.add_argument("--slug", type=valid_slug, help="Folder name; defaults to company-role.")
    parser.add_argument("--stage", choices=STAGES, default="unknown", help="Explicit known stage; default unknown.")
    parser.add_argument("--date", type=iso_date, help="User-local workspace date; omitted dates remain blank.")
    parser.add_argument("--output-root", type=Path, default=REPO_ROOT / "applications")
    args = parser.parse_args()
    try:
        slug = args.slug or default_slug(args.company, args.role)
        target = args.output_root / slug
        if target.exists() or target.is_symlink():
            raise ValueError(f"Application folder already exists; refusing to overwrite: {target}")
        files = prepare_files(args.company, args.role, args.stage, args.date or "")
        # All arguments and templates are checked before creating the workspace.
        args.output_root.mkdir(parents=True, exist_ok=True)
        target.mkdir(exist_ok=False)
        for relative, text in files.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
    except (OSError, ValueError, argparse.ArgumentTypeError) as error:
        parser.exit(1, f"Cannot initialize application: {error}\n")
    print(f"Created draft workspace: {target}")
    print(f"Copied {sum(name.startswith('letters/') for name in files)} letter templates; "
          "resume, JD, contacts, and messages still need tailoring/research/review. Nothing was submitted or sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
