# Pre-Commit Hook

Before performing `git commit`, the Claude agent must verify:
1. `npm run lint` or syntax checks pass without blocking errors.
2. No temporary debug logging (e.g. `console.log`, `print`) is committed in production paths.
3. Commit message adheres to the agent convention: `[agent:claude] <type>(<scope>): <summary>`.
