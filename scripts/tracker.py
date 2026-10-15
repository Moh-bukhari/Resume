#!/usr/bin/env python3
"""Maintain the GitHub job tracker. Records local updates; never applies or sends."""

from __future__ import annotations

import argparse
from datetime import date
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any
from urllib.parse import urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACKER = REPO_ROOT / "tracker" / "tracker.json"
STATUSES = {"Unknown", "Saved", "Applied", "Interviewing", "Offer", "Accepted",
            "Rejected", "Withdrew", "Posting closed"}
NETWORKING = {"Not started", "Reached out", "Talked", "Referral asked", "Referred", "No reply"}
EVENT_TYPES = {"application", "sent", "reply", "interview_scheduled", "interview", "offer",
               "accepted", "rejected", "withdrawn", "posting_closed", "note", "tracker_update"}
DATE_FIELDS = {"apply_by", "deadline", "applied_on", "interview_on", "last_contact",
               "posted_on", "added_on", "updated_on"}
BOOL_FIELDS = {"research_done", "proof_done", "resume_done"}
PATH_FIELDS = {"packet_path", "resume_path", "letters_path"}
TEXT_FIELDS = {"company", "role", "priority", "contact", "log", "job_link", "location",
               "work_mode", "job_type", "team", "pay", "start_date", "req_id", "about_role",
               "must_haves", "nice_to_haves", "keywords", "interview_process", "strongest_proof",
               "gaps", "prep_plan", "ai_notes", "source_id"}
EDITABLE = (TEXT_FIELDS | DATE_FIELDS | BOOL_FIELDS | PATH_FIELDS |
            {"status", "networking", "fit", "bank_bullet_ids", "review_notes"}) - {"source_id", "added_on"}
COMPANY_FIELDS = ("priority", "what_they_do", "industry", "hq", "bay_area_office", "mena_office",
                  "stage_and_size", "careers_page", "job_board", "early_career_program",
                  "roles_to_search_for", "why_it_fits", "notes", "added_on", "updated_on", "source_id")


def iso_date(value: str) -> str:
    try:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError
    except (ValueError, TypeError) as error:
        raise ValueError("Dates must use YYYY-MM-DD.") from error
    return value


def valid_url(value: Any) -> bool:
    if not isinstance(value, str) or any(character.isspace() for character in value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname) and not parsed.username and not parsed.password
    except ValueError:
        return False


def safe_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip() or "\\" in value:
        return False
    path = Path(value)
    return (bool(path.parts) and not path.is_absolute() and ".." not in path.parts and path.parts[0] == "applications"
            and (REPO_ROOT / path).resolve().is_relative_to((REPO_ROOT / "applications").resolve()))


