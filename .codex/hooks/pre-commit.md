# Codex Pre-Commit Hook

Verify before commit:
1. `npm test` or backend unit tests pass.
2. Commit message uses prefix: `[agent:codex] <type>(<scope>): <summary>`.
3. No `.env` credentials or secrets are staged.
