# AGENTS.md — Multi-Agent Workspace Orchestration Protocol

> **Role & Purpose**: This document is the master coordination specification for AI Agents (including **Antigravity**, **Claude Code CLI**, **OpenAI Codex**, and **Cursor**) operating concurrently within this monorepo repository.

---

## 1. System Overview

This repository is a full-stack, enterprise-grade, multi-platform **Trello Clone** augmented with AI capabilities (MCP Server, RAG Pipeline, and Chatbot).

### Workspace Architecture
```
trello-clone/
├── .agent/                  # Antigravity agent configuration, rules, workflows
├── .claude/                 # Claude Code CLI configuration (commands, skills, policies)
├── .codex/                  # OpenAI Codex configuration & agent templates
├── certs/                   # SSL/TLS and local dev certificates
├── Chatbot-Frontend/        # Embeddable AI Assistant widget (React + Vite)
├── docs/                    # System documentation, architecture diagrams, API specs
├── Trello-Clone-AI-RAG/     # Semantic search & contextual RAG service (FastAPI / LangChain)
├── Trello-Clone-Backend/    # Core REST / WebSocket API (Node.js / Express / Prisma)
├── Trello-Clone-Desktop/    # Desktop client (Electron / Tauri)
├── Trello-Clone-Frontend/   # Web application (Next.js / React Kanban UI)
├── Trello-Clone-Infra/      # Docker Compose, Kubernetes, CI/CD pipelines
├── Trello-Clone-MCP/        # Model Context Protocol server exposing board operations to AI
├── Trello-Clone-Mobile/     # Mobile client (React Native / Expo)
├── AGENTS.md                # Multi-agent coordination agreement (THIS FILE)
├── CLAUDE.md                # Claude Code specific execution guide
└── mcp-reference-architecture.md # MCP integration architecture
```

---

## 2. Multi-Agent Concurrency & Ownership Rules

When two or more AI agents run concurrently via CLI (e.g. `claude` in Terminal 1, `agy` or `codex` in Terminal 2):

### 2.1 Domain Allocation (Separation of Concerns)
To avoid merge conflicts and file thrashing, agents should operate primarily on designated domains:
* **Agent 1 (Frontend & Experience Focus - e.g., Claude Code)**:
  * Primary: `Trello-Clone-Frontend/`, `Chatbot-Frontend/`, `Trello-Clone-Mobile/`, `Trello-Clone-Desktop/`
* **Agent 2 (Backend, Core & RAG Focus - e.g., Antigravity / Codex)**:
  * Primary: `Trello-Clone-Backend/`, `Trello-Clone-AI-RAG/`, `Trello-Clone-MCP/`, `Trello-Clone-Infra/`
* **Shared Territory**: `docs/`, `certs/`, root configuration (`package.json`, `docker-compose.yml`).
  * *Rule for Shared Territory*: Always read before write. Use atomic edits. Never overwrite whole configuration files without inspecting previous commits.

### 2.2 File Locking & Coordination Protocol
1. **Pre-edit Verification**: Always check `git status` or inspect the target file to ensure another agent has not introduced intermediate changes.
2. **Commit Atomicity**: Commit logically self-contained units with descriptive prefixes:
   - `[agent:claude] feat(frontend): ...`
   - `[agent:anti] feat(backend): ...`
   - `[agent:codex] fix(rag): ...`
3. **Do Not Overwrite Agent Configurations**:
   - Agent Claude must not alter `.agent/` or `.codex/` unless explicitly instructed.
   - Antigravity / Codex must not alter `.claude/` unless explicitly instructed.
   - Both must adhere to `AGENTS.md`.

---

## 3. Technology Stack & Standard Commands

| Module | Stack | Dev Command | Build / Test |
| :--- | :--- | :--- | :--- |
| **Backend** | Node.js, Express, TypeScript, Prisma, PostgreSQL, Redis | `npm run dev` (in `Trello-Clone-Backend`) | `npm run build` / `npm test` |
| **Frontend** | React 19, Vite / Next.js, TailwindCSS, Zustand, DnD Kit | `npm run dev` (in `Trello-Clone-Frontend`) | `npm run build` / `npm test` |
| **MCP Server** | TypeScript, @modelcontextprotocol/sdk | `npm run build && npm start` (in `Trello-Clone-MCP`) | `npm test` |
| **AI-RAG** | Python 3.11+, FastAPI, LangChain, ChromaDB / pgvector | `uvicorn app.main:app --reload` | `pytest` |
| **Chatbot Frontend** | React, TailwindCSS, Vite | `npm run dev` (in `Chatbot-Frontend`) | `npm run build` |
| **Mobile** | React Native, Expo | `npx expo start` | `npm test` |
| **Desktop** | Electron / Tauri, React | `npm run dev` | `npm run build` |
| **Infra** | Docker Compose, Postgres, Redis, MinIO | `docker compose up -d` (in root or `Trello-Clone-Infra`) | - |

---

## 4. MCP (Model Context Protocol) Integration

This repo exposes an internal MCP server at `Trello-Clone-MCP`. AI agents can use this MCP server to:
1. `list_boards`: Query active user boards.
2. `get_board_data`: Fetch lists, cards, labels, and activity history.
3. `create_card`: Create tasks autonomously based on developer discussions.
4. `move_card`: Update status (e.g., In Progress -> Code Review -> Done).
5. `rag_search_tasks`: Query historical cards and documentation semantically.

Refer to `mcp-reference-architecture.md` for tool schemas and connection parameters.

---

## 5. Agent Workflow Guidelines

1. **Check Requirements**: Always review `docs/` and task plans in `.claude/plans/` or `.codex/plans/` before beginning code generation.
2. **Type Safety**: Maintain strict TypeScript interfaces between Backend and Frontend. Never use `any` where explicit domain types exist.
3. **Environment Variables**: Always define defaults in `.env.example` in each sub-project. Never commit plain `.env` with secret keys.
4. **Testing**: When adding a feature, provide unit or integration tests in the corresponding submodule.