def validate_tracker(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["Tracker must be an object."], warnings
    required = {"schema_version", "updated_on", "settings", "sources", "companies", "jobs"}
    if required - data.keys():
        return ["Tracker missing: " + ", ".join(sorted(required - data.keys()))], warnings
    if data["schema_version"] != "1.0":
        errors.append("Expected tracker schema_version 1.0.")
    try:
        iso_date(data["updated_on"])
    except ValueError:
        errors.append("updated_on must be YYYY-MM-DD.")
    settings = data["settings"]
    if not isinstance(settings, dict):
        errors.append("settings must be an object.")
    else:
        for key in ("contact_followup_days", "application_followup_days", "lookahead_days", "fit1_decision_days"):
            if type(settings.get(key)) is not int or settings[key] < 0:
                errors.append(f"settings.{key} must be a nonnegative integer.")
        if settings.get("contact_followup_unit") not in {"calendar", "business"}:
            errors.append("contact_followup_unit must be calendar or business.")
        if not isinstance(settings.get("timezone"), str):
            errors.append("settings.timezone is required.")
        offsets = settings.get("planning_offsets")
        if not isinstance(offsets, dict) or any(type(offsets.get(k)) is not int or offsets[k] < 0
                                              for k in ("research", "networking", "proof", "resume")):
            errors.append("planning_offsets needs nonnegative research/networking/proof/resume integers.")
    for name in ("sources", "companies", "jobs"):
        if not isinstance(data[name], list):
            errors.append(f"{name} must be a list.")
    if errors:
        return errors, warnings
    source_ids: set[str] = set()
    for source in data["sources"]:
        if not isinstance(source, dict) or not isinstance(source.get("id"), str):
            errors.append("Every source needs an id.")
        elif source["id"] in source_ids:
            errors.append("Duplicate source ID: " + source["id"])
        else:
            source_ids.add(source["id"])
    company_names: set[str] = set()
    company_ids: set[str] = set()
    for company in data["companies"]:
        if not isinstance(company, dict) or not isinstance(company.get("name"), str) or not company["name"].strip():
            errors.append("Every company needs a nonempty name.")
            continue
        identifier = company.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"C\d{3,}", identifier) or identifier in company_ids:
            errors.append(f"Invalid/duplicate company ID: {identifier}")
        company_ids.add(str(identifier))
        if company["name"] in company_names:
            errors.append("Duplicate company: " + company["name"])
        company_names.add(company["name"])
    bank = json.loads((REPO_ROOT / "bank" / "experience-bank.json").read_text(encoding="utf-8"))
    bank_ids = {bullet["id"] for bullet in bank["bullets"]}
    job_ids: set[str] = set()
    for job in data["jobs"]:
        if not isinstance(job, dict):
            errors.append("Each job must be an object.")
            continue
        identifier = job.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"R\d{3,}", identifier):
            errors.append(f"Invalid job ID: {identifier}")
            continue
        if identifier in job_ids:
            errors.append("Duplicate job ID: " + identifier)
        job_ids.add(identifier)
        missing = {"company", "role", "status", "networking", "events", "bank_bullet_ids", "review_notes"} - job.keys()
        if missing:
            errors.append(f"{identifier} missing: {', '.join(sorted(missing))}")
            continue
        if job["company"] not in company_names:
            errors.append(f"{identifier}: company must match a company record.")
        if not isinstance(job["role"], str) or not job["role"].strip():
            errors.append(f"{identifier}: role must be nonempty.")
        if not isinstance(job["status"], str) or job["status"] not in STATUSES:
            errors.append(f"{identifier}: invalid application status.")
        if not isinstance(job["networking"], str) or job["networking"] not in NETWORKING:
            errors.append(f"{identifier}: invalid networking status.")
        if job.get("priority") is not None and (not isinstance(job["priority"], str) or job["priority"] not in {"High", "Medium", "Low"}):
            errors.append(f"{identifier}: priority must be High, Medium, Low, or null.")
        if job.get("fit") is not None and (type(job["fit"]) is not int or not 1 <= job["fit"] <= 5):
            errors.append(f"{identifier}: fit must be 1–5 or null.")
        for key in BOOL_FIELDS:
            if type(job.get(key)) is not bool:
                errors.append(f"{identifier}.{key} must be a boolean.")
        for key in DATE_FIELDS:
            if job.get(key) is not None:
                try:
                    iso_date(job[key])
                except ValueError:
                    errors.append(f"{identifier}.{key} must be YYYY-MM-DD or null.")
        for key in ("applied_on", "last_contact"):
            if isinstance(job.get(key), str) and job[key] > data["updated_on"]:
                errors.append(f"{identifier}.{key} cannot be after the recorded update date.")
        for key in TEXT_FIELDS - {"company", "role", "priority"}:
            if job.get(key) is not None and not isinstance(job[key], str):
                errors.append(f"{identifier}.{key} must be text or null.")
        if job.get("job_link") is not None and not valid_url(job["job_link"]):
            errors.append(f"{identifier}: job_link must be an HTTP(S) URL or null.")
        for key in PATH_FIELDS:
            if job.get(key) is not None:
                if not safe_path(job[key]):
                    errors.append(f"{identifier}.{key} must be a safe applications/ path.")
                elif not (REPO_ROOT / job[key]).exists():
                    warnings.append(f"{identifier}.{key}: linked path does not exist yet.")
        for key in ("bank_bullet_ids", "review_notes", "events"):
            if not isinstance(job[key], list):
                errors.append(f"{identifier}.{key} must be a list.")
        if isinstance(job["bank_bullet_ids"], list):
            for bullet_id in job["bank_bullet_ids"]:
                if not isinstance(bullet_id, str) or bullet_id not in bank_ids:
                    errors.append(f"{identifier}: unknown bank bullet ID {bullet_id}.")
        if isinstance(job["review_notes"], list) and any(not isinstance(n, str) for n in job["review_notes"]):
            errors.append(f"{identifier}.review_notes must contain text.")
        event_ids: set[str] = set()
        if isinstance(job["events"], list):
            for event in job["events"]:
                if not isinstance(event, dict):
                    errors.append(f"{identifier}: event must be an object.")
                    continue
                event_id = event.get("id")
                if not isinstance(event_id, str) or not re.fullmatch(re.escape(identifier) + r"-E\d{3,}", event_id) or event_id in event_ids:
                    errors.append(f"{identifier}: invalid/duplicate event ID {event_id}.")
                event_ids.add(str(event_id))
                if not isinstance(event.get("type"), str) or event["type"] not in EVENT_TYPES:
                    errors.append(f"{identifier}: invalid event type.")
                if event.get("confirmed_by") not in {"user", "tool", "imported_workbook"}:
                    errors.append(f"{identifier}: event needs user/tool/imported_workbook provenance.")
                if not isinstance(event.get("note"), str) or not event["note"].strip():
                    errors.append(f"{identifier}: event needs an evidence note.")
                for key in ("occurred_on", "recorded_on"):
                    if event.get(key) is not None:
                        try:
                            iso_date(event[key])
                        except ValueError:
                            errors.append(f"{identifier}: event.{key} must be YYYY-MM-DD or null.")
                if (isinstance(event.get("occurred_on"), str) and isinstance(event.get("recorded_on"), str)
                        and event.get("type") not in {"interview_scheduled", "note"}
                        and event["occurred_on"] > event["recorded_on"]):
                    errors.append(f"{identifier}: a completed event cannot occur after its record date.")
        if job["status"] == "Applied" and not job.get("applied_on"):
            warnings.append(f"{identifier}: application date unknown; no reminder date can be inferred.")
        if job["networking"] in {"Reached out", "Referral asked"} and not job.get("last_contact"):
            warnings.append(f"{identifier}: outreach date unknown; contact follow-up remains undated.")
        if not job.get("job_link"):
            warnings.append(f"{identifier}: posting URL missing; full JD still needs sourcing.")
    return errors, warnings


