# Review Command (/review)

When invoked, Claude should:
1. Run `git diff` or inspect uncommitted changes in the working directory.
2. Check for:
   - TypeScript compile-time errors or missing types.
   - Any violation of separation of concerns (e.g. backend logic written in frontend components).
   - Hardcoded API URLs or secrets.
   - Missing unit tests for newly introduced logic.
3. Output a structured code review summary with actionable suggestions.
