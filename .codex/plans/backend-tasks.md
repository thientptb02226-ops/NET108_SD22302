# Backend Implementation Plan

1. **Database & Models**:
   - `User`, `Workspace`, `WorkspaceMember`, `Board`, `List`, `Card`, `Label`, `Comment`, `ActivityLog`.
2. **REST API Endpoints**:
   - `/api/v1/auth`: Register, login, refresh, profile.
   - `/api/v1/boards`: CRUD operations, member invitations.
   - `/api/v1/lists`: List ordering, creation, archiving.
   - `/api/v1/cards`: Card details, moving positions, attachments, labels.
3. **Realtime WebSocket Server**:
   - Socket.io rooms per board ID for instant card movement sync.
4. **MCP Server Integration**:
   - Provide direct DB / internal service methods for `Trello-Clone-MCP`.

