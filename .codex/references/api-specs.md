# API Specification Reference

All endpoints prefixed with `/api/v1`.

### Auth
- `POST /auth/register` - `{ email, password, name }`
- `POST /auth/login` - `{ email, password }` -> returns `{ accessToken, user }`
- `GET /auth/me` - Bearer Token Auth

### Boards
- `GET /boards` - List boards for current user
- `POST /boards` - Create board `{ title, workspaceId, background }`
- `GET /boards/:id` - Get board details with lists and cards
- `DELETE /boards/:id` - Archive / delete board

### Lists & Cards
- `POST /lists` - Create list `{ boardId, title, position }`
- `PUT /lists/:id/reorder` - `{ newPosition }`
- `POST /cards` - Create card `{ listId, title, description, position }`
- `PUT /cards/:id/move` - Move card `{ targetListId, position }`

