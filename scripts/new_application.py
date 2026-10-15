#!/usr/bin/env python3
"""Create a local application workspace of untailored, unsent draft templates."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata
from typing import Any

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


def confirmed_event(job: dict[str, Any], event_type: str) -> dict[str, Any] | None:
    """Select the latest known occurrence, independent of recording order.

    Tracker validation guarantees ISO dates. Undated completed events establish
    that an action happened, but must not erase a known completion date.
    Scheduled interviews are a separate event type and never enter this list.
    """
    events = [event for event in job.get("events", [])
              if event.get("type") == event_type
              and event.get("confirmed_by") in {"user", "tool", "imported_workbook"}]
    return max(events, key=lambda event: event.get("occurred_on") or "") if events else None


def tracker_stage(job: dict[str, Any], explicit: str | None) -> tuple[str, str | None, str | None]:
    application = confirmed_event(job, "application")
    interview = confirmed_event(job, "interview")
    applied_on = job.get("applied_on") or (application or {}).get("occurred_on")
    interviewed_on = (interview or {}).get("occurred_on")
    applied = bool(applied_on or application or job.get("status", "").lower() == "applied")
    if explicit == "before_application" and (applied or interview):
        raise ValueError("before_application conflicts with a recorded application or completed interview")
    stage = explicit
    if stage is None:
        if interview:
            stage = "interview_completed"
        elif applied:
            stage = "after_application"
        elif job.get("status", "").lower() == "saved":
            stage = "before_application"
        else:
            # Interviewing may mean an upcoming conversation, not a completed
            # interview or a formal application.
            stage = "unknown"
    return stage, applied_on, interviewed_on


def tracker_files(files: dict[str, str], job: dict[str, Any], stage: str,
                  application_date: str | None, interview_date: str | None,
                  explicit_stage: bool) -> None:
    """Seed recorded facts while keeping imported summaries and drafts unreviewed."""
    contacts = json.loads(files["contacts.json"])
    contacts.update(application_date=application_date, interview_date=interview_date)
    contact_errors, _ = validate_contacts(contacts)
    if contact_errors:
        raise ValueError("Tracker context conflicts with contact records: " + "; ".join(contact_errors))
    files["contacts.json"] = json.dumps(contacts, ensure_ascii=False, indent=2) + "\n"
    notes = files["tailoring-notes.md"]
    if not explicit_stage:
        notes = notes.replace("Application stage explicitly supplied to initializer:",
                              "Application stage inferred from confirmed tracker context:")
    notes = notes.replace("- Application and interview dates: not supplied by the initializer.",
                          f"- Application date: {application_date or 'unknown'}; "
                          f"completed interview date: {interview_date or 'unknown'}. "
                          "Scheduled interview dates do not establish completed interviews.")
    if stage == "after_application":
        notes = notes.replace("submitted — explicitly supplied application stage; date unknown",
                              "submitted — recorded tracker context; " + (application_date or "date unknown"))
        notes = notes.replace("initializer stage `after_application`; exact submission date not supplied",
                              f"tracker job `{job['id']}`; submission date: {application_date or 'unknown'}")
    files["tailoring-notes.md"] = notes
    summary = [
        "# Job description — full posting pending", "",
        f"- Tracker ID: {job['id']}",
        f"- Company: {job['company']}",
        f"- Role imported from tracker: {job['role']}",
        f"- Official posting URL: {job.get('job_link') or '[pending]'}",
        f"- Requisition ID: {job.get('req_id') or '[unknown]'}",
        f"- Imported source ID: {job.get('source_id') or '[unknown]'}", "",
        "## Imported tracker summary", "",
        "These are historical tracker notes, not the complete job description. "
        "The opening and requirements have not been live verified by this initializer. "
        "Obtain the full posting before tailoring; retain its source and access date.", "",
    ]
    for key, title in (("about_role", "About the role"), ("must_haves", "Must-haves"),
                       ("nice_to_haves", "Nice-to-haves"), ("keywords", "Keywords"),
                       ("interview_process", "Interview process")):
        value = job.get(key)
        if value:
            summary.extend((f"### {title}", "", str(value), ""))
    files["job-description.md"] = "\n".join(summary) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--company", type=metadata_value)
    parser.add_argument("--role", type=metadata_value)
    parser.add_argument("--tracker-id", help="Existing tracker ID, such as R001; infers company and role.")
    parser.add_argument("--tracker", type=Path, default=REPO_ROOT / "tracker" / "tracker.json",
                        help="Tracker JSON to read when --tracker-id is supplied.")
    parser.add_argument("--slug", type=valid_slug,
                        help="Folder name; defaults to company-role, prefixed by the tracker ID when supplied.")
    parser.add_argument("--stage", choices=STAGES,
                        help="Explicit known stage; otherwise use tracker evidence, or unknown without a tracker.")
    parser.add_argument("--date", type=iso_date, help="User-local workspace date; omitted dates remain blank.")
    parser.add_argument("--output-root", type=Path, default=REPO_ROOT / "applications")
    args = parser.parse_args()
    created_target: Path | None = None
    tracker_save_started = False
    try:
        tracker_data = None
        job = None
        application_date = interview_date = None
        if args.tracker_id:
            from tracker import load_tracker, save_tracker, validate_tracker
            tracker_data = load_tracker(args.tracker)
            matches = [item for item in tracker_data["jobs"] if item["id"] == args.tracker_id]
            if len(matches) != 1:
                raise ValueError(f"Expected one tracker job with ID {args.tracker_id!r}")
            job = matches[0]
            for key in ("company", "role"):
                expected = metadata_value(job[key])
                supplied = getattr(args, key)
                if supplied is not None and supplied != expected:
                    raise ValueError(f"--{key} conflicts with tracker {args.tracker_id}; "
                                     "correct the tracker first rather than changing its imported identity")
                setattr(args, key, expected)
            stage, application_date, interview_date = tracker_stage(job, args.stage)
        else:
            if not args.company or not args.role:
                raise ValueError("--company and --role are required unless --tracker-id is supplied")
            stage = args.stage or "unknown"
        base_slug = default_slug(args.company, args.role)
        slug = args.slug or valid_slug((args.tracker_id.lower() + "-" if job else "") + base_slug)
        target = args.output_root / slug
        if target.exists() or target.is_symlink():
            raise ValueError(f"Application folder already exists; refusing to overwrite: {target}")
        relative_target = None
        try:
            relative_target = target.resolve().relative_to((REPO_ROOT / "applications").resolve())
        except ValueError:
            pass  # Temporary/external scaffolds must not modify the real tracker.
        if job and relative_target is not None:
            packet_path = "applications/" + relative_target.as_posix()
            existing = job.get("packet_path")
            if existing and existing != packet_path:
                raise ValueError(f"Tracker {job['id']} is already linked to another packet: {existing}")
        files = prepare_files(args.company, args.role, stage, args.date or "")
        if job:
            tracker_files(files, job, stage, application_date, interview_date, args.stage is not None)
        try:
            tracker_path = args.tracker.resolve().relative_to(REPO_ROOT).as_posix() if job else None
        except ValueError:
            tracker_path = str(args.tracker)
        files["application.json"] = json.dumps({
            "schema_version": "1.0", "application_id": args.tracker_id or None,
            "tracker_path": tracker_path, "company": args.company, "role": args.role,
            "job_link": job.get("job_link") if job else None,
            "req_id": job.get("req_id") if job else None, "created_on": args.date or None,
        }, ensure_ascii=False, indent=2) + "\n"
        # All arguments and templates are checked before creating the workspace.
        args.output_root.mkdir(parents=True, exist_ok=True)
        target.mkdir(exist_ok=False)
        created_target = target
        for relative, text in files.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
        if job and relative_target is not None:
            job["packet_path"] = packet_path
            job["letters_path"] = packet_path + "/letters"
            # The copied resume is an unreviewed starter; resume_path and
            # preparation checkboxes deliberately remain untouched.
            if args.date:
                tracker_data["updated_on"] = args.date
                job["updated_on"] = args.date
            tracker_errors, _ = validate_tracker(tracker_data)
            if tracker_errors:
                raise ValueError("Invalid tracker link: " + "; ".join(tracker_errors))
            tracker_save_started = True
            save_tracker(tracker_data, args.tracker)
    except (OSError, ValueError, argparse.ArgumentTypeError, subprocess.CalledProcessError) as error:
        if created_target is not None and not tracker_save_started:
            shutil.rmtree(created_target)
        retained = (f" Packet retained at {created_target}; inspect the tracker link and regenerate views "
                    "before retrying because tracker saving may have completed."
                    if created_target is not None and tracker_save_started else "")
        parser.exit(1, f"Cannot initialize application: {error}.{retained}\n")
    print(f"Created draft workspace: {target}")
    print(f"Copied {sum(name.startswith('letters/') for name in files)} letter templates; "
          "resume, JD, contacts, and messages still need tailoring/research/review. Nothing was submitted or sent.")
    if job:
        print(f"Tracker context: {job['id']}; stage {stage}. " +
              ("Linked packet and letter paths; preparation status unchanged."
               if relative_target is not None else "External output root: tracker left unchanged."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
