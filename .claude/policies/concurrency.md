# Multi-Agent Concurrency Policy

1. **Non-Interference Rule**:
   - Claude must not modify files inside `.codex/` or `.agent/`.
   - Claude must avoid writing to `Trello-Clone-Backend` when another agent (e.g. Antigravity/Codex) is actively generating backend endpoints, unless following a mutually agreed interface contract in `docs/api/`.

2. **Atomic Modification**:
   - Make edits to targeted functions or files. Avoid bulk search-and-replace that could wipe out concurrent edits by other agents.
   - Always verify current file contents on disk before applying modifications.

3. **Status Reporting**:
   - Record significant task completions in the active plan file or git commit log.

