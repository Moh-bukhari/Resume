#!/usr/bin/env python3
"""Render the resume bank's Markdown and CSV views from its canonical JSON.

Run from any directory. No dependencies beyond Python's standard library.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path
from typing import Any


DEFAULT_BANK_DIR = Path(__file__).resolve().parents[1] / "bank"
CSV_FIELDS = (
    "id", "experience", "title", "dates", "text", "tags", "status",
    "scope_note", "sources",
)


def load_bank(bank_dir: Path) -> dict[str, Any]:
    with (bank_dir / "experience-bank.json").open(encoding="utf-8") as handle:
        bank = json.load(handle)
    if not isinstance(bank, dict):
        raise ValueError("The bank JSON must contain an object.")
    return bank


def label(key: str) -> str:
    return key.replace("_", " ").capitalize()


def scalar(value: Any) -> str:
    if value is None:
        return "Not supplied"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return str(value)


def cell(value: Any) -> str:
    """Keep text containing pipes or line breaks inside a Markdown table cell."""
    return scalar(value).replace("|", "\\|").replace("\r\n", "\n").replace("\n", "<br>")


def detail_lines(value: Any, indent: int = 0) -> list[str]:
    """Render arbitrary structured metadata without dropping unfamiliar fields."""
    pad = " " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}- **{label(key)}:**")
                lines.extend(detail_lines(item, indent + 2))
            else:
                text = scalar(item).replace("\n", "\n" + pad + "  ")
                lines.append(f"{pad}- **{label(key)}:** {text}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.extend(detail_lines(item, indent + 2))
            else:
                text = scalar(item).replace("\n", "\n" + pad + "  ")
                lines.append(f"{pad}- {text}")
    else:
        lines.append(pad + scalar(value))
    return lines


def render_markdown(bank: dict[str, Any]) -> str:
    experiences = bank["experiences"]
    bullets = bank["bullets"]
    profile = bank["profile"]
    lines = [
        f"# {profile['name']} — master experience bank", "",
        f"Updated: {bank['updated_client_date']} (client date).", "",
        f"Schema: {bank['schema_version']}.", "",
        f"{len(experiences)} experience/project entries; {len(bullets)} selectable bullet options; "
        f"{len(bank['metrics'])} numeric facts; {len(bank['awards'])} awards.", "",
        "This is a complete source library, not a resume to submit. Later explicit corrections "
        "take precedence over older drafts.", "",
        "Generated from [experience-bank.json](experience-bank.json). Edit the JSON, then run "
        "`python3 scripts/render_bank.py` from the repository root; do not edit this generated view directly.", "",
        "## Profile and education", "",
    ]
    lines.extend(detail_lines(profile))
    lines.extend([
        "", "## How to read the bank", "",
        "`ready` means grounded in the user's supplied experience, with code corroboration where cited; "
        "it does not mean independent employment verification. `implementation_in_progress` means work "
        "has begun without implying completed rollout. `planned_only` is not a completed achievement. "
        "`needs_detail` records projects that need concrete capability or implementation descriptions. "
        "Read each bullet's scope and source references before using it. IDs remain stable even when a "
        "project is split into separate entries; a bullet ID prefix need not match its experience ID.", "",
        "## All experience and project bullets", "",
    ])
    exp_core = {
        "id", "name", "kind", "title", "dates", "location", "context",
        "ownership", "best_for", "sources", "url",
    }
    bullet_core = {"id", "experience_id", "text", "tags", "status", "scope_note", "sources"}
    for experience in experiences:
        lines.extend([
            f"### {experience['name']} ({experience['id']})", "",
            f"**{experience['title']} | {experience['dates']} | {experience['location']}**", "",
            experience["context"], "",
            f"**Ownership:** {experience['ownership']}", "",
            f"**Useful for:** {', '.join(experience['best_for'])}.", "",
            f"**Kind:** {experience['kind']}. **Sources:** {', '.join(experience['sources'])}.", "",
        ])
        if experience.get("url"):
            lines.extend([f"**Link:** {experience['url']}", ""])
        metadata = {key: value for key, value in experience.items() if key not in exp_core}
        if metadata:
            lines.extend(["**Additional scope and implementation details:**", ""])
            lines.extend(detail_lines(metadata))
            lines.append("")
        for bullet in bullets:
            if bullet["experience_id"] != experience["id"]:
                continue
            lines.append(f"- **{bullet['id']} [{bullet['status']}]:** {bullet['text']}")
            if bullet["scope_note"]:
                lines.append(f"  Scope: {bullet['scope_note']}")
            lines.append(f"  Tags: {', '.join(bullet['tags'])}. Sources: {', '.join(bullet['sources'])}.")
            extras = {key: value for key, value in bullet.items() if key not in bullet_core}
            lines.extend(detail_lines(extras, 2))
        lines.append("")

    lines.extend([
        "## Numeric facts and attribution", "",
        "| ID | Value | Meaning | Status | Limit |",
        "| --- | --- | --- | --- | --- |",
    ])
    metric_keys = ("id", "value", "meaning", "status", "avoid")
    for metric in bank["metrics"]:
        lines.append("| " + " | ".join(cell(metric[key]) for key in metric_keys) + " |")
        extras = {key: value for key, value in metric.items() if key not in metric_keys}
        if extras:
            lines.extend(["", f"Additional details for **{metric['id']}**:", ""])
            lines.extend(detail_lines(extras))
            lines.append("")

    lines.extend(["", "## Awards", ""])
    for award in bank["awards"]:
        lines.extend(detail_lines(award))
        lines.append("")
    lines.extend(["## Skills", ""])
    lines.extend(detail_lines(bank["skills"]))
    lines.extend(["", "## Coursework", ""])
    lines.extend(detail_lines(bank["coursework"]))
    lines.extend([
        "", "No certifications, professional licenses, additional leadership roles, or volunteer "
        "positions have been supplied yet. This does not mean none exist.", "",
        "## Summary options", "",
    ])
    for summary in bank["summaries"]:
        lines.extend([f"### {summary['id']} — {summary['role_family']}", "", summary["text"], ""])
        lines.extend(detail_lines({key: value for key, value in summary.items()
                                   if key not in {"id", "role_family", "text"}}))

    lines.extend([
        "## Choosing evidence for a job", "",
        "| Role family | Start with | Add if relevant | Guidance |",
        "| --- | --- | --- | --- |",
    ])
    for role in bank["role_maps"]:
        values = [role["family"], ", ".join(role["primary"]), ", ".join(role["secondary"]), role["note"]]
        lines.append("| " + " | ".join(cell(value) for value in values) + " |")
        extras = {key: value for key, value in role.items()
                  if key not in {"family", "primary", "secondary", "note"}}
        if extras:
            lines.extend(["", f"Additional guidance for **{role['family']}**:", ""])
            lines.extend(detail_lines(extras))
    lines.extend(["", "## Tailoring rules", ""])
    lines.extend(f"{number}. {rule}" for number, rule in enumerate(bank["tailoring_rules"], 1))
    lines.extend(["", "## Clarifications already recorded", ""])
    lines.extend(detail_lines(bank["answered_clarifications"]))
    lines.extend([
        "", "## Details that would strengthen future versions", "",
        "These are questions, not implied facts. Partial answers and unknowns are fine. "
        "The current bank can already be used.", "",
    ])
    for question in bank["questions"]:
        lines.append(f"- **{question['id']} — {question['topic']} ({question['priority']}):** {question['question']}")
        lines.extend(detail_lines({key: value for key, value in question.items()
                                   if key not in {"id", "topic", "priority", "question"}}, 2))
    lines.extend(["", "## Sources and provenance", ""])
    for source in bank["sources"]:
        lines.extend([f"### {source['id']}", "", source["description"], ""])
        source_metadata = {key: value for key, value in source.items()
                           if key not in {"id", "description"}}
        # Source local_path entries are relative to the repository root;
        # the generated document lives in bank/. Existing study links are
        # already relative to bank/, so keep their original base.
        for key in ("local_path", "path", "study"):
            if key in source_metadata:
                relative = str(source_metadata[key])
                target = relative if key == "study" else "../" + relative
                source_metadata[key] = f"[{relative}](<{target}>)"
        lines.extend(detail_lines(source_metadata))
        lines.append("")
    lines.extend(["## Submission status", "", bank["submission_status"], ""])

    known = {
        "schema_version", "updated_client_date", "profile", "sources", "experiences", "bullets",
        "metrics", "awards", "skills", "coursework", "summaries", "role_maps", "questions",
        "answered_clarifications", "tailoring_rules", "submission_status",
    }
    extra = {key: value for key, value in bank.items() if key not in known}
    if extra:
        lines.extend(["## Additional research and metadata", ""])
        lines.extend(detail_lines(extra))
        lines.append("")
    lines.extend([
        "## Reuse in the next application", "",
        "> Tailor a one-page resume for this job using only supported facts from this bank. "
        "Select the most relevant bullet IDs, preserve titles/dates/metric scope, and keep planned "
        "work distinct from completed outcomes. Keep Tamara first unless I ask otherwise. "
        "Do not add tools, industries, customer deployments, conversion rates, or seniority just "
        "because the job asks for them. Provide the complete Overleaf-ready LaTeX document with "
        "pdfLaTeX, plus a brief note about any important missing evidence.", "",
        "The JSON is the canonical source. The CSV has one selectable bullet per row. "
        "Existing resume files are prior drafts, not evidence of submitted applications.", "",
    ])
    return "\n".join(lines)


def render_csv(bank: dict[str, Any]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    experiences = {experience["id"]: experience for experience in bank["experiences"]}
    for bullet in bank["bullets"]:
        experience = experiences[bullet["experience_id"]]
        writer.writerow({
            "id": bullet["id"], "experience": experience["name"], "title": experience["title"],
            "dates": experience["dates"], "text": bullet["text"], "tags": "; ".join(bullet["tags"]),
            "status": bullet["status"], "scope_note": bullet["scope_note"],
            "sources": "; ".join(bullet["sources"]),
        })
    return stream.getvalue()


def generated_files(bank: dict[str, Any]) -> dict[str, bytes]:
    return {
        "experience-bank.md": render_markdown(bank).encode("utf-8"),
        "bullet-bank.csv": render_csv(bank).encode("utf-8-sig"),
    }


def stale_files(bank_dir: Path, bank: dict[str, Any]) -> list[str]:
    return [name for name, expected in generated_files(bank).items()
            if not (bank_dir / name).is_file() or (bank_dir / name).read_bytes() != expected]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank-dir", type=Path, default=DEFAULT_BANK_DIR,
                        help="Directory containing experience-bank.json (default: repository bank/).")
    parser.add_argument("--check", action="store_true", help="Report stale views without writing files.")
    args = parser.parse_args()
    try:
        bank = load_bank(args.bank_dir)
        if args.check:
            stale = stale_files(args.bank_dir, bank)
            if stale:
                parser.exit(1, "Stale or missing generated views: " + ", ".join(stale) +
                            ". Run scripts/render_bank.py with the same --bank-dir.\n")
            print("Generated bank views are up to date.")
        else:
            for name, content in generated_files(bank).items():
                (args.bank_dir / name).write_bytes(content)
                print(f"Rendered {name}")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Cannot render bank: {error}. Run scripts/check_bank.py to validate the source.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
