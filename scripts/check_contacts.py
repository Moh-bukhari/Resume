#!/usr/bin/env python3
"""Validate local contact evidence and outreach records; never verify or send online."""

from __future__ import annotations

import argparse
from datetime import date, datetime
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlsplit


STAGES = {"unknown", "before_application", "after_application", "interview_completed"}


def is_date(value: Any, timestamp: bool = False) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        if date.fromisoformat(value).isoformat() == value:
            return True
    except ValueError:
        pass
    if timestamp and "T" in value:
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return True
        except ValueError:
            pass
    return False


def is_url(value: Any) -> bool:
    if not isinstance(value, str) or any(character.isspace() for character in value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme in {"http", "https"} and bool(parsed.hostname) and not parsed.username and not parsed.password
    except ValueError:
        return False


def validate_contacts(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    def required(record: Any, keys: tuple[str, ...], where: str) -> bool:
        if not isinstance(record, dict):
            errors.append(f"{where} must be an object")
            return False
        missing = [key for key in keys if key not in record]
        if missing:
            errors.append(f"{where} missing: {', '.join(missing)}")
        return not missing

    def text(value: Any, where: str, allow_blank: bool = False) -> bool:
        if not isinstance(value, str) or (not value.strip() and not allow_blank):
            errors.append(f"{where} must be {'a string' if allow_blank else 'a nonempty string'}")
            return False
        return True

    def evidence_sources(value: Any, where: str) -> bool:
        if not isinstance(value, list):
            errors.append(f"{where} must be a list")
            return False
        for index, source in enumerate(value):
            location = f"{where}[{index}]"
            if not required(source, ("url", "accessed_date", "supporting_detail"), location):
                continue
            offline_evidence = source.get("source_type") in {
                "user_provided", "confirmed_thread", "provider_result",
            }
            if not is_url(source["url"]) and not (source["url"] is None and offline_evidence):
                errors.append(f"{location}.url must be an HTTP(S) source URL, or null with an explicit "
                              "user_provided/confirmed_thread/provider_result source_type")
            if source["accessed_date"] is not None and not is_date(source["accessed_date"]):
                errors.append(f"{location}.accessed_date must be YYYY-MM-DD or null when unknown")
            text(source["supporting_detail"], location + ".supporting_detail")
        return bool(value)

    root_keys = ("schema_version", "company", "role", "application_stage", "application_date",
                 "interview_date", "research_status", "contacts", "outreach_events")
    if not required(data, root_keys, "contacts file"):
        return errors, warnings
    if data["schema_version"] != "1.0":
        errors.append("Unsupported schema_version; expected 1.0")
    for key in ("company", "role"):
        text(data[key], key, allow_blank=True)  # Blank starter templates are valid.
    text(data["research_status"], "research_status")
    if not isinstance(data["application_stage"], str) or data["application_stage"] not in STAGES:
        errors.append("application_stage must be unknown, before_application, after_application, or interview_completed")
    for key in ("created_on", "application_date", "interview_date"):
        if key in data and data[key] is not None and not is_date(data[key]):
            errors.append(f"{key} must be YYYY-MM-DD or null when unknown")
    for key in ("contacts", "outreach_events"):
        if not isinstance(data[key], list):
            errors.append(f"{key} must be a list")
    if errors:
        return errors, warnings

    identifiers: set[str] = set()
    contact_keys = (
        "id", "name", "employer", "title", "linkedin_url", "professional_email", "identity_sources",
        "relevance_reason", "hiring_connection_status", "email_source_type", "email_sources", "verification",
        "preferred_channel",
    )
    for index, contact in enumerate(data["contacts"]):
        where = f"contacts[{index}]"
        if not required(contact, contact_keys, where):
            continue
        for key in ("id", "name", "employer", "title", "relevance_reason"):
            text(contact[key], where + "." + key)
        identifier = contact["id"]
        if isinstance(identifier, str):
            if identifier in identifiers:
                errors.append(f"Duplicate contact ID: {identifier}")
            identifiers.add(identifier)
        linkedin = contact["linkedin_url"]
        if linkedin is not None:
            if not is_url(linkedin):
                errors.append(f"{where}.linkedin_url must be a LinkedIn HTTP(S) profile URL or null")
            else:
                hostname = urlsplit(linkedin).hostname or ""
                if hostname != "linkedin.com" and not hostname.endswith(".linkedin.com"):
                    errors.append(f"{where}.linkedin_url must use linkedin.com")
                elif not re.match(r"^/(?:in|pub)/[^/]+", urlsplit(linkedin).path):
                    errors.append(f"{where}.linkedin_url must identify a person, not a company/search page")
        email = contact["professional_email"]
        if email is not None and (not isinstance(email, str) or not re.fullmatch(r"[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+", email)):
            errors.append(f"{where}.professional_email must be a plain email address or null")
        has_identity = evidence_sources(contact["identity_sources"], where + ".identity_sources")
        has_email = evidence_sources(contact["email_sources"], where + ".email_sources")
        connection = contact["hiring_connection_status"]
        if not isinstance(connection, str) or connection not in {"confirmed", "likely", "unknown"}:
            errors.append(f"{where}.hiring_connection_status must be confirmed, likely, or unknown")
        elif connection == "confirmed" and not has_identity:
            errors.append(f"{where}: confirmed hiring connection requires identity/source evidence")
        source_type = contact["email_source_type"]
        if not isinstance(source_type, str) or source_type not in {
            "published", "provider_returned", "user_provided", "inferred", "unknown",
        }:
            errors.append(f"{where}.email_source_type must be published, provider_returned, user_provided, inferred, or unknown")
        elif source_type in {"published", "provider_returned", "user_provided"} and not has_email:
            errors.append(f"{where}: {source_type} email claim requires email source evidence")
        elif source_type in {"published", "provider_returned", "user_provided"} and email is None:
            errors.append(f"{where}: {source_type} email claim has no professional_email")
        elif source_type == "inferred" and email:
            warnings.append(f"{where}: inferred address is unconfirmed; do not treat it as a verified recipient")
        elif source_type == "unknown" and email:
            warnings.append(f"{where}: address origin is unknown; do not treat it as a verified recipient")
        verification = contact["verification"]
        if required(verification, ("provider", "result", "checked_at", "limitations"), where + ".verification"):
            provider = verification["provider"]
            if provider is not None:
                text(provider, where + ".verification.provider")
            result = verification["result"]
            text(result, where + ".verification.result")
            text(verification["limitations"], where + ".verification.limitations", allow_blank=True)
            if verification["checked_at"] is not None and not is_date(verification["checked_at"], timestamp=True):
                errors.append(f"{where}.verification.checked_at must be an ISO date/timestamp or null")
            checked = isinstance(result, str) and result not in {"not_checked", "unknown"}
            if checked and (not provider or not has_email):
                errors.append(f"{where}: verification results require a named provider and email source evidence")
            if source_type == "inferred" and checked:
                warnings.append(f"{where}: checking an inferred address does not establish ownership or identity; "
                                "preserve its inferred origin and the provider's actual limitations")
        channel = contact["preferred_channel"]
        if not isinstance(channel, str) or channel not in {"email", "linkedin", "official_channel", "unknown"}:
            errors.append(f"{where}.preferred_channel must be email, linkedin, official_channel, or unknown")
        elif channel == "email" and not email:
            errors.append(f"{where}: preferred email channel has no professional_email")
        elif channel == "linkedin" and not linkedin:
            errors.append(f"{where}: preferred LinkedIn channel has no linkedin_url")

    event_keys = ("event_type", "occurred_at", "recipient_id", "confirmed_by", "evidence_note")
    for index, event in enumerate(data["outreach_events"]):
        where = f"outreach_events[{index}]"
        if not required(event, event_keys, where):
            continue
        event_type = event["event_type"]
        if not isinstance(event_type, str) or event_type not in {"draft", "sent", "reply", "interview", "application"}:
            errors.append(f"{where}.event_type must be draft, sent, reply, interview, or application")
        confirmer = event["confirmed_by"]
        if not isinstance(confirmer, str) or confirmer not in {"user", "tool_result", "none"}:
            errors.append(f"{where}.confirmed_by must be user, tool_result, or none")
        occurred = event["occurred_at"]
        if occurred is not None and not is_date(occurred, timestamp=True):
            errors.append(f"{where}.occurred_at must be an ISO date/timestamp or null when unknown")
        recipient = event["recipient_id"]
        if recipient is not None and (not isinstance(recipient, str) or recipient not in identifiers):
            errors.append(f"{where}.recipient_id references an unknown contact")
        note_valid = text(event["evidence_note"], where + ".evidence_note", allow_blank=event_type == "draft")
        if event_type in ("sent", "reply", "interview", "application"):
            if confirmer not in ("user", "tool_result"):
                errors.append(f"{where}: completed events require user or tool_result confirmation")
            if note_valid and not event["evidence_note"].strip():
                errors.append(f"{where}: completed events require an evidence_note")
            if occurred is None:
                warnings.append(f"{where}: event date is unknown; preserved as null rather than inferred")
    if data["application_stage"] == "before_application":
        if data["application_date"] is not None or data["interview_date"] is not None:
            errors.append("before_application conflicts with a recorded application/interview date")
        if any(isinstance(event, dict) and event.get("event_type") in {"application", "interview"}
               for event in data["outreach_events"]):
            errors.append("before_application conflicts with a recorded application/interview event")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to an application contacts.json file.")
    args = parser.parse_args()
    try:
        with args.path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        errors, warnings = validate_contacts(data)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Cannot read contacts: {error}\n")
    for warning in warnings:
        print("Note: " + warning)
    if errors:
        parser.exit(1, "Contact validation failed:\n- " + "\n- ".join(errors) + "\n")
    print(f"Contact records valid: {len(data['contacts'])} contacts, {len(data['outreach_events'])} events. "
          "This checks recorded evidence structure, not live identity, deliverability, or permission to send.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
