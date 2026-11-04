# Refactor Command (/refactor)

When refactoring code:
1. Ensure unit tests are in place before touching production methods.
2. Maintain backwards compatibility with API contracts consumed by frontend clients.
3. Keep database migrations non-destructive (e.g. use additive column migrations rather than dropping columns).

