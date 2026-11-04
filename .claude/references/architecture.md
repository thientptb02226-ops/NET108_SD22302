# Architecture Reference

## Component Relationships
- **Frontend (`Trello-Clone-Frontend`)**:
  - Communicates with Backend via REST (`http://localhost:5000/api/v1`) and WebSockets (`ws://localhost:5000`).
  - Calls `Chatbot-Frontend` or integrates chatbot widget on the board canvas.
- **Backend (`Trello-Clone-Backend`)**:
  - Connects to PostgreSQL via Prisma ORM.
  - Connects to Redis for session caching and Pub/Sub event broadcasting.
  - Exposes REST endpoints consumed by Frontend, Mobile, Desktop, and MCP.
- **AI-RAG (`Trello-Clone-AI-RAG`)**:
  - Synchronizes card descriptions and comments into ChromaDB vector store.
  - Exposes `/query` and `/ingest` endpoints.
- **MCP Server (`Trello-Clone-MCP`)**:
  - Acts as the tool interface between Claude Code CLI / Antigravity and the Trello data layer.

