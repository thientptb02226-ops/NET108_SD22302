# Model Context Protocol (MCP) Reference Architecture

> **Purpose**: This document specifies how Model Context Protocol (MCP) servers and clients are structured to bridge AI agents (Antigravity, Claude, Codex) with the Trello-Clone ecosystem.

---

## 1. High-Level Architecture Diagram

```
+-------------------------------------------------------------+
|                     AI Agent Clients                        |
|   (Antigravity IDE / Claude Code CLI / OpenAI Codex CLI)     |
+-------------------------------------------------------------+
                              |
                     JSON-RPC over stdio / SSE
                              |
                              v
+-------------------------------------------------------------+
|             Trello-Clone-MCP Server (TypeScript)            |
|  - Tool Definitions (boards, lists, cards, search)          |
|  - Resource Providers (board state, activity logs)          |
|  - Prompt Templates (daily standup, sprint backlog)         |
+-------------------------------------------------------------+
          |                                      |
          | Internal REST / GraphQL              | Embeddings / Semantic
          v                                      v
+------------------------+             +----------------------+
|  Trello-Clone-Backend  |             |  Trello-Clone-AI-RAG |
|  - PostgreSQL / Prisma |             |  - ChromaDB / Vector |
|  - Real-time WebSocket |             |  - LangChain Engine  |
+------------------------+             +----------------------+
```

---

## 2. MCP Tools Exposed by `Trello-Clone-MCP`

The MCP server implements the official `@modelcontextprotocol/sdk` and exposes the following tools:

### 2.1 `trello_list_boards`
* **Description**: Returns all boards accessible by the current workspace/user.
* **Input**:
  ```json
  {
    "workspaceId": "string (optional)",
    "status": "active | archived | all"
  }
  ```
* **Output**: Array of board objects (id, title, description, memberCount, listCount).

### 2.2 `trello_get_board_details`
* **Description**: Returns a full board view including lists, cards, assigned users, and labels.
* **Input**:
  ```json
  {
    "boardId": "string"
  }
  ```

### 2.3 `trello_create_card`
* **Description**: Creates a new task card on a specified board list.
* **Input**:
  ```json
  {
    "listId": "string",
    "title": "string",
    "description": "string (optional)",
    "dueDate": "ISO8601 string (optional)",
    "labels": ["string"]
  }
  ```

### 2.4 `trello_move_card`
* **Description**: Updates card ordering or moves card across columns (lists).
* **Input**:
  ```json
  {
    "cardId": "string",
    "targetListId": "string",
    "position": "number"
  }
  ```

### 2.5 `trello_rag_search`
* **Description**: Executes semantic vector search across all board descriptions, card comments, and project attachments.
* **Input**:
  ```json
  {
    "query": "string",
    "limit": "number (default: 5)"
  }
  ```

---

## 3. Configuration in AI Clients

### Adding MCP to Claude Code (`~/.claude/claude_desktop_config.json` or project level):
```json
{
  "mcpServers": {
    "trello-clone": {
      "command": "node",
      "args": ["<WORKSPACE_PATH>/Trello-Clone-MCP/dist/index.js"],
      "env": {
        "TRELLO_API_URL": "http://localhost:5000/api/v1",
        "TRELLO_API_KEY": "dev_agent_secret_key"
      }
    }
  }
}
```

### Adding MCP to Antigravity:
Configure in `.agent/rules/` or via Antigravity MCP settings using the same executable entry point.
