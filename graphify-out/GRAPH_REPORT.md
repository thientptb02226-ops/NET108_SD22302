# Graph Report - Net108Khai  (2026-11-08)

## Corpus Check
- 100 files · ~607,567 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 18 file(s) not represented in the graph (top: .example 3, (none) 2, .csv 2)

## Summary
- 862 nodes · 1460 edges · 60 communities (49 shown, 11 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f0c8c094`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- backend/src/index.ts
- useCommerceStore.ts
- Chatbot-Frontend/package.json
- Trello-Clone-MCP/package.json
- docx
- postgres
- package.json
- Trello-Clone-Mobile/package.json
- Trello-Clone-Desktop/package.json
- compilerOptions
- compilerOptions
- backend/package.json
- ai-service/main.py
- ref_node_fs
- frontend/package.json
- compilerOptions
- compilerOptions
- .agent/skills/idea-refine/scripts/idea-refine.sh
- .claude/skills/idea-refine/scripts/idea-refine.sh
- skills/idea-refine/scripts/idea-refine.sh
- Trello-Clone-Backend/package.json
- compilerOptions
- scripts
- generate_all_lab1_diagrams.py
- generate_14_usecase_diagrams.py
- create_full_lab1_document
- @prisma/client
- scripts
- Task
- AuthController.cs
- vite-env.d.ts
- dependencies
- Trello-Clone-Frontend/package.json
- CartItem
- User
- Order
- Product
- CommerceDbContext
- CommerceQuote
- CommerceIdempotency
- dependencies
- create_lab1_document
- generate_lab2_document.py
- http
- AiActionApproval
- devDependencies
- generate_lab1_docx
- OrderItem
- WeatherForecast
- insert_chapter3_and_diagrams.py
- dependencies
- AiNativeCommerce.Api.csproj
- Category
- docx_oxml_ns
- insert_toc_and_finalize_lab1.py
- scripts
- scripts

## God Nodes (most connected - your core abstractions)
1. `CommerceDbContext` - 34 edges
2. `Order` - 23 edges
3. `useCommerceStore` - 22 edges
4. `Product` - 21 edges
5. `User` - 17 edges
6. `CommerceQuote` - 17 edges
7. `compilerOptions` - 16 edges
8. `express` - 15 edges
9. `react` - 15 edges
10. `CartItem` - 14 edges

## Surprising Connections (you probably didn't know these)
- `express@^4.19.2` --declares--> `express`  [EXTRACTED]
  Trello-Clone-Backend/package.json → source code/Dự Án Cuối/backend/package.json
- `typescript@^5.5.2` --declares--> `typescript`  [EXTRACTED]
  Trello-Clone-Backend/package.json → Chatbot-Frontend/package.json
- `typescript@^5.5.2` --declares--> `typescript`  [EXTRACTED]
  Trello-Clone-MCP/package.json → Chatbot-Frontend/package.json
- `cors@^2.8.5` --declares--> `cors`  [EXTRACTED]
  Trello-Clone-Backend/package.json → source code/Dự Án Cuối/backend/package.json
- `jsonwebtoken@^9.0.2` --declares--> `jsonwebtoken`  [EXTRACTED]
  Trello-Clone-Backend/package.json → source code/Dự Án Cuối/backend/package.json

## Import Cycles
- None detected.

## Communities (60 total, 11 thin omitted)

### Community 0 - "backend/src/index.ts"
Cohesion: 0.16
Nodes (20): express, app, globalForPrisma, prisma, authenticateToken(), AuthUser, Express, Request (+12 more)

### Community 1 - "useCommerceStore.ts"
Cohesion: 0.12
Nodes (32): lucide-react, react, App(), AdminDashboard(), AiAssistantWidget(), CartDrawer(), CheckoutModal(), HeroBanner() (+24 more)

### Community 2 - "Chatbot-Frontend/package.json"
Cohesion: 0.11
Nodes (21): description, devDependencies, @types/react@^18.3.3, @types/react-dom@^18.3.0, typescript@^5.5.2, vite@^5.3.1, @vitejs/plugin-react@^4.3.1, @types/react (+13 more)

### Community 3 - "Trello-Clone-MCP/package.json"
Cohesion: 0.09
Nodes (24): axios, @modelcontextprotocol/sdk, dotenv@^16.4.5, @types/node@^20.14.9, dependencies, axios@^1.7.2, dotenv@^16.4.5, @modelcontextprotocol/sdk@^0.6.0 (+16 more)

### Community 4 - "docx"
Cohesion: 0.24
Nodes (4): main(), main(), insert_missing_section(), style_table()

### Community 5 - "postgres"
Cohesion: 0.07
Nodes (27): container_name, image, ports, volumes, POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, container_name (+19 more)

### Community 6 - "package.json"
Cohesion: 0.12
Nodes (15): description, keywords, license, name, private, scripts, build:all, dev:backend (+7 more)

### Community 7 - "Trello-Clone-Mobile/package.json"
Cohesion: 0.16
Nodes (14): expo, react-native, dependencies, expo@~51.0.0, react@18.2.0, react-native@0.74.2, description, react (+6 more)

### Community 8 - "Trello-Clone-Desktop/package.json"
Cohesion: 0.18
Nodes (12): electron, electron-builder, description, devDependencies, electron@^31.0.2, electron-builder@^24.13.3, main, name (+4 more)

### Community 9 - "compilerOptions"
Cohesion: 0.17
Nodes (11): compilerOptions, esModuleInterop, forceConsistentCasingInFileNames, module, moduleResolution, outDir, rootDir, skipLibCheck (+3 more)

### Community 10 - "compilerOptions"
Cohesion: 0.18
Nodes (10): compilerOptions, esModuleInterop, module, moduleResolution, outDir, rootDir, skipLibCheck, strict (+2 more)

### Community 11 - "backend/package.json"
Cohesion: 0.14
Nodes (19): prisma, ts-node, ts-node-dev, @types/bcryptjs, @types/node, @types/uuid, description, devDependencies (+11 more)

### Community 12 - "ai-service/main.py"
Cohesion: 0.10
Nodes (16): ActionApproval, api_chat(), api_recommend(), api_search(), ChatMessage, ChatRequest, ChatResponse, extract_price_constraint() (+8 more)

### Community 13 - "ref_node_fs"
Cohesion: 0.29
Nodes (3): [tool, file, ...extra], [tool, file, ...extra], [tool, file, ...extra]

### Community 14 - "frontend/package.json"
Cohesion: 0.13
Nodes (18): postcss, @types/react, @types/react-dom, vite, @vitejs/plugin-react, devDependencies, postcss@^8.4.38, @types/react@^18.3.3 (+10 more)

### Community 15 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+9 more)

### Community 16 - "compilerOptions"
Cohesion: 0.14
Nodes (13): compilerOptions, esModuleInterop, forceConsistentCasingInFileNames, lib, module, moduleResolution, outDir, resolveJsonModule (+5 more)

### Community 20 - "Trello-Clone-Backend/package.json"
Cohesion: 0.14
Nodes (17): @types/cors, @types/express, @types/jsonwebtoken, @types/cors@^2.8.17, @types/express@^4.17.21, @types/jsonwebtoken@^9.0.6, description, devDependencies (+9 more)

### Community 21 - "compilerOptions"
Cohesion: 0.25
Nodes (7): compilerOptions, allowSyntheticDefaultImports, composite, module, moduleResolution, skipLibCheck, include

### Community 22 - "scripts"
Cohesion: 0.29
Nodes (7): scripts, build, db:push, db:seed, db:studio, dev, start

### Community 23 - "generate_all_lab1_diagrams.py"
Cohesion: 0.23
Nodes (13): draw_actor(), draw_arrow(), draw_dashed_line(), draw_ellipse_uc(), generate_admin_usecase(), generate_agent_usecase(), generate_appmap_diagram(), generate_customer_usecase() (+5 more)

### Community 24 - "generate_14_usecase_diagrams.py"
Cohesion: 0.09
Nodes (25): draw_actor(), draw_dashed_arrow(), draw_header(), draw_legend(), draw_oval(), draw_solid_association(), main(), render_diagram() (+17 more)

### Community 26 - "@prisma/client"
Cohesion: 0.17
Nodes (8): bcryptjs, @prisma/client, bcryptjs@^2.4.3, @prisma/client@^5.10.0, bcryptjs_1, client_1, prisma, prisma

### Community 27 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, start, test

### Community 28 - "Task"
Cohesion: 0.09
Nodes (20): AdminController, AiController, AuthController, CartController, CatalogController, CheckoutController, OrdersController, WeatherForecastController (+12 more)

### Community 29 - "AuthController.cs"
Cohesion: 0.21
Nodes (4): AiNativeCommerce.Api.DTOs, AiNativeCommerce.Api.Data, AiNativeCommerce.Api.Controllers, AiNativeCommerce.Api.Models

### Community 33 - "dependencies"
Cohesion: 0.10
Nodes (22): cors, dotenv, jsonwebtoken, socket.io, uuid, zod, dependencies, cors@^2.8.5 (+14 more)

### Community 34 - "Trello-Clone-Frontend/package.json"
Cohesion: 0.16
Nodes (16): react-dom, @dnd-kit/core, @dnd-kit/sortable, @dnd-kit/utilities, socket.io-client, dependencies, @dnd-kit/core@^6.1.0, @dnd-kit/sortable@^8.0.0 (+8 more)

### Community 35 - "CartItem"
Cohesion: 0.12
Nodes (15): DbInitializer, Cart, CreatedAt, Id, Items, UpdatedAt, UserId, CartItem (+7 more)

### Community 36 - "User"
Cohesion: 0.13
Nodes (13): Role, Description, Id, Name, User, CreatedAt, Email, FullName (+5 more)

### Community 37 - "Order"
Cohesion: 0.12
Nodes (16): Order, CreatedAt, Currency, Id, Items, OrderNumber, PaymentMethod, PaymentStatus (+8 more)

### Community 38 - "Product"
Cohesion: 0.13
Nodes (15): Product, AiTagsJson, Category, CategoryId, CreatedAt, Description, Id, ImageUrl (+7 more)

### Community 39 - "CommerceDbContext"
Cohesion: 0.14
Nodes (12): CommerceDbContext, AiActionApprovals, CartItems, Carts, Categories, CommerceIdempotencies, CommerceQuotes, OrderItems (+4 more)

### Community 40 - "CommerceQuote"
Cohesion: 0.14
Nodes (14): CommerceQuote, CartId, CreatedAt, Currency, DiscountMinor, ExpiresAt, Fingerprint, Id (+6 more)

### Community 41 - "CommerceIdempotency"
Cohesion: 0.17
Nodes (10): CommerceIdempotency, CreatedAt, ExpiresAt, HttpStatus, Id, Operation, RequestHash, RequestKey (+2 more)

### Community 42 - "dependencies"
Cohesion: 0.17
Nodes (12): clsx, react-dom, tailwind-merge, zustand, dependencies, clsx@^2.1.0, lucide-react@^0.344.0, react@^18.3.1 (+4 more)

### Community 44 - "generate_lab2_document.py"
Cohesion: 0.40
Nodes (9): add_body_paragraph(), add_heading_with_bookmark(), add_image_with_caption(), build_lab2(), create_styled_table(), format_cell_text(), set_cell_margins(), set_cell_shading() (+1 more)

### Community 45 - "http"
Cohesion: 0.20
Nodes (9): ASPNETCORE_ENVIRONMENT, applicationUrl, commandName, dotnetRunMessages, environmentVariables, launchBrowser, profiles, http (+1 more)

### Community 46 - "AiActionApproval"
Cohesion: 0.22
Nodes (8): AiActionApproval, ActionType, CreatedAt, Description, Id, PayloadJson, Status, UserId

### Community 47 - "devDependencies"
Cohesion: 0.22
Nodes (9): autoprefixer, tailwindcss, autoprefixer@^10.4.19, tailwindcss@^3.4.4, devDependencies, autoprefixer@^10.4.19, tailwindcss@^3.4.4, vite@^5.3.1 (+1 more)

### Community 49 - "OrderItem"
Cohesion: 0.22
Nodes (9): OrderItem, Id, Order, OrderId, Product, ProductId, Quantity, SubtotalMinor (+1 more)

### Community 50 - "WeatherForecast"
Cohesion: 0.25
Nodes (6): AiNativeCommerce.Api, WeatherForecast, Date, Summary, TemperatureC, TemperatureF

### Community 52 - "insert_chapter3_and_diagrams.py"
Cohesion: 0.43
Nodes (6): add_body_paragraph(), add_image_with_caption(), add_styled_heading(), create_styled_table(), main(), set_cell_properties()

### Community 53 - "dependencies"
Cohesion: 0.29
Nodes (7): dependencies, lucide-react@^0.395.0, react@^18.3.1, react-dom@^18.3.1, lucide-react, react, lucide-react@^0.395.0

### Community 54 - "AiNativeCommerce.Api.csproj"
Cohesion: 0.29
Nodes (6): net10.0, BCrypt.Net-Next (4.2.0), Microsoft.AspNetCore.Authentication.JwtBearer (10.0.14), Microsoft.AspNetCore.OpenApi (10.0.13), Microsoft.EntityFrameworkCore.Sqlite (10.0.14), Microsoft.NET.Sdk.Web

### Community 55 - "Category"
Cohesion: 0.29
Nodes (7): Category, Description, Icon, Id, Name, Products, Slug

### Community 57 - "insert_toc_and_finalize_lab1.py"
Cohesion: 0.53
Nodes (4): main(), make_page_break(), make_toc_heading(), make_toc_row()

### Community 58 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, build, dev, preview

### Community 59 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, build, dev, preview

## Knowledge Gaps
- **116 isolated node(s):** `net10.0`, `BCrypt.Net-Next (4.2.0)`, `Microsoft.AspNetCore.Authentication.JwtBearer (10.0.14)`, `Microsoft.AspNetCore.OpenApi (10.0.13)`, `Microsoft.EntityFrameworkCore.Sqlite (10.0.14)` (+111 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 389 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `typescript` connect `Chatbot-Frontend/package.json` to `Trello-Clone-Frontend/package.json`, `Trello-Clone-MCP/package.json`, `Trello-Clone-Backend/package.json`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Order` (e.g. with `CheckoutController.ProcessCheckout()` and `DbInitializer.Initialize()`) actually correct?**
  _`Order` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `net10.0`, `BCrypt.Net-Next (4.2.0)`, `Microsoft.AspNetCore.Authentication.JwtBearer (10.0.14)` to the rest of the system?**
  _116 weakly-connected nodes found - possible missing edges._
- **Should `useCommerceStore.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.1207843137254902 - nodes in this community are weakly interconnected._
- **Why does `zustand` connect `dependencies` to `useCommerceStore.ts`, `Trello-Clone-Frontend/package.json`, `frontend/package.json`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Should `Chatbot-Frontend/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.11255411255411256 - nodes in this community are weakly interconnected._
- **Why does `CommerceDbContext` connect `CommerceDbContext` to `CartItem`, `User`, `Order`, `Product`, `CommerceQuote`, `CommerceIdempotency`, `AiActionApproval`, `OrderItem`, `Category`, `Task`, `AuthController.cs`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._