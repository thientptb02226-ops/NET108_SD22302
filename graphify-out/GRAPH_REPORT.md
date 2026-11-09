# Graph Report - Net108Khai  (2026-11-09)

## Corpus Check
- 71 files · ~602,886 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 3, .csv 2, .mdc 1)

## Summary
- 574 nodes · 1013 edges · 36 communities (26 shown, 10 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 21 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5b3f0ea7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- generate_lab2_diagrams.py
- useCommerceStore.ts
- CartItem
- docx
- postgres
- package.json
- ai-service/main.py
- ref_node_fs
- frontend/package.json
- compilerOptions
- .agent/skills/idea-refine/scripts/idea-refine.sh
- .claude/skills/idea-refine/scripts/idea-refine.sh
- skills/idea-refine/scripts/idea-refine.sh
- compilerOptions
- generate_all_lab1_diagrams.py
- generate_14_usecase_diagrams.py
- Task
- AuthController.cs
- vite-env.d.ts
- CartItem
- User
- Order
- Product
- CommerceDbContext
- CommerceQuote
- CommerceIdempotency
- create_lab1_document
- http
- AiActionApproval
- OrderItem
- AiNativeCommerce.Api.csproj

## God Nodes (most connected - your core abstractions)
1. `CommerceDbContext` - 33 edges
2. `Order` - 23 edges
3. `useCommerceStore` - 22 edges
4. `Product` - 21 edges
5. `User` - 17 edges
6. `CommerceQuote` - 17 edges
7. `compilerOptions` - 16 edges
8. `CartItem` - 14 edges
9. `CommerceIdempotency` - 14 edges
10. `OrderItem` - 14 edges

## Surprising Connections (you probably didn't know these)
- `ProductCardProps` --references--> `Product`  [EXTRACTED]
  source code/Dự Án Cuối/frontend/src/components/ProductCard.tsx → source code/Dự Án Cuối/frontend/src/types/index.ts
- `AdminController` --references--> `CommerceDbContext`  [EXTRACTED]
  source code/Dự Án Cuối/backend-dotnet/Controllers/AdminController.cs → source code/Dự Án Cuối/backend-dotnet/Data/CommerceDbContext.cs
- `AuthController` --references--> `CommerceDbContext`  [EXTRACTED]
  source code/Dự Án Cuối/backend-dotnet/Controllers/AuthController.cs → source code/Dự Án Cuối/backend-dotnet/Data/CommerceDbContext.cs
- `CartController` --references--> `CommerceDbContext`  [EXTRACTED]
  source code/Dự Án Cuối/backend-dotnet/Controllers/CartController.cs → source code/Dự Án Cuối/backend-dotnet/Data/CommerceDbContext.cs
- `CatalogController` --references--> `CommerceDbContext`  [EXTRACTED]
  source code/Dự Án Cuối/backend-dotnet/Controllers/CatalogController.cs → source code/Dự Án Cuối/backend-dotnet/Data/CommerceDbContext.cs

## Import Cycles
- None detected.

## Communities (36 total, 10 thin omitted)

### Community 0 - "generate_lab2_diagrams.py"
Cohesion: 0.36
Nodes (4): generate_ai_evidence(), generate_erd_level2(), generate_ui_flow(), main()

### Community 1 - "useCommerceStore.ts"
Cohesion: 0.14
Nodes (29): lucide-react, react, App(), AdminDashboard(), AiAssistantWidget(), CartDrawer(), CheckoutModal(), HeroBanner() (+21 more)

### Community 2 - "CartItem"
Cohesion: 0.25
Nodes (8): CartItem, Cart, CartId, Id, Product, ProductId, Quantity, UnitPriceMinor

### Community 4 - "docx"
Cohesion: 0.06
Nodes (26): main(), generate_lab1_docx(), add_body_paragraph(), add_heading_with_bookmark(), add_image_with_caption(), build_lab2(), create_styled_table(), format_cell_text() (+18 more)

### Community 5 - "postgres"
Cohesion: 0.09
Nodes (21): POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER, container_name, environment, image, ports, restart (+13 more)

### Community 6 - "package.json"
Cohesion: 0.17
Nodes (11): description, keywords, license, name, private, scripts, dev:ai, dev:dotnet (+3 more)

### Community 12 - "ai-service/main.py"
Cohesion: 0.11
Nodes (13): ActionApproval, api_chat(), api_recommend(), api_search(), ChatMessage, ChatRequest, ChatResponse, extract_price_constraint() (+5 more)

### Community 13 - "ref_node_fs"
Cohesion: 0.29
Nodes (3): [tool, file, ...extra], [tool, file, ...extra], [tool, file, ...extra]

### Community 14 - "frontend/package.json"
Cohesion: 0.07
Nodes (36): autoprefixer, clsx, postcss, react-dom, tailwind-merge, tailwindcss, @types/react, @types/react-dom (+28 more)

### Community 15 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+9 more)

### Community 21 - "compilerOptions"
Cohesion: 0.25
Nodes (7): compilerOptions, allowSyntheticDefaultImports, composite, module, moduleResolution, skipLibCheck, include

### Community 23 - "generate_all_lab1_diagrams.py"
Cohesion: 0.23
Nodes (13): draw_actor(), draw_arrow(), draw_dashed_line(), draw_ellipse_uc(), generate_admin_usecase(), generate_agent_usecase(), generate_appmap_diagram(), generate_customer_usecase() (+5 more)

### Community 24 - "generate_14_usecase_diagrams.py"
Cohesion: 0.12
Nodes (21): draw_actor(), draw_dashed_arrow(), draw_header(), draw_legend(), draw_oval(), draw_solid_association(), main(), render_diagram() (+13 more)

### Community 28 - "Task"
Cohesion: 0.09
Nodes (19): AdminController, AiController, AuthController, CartController, CatalogController, CheckoutController, OrdersController, AddCartItemRequest (+11 more)

### Community 29 - "AuthController.cs"
Cohesion: 0.18
Nodes (4): AiNativeCommerce.Api.DTOs, AiNativeCommerce.Api.Data, AiNativeCommerce.Api.Controllers, AiNativeCommerce.Api.Models

### Community 35 - "CartItem"
Cohesion: 0.13
Nodes (14): DbInitializer, Cart, CreatedAt, Id, Items, UpdatedAt, UserId, Category (+6 more)

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

### Community 45 - "http"
Cohesion: 0.20
Nodes (9): ASPNETCORE_ENVIRONMENT, applicationUrl, commandName, dotnetRunMessages, environmentVariables, launchBrowser, profiles, http (+1 more)

### Community 46 - "AiActionApproval"
Cohesion: 0.22
Nodes (8): AiActionApproval, ActionType, CreatedAt, Description, Id, PayloadJson, Status, UserId

### Community 49 - "OrderItem"
Cohesion: 0.22
Nodes (9): OrderItem, Id, Order, OrderId, Product, ProductId, Quantity, SubtotalMinor (+1 more)

### Community 54 - "AiNativeCommerce.Api.csproj"
Cohesion: 0.25
Nodes (7): net10.0, BCrypt.Net-Next (4.2.0), Microsoft.AspNetCore.Authentication.JwtBearer (10.0.14), Microsoft.AspNetCore.OpenApi (10.0.13), Microsoft.EntityFrameworkCore.Sqlite (10.0.14), Microsoft.NET.Sdk.Web, AiNativeCommerce.Api

## Knowledge Gaps
- **112 isolated node(s):** `CreatedAt`, `Id`, `Items`, `UpdatedAt`, `UserId` (+107 more)
  These have ≤1 connection - possible missing edges. (Counts symbols only; 286 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CommerceDbContext` connect `CommerceDbContext` to `CartItem`, `CartItem`, `User`, `Order`, `Product`, `CommerceQuote`, `CommerceIdempotency`, `AiActionApproval`, `OrderItem`, `Task`, `AuthController.cs`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Order` (e.g. with `CheckoutController.ProcessCheckout()` and `DbInitializer.Initialize()`) actually correct?**
  _`Order` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `CreatedAt`, `Id`, `Items` to the rest of the system?**
  _112 weakly-connected nodes found - possible missing edges._
- **Should `useCommerceStore.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.14202898550724638 - nodes in this community are weakly interconnected._
- **Why does `Order` connect `Order` to `CartItem`, `User`, `CommerceDbContext`, `AiActionApproval`, `OrderItem`, `Task`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Should `docx` be split into smaller, more focused modules?**
  _Cohesion score 0.06409130816505706 - nodes in this community are weakly interconnected._
- **Why does `Product` connect `Product` to `CartItem`, `CartItem`, `User`, `CommerceDbContext`, `AiActionApproval`, `OrderItem`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._