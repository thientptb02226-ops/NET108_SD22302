# CLAUDE.md — Claude Code Guidelines

Welcome to the **Trello Clone Multi-Agent Monorepo**. This file guides Claude Code CLI when executing tasks in this repository.

---

## 1. Primary Operating Scope & Agent Personas

This workspace implements the standard **6-Step Agentic Loop** (from Code Web Không Khó - Agent Hub):
`Plan` ➔ `Design` ➔ `Build` ➔ `Test` ➔ `Deploy` ➔ `Maintain`

Available Agent Personas in `.claude/agents/`:
- `project-manager`: Planning, user stories, roadmap tracking (`docs/03-san-pham/roadmap.md`).
- `ui-ux-designer`: Wireframes, responsive layouts, TailwindCSS, accessibility.
- `software-engineer`: Clean code, TypeScript, API implementations.
- `qa-test-engineer`: Unit tests, edge case verification, integration tests.
- `devops-engineer`: Docker, CI/CD pipelines, release rollback mechanisms.
- `sre-ops-engineer`: Monitoring, structured logging, incident triaging.

- **Primary Focus**: Frontend Web (`Trello-Clone-Frontend`), Chatbot Assistant (`Chatbot-Frontend`), Mobile (`Trello-Clone-Mobile`), and Desktop (`Trello-Clone-Desktop`).
- **Secondary / Collaborative**: You may modify `Trello-Clone-Backend` or `Trello-Clone-MCP` when required for end-to-end feature delivery, following the contracts defined in `docs/02-ky-thuat/`.

---

## 2. Directory Navigation & Key Commands

### Web Frontend (`Trello-Clone-Frontend`)
```bash
cd Trello-Clone-Frontend
npm install
npm run dev        # Starts Vite dev server (default port 3000)
npm run build      # Production bundle
npm run test       # Run Vitest test suites
npm run lint       # Run ESLint check
```

### Chatbot UI (`Chatbot-Frontend`)
```bash
cd Chatbot-Frontend
npm install
npm run dev        # Starts Chatbot widget dev server (port 3001)
npm run build
```

### Backend (`Trello-Clone-Backend`)
```bash
cd Trello-Clone-Backend
npm install
npm run dev        # Starts Express/TypeScript API with nodemon (port 5000)
npx prisma migrate dev
```

### MCP Server (`Trello-Clone-MCP`)
```bash
cd Trello-Clone-MCP
npm install
npm run build
npm start
```

---

## 3. Code Style & Architecture Rules

1. **Architecture Style**:
   - Modern React with Functional Components and custom hooks.
   - Global state: Zustand (`useBoardStore`, `useAuthStore`, `useChatStore`).
   - Drag and Drop: `@dnd-kit/core` & `@dnd-kit/sortable`.
   - Styling: TailwindCSS with utility-first classes, semantic color variables.
2. **TypeScript**:
   - Strict mode enabled (`noImplicitAny: true`).
   - Shared domain entities (Card, List, Board, User, Comment, Label) defined in `src/types/`.
3. **API Communication**:
   - Axios or native fetch wrapped in `src/services/apiClient.ts`.
   - All async calls must handle loading and error states cleanly.
4. **Git Commit Convention**:
   - Always prefix your commits with `[agent:claude]` so other agents and developers know the origin of the commit:
     - `git commit -m "[agent:claude] feat(ui): implement card drag-and-drop animations"`

---

## 4. Karpathy Behavioral Guidelines (MANDATORY)

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) (via `multica-ai/andrej-karpathy-skills`).

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

### 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports/variables/functions that YOUR changes made unused.

### 4. Goal-Driven Execution
**Define success criteria. Loop until verified.**
- Transform tasks into verifiable goals:
  - "Add validation" ➔ "Write tests for invalid inputs, then make them pass"
  - "Fix the bug" ➔ "Write a test that reproduces it, then make it pass"
- For multi-step tasks, state a brief plan:
  ```
  1. [Step] ➔ verify: [check]
  2. [Step] ➔ verify: [check]
  3. [Step] ➔ verify: [check]
  ```
- Detailed anti-patterns & examples: [karpathy-examples.md](file:///c:/Net108Khai/docs/01-tong-quan/karpathy-examples.md)

---

## 5. Multi-Agent Coexistence Policies

- Read `AGENTS.md` before making any root-level structural changes.
- Refer to `.claude/policies/` for concurrency handling and safety rules.
- Refer to `.claude/rules/` for detailed coding standards.
- Do not modify `.codex/` or `.agent/` folders.

