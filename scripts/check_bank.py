#!/usr/bin/env python3
"""Validate resume bank facts, references, and deterministic generated views."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path, PureWindowsPath
from typing import Any

from render_bank import DEFAULT_BANK_DIR, load_bank, stale_files


def validate_bank(bank: dict[str, Any], bank_dir: Path) -> list[str]:
    errors: list[str] = []

    def require(record: Any, fields: tuple[str, ...], where: str) -> bool:
        if not isinstance(record, dict):
            errors.append(f"{where} must be an object")
            return False
        missing = [key for key in fields if key not in record]
        if missing:
            errors.append(f"{where} is missing: {', '.join(missing)}")
        return not missing

    required = (
        "schema_version", "updated_client_date", "profile", "sources", "experiences", "bullets",
        "metrics", "awards", "skills", "coursework", "summaries", "role_maps", "questions",
        "answered_clarifications", "tailoring_rules", "submission_status",
    )
    if not require(bank, required, "bank"):
        return errors
    try:
        date.fromisoformat(bank["updated_client_date"])
    except (ValueError, TypeError):
        errors.append("updated_client_date must be an ISO date (YYYY-MM-DD)")
    for key in ("schema_version", "submission_status"):
        if not isinstance(bank[key], str) or not bank[key].strip():
            errors.append(f"{key} must be a nonempty string")
    if not require(bank["profile"], ("name", "phone", "email", "linkedin", "website", "education",
                                   "languages", "availability", "location_preferences", "work_authorization"), "profile"):
        return errors
    require(bank["profile"]["education"], ("institution", "degree", "dates", "graduation", "gpa", "location"),
            "profile.education")
    for key in ("skills", "coursework"):
        if not isinstance(bank[key], dict):
            errors.append(f"{key} must be an object")
    list_keys = ("sources", "experiences", "bullets", "metrics", "awards", "summaries", "role_maps",
                 "questions", "answered_clarifications", "tailoring_rules")
    for key in list_keys:
        if not isinstance(bank[key], list):
            errors.append(f"{key} must be a list")
    if errors:
        return errors

    record_fields = {
        "sources": ("id", "description"),
        "experiences": ("id", "name", "kind", "title", "dates", "location", "context", "ownership", "best_for", "sources"),
        "bullets": ("id", "experience_id", "text", "tags", "sources", "status", "scope_note"),
        "metrics": ("id", "value", "meaning", "status", "avoid"),
        "awards": ("project", "award", "date", "amount", "source"),
        "summaries": ("id", "role_family", "text"),
        "role_maps": ("family", "primary", "secondary", "note"),
        "questions": ("id", "priority", "topic", "question"),
    }
    all_ids: dict[str, str] = {}
    section_ids: dict[str, set[str]] = {}
    for section, fields in record_fields.items():
        section_ids[section] = set()
        for index, record in enumerate(bank[section]):
            where = f"{section}[{index}]"
            if not require(record, fields, where):
                continue
            if "id" in fields:
                identifier = record["id"]
                if not isinstance(identifier, str) or not identifier.strip():
                    errors.append(f"{where}.id must be a nonempty string")
                    continue
                if identifier in all_ids:
                    errors.append(f"Duplicate ID {identifier}: {all_ids[identifier]} and {where}")
                all_ids[identifier] = where
                section_ids[section].add(identifier)
            for key in fields:
                value = record[key]
                if key == "amount" and value is None:
                    continue
                if key in {"tags", "sources", "best_for", "primary", "secondary"}:
                    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                        errors.append(f"{where}.{key} must be a list of strings")
                    elif len(value) != len(set(value)):
                        errors.append(f"{where}.{key} contains duplicate entries")
                elif not isinstance(value, str):
                    errors.append(f"{where}.{key} must be a string")
                elif not value.strip() and key != "scope_note":
                    errors.append(f"{where}.{key} must not be empty")
    if errors:
        return errors

    def check_metadata(value: Any, where: str) -> None:
        if isinstance(value, list):
            for index, item in enumerate(value):
                check_metadata(item, f"{where}[{index}]")
        elif isinstance(value, dict):
            for key, item in value.items():
                location = f"{where}.{key}"
                if key == "source":
                    if not isinstance(item, str) or item not in section_ids["sources"]:
                        errors.append(f"{location} references unknown source {item!r}")
                elif key == "sources" and where != "bank":
                    if not isinstance(item, list) or not all(isinstance(ref, str) for ref in item):
                        errors.append(f"{location} must contain source IDs")
                    else:
                        unknown = set(item) - section_ids["sources"]
                        if unknown:
                            errors.append(f"{location} references unknown sources: {', '.join(sorted(unknown))}")
                elif key == "experience_id":
                    if not isinstance(item, str) or item not in section_ids["experiences"]:
                        errors.append(f"{location} references unknown experience {item!r}")
                elif key in {"local_path", "study", "path"} and isinstance(item, str):
                    if Path(item).is_absolute() or PureWindowsPath(item).is_absolute():
                        errors.append(f"{location} must use a portable relative path, not {item!r}")
                    # local_path/path are repository-root-relative; legacy study
                    # links are relative to the bank/ document that contains them.
                    elif not ((bank_dir if key == "study" else bank_dir.parent) / item).is_file():
                        errors.append(f"{location} points to a missing local file: {item}")
                check_metadata(item, location)

    check_metadata(bank, "bank")
    for index, role in enumerate(bank["role_maps"]):
        for key in ("primary", "secondary"):
            unknown = set(role[key]) - section_ids["bullets"]
            if unknown:
                errors.append(f"role_maps[{index}].{key} references unknown bullets: {', '.join(sorted(unknown))}")
    for index, experience in enumerate(bank["experiences"]):
        if experience["kind"] not in {"experience", "project"}:
            errors.append(f"experiences[{index}].kind must be experience or project")
        if not experience["sources"]:
            errors.append(f"experiences[{index}] needs at least one source")
    valid_statuses = {"ready", "planned_only", "needs_detail", "implementation_in_progress", "use_scoped_wording"}
    for index, bullet in enumerate(bank["bullets"]):
        if bullet["status"] not in valid_statuses:
            errors.append(f"bullets[{index}].status is unrecognized: {bullet['status']}")
        if not bullet["sources"]:
            errors.append(f"bullets[{index}] needs at least one source")
    for section in ("answered_clarifications", "tailoring_rules"):
        if not all(isinstance(item, str) and item.strip() for item in bank[section]):
            errors.append(f"{section} must contain nonempty strings")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank-dir", type=Path, default=DEFAULT_BANK_DIR,
                        help="Directory containing experience-bank.json (default: repository bank/).")
    parser.add_argument("--source-only", action="store_true",
                        help="Validate JSON without checking generated views (useful before rendering edits).")
    args = parser.parse_args()
    try:
        bank = load_bank(args.bank_dir)
        errors = validate_bank(bank, args.bank_dir)
        if not errors and not args.source_only:
            stale = stale_files(args.bank_dir, bank)
            if stale:
                errors.append("Stale or missing generated views: " + ", ".join(stale) +
                              "; run scripts/render_bank.py with the same --bank-dir")
        if errors:
            parser.exit(1, "Bank validation failed:\n- " + "\n- ".join(errors) + "\n")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Cannot validate bank: {error}\n")
    print(f"Bank valid: {len(bank['experiences'])} entries, {len(bank['bullets'])} bullets, "
          f"{len(bank['metrics'])} numeric facts; " +
          ("source only." if args.source_only else "Markdown and CSV are synchronized."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
