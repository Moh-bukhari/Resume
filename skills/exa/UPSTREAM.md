# Exa upstream skill

- Publisher: Exa Labs.
- Repository: <https://github.com/exa-labs/exa-mcp-server>.
- Pinned commit: `e9c3b0126a3373eb1aeaca162e84d0791ff4c7f7`.
- Source: [skills/search](https://github.com/exa-labs/exa-mcp-server/tree/e9c3b0126a3373eb1aeaca162e84d0791ff4c7f7/skills/search).
- Local entry: [search/SKILL.md](search/SKILL.md).
- License: [MIT](LICENSE), copyright Exa Labs 2025.
- Retrieved and reviewed: 2026-10-15.

The twelve files under `search/` are unchanged upstream sources: one skill and
eleven reference documents. The root upstream license is preserved here.

The specialist people-search guidance is in
[patterns-people.md](search/references/patterns-people.md). It covers searches by
role, employer, and location, LinkedIn-weighted discovery, supplementary company
pages, and deduplication. Search results still need identity and current-role
checks. This skill is not an email deliverability service.

The upstream instructions require connected Exa `web_search_exa` and
`web_fetch_exa` tools. Exa supports OAuth or API-key access and describes
rate-limited anonymous access. Availability, quotas, and any charges depend on
the connected service and account. Copying these files does not install or
authenticate Exa, run searches, or establish that the tool names are available
in a future host. Follow the current host's tools and higher-priority repository
instructions when upstream examples use another agent's invocation syntax.

No executable code is included in this skill. Its Markdown contains an
illustrative `[text](url)` link in `references/synthesis.md`; `url` is example
syntax, not a missing bundled resource. No live Exa runs were performed to
validate this snapshot.
