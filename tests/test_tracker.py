"""Functional checks for tracker evidence, reminders, and application packets.

All mutations use disposable tracker copies and output folders. The repository's
tracker, applications, and imported workbook are only read as source fixtures.
Run with: python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import render_tracker  # noqa: E402
from check_contacts import validate_contacts  # noqa: E402


class TrackerWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="resume-tracker-test-")
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.path = self.folder / "tracker.json"
        self.source_path = ROOT / "tracker" / "tracker.json"
        self.source_bytes = self.source_path.read_bytes()
        self.fixture = json.loads(self.source_bytes)
        # Even if a future production tracker links packets, test updates must
        # never reach refresh_packet_context() with those production paths.
        self.data = deepcopy(self.fixture)
        for job in self.data["jobs"]:
            for key in ("packet_path", "resume_path", "letters_path"):
                job[key] = None
        self.write_data()
        self.addCleanup(self.assert_source_unchanged)

    def assert_source_unchanged(self) -> None:
        self.assertEqual(self.source_path.read_bytes(), self.source_bytes)

    def write_data(self) -> None:
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")

    def read_data(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def job(self, identifier: str = "R001") -> dict:
        return next(job for job in self.read_data()["jobs"] if job["id"] == identifier)

    def cli(self, script: str, *arguments: str, expected: int = 0) -> subprocess.CompletedProcess:
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / script), *arguments],
                                cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, expected,
                         f"Command failed: {script} {arguments!r}\n{result.stdout}\n{result.stderr}")
        return result

    def tracker(self, *arguments: str, expected: int = 0) -> subprocess.CompletedProcess:
        return self.cli("tracker.py", "--tracker", str(self.path), *arguments, expected=expected)

    def event(self, kind: str, *, occurred: str | None = None,
              extra: tuple[str, ...] = (), expected: int = 0) -> subprocess.CompletedProcess:
        arguments = ["event", "R001", "--type", kind, "--on", "2026-10-15",
                     "--confirmed-by", "user", "--note", "User-confirmed test event."]
        if occurred is not None:
            arguments += ["--event-date", occurred]
        return self.tracker(*arguments, *extra, expected=expected)

    def render(self, *, check: bool = False, expected: int = 0) -> subprocess.CompletedProcess:
        arguments = ["--tracker", str(self.path), "--output-dir", str(self.folder),
                     "--as-of", "2026-10-15"]
        if check:
            arguments.append("--check")
        return self.cli("render_tracker.py", *arguments, expected=expected)

    def snapshot(self) -> dict[str, bytes]:
        return {path.relative_to(self.folder).as_posix(): path.read_bytes()
                for path in self.folder.rglob("*") if path.is_file()}

    def prepare(self, identifier: str, *, expected: int = 0) -> subprocess.CompletedProcess:
        return self.cli("new_application.py", "--tracker", str(self.path),
                        "--tracker-id", identifier, "--date", "2026-10-15",
                        "--output-root", str(self.folder / "packets"), expected=expected)

    def packet(self, identifier: str) -> Path:
        matches = list((self.folder / "packets").glob(identifier.lower() + "-*"))
        self.assertEqual(len(matches), 1)
        return matches[0]

    def test_import_preserves_ids_company_watchlist_and_unknown_outreach(self) -> None:
        self.assertEqual(len(self.fixture["jobs"]), 10)
        self.assertEqual(len(self.fixture["companies"]), 41)
        self.assertEqual([job["id"] for job in self.fixture["jobs"]],
                         [f"R{number:03d}" for number in range(1, 11)])
        source = next(item for item in self.fixture["sources"]
                      if item["id"] == "XLSX-2026-10-15")
        self.assertEqual(hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest(),
                         source["sha256"])
        mercor = self.job("R010")
        self.assertEqual((mercor["status"], mercor["applied_on"]),
                         ("Applied", "2026-10-14"))
        self.assertIsNone(mercor["contact"])
        self.assertIsNone(mercor["last_contact"])
        self.assertFalse(any(event["type"] == "sent" for event in mercor["events"]))
        self.assertFalse(mercor["proof_done"])
        self.assertTrue(any("against the factual bank" in note
                            for note in render_tracker.missing_details(self.job())))
        self.render()
        dashboard = (self.folder / "README.md").read_text(encoding="utf-8")
        self.assertIn("10 jobs · 41 companies", dashboard)
        self.assertIn("contact is unknown", dashboard)

    def test_sent_reply_and_backfilled_message_preserve_latest_conversation(self) -> None:
        self.event("sent", occurred="2026-10-10", extra=("--contact", "Current Recipient"))
        self.event("reply", occurred="2026-10-14")
        self.event("sent", occurred="2026-10-11", extra=("--contact", "Historical Recipient"))
        job = self.job()
        self.assertEqual((job["networking"], job["last_contact"], job["contact"]),
                         ("Talked", "2026-10-14", "Current Recipient"))
        self.assertTrue(job["events"][-1]["history_only"])
        self.assertEqual(len({event["id"] for event in job["events"]}), len(job["events"]))
        self.assertFalse(any(item["kind"] == "Follow-up"
                             for item in render_tracker.schedule(job, self.data["settings"])))

    def test_undated_sent_message_cannot_reuse_old_followup_date(self) -> None:
        self.event("sent", occurred="2026-10-10")
        self.assertTrue(any(item["kind"] == "Follow-up"
                            for item in render_tracker.schedule(self.job(), self.data["settings"])))
        self.event("sent")
        job = self.job()
        self.assertEqual(job["networking"], "Reached out")
        self.assertIsNone(job["last_contact"])
        self.assertIsNone(job["events"][-1]["occurred_on"])
        self.assertFalse(any(item["kind"] == "Follow-up"
                             for item in render_tracker.schedule(job, self.data["settings"])))
        self.assertTrue(any("last-contact date is unknown" in note
                            for note in render_tracker.missing_details(job)))

    def test_future_interview_is_scheduled_not_completed_and_unknown_reschedule_is_undated(self) -> None:
        self.event("interview_scheduled", occurred="2026-10-20")
        self.assertEqual(self.job()["interview_on"], "2026-10-20")
        self.assertFalse(any(event["type"] == "interview" for event in self.job()["events"]))
        before = self.snapshot()
        self.event("interview", occurred="2026-10-20", expected=1)
        self.assertEqual(self.snapshot(), before)
        self.prepare("R001")
        record = json.loads((self.packet("R001") / "contacts.json").read_text(encoding="utf-8"))
        self.assertEqual(record["application_stage"], "unknown")
        self.assertIsNone(record["interview_date"])
        self.event("interview_scheduled")
        self.assertIsNone(self.job()["interview_on"])
        self.assertFalse(any(item["kind"] == "Interview"
                             for item in render_tracker.schedule(self.job(), self.data["settings"])))

    def test_completed_events_require_confirmation_and_cannot_be_future_dated(self) -> None:
        before = self.snapshot()
        result = self.tracker("event", "R001", "--type", "sent", "--on", "2026-10-15",
                              "--note", "Missing confirmation.", expected=2)
        self.assertIn("--confirmed-by", result.stderr)
        self.tracker("update", "R001", "--set", "status=Applied", "--on", "2026-10-15",
                     "--note", "Unsupported status transition.", expected=1)
        self.event("application", occurred="2026-10-16", expected=1)
        self.assertEqual(self.snapshot(), before)

    def test_invalid_update_does_not_change_source_or_generated_views(self) -> None:
        self.render()
        before = self.snapshot()
        for assignment in ("fit=6", "bank_bullet_ids=[\"NOT-A-BANK-ID\"]",
                           "resume_path=../outside.pdf", "deadline=2026-02-30"):
            with self.subTest(assignment=assignment):
                self.tracker("update", "R001", "--set", assignment, "--on", "2026-10-15",
                             "--note", "Invalid proposal must remain unapplied.", expected=1)
                self.assertEqual(self.snapshot(), before)

    def test_dry_run_shows_proposal_without_touching_any_files(self) -> None:
        self.render()
        before = self.snapshot()
        result = self.tracker("--dry-run", "event", "R001", "--type", "application",
                              "--event-date", "2026-10-15", "--on", "2026-10-15",
                              "--confirmed-by", "user", "--note", "A confirmed test application.")
        proposed = json.loads(result.stdout.split("\nDry run:", 1)[0])
        self.assertEqual(proposed["status"], "Applied")
        self.assertEqual(proposed["applied_on"], "2026-10-15")
        self.assertEqual(self.job()["status"], "Saved")
        self.assertEqual(self.snapshot(), before)

    def test_external_packets_keep_known_stage_dates_templates_and_refuse_overwrite(self) -> None:
        tracker_before = self.path.read_bytes()
        for identifier, stage, applied_on in (("R001", "before_application", None),
                                               ("R010", "after_application", "2026-10-14")):
            with self.subTest(identifier=identifier):
                self.prepare(identifier)
                packet = self.packet(identifier)
                contacts = json.loads((packet / "contacts.json").read_text(encoding="utf-8"))
                self.assertEqual(contacts["application_stage"], stage)
                self.assertEqual(contacts["application_date"], applied_on)
                self.assertIsNone(contacts["interview_date"])
                self.assertEqual(contacts["outreach_events"], [])
                self.assertEqual(validate_contacts(contacts)[0], [])
                letters = list((packet / "letters").glob("*.md"))
                self.assertEqual(len(letters), 8)
                resume = (packet / "resume.tex").read_text(encoding="utf-8")
                self.assertIn("\\documentclass", resume)
                self.assertIn("\\end{document}", resume)
                description = (packet / "job-description.md").read_text(encoding="utf-8")
                self.assertIn("full posting pending", description)
                before = self.snapshot()
                result = self.prepare(identifier, expected=1)
                self.assertIn("refusing to overwrite", result.stderr)
                self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.path.read_bytes(), tracker_before)

    def test_history_preserves_offer_and_packet_uses_latest_completed_interview(self) -> None:
        self.event("interview", occurred="2026-10-14")
        self.event("offer", occurred="2026-10-15")
        self.event("interview", occurred="2026-10-10")
        self.assertEqual(self.job()["status"], "Offer")
        self.assertTrue(self.job()["events"][-1]["history_only"])
        self.prepare("R001")
        contacts = json.loads((self.packet("R001") / "contacts.json").read_text(encoding="utf-8"))
        self.assertEqual(contacts["application_stage"], "interview_completed")
        self.assertEqual(contacts["interview_date"], "2026-10-14")
        self.assertIsNone(contacts["application_date"])

    def test_generated_check_detects_stale_view_then_passes_after_render(self) -> None:
        self.render()
        self.render(check=True)
        dashboard = self.folder / "README.md"
        dashboard.write_text("Outdated dashboard.\n", encoding="utf-8")
        before = self.snapshot()
        result = self.render(check=True, expected=1)
        self.assertIn("missing or outdated", result.stderr)
        self.assertEqual(self.snapshot(), before)
        self.render()
        self.render(check=True)

    def test_add_assigns_new_ids_without_marking_an_application_or_outreach(self) -> None:
        existing_ids = [job["id"] for job in self.read_data()["jobs"]]
        self.tracker("add", "--company", "Example Test Company", "--role", "Growth Associate",
                     "--url", "https://example.com/jobs/growth", "--on", "2026-10-15",
                     "--note", "User supplied a target, not an application.")
        current = self.read_data()
        self.assertEqual([job["id"] for job in current["jobs"][:-1]], existing_ids)
        added = current["jobs"][-1]
        self.assertEqual((added["id"], added["status"], added["networking"]),
                         ("R011", "Saved", "Not started"))
        self.assertIsNone(added["applied_on"])
        self.assertIsNone(added["last_contact"])
        self.assertFalse(any(event["type"] in {"application", "sent"} for event in added["events"]))
        self.assertEqual(len(current["companies"]), 42)


if __name__ == "__main__":
    unittest.main()
