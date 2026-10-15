# Apify community upstream skill

- Author: [Daniela Ryplová](https://github.com/danielarypl).
- Publisher: Apify's community skill catalog; this is community authored.
- Repository: <https://github.com/apify/awesome-skills>.
- Pinned commit: `1eb0cd0c12e35a0d0a17c23f0f462d7062fd5813`.
- Source: [skills/apify-verified-email-finder](https://github.com/apify/awesome-skills/tree/1eb0cd0c12e35a0d0a17c23f0f462d7062fd5813/skills/apify-verified-email-finder).
- Local entry: [apify-verified-email-finder/SKILL.md](apify-verified-email-finder/SKILL.md).
- License: [Apache License 2.0](LICENSE), copied from the upstream repository root.
- Retrieved and reviewed: 2026-10-15.

All nine files under `apify-verified-email-finder/` are unchanged upstream
sources, including the optional JavaScript helper and its `package.json`.

The skill routes company URLs or discovery inputs to Apify Actors, selects
department contacts, requires email verification, records provenance, and
distinguishes verified, catch-all, invalid, and unresolved results. Its
wrong-company hostname check addresses a documented enrichment mismatch.
Provider-reported email verification does not independently prove current
employment or hiring responsibility.

Execution requires either an authenticated Apify MCP connection or the optional
script path with Node.js 20.6+ and `APIFY_TOKEN`. Actor runs and enrichment may
consume paid credits. Credentials, integrations, and runtimes have not been
installed or configured by copying this skill. Keep tokens and bulk raw provider
exports out of the repository; retain only relevant contact evidence in an
application record. Upstream `${CLAUDE_PLUGIN_ROOT}` command examples
depend on the host's installed layout; they are not evidence that a plugin is
installed here.

The optional `reference/scripts/run_actor.js` was read statically, not executed.
Its requests target `api.apify.com`; it sends the account token in the query
string, submits the supplied Actor input, polls status, downloads dataset
records, and optionally writes an output file. It also sets an Apify usage
analytics User-Agent. No unrelated external destination or embedded credential
was identified in that static read. Avoid capturing authenticated request URLs
in logs. An elapsed polling timeout does not abort the remote run, so spending
may continue remotely. The helper has not been runtime-tested here; its CSV
export truncates long scalar strings and its summary function uses `require`
inside an ES module with a catch fallback. Preserve the upstream sources and
review execution behavior before using the helper.

No Actor, lookup, verification, package installation, or third-party helper was
run to validate this snapshot.
