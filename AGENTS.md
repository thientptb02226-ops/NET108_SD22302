# AGENTS.md — Multi-Agent Workspace Orchestration Protocol

> **Role & Purpose**: This document is the master coordination specification for AI Agents (including **Antigravity**, **Claude Code CLI**, **OpenAI Codex**, and **Cursor**) operating concurrently within this monorepo repository.

---

## 1. System Overview

This repository is an enterprise-grade **AI-Native Commerce Platform** designed for FPT Polytechnic NET108 (.NET Project 1), featuring:
- C# ASP.NET Core Web API Backend (.NET 10/8, Entity Framework Core)
- React 18 + Vite + TailwindCSS Frontend Storefront & Admin Portal
- Python FastAPI AI Microservice (NLP Semantic Search & HITL Agent)
- 15-Minute Quote Lock Fingerprinting & Idempotency Saga Checkout

### Workspace Architecture
```
NET108_SD22302/
├── .agent/                  # Antigravity agent configuration, rules, workflows
├── .claude/                 # Claude Code CLI configuration (commands, skills, policies)
├── .codex/                  # OpenAI Codex configuration & agent templates
├── docs/                    # System documentation, architecture diagrams, API specs
├── scripts/                 # Automation & utility scripts
├── source code/
│   └── Dự Án Cuối/
│       ├── backend-dotnet/  # C# ASP.NET Core Web API (NET108 Core)
│       ├── frontend/        # React 18 + Vite + Tailwind Storefront & Admin
│       ├── ai-service/      # Python FastAPI NLP & Agent Service
│       ├── database/        # PostgreSQL 3NF DDL & Seed Data
│       ├── CHECKLIST.md     # Granular task checklist for AI agents
│       ├── start-all.bat    # 1-Click Multi-service Launcher
│       └── run.ps1          # PowerShell launcher
├── Các Bài Lab/             # FPT Polytechnic Lab assignments (Lab 1 - Lab 8)
├── AGENTS.md                # Multi-agent coordination agreement (THIS FILE)
└── CLAUDE.md                # Claude Code specific execution guide
```

---

## 2. Multi-Agent Concurrency & Ownership Rules

When two or more AI agents run concurrently via CLI (e.g. `claude` in Terminal 1, `agy` or `codex` in Terminal 2):

### 2.1 Domain Allocation (Separation of Concerns)
To avoid merge conflicts and file thrashing, agents should operate primarily on designated domains:
* **Frontend & Experience Focus (e.g., Claude Code)**:
  * Primary: `source code/Dự Án Cuối/frontend/`
* **Backend, C# & AI Core Focus (e.g., Antigravity / Codex)**:
  * Primary: `source code/Dự Án Cuối/backend-dotnet/`, `source code/Dự Án Cuối/ai-service/`, `source code/Dự Án Cuối/database/`
* **Shared Territory**: `docs/`, `Các Bài Lab/`, root configuration (`package.json`, `docker-compose.yml`, `source code/Dự Án Cuối/CHECKLIST.md`).
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
| **Backend C# (.NET 10/8)** | C#, ASP.NET Core Web API, Entity Framework Core, SQLite / PostgreSQL | `dotnet run` (in `source code/Dự Án Cuối/backend-dotnet`) | `dotnet build` / `dotnet test` |
| **Frontend Web** | React 18, Vite, TailwindCSS, Zustand, Lucide Icons | `npm run dev` (in `source code/Dự Án Cuối/frontend`) | `npm run build` |
| **AI Microservice** | Python 3.12, FastAPI, Pydantic, HTTPX, Gemini API | `python main.py` (in `source code/Dự Án Cuối/ai-service`) | `python -m py_compile main.py` |
| **Database** | SQLite (`dev.db`) & PostgreSQL 3NF DDL (`schema_postgresql.sql`) | Tự động tạo khi `dotnet run` | - |
| **All-in-one** | Multi-service script (Backend + Frontend + AI + Browser) | `.\start-all.bat` hoặc `.\run.ps1` (in `source code/Dự Án Cuối`) | - |

---

## 4. MCP (Model Context Protocol) Integration

This repo exposes an internal MCP server at `Trello-Clone-MCP`. AI agents can use this MCP server to:
1. `list_boards`: Query active user boards.
2. `get_board_data`: Fetch lists, cards, labels, and activity history.
3. `create_card`: Create tasks autonomously based on developer discussions.
4. `move_card`: Update status (e.g., In Progress -> Code Review -> Done).
5. `rag_search_tasks`: Query historical cards and documentation semantically.

Refer to `docs/02-ky-thuat/mcp-reference-architecture.md` for tool schemas and connection parameters.

---

## 5. Agent Workflow & Karpathy Guidelines

All agents (Antigravity, Claude Code, Codex, Cursor) MUST strictly follow the **Karpathy Guidelines** (`skills/karpathy-guidelines/SKILL.md`):

1. **Think Before Coding**: State assumptions explicitly, surface tradeoffs, ask when uncertain.
2. **Simplicity First**: Minimum code that solves the problem. Nothing speculative.
3. **Surgical Changes**: Touch only what you must. Never "improve" adjacent code or refactor things that aren't broken.
4. **Goal-Driven Execution**: State verifiable success criteria (`Step` ➔ `verify`). Loop until tests pass.
5. **Check Requirements**: Review `docs/` and task plans before code generation.
6. **Type Safety**: Maintain strict TypeScript interfaces between Backend and Frontend. Never use `any`.
7. **Environment Variables**: Always define defaults in `.env.example`. Never commit `.env` with secret keys.
8. **Testing**: Provide unit or integration tests mapping to `docs/02-ky-thuat/test-cases-p0-p1.csv`.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.
