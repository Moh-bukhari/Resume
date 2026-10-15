#!/usr/bin/env python3
"""Render a GitHub-readable application tracker from canonical JSON.

Only standard-library modules are used. Generated dates are deliberately static:
--as-of defaults to the JSON's updated_on, never the machine's current date.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date, timedelta
import html
import io
import json
import os
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import quote, urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACKER = ROOT / "tracker" / "tracker.json"
TERMINAL = {"Accepted", "Rejected", "Withdrew", "Posting closed"}
PREPARATION = (("research_done", "Research"), ("proof_done", "Proof / demo"),
               ("resume_done", "Resume"))
SCHEDULE_DATES = ("apply_by", "deadline", "applied_on", "interview_on", "last_contact")
ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")


def parse_date(value: Any, label: str) -> date | None:
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValueError(f"{label} must be an ISO YYYY-MM-DD string or null")
    try:
        result = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must use YYYY-MM-DD: {value!r}") from exc
    if result.isoformat() != value:
        raise ValueError(f"{label} must use YYYY-MM-DD: {value!r}")
    return result


def plain(value: Any) -> str:
    if value is None or value == "":
        return "—"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def escaped(value: Any) -> str:
    """Keep imported spreadsheet strings as visible data, not HTML or links."""
    text = html.escape(plain(value), quote=False)
    return re.sub(r"([\\`*_{}\[\]()#!|>])", r"\\\1", text)


def cell(value: Any) -> str:
    return escaped(value).replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def url_link(label: str, url: Any) -> str:
    if not isinstance(url, str) or not url:
        return escaped(label)
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return escaped(label) + " (URL needs review)"
    return f"[{escaped(label)}](<{quote(url, safe=':/?&=#%+@,;~!$-_.')}>)"


def local_link(label: str, raw_path: Any, page: Path) -> str | None:
    """Link only existing paths inside the repository, without assuming files exist."""
    if not isinstance(raw_path, str) or not raw_path:
        return None
    path = Path(raw_path)
    if path.is_absolute() or ".." in path.parts:
        return None
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT) or not resolved.exists():
        return None
    relative = os.path.relpath(resolved, page.parent)
    return f"[{escaped(label)}](<{quote(relative, safe='/.-_')}>)"


def table(headers: list[str], rows: list[list[str]]) -> list[str]:
    return ["| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
            *("| " + " | ".join(row) + " |" for row in rows)]


def load_tracker(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        tracker = json.load(handle)
    if not isinstance(tracker, dict):
        raise ValueError("Tracker JSON must contain an object")
    if str(tracker.get("schema_version")) != "1.0":
        raise ValueError("Supported tracker schema_version is 1.0")
    if parse_date(tracker.get("updated_on"), "updated_on") is None:
        raise ValueError("Tracker updated_on is required")
    for collection in ("jobs", "companies"):
        records = tracker.get(collection)
        if not isinstance(records, list):
            raise ValueError(f"{collection} must be an array")
        ids: set[str] = set()
        for record in records:
            if not isinstance(record, dict):
                raise ValueError(f"Every {collection} record must be an object")
            record_id = record.get("id")
            if not isinstance(record_id, str) or not ID_PATTERN.fullmatch(record_id):
                raise ValueError(f"Invalid {collection} ID: {record_id!r}")
            if record_id in ids:
                raise ValueError(f"Duplicate {collection} ID: {record_id}")
            ids.add(record_id)
            if collection == "jobs":
                for field in SCHEDULE_DATES:
                    parse_date(record.get(field), f"{record_id}.{field}")
                for field, _ in PREPARATION:
                    if not isinstance(record.get(field), bool):
                        raise ValueError(f"{record_id}.{field} must be true or false")
    settings = tracker.get("settings", {})
    if not isinstance(settings, dict):
        raise ValueError("settings must be an object")
    for key, default in (("contact_followup_days", 5), ("application_followup_days", 14),
                         ("lookahead_days", 7), ("fit1_decision_days", 3)):
        value = settings.get(key, default)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"settings.{key} must be a nonnegative integer")
    if settings.get("contact_followup_unit", "calendar") not in {"calendar", "business"}:
        raise ValueError("settings.contact_followup_unit must be calendar or business")
    offsets = settings.get("planning_offsets", {})
    if not isinstance(offsets, dict):
        raise ValueError("settings.planning_offsets must be an object")
    for key, value in offsets.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"settings.planning_offsets.{key} must be a nonnegative integer")
    return tracker


def add_days(start: date, count: int, unit: str = "calendar") -> date:
    if unit == "calendar":
        return start + timedelta(days=count)
    result = start
    while count:
        result += timedelta(days=1)
        if result.weekday() < 5:
            count -= 1
    return result


def preparation(job: dict[str, Any]) -> str:
    completed = sum(job[field] for field, _ in PREPARATION)
    labels = [f"{'✓' if job[field] else '○'} {label}" for field, label in PREPARATION]
    return f"{completed}/3 · " + " · ".join(labels)


def missing_details(job: dict[str, Any]) -> list[str]:
    notes = []
    if job.get("status") in {"Applied", "Interviewing", "Offer", "Accepted"} and not job.get("applied_on"):
        notes.append("Application recorded, but applied date is unknown")
    if job.get("networking") not in {None, "Not started"}:
        if not job.get("contact"):
            notes.append("Networking recorded, but contact is unknown")
        if not job.get("last_contact"):
            notes.append("Networking recorded, but last-contact date is unknown; follow-up cannot be dated")
    if job.get("status") == "Interviewing" and not job.get("interview_on"):
        notes.append("Interviewing recorded; next interview date is unknown")
    if not job.get("bank_bullet_ids"):
        notes.append("Imported fit/proof analysis needs review against the factual bank")
    for key, label in (("packet_path", "Application folder"), ("resume_path", "Resume PDF"),
                       ("letters_path", "Outreach drafts")):
        raw = job.get(key)
        if raw and local_link(label, raw, ROOT / "tracker" / "README.md") is None:
            notes.append(f"{label} path is recorded but is missing or needs review")
    return notes


def schedule(job: dict[str, Any], settings: dict[str, Any]) -> list[dict[str, Any]]:
    """Derive recommendations from known dates, without recording any action."""
    if job.get("status") in TERMINAL:
        return []
    items: list[dict[str, Any]] = []
    job_id = job["id"]

    def add(when: date | None, label: str, kind: str) -> None:
        if when:
            items.append({"date": when, "label": label, "kind": kind, "job": job})

    applied = parse_date(job.get("applied_on"), f"{job_id}.applied_on")
    target = parse_date(job.get("apply_by") or job.get("deadline"), f"{job_id}.target")
    if job.get("status") in {"Saved", "Unknown", None} and not applied and target:
        offsets = settings.get("planning_offsets", {})
        steps = (("research", "research_done", "Research the role"),
                 ("proof", "proof_done", "Prepare relevant proof / demo"),
                 ("resume", "resume_done", "Tailor and review the resume"))
        for key, field, label in steps:
            if not job[field]:
                add(target - timedelta(days=offsets.get(key, {"research": 10, "proof": 4, "resume": 2}[key])),
                    label + " (suggested prep date)", "Preparation")
        if job.get("networking") in {None, "Not started"}:
            add(target - timedelta(days=offsets.get("networking", 9)),
                "Consider relevant outreach; do not delay applying", "Preparation")
        add(target, "Apply by target" if job.get("apply_by") else "Application deadline", "Application")
    if applied and job.get("status") == "Applied":
        add(add_days(applied, settings.get("application_followup_days", 14)),
            "Consider application follow-up if appropriate; check for replies first", "Follow-up")
    contact = parse_date(job.get("last_contact"), f"{job_id}.last_contact")
    if contact and job.get("networking") in {"Reached out", "Referral asked"}:
        add(add_days(contact, settings.get("contact_followup_days", 5),
                     settings.get("contact_followup_unit", "calendar")),
            "Review the actual thread before considering an outreach follow-up", "Follow-up")
    interview = parse_date(job.get("interview_on"), f"{job_id}.interview_on")
    if job.get("status") not in {"Offer", "Accepted"}:
        add(interview, "Interview (recorded date; completion is not inferred)", "Interview")
    return items


def timing(when: date, as_of: date) -> str:
    delta = (when - as_of).days
    if delta < 0:
        return f"{abs(delta)} day(s) past scheduled date"
    if delta == 0:
        return "Today in this snapshot"
    return f"In {delta} day(s)"


def job_link(job: dict[str, Any], prefix: str = "jobs/") -> str:
    return f"[{escaped(job['id'])}](<{prefix}{job['id']}.md>)"


def render_dashboard(tracker: dict[str, Any], as_of: date, output: Path) -> str:
    jobs = tracker["jobs"]
    settings = tracker.get("settings", {})
    counts: dict[str, int] = {}
    for job in jobs:
        status = job.get("status") or "Unknown"
        counts[status] = counts.get(status, 0) + 1
    lines = ["# Job search tracker", "",
             f"**Snapshot as of {as_of.isoformat()} · {escaped(settings.get('timezone', 'Timezone not supplied'))}.** "
             f"Source last updated {escaped(tracker['updated_on'])}.", "",
             "This is a static GitHub view. Dates and due items change only when the tracker is rendered again; "
             "opening this page does not refresh them.", "",
             "Tell the AI: **“Prepare R001”**, **“I applied to R001 on YYYY-MM-DD”**, or "
             "**“I sent the R001 outreach message on YYYY-MM-DD.”** It can update the tracker and linked materials "
             "as work progresses. Preparation never records an application or a sent message.", "",
             f"**{len(jobs)} jobs · {len(tracker['companies'])} companies.** "
             + " · ".join(f"{escaped(status)}: {count}" for status, count in sorted(counts.items())), "",
             "[Company watchlist](companies.md) · [Spreadsheet-style job table](jobs.csv) · "
             "[How to update](HOW-TO-UPDATE.md) · "
             "[Candidate evidence bank](../bank/experience-bank.md)", "",
             "## Due items and upcoming dates", "",
             "These are reminders to review, not records of applications or messages being sent. "
             "Preparation targets are suggestions; do not postpone a required application to finish outreach. "
             "Past dates do not prove an interview or task happened.", ""]
    horizon = as_of + timedelta(days=settings.get("lookahead_days", 7))
    items = []
    for job in jobs:
        scheduled = schedule(job, settings)
        # The dashboard shows the next pending prep step; detail pages retain
        # the full schedule so one job does not crowd out all the others.
        preparation_items = [item for item in scheduled if item["kind"] == "Preparation"]
        if preparation_items:
            items.append(min(preparation_items, key=lambda item: (item["date"], item["label"])))
        items.extend(item for item in scheduled if item["kind"] != "Preparation")
    items = [item for item in items if item["date"] <= horizon]
    items.sort(key=lambda item: (item["date"], item["job"]["id"], item["label"]))
    if items:
        lines.extend(table(["Date", "Timing", "Job", "Type", "Next review"], [
            [item["date"].isoformat(), cell(timing(item["date"], as_of)),
             job_link(item["job"]), cell(item["kind"]), cell(item["label"])] for item in items]))
    else:
        lines.append(f"No recorded or derived dates fall on or before {horizon.isoformat()} for active jobs.")
    lines.extend(["", "## Applications", "",
                  "Research, proof, and resume completion come from their own checkboxes. "
                  "Applying never marks unfinished preparation complete. Networking has its own state.", ""])
    rows = []
    for job in jobs:
        page = output / "README.md"
        links = [link for label, key in (("Packet", "packet_path"), ("Resume", "resume_path"),
                                         ("Letters", "letters_path"))
                 if (link := local_link(label, job.get(key), page))]
        rows.append([job_link(job), cell(job.get("company")), cell(job.get("role")),
                     cell(job.get("status")), cell(job.get("priority")), cell(job.get("fit")),
                     cell(preparation(job)), cell(job.get("networking")),
                     cell(job.get("applied_on")), cell(job.get("apply_by") or job.get("deadline")),
                     " · ".join(links) if links else "—"])
    lines.extend(table(["ID", "Company", "Role", "Application", "Priority", "Fit", "Preparation", "Networking",
                        "Applied", "Apply target / deadline", "Materials"], rows))
    warnings = [(job, note) for job in jobs for note in missing_details(job)]
    lines.extend(["", "## Details to confirm", ""])
    if warnings:
        lines.extend(f"- {job_link(job)}: {escaped(note)}." for job, note in warnings)
    else:
        lines.append("No missing details were detected by the basic tracker checks.")
    lines.extend(["", "## Scheduling policy", "",
                  f"- Contact follow-up: {settings.get('contact_followup_days', 5)} "
                  f"{escaped(settings.get('contact_followup_unit', 'calendar'))} days after a recorded last-contact date; "
                  "review the thread and recipient circumstances before drafting.",
                  f"- Application follow-up: {settings.get('application_followup_days', 14)} calendar days after "
                  "the recorded applied date while the application remains Applied.",
                  f"- Upcoming window: {settings.get('lookahead_days', 7)} calendar days after this snapshot date.",
                  "- Unknown dates stay unknown. Reminders do not create sent, submitted, or completed events.", "",
                  "For maintainers: edit [tracker.json](tracker.json), then run "
                  "`python3 scripts/render_tracker.py --as-of YYYY-MM-DD` from the repository root.", ""])
    return "\n".join(lines)


def section(lines: list[str], title: str, value: Any) -> None:
    lines.extend([f"## {title}", ""])
    if value is None or value == "" or value == []:
        lines.extend(["Not recorded.", ""])
    elif isinstance(value, list):
        lines.extend(f"- {escaped(item)}" for item in value)
        lines.append("")
    else:
        lines.extend(escaped(value).replace("\r\n", "\n").split("\n"))
        lines.append("")


def render_job(job: dict[str, Any], tracker: dict[str, Any], as_of: date, output: Path) -> str:
    page = output / "jobs" / f"{job['id']}.md"
    lines = [f"# {escaped(job['id'])} · {escaped(job.get('company'))} · {escaped(job.get('role'))}", "",
             "[Back to tracker](../README.md) · [Candidate evidence bank](../../bank/experience-bank.md)", "",
             f"Snapshot: **{as_of.isoformat()}**. Record updated: {escaped(job.get('updated_on'))}.", "",
             f"**Application:** {escaped(job.get('status'))} · **Networking:** {escaped(job.get('networking'))}", "",
             f"**Preparation:** {escaped(preparation(job))}", ""]
    if job.get("job_link"):
        lines.extend([url_link("Job posting", job["job_link"]), ""])
    materials = [link for label, key in (("Application folder", "packet_path"), ("Resume PDF", "resume_path"),
                                         ("Outreach drafts", "letters_path"))
                 if (link := local_link(label, job.get(key), page))]
    lines.extend(["**Materials:** " + (" · ".join(materials) if materials else "No linked application materials yet."), ""])
    fields = (("priority", "Priority"), ("fit", "Fit rating (imported judgment)"),
              ("apply_by", "Target application date"), ("deadline", "Posting deadline"),
              ("applied_on", "Applied on"), ("interview_on", "Interview on (completion not inferred)"),
              ("contact", "Contact"), ("last_contact", "Last contact"), ("location", "Location"),
              ("work_mode", "Work mode"), ("job_type", "Employment type"), ("team", "Team"),
              ("pay", "Pay (posting / imported text)"), ("start_date", "Start date / timing"),
              ("posted_on", "Posted on"), ("req_id", "Requisition ID"), ("added_on", "Added on"),
              ("source_id", "Source ID"))
    lines.extend(table(["Field", "Recorded value"], [[label, cell(job.get(key))] for key, label in fields]))
    lines.extend(["", "## Scheduling recommendations", ""])
    items = sorted(schedule(job, tracker.get("settings", {})), key=lambda item: (item["date"], item["label"]))
    if items:
        lines.extend(table(["Date", "Timing", "Review"], [[item["date"].isoformat(),
                           cell(timing(item["date"], as_of)), cell(item["label"])] for item in items]))
        lines.append("")
    else:
        lines.extend(["No date-based reminders can be derived for the current state.", ""])
    section(lines, "Details to confirm", missing_details(job))
    for key, title in (("about_role", "About the role"), ("must_haves", "Must-haves"),
                       ("nice_to_haves", "Nice-to-haves"), ("keywords", "Keywords"),
                       ("interview_process", "Interview process")):
        section(lines, title, job.get(key))
    section(lines, "Selected bank bullet IDs", job.get("bank_bullet_ids"))
    section(lines, "Review notes", job.get("review_notes"))
    lines.extend(["## Imported analysis — verify before using", "",
                  "The following cells preserve the workbook's original analysis. They are historical planning "
                  "notes, not verified candidate accomplishments. Check claims against the current factual bank "
                  "and review notes before reusing them in a resume or letter.", ""])
    for key, title in (("strongest_proof", "Imported strongest proof"), ("gaps", "Imported gaps"),
                       ("prep_plan", "Imported preparation plan"), ("ai_notes", "Imported AI notes")):
        lines.extend([f"### {title}", "", escaped(job.get(key)).replace("\r\n", "\n"), ""])
    section(lines, "Activity log (recorded text)", job.get("log"))
    lines.extend(["## Confirmed events", "",
                  "Only recorded events are shown. A draft or generated file is never proof of sending or applying.", ""])
    events = job.get("events") or []
    if not events:
        lines.extend(["No structured events recorded. Existing imported status, dates, and log remain visible above.", ""])
    else:
        for event in events:
            if isinstance(event, dict):
                lines.append("- " + "; ".join(f"**{escaped(key)}:** {escaped(value)}" for key, value in event.items()))
            else:
                lines.append(f"- {escaped(event)}")
        lines.append("")
    return "\n".join(lines)


def render_companies(tracker: dict[str, Any], as_of: date) -> str:
    lines = ["# Company watchlist", "", "[Back to tracker](README.md)", "",
             f"Snapshot as of **{as_of.isoformat()}**. Imported company information may be outdated; "
             "verify current roles and dates before applying.", ""]
    rows = []
    for company in tracker["companies"]:
        rows.append([cell(company["id"]), cell(company.get("name")), cell(company.get("priority")),
                     cell(company.get("industry")), url_link("Careers", company.get("careers_page"))
                     if company.get("careers_page") else "—"])
    lines.extend(table(["ID", "Company", "Priority", "Industry", "Careers"], rows))
    lines.append("")
    for company in tracker["companies"]:
        lines.extend([f"## {escaped(company['id'])} · {escaped(company.get('name'))}", ""])
        rows = []
        for key, value in company.items():
            if key in {"id", "name"}:
                continue
            label = key.replace("_", " ").capitalize()
            rendered = url_link(str(value), value) if key in {"careers_page", "job_board"} and value else cell(value)
            rows.append([label, rendered])
        lines.extend(table(["Field", "Imported value"], rows))
        lines.append("")
    return "\n".join(lines)


def csv_safe(value: Any) -> str:
    if value is None:
        return ""
    text = json.dumps(value, ensure_ascii=False, sort_keys=True) if isinstance(value, (dict, list)) else str(value)
    # CSV quoting alone does not prevent spreadsheet formula execution.
    stripped = text.lstrip()
    if stripped.startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r", "\n")):
        text = "'" + text
    return text


def render_csv(tracker: dict[str, Any]) -> str:
    fields = list(dict.fromkeys(key for job in tracker["jobs"] for key in job))
    if not fields:
        fields = ["id", "company", "role", "status"]
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(fields)
    for job in tracker["jobs"]:
        writer.writerow([csv_safe(job.get(field)) for field in fields])
    return output.getvalue()


def render_files(tracker: dict[str, Any], as_of: date, output: Path) -> dict[Path, str]:
    files = {output / "README.md": render_dashboard(tracker, as_of, output),
             output / "companies.md": render_companies(tracker, as_of),
             output / "jobs.csv": render_csv(tracker)}
    files.update({output / "jobs" / f"{job['id']}.md": render_job(job, tracker, as_of, output)
                  for job in tracker["jobs"]})
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tracker", type=Path, default=DEFAULT_TRACKER, help="Canonical tracker JSON")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "tracker", help="Generated view directory")
    parser.add_argument("--as-of", help="Static snapshot date YYYY-MM-DD; defaults to tracker.updated_on")
    parser.add_argument("--check", action="store_true", help="Check generated views without writing")
    args = parser.parse_args(argv)
    try:
        tracker = load_tracker(args.tracker)
        as_of = parse_date(args.as_of or tracker["updated_on"], "--as-of")
        assert as_of is not None
        files = render_files(tracker, as_of, args.output_dir.resolve())
        outdated = []
        for path, content in files.items():
            if args.check:
                if not path.is_file() or path.read_text(encoding="utf-8") != content:
                    outdated.append(str(path))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="")
        if outdated:
            print("Tracker views are missing or outdated:\n" + "\n".join(outdated), file=sys.stderr)
            return 1
        print(f"{'Checked' if args.check else 'Rendered'} {len(files)} tracker views "
              f"({len(tracker['jobs'])} jobs, {len(tracker['companies'])} companies), as of {as_of}.")
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"Tracker render failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
