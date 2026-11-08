# Graph Report - Net108Khai  (2026-11-08)

## Corpus Check
- 82 files · ~602,103 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .example 3, (none) 2, .csv 2)

## Summary
- 629 nodes · 1047 edges · 33 communities (26 shown, 7 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `69e1813c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- backend/src/index.ts
- useCommerceStore.ts
- Trello-Clone-Frontend/package.json
- Trello-Clone-MCP/package.json
- generate_lab1.py
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
- seed.js
- scripts
- @types/express
- @types/jsonwebtoken
- vite-env.d.ts

## God Nodes (most connected - your core abstractions)
1. `useCommerceStore` - 22 edges
2. `compilerOptions` - 16 edges
3. `express` - 15 edges
4. `react` - 15 edges
5. `create_lab1_document()` - 14 edges
6. `compilerOptions` - 12 edges
7. `lucide-react` - 12 edges
8. `App()` - 12 edges
9. `generate_lab1_docx()` - 11 edges
10. `create_full_lab1_document()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `typescript@^5.5.2` --declares--> `typescript`  [EXTRACTED]
  Trello-Clone-Backend/package.json → Chatbot-Frontend/package.json
- `typescript@^5.5.2` --declares--> `typescript`  [EXTRACTED]
  Trello-Clone-MCP/package.json → Chatbot-Frontend/package.json
- `cors@^2.8.5` --declares--> `cors`  [EXTRACTED]
  Trello-Clone-Backend/package.json → source code/Dự Án Cuối/backend/package.json
- `express@^4.19.2` --declares--> `express`  [EXTRACTED]
  Trello-Clone-Backend/package.json → source code/Dự Án Cuối/backend/package.json
- `jsonwebtoken@^9.0.2` --declares--> `jsonwebtoken`  [EXTRACTED]
  Trello-Clone-Backend/package.json → source code/Dự Án Cuối/backend/package.json

## Import Cycles
- None detected.

## Communities (33 total, 7 thin omitted)

### Community 0 - "backend/src/index.ts"
Cohesion: 0.07
Nodes (45): bcryptjs, cors, dotenv, express, jsonwebtoken, @prisma/client, socket.io, zod (+37 more)

### Community 1 - "useCommerceStore.ts"
Cohesion: 0.14
Nodes (29): lucide-react, react, App(), AdminDashboard(), AiAssistantWidget(), CartDrawer(), CheckoutModal(), HeroBanner() (+21 more)

### Community 2 - "Trello-Clone-Frontend/package.json"
Cohesion: 0.06
Nodes (51): dependencies, lucide-react@^0.395.0, react@^18.3.1, react-dom@^18.3.1, description, devDependencies, @types/react@^18.3.3, @types/react-dom@^18.3.0 (+43 more)

### Community 3 - "Trello-Clone-MCP/package.json"
Cohesion: 0.09
Nodes (22): axios, @modelcontextprotocol/sdk, dotenv@^16.4.5, dependencies, axios@^1.7.2, dotenv@^16.4.5, @modelcontextprotocol/sdk@^0.6.0, description (+14 more)

### Community 4 - "generate_lab1.py"
Cohesion: 0.05
Nodes (27): main(), create_lab1_document(), generate_lab1_docx(), add_body_paragraph(), add_heading_with_bookmark(), add_image_with_caption(), build_lab2(), create_styled_table() (+19 more)

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
Cohesion: 0.12
Nodes (21): prisma, ts-node, ts-node-dev, @types/bcryptjs, @types/node, @types/uuid, uuid, uuid@^9.0.1 (+13 more)

### Community 12 - "ai-service/main.py"
Cohesion: 0.10
Nodes (16): ActionApproval, api_chat(), api_recommend(), api_search(), ChatMessage, ChatRequest, ChatResponse, extract_price_constraint() (+8 more)

### Community 13 - "ref_node_fs"
Cohesion: 0.29
Nodes (3): [tool, file, ...extra], [tool, file, ...extra], [tool, file, ...extra]

### Community 14 - "frontend/package.json"
Cohesion: 0.05
Nodes (43): autoprefixer, clsx, postcss, react-dom, tailwind-merge, tailwindcss, @types/react, @types/react-dom (+35 more)

### Community 15 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+9 more)

### Community 16 - "compilerOptions"
Cohesion: 0.13
Nodes (14): compilerOptions, esModuleInterop, forceConsistentCasingInFileNames, lib, module, moduleResolution, outDir, resolveJsonModule (+6 more)

### Community 20 - "Trello-Clone-Backend/package.json"
Cohesion: 0.18
Nodes (13): @types/cors, @types/cors@^2.8.17, description, devDependencies, tsx@^4.16.2, @types/cors@^2.8.17, @types/node@^20.14.9, typescript@^5.5.2 (+5 more)

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

### Community 26 - "seed.js"
Cohesion: 0.40
Nodes (3): bcryptjs_1, client_1, prisma

### Community 27 - "scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, start, test

### Community 28 - "@types/express"
Cohesion: 0.67
Nodes (3): @types/express, @types/express@^4.17.21, @types/express@^4.17.21

### Community 29 - "@types/jsonwebtoken"
Cohesion: 0.67
Nodes (3): @types/jsonwebtoken, @types/jsonwebtoken@^9.0.6, @types/jsonwebtoken@^9.0.6

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `typescript` connect `Trello-Clone-Frontend/package.json` to `Trello-Clone-MCP/package.json`, `Trello-Clone-Backend/package.json`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Should `backend/src/index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.06775956284153005 - nodes in this community are weakly interconnected._
- **Why does `zustand` connect `frontend/package.json` to `useCommerceStore.ts`, `Trello-Clone-Frontend/package.json`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Should `useCommerceStore.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.14202898550724638 - nodes in this community are weakly interconnected._
- **Why does `express` connect `backend/src/index.ts` to `backend/package.json`, `Trello-Clone-Backend/package.json`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Should `Trello-Clone-Frontend/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.05587808417997097 - nodes in this community are weakly interconnected._
- **Should `Trello-Clone-MCP/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.09333333333333334 - nodes in this community are weakly interconnected._