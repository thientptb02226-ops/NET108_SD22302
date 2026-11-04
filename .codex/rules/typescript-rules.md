# TypeScript & Node.js Rules for Codex

1. **Strict Types**: Always provide return types for service functions and controllers.
2. **Error Handling**: Use custom HTTP exception classes (e.g., `BadRequestException`, `NotFoundException`, `UnauthorizedException`) caught by a global error handling middleware.
3. **Database Access**: Encapsulate database queries in dedicated service or repository classes. Never write raw SQL directly in controllers.
4. **Validation**: Use class-validator or Zod schemas to validate all request bodies before hitting business logic.

