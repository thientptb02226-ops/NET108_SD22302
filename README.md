# 🚀 Trello Clone — Multi-Agent AI Monorepo

Dự án Monorepo đầy đủ cho hệ thống **Trello Clone** tích hợp AI (MCP Server, RAG Pipeline, Chatbot Assistant) và được cấu hình sẵn môi trường cộng tác cho nhiều AI Agent CLI chạy song song (**Claude Code**, **Antigravity**, **OpenAI Codex**).

---

## 📂 Cấu trúc thư mục

```
trello-clone/
├── .agent/                  # Cấu hình Antigravity Agent (rules, skills, workflows)
├── .claude/                 # Cấu hình Claude Code CLI (commands, hooks, plans, policies, rules, skills)
├── .codex/                  # Cấu hình OpenAI Codex (commands, hooks, policies, references, rules)
├── certs/                   # Chứng chỉ SSL / Dev certs
├── Chatbot-Frontend/        # Giao diện widget Chatbot AI (React + Vite)
├── docs/                    # Tài liệu kiến trúc hệ thống, API specs, Multi-agent protocol
├── Trello-Clone-AI-RAG/     # Dịch vụ RAG tìm kiếm ngữ nghĩa (Python FastAPI / LangChain)
├── Trello-Clone-Backend/    # Core REST & WebSocket API (Node.js / Express / TypeScript / Prisma)
├── Trello-Clone-Desktop/    # Desktop App (Electron / Tauri)
├── Trello-Clone-Frontend/   # Web App Kanban Board (Next.js / React / TailwindCSS)
├── Trello-Clone-Infra/      # Docker, Kubernetes, CI/CD scripts
├── Trello-Clone-MCP/        # Model Context Protocol Server (kết nối trực tiếp AI với Board)
├── Trello-Clone-Mobile/     # Mobile App (React Native / Expo)
├── AGENTS.md                # Bản thỏa ước điều phối đa tác nhân (Multi-Agent Protocol)
├── CLAUDE.md                # Hướng dẫn dành riêng cho Claude Code CLI
└── mcp-reference-architecture.md # Kiến trúc MCP chi tiết
```

---

## 🤖 Hướng dẫn chạy 2 Con AI CLI cùng lúc (Multi-Agent)

### 1. Terminal 1 — Chạy Claude Code CLI
```bash
claude
```
*Claude sẽ tự động đọc `CLAUDE.md`, `AGENTS.md` và `.claude/` để làm việc.*

### 2. Terminal 2 — Chạy Antigravity CLI (hoặc Codex)
```bash
agy
```
*Antigravity sẽ phối hợp nhịp nhàng theo quy chuẩn chia task trong `AGENTS.md`.*

---

## 🛠️ Khởi động Hạ tầng (Postgres, Redis, ChromaDB)

```bash
docker compose up -d
```
