# System Architecture & Multi-Agent Collaboration

## 1. High-Level Overview

The Trello-Clone Monorepo contains:
- **Trello-Clone-Backend**: Core REST & Real-time WebSocket server.
- **Trello-Clone-Frontend**: Full-featured Kanban web app with drag-and-drop.
- **Trello-Clone-MCP**: MCP Server exposing board management tools directly to AI coding agents.
- **Trello-Clone-AI-RAG**: Vector search and semantic intelligence layer.
- **Chatbot-Frontend**: AI assistant interface embedded in the Kanban board.
- **Trello-Clone-Desktop**: Native desktop client.
- **Trello-Clone-Mobile**: Native mobile application.
- **Trello-Clone-Infra**: Docker Compose and deployment manifests.

## 2. Multi-Agent CLI Concurrency

```
                        +----------------------+
                        |   Human Developer    |
                        +----------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v                                                   v
+------------------+                               +------------------+
| Claude Code CLI  |                               | Antigravity CLI  |
| (Terminal 1)     |                               | (Terminal 2)     |
+------------------+                               +------------------+
         |                                                   |
         | Read/Write                                        | Read/Write
         v                                                   v
+---------------------------------------------------------------------+
|                      Shared Monorepo Workspace                      |
|                                                                     |
|  [Frontend & UI]            [Backend & DB]           [MCP & RAG]    |
|  - Trello-Clone-Frontend    - Trello-Clone-Backend   - MCP Server   |
|  - Chatbot-Frontend         - PostgreSQL / Redis     - AI-RAG       |
+---------------------------------------------------------------------+
```
