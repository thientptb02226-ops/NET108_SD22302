# CLAUDE.md — Claude Code Guidelines

Welcome to the **Trello Clone Multi-Agent Monorepo**. This file guides Claude Code CLI when executing tasks in this repository.

---

## 1. Primary Operating Scope

- **Primary Focus**: Frontend Web (`Trello-Clone-Frontend`), Chatbot Assistant (`Chatbot-Frontend`), Mobile (`Trello-Clone-Mobile`), and Desktop (`Trello-Clone-Desktop`).
- **Secondary / Collaborative**: You may modify `Trello-Clone-Backend` or `Trello-Clone-MCP` when required for end-to-end feature delivery, following the contracts defined in `docs/api/`.

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

## 4. Multi-Agent Coexistence Policies

- Read `AGENTS.md` before making any root-level structural changes.
- Refer to `.claude/policies/` for concurrency handling and safety rules.
- Refer to `.claude/rules/` for detailed coding standards.
- Do not modify `.codex/` or `.agent/` folders.