def load_tracker(path: Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors, _ = validate_tracker(data)
    if errors:
        raise ValueError("Invalid tracker:\n" + "\n".join(errors))
    return data


def resolve_job(data: dict[str, Any], identifier: str) -> dict[str, Any]:
    for job in data["jobs"]:
        if job["id"] == identifier.upper():
            return job
    raise ValueError("Unknown job ID: " + identifier)


def save_tracker(data: dict[str, Any], path: Path, render: bool = True) -> None:
    errors, _ = validate_tracker(data)
    if errors:
        raise ValueError("Tracker update rejected:\n" + "\n".join(errors))
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".tracker-", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    if render:
        completed = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "render_tracker.py"),
                                    "--tracker", str(path), "--output-dir", str(path.parent),
                                    "--as-of", data["updated_on"]], capture_output=True, text=True)
        if completed.returncode:
            raise ValueError("Tracker JSON saved, but view generation failed; rerun render_tracker.py.\n" +
                             completed.stdout + completed.stderr)


def new_event(job: dict[str, Any], kind: str, occurred_on: str | None, recorded_on: str,
              confirmed_by: str, note: str, **extra: Any) -> dict[str, Any]:
    numbers = [int(event["id"].rsplit("E", 1)[1]) for event in job["events"]]
    event = {"id": f"{job['id']}-E{max(numbers, default=0) + 1:03d}", "type": kind,
             "occurred_on": occurred_on, "recorded_on": recorded_on,
             "confirmed_by": confirmed_by, "note": note, **extra}
    job["events"].append(event)
    return event


def project_event(job: dict[str, Any], event: dict[str, Any], history_only: bool = False) -> None:
    """Apply a new current event without letting backfilled history regress state."""
    kind, occurred = event["type"], event["occurred_on"]
    contact_types = {"sent", "reply"}
    lifecycle = {"application", "interview", "offer", "accepted", "rejected", "withdrawn", "posting_closed"}
    if kind in contact_types:
        known = [e["occurred_on"] for e in job["events"] if e is not event
                 and e["type"] in contact_types and e.get("occurred_on")]
        if job.get("last_contact"):
            known.append(job["last_contact"])
        history_only = history_only or bool(occurred and known and occurred < max(known))
    elif kind in lifecycle:
        known = [e["occurred_on"] for e in job["events"] if e is not event
                 and e["type"] in lifecycle and e.get("occurred_on")]
        history_only = history_only or bool(occurred and known and occurred < max(known))
    if kind in {"application", "interview", "interview_scheduled"} and job["status"] in {
            "Offer", "Accepted", "Rejected", "Withdrew", "Posting closed"}:
        history_only = True
    if kind == "offer" and job["status"] in {"Accepted", "Rejected", "Withdrew", "Posting closed"}:
        history_only = True
    event["history_only"] = history_only
    if history_only:
        return
    before = {key: job.get(key) for key in ("status", "networking", "applied_on", "interview_on",
                                           "last_contact", "contact")}
    if event.get("contact"):
        job["contact"] = event["contact"]
    if kind == "application":
        if job["status"] in {"Unknown", "Saved", "Applied"}:
            job["status"] = "Applied"
        if occurred:
            job["applied_on"] = occurred
    elif kind in contact_types:
        job["networking"] = "Reached out" if kind == "sent" else "Talked"
        # An undated new touch cannot start a timer using an older touch's date.
        job["last_contact"] = occurred
    elif kind in {"interview_scheduled", "interview"}:
        job["status"] = "Interviewing"
        if kind == "interview_scheduled":
            job["interview_on"] = occurred
        elif occurred and job.get("interview_on") == occurred:
            job["interview_on"] = None
    elif kind in {"offer", "accepted", "rejected", "withdrawn", "posting_closed"}:
        job["status"] = {"offer": "Offer", "accepted": "Accepted", "rejected": "Rejected",
                         "withdrawn": "Withdrew", "posting_closed": "Posting closed"}[kind]
    changes = {key: {"before": value, "after": job.get(key)}
               for key, value in before.items() if job.get(key) != value}
    if changes:
        event["changes"] = changes


