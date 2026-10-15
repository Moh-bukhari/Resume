# Application system — Claude entry point

Read [START-HERE.md](START-HERE.md), then [AGENTS.md](AGENTS.md). They route
to the same shared Markdown instructions used by every AI assistant. Follow
[docs/WORKFLOWS.md](docs/WORKFLOWS.md) and read [docs/HANDOFF.md](docs/HANDOFF.md)
before continuing unfinished work.

Candidate facts live in `bank/experience-bank.json`; application state and
events live in `tracker/tracker.json`. Update the correct master, regenerate
views, check, and publish supported changes. Draft creation does not record
an application or a sent message. Preserve stable job IDs and actual evidence.
Do not keep separate Claude-only facts or operating rules.