def parse_assignment(raw: str) -> tuple[str, Any]:
    if "=" not in raw:
        raise ValueError("Use --set field=value.")
    key, value = raw.split("=", 1)
    if key not in EDITABLE:
        raise ValueError("Field cannot be changed with --set: " + key)
    if value == "null":
        parsed: Any = None
    elif key in BOOL_FIELDS:
        if value not in {"true", "false"}:
            raise ValueError(key + " needs true or false.")
        parsed = value == "true"
    elif key == "fit":
        parsed = int(value)
    elif key in {"bank_bullet_ids", "review_notes"}:
        parsed = json.loads(value)
    else:
        parsed = value
    return key, parsed


def refresh_packet_context(job: dict[str, Any], changed_keys: set[str], tracker_path: Path) -> None:
    """Keep linked packet context current; completed interviews come only from events."""
    if not job.get("packet_path") or not (changed_keys & {"status", "applied_on", "events"}):
        return
    path = REPO_ROOT / job["packet_path"] / "contacts.json"
    if not path.exists():
        return
    manifest_path = path.parent / "application.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        linked_source = manifest.get("tracker_path")
        if not linked_source or (REPO_ROOT / linked_source).resolve() != tracker_path.resolve():
            return  # An alternate tracker copy must not change another tracker's packet.
        if manifest.get("application_id") != job["id"]:
            raise ValueError("Linked packet has a different application ID; reconcile it first.")
    elif tracker_path.resolve() != DEFAULT_TRACKER.resolve():
        return
    from check_contacts import validate_contacts
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("company") != job["company"] or record.get("role") != job["role"]:
        raise ValueError("Linked contacts.json identity differs; reconcile it before this update.")
    completed = [event for event in job["events"] if event["type"] == "interview"]
    if completed:
        record["application_stage"] = "interview_completed"
        known_dates = [event["occurred_on"] for event in completed if event.get("occurred_on")]
        if known_dates:
            record["interview_date"] = max(known_dates)
    elif job["status"] == "Applied" or job.get("applied_on") or any(e["type"] == "application" for e in job["events"]):
        record["application_stage"] = "after_application"
    elif job["status"] == "Saved":
        record["application_stage"] = "before_application"
    if job.get("applied_on"):
        record["application_date"] = job["applied_on"]
    errors, _ = validate_contacts(record)
    if errors:
        raise ValueError("Linked contact context is invalid: " + "; ".join(errors))
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tracker", type=Path, default=DEFAULT_TRACKER)
    parser.add_argument("--dry-run", action="store_true", help="Show proposed JSON; write nothing.")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Validate source data and report unresolved evidence.")
    show = commands.add_parser("show")
    show.add_argument("id")
    update = commands.add_parser("update", help="Update specified fields and regenerate views.")
    update.add_argument("id")
    update.add_argument("--set", dest="assignments", action="append", required=True)
    event = commands.add_parser("event", help="Record an actual confirmed event; sends/submits nothing.")
    event.add_argument("id")
    event.add_argument("--type", choices=sorted(EVENT_TYPES - {"tracker_update"}), required=True)
    event.add_argument("--event-date", help="Actual event date; omitted stays unknown.")
    event.add_argument("--contact", help="Actual contact name/title, if confirmed.")
    event.add_argument("--history-only", action="store_true",
                       help="Record past evidence without changing current status, contact, or dates.")
    add = commands.add_parser("add", help="Add a saved opportunity; never mark it applied.")
    add.add_argument("--company", required=True)
    add.add_argument("--role", required=True)
    add.add_argument("--url")
    for command in (update, event, add):
        command.add_argument("--on", required=True, help="Client-local record/update date, YYYY-MM-DD.")
        command.add_argument("--note", required=True, help="Evidence or reason for the change.")
        command.add_argument("--confirmed-by", choices=("user", "tool"), required=command is event)
    args = parser.parse_args()
    try:
        data = load_tracker(args.tracker)
        if args.command == "check":
            errors, warnings = validate_tracker(data)
            for warning in warnings:
                print("Note: " + warning)
            print(f"Tracker valid: {len(data['jobs'])} jobs, {len(data['companies'])} companies; "
                  "events are recorded evidence, not a live application/email check.")
            return bool(errors)
        if args.command == "show":
            print(json.dumps(resolve_job(data, args.id), ensure_ascii=False, indent=2))
            return 0
        on = iso_date(args.on)
        if not args.note.strip():
            raise ValueError("An evidence/reason note is required.")
        if args.command == "add":
            company, role = args.company.strip(), args.role.strip()
            if not company or not role or any(c in company + role for c in "\r\n\x00"):
                raise ValueError("Company and role must be nonempty single-line text.")
            if args.url and not valid_url(args.url):
                raise ValueError("--url must be an HTTP(S) posting URL.")
            if args.url and any(job.get("job_link") == args.url for job in data["jobs"]):
                raise ValueError("This posting URL already exists; update its existing ID.")
            if company not in {c["name"] for c in data["companies"]}:
                number = max((int(c["id"][1:]) for c in data["companies"]), default=0) + 1
                data["companies"].append({"id": f"C{number:03d}", "name": company,
                                          **{key: None for key in COMPANY_FIELDS}, "added_on": on, "updated_on": on})
            number = max((int(job["id"][1:]) for job in data["jobs"]), default=0) + 1
            job = {key: None for key in TEXT_FIELDS | DATE_FIELDS | PATH_FIELDS}
            job.update({"id": f"R{number:03d}", "company": company, "role": role, "status": "Saved",
                        "networking": "Not started", "fit": None, **{key: False for key in BOOL_FIELDS},
                        "job_link": args.url, "added_on": on, "updated_on": on,
                        "bank_bullet_ids": [], "review_notes": [], "events": []})
            data["jobs"].append(job)
            new_event(job, "note", on, on, args.confirmed_by or "tool", args.note)
            changed_keys: set[str] = set()
        else:
            job = resolve_job(data, args.id)
            if args.command == "update":
                changes = dict(parse_assignment(raw) for raw in args.assignments)
                protected = (bool({"applied_on", "interview_on", "last_contact"} & changes.keys()) or
                             ("status" in changes and changes["status"] not in {"Saved", "Unknown"}) or
                             ("networking" in changes and changes["networking"] != "Not started"))
                if protected and not args.confirmed_by:
                    raise ValueError("Actual application/outreach/date changes need --confirmed-by user|tool "
                                     "and a note describing the confirmation.")
                changed = {key: {"before": job.get(key), "after": value}
                           for key, value in changes.items() if job.get(key) != value}
                if not changed:
                    print("No changes; files left untouched.")
                    return 0
                if job.get("packet_path") and {"company", "role"} & changed.keys():
                    raise ValueError("This job already has a packet. Reconcile its identity and manifest "
                                     "together before changing the tracker company/role.")
                job.update(changes)
                new_event(job, "tracker_update", on, on, args.confirmed_by or "tool", args.note, changes=changed)
                changed_keys = set(changes)
            else:
                occurred = iso_date(args.event_date) if args.event_date else None
                kind = args.type
                if occurred and occurred > on and kind not in {"interview_scheduled", "note"}:
                    raise ValueError("A completed event cannot be dated after the record date; "
                                     "use interview_scheduled for a future interview.")
                recorded = new_event(job, kind, occurred, on, args.confirmed_by, args.note,
                                     **({"contact": args.contact} if args.contact else {}))
                project_event(job, recorded, args.history_only)
                changed_keys = {"events", "status", "applied_on"}
            job["updated_on"] = on
        data["updated_on"] = on
        errors, _ = validate_tracker(data)
        if errors:
            raise ValueError("Update rejected:\n" + "\n".join(errors))
        if args.dry_run:
            print(json.dumps(job, ensure_ascii=False, indent=2))
            print("Dry run: no tracker, packet, or generated views were changed.")
            return 0
        # Validate packet context before publishing the tracker change. No external action occurs.
        refresh_packet_context(job, changed_keys, args.tracker)
        save_tracker(data, args.tracker)
        print(f"Updated {job['id']}; GitHub views regenerated. Commit and push to publish.")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        parser.exit(1, f"Tracker: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
