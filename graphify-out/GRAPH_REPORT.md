# Graph Report - Net108Khai  (2026-11-05)

## Corpus Check
- 32 files · ~352,111 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .mdc 1, .example 1)

## Summary
- 319 nodes · 413 edges · 23 communities (18 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `60beb08e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Trello-Clone-Backend/package.json
- Trello-Clone-Frontend/package.json
- Chatbot-Frontend/package.json
- Trello-Clone-MCP/package.json
- generate_lab1.py
- postgres
- package.json
- Trello-Clone-Mobile/package.json
- Trello-Clone-Desktop/package.json
- compilerOptions
- compilerOptions
- create_lab1_document
- main.py
- ref_node_fs
- App.tsx
- generate_enhanced_diagrams.py
- .agent/skills/idea-refine/scripts/idea-refine.sh
- .claude/skills/idea-refine/scripts/idea-refine.sh
- skills/idea-refine/scripts/idea-refine.sh
- typescript
- devDependencies
- scripts

## God Nodes (most connected - your core abstractions)
1. `create_lab1_document()` - 14 edges
2. `generate_lab1_docx()` - 11 edges
3. `create_full_lab1_document()` - 10 edges
4. `compilerOptions` - 10 edges
5. `compilerOptions` - 9 edges
6. `typescript` - 8 edges
7. `scripts` - 8 edges
8. `draw_arrow()` - 7 edges
9. `postgres` - 7 edges
10. `redis` - 6 edges

## Surprising Connections (you probably didn't know these)
- `typescript@^5.5.2` --declares--> `typescript`  [EXTRACTED]
  Trello-Clone-Backend/package.json → Chatbot-Frontend/package.json
- `typescript@^5.5.2` --declares--> `typescript`  [EXTRACTED]
  Trello-Clone-Frontend/package.json → Chatbot-Frontend/package.json
- `typescript@^5.5.2` --declares--> `typescript`  [EXTRACTED]
  Trello-Clone-MCP/package.json → Chatbot-Frontend/package.json
- `lucide-react@^0.395.0` --declares--> `lucide-react`  [EXTRACTED]
  Trello-Clone-Frontend/package.json → Chatbot-Frontend/package.json
- `react-dom@^18.3.1` --declares--> `react-dom`  [EXTRACTED]
  Trello-Clone-Frontend/package.json → Chatbot-Frontend/package.json

## Import Cycles
- None detected.

## Communities (23 total, 5 thin omitted)

### Community 0 - "Trello-Clone-Backend/package.json"
Cohesion: 0.07
Nodes (32): cors, express, jsonwebtoken, socket.io, @types/cors, @types/express, @types/jsonwebtoken, zod (+24 more)

### Community 1 - "Trello-Clone-Frontend/package.json"
Cohesion: 0.16
Nodes (16): @dnd-kit/core, @dnd-kit/sortable, @dnd-kit/utilities, socket.io-client, zustand, dependencies, @dnd-kit/core@^6.1.0, @dnd-kit/sortable@^8.0.0 (+8 more)

### Community 2 - "Chatbot-Frontend/package.json"
Cohesion: 0.15
Nodes (15): dependencies, lucide-react@^0.395.0, react@^18.3.1, react-dom@^18.3.1, description, lucide-react, react, react-dom (+7 more)

### Community 3 - "Trello-Clone-MCP/package.json"
Cohesion: 0.08
Nodes (27): typescript, axios, @modelcontextprotocol/sdk, dotenv@^16.4.5, @types/node@^20.14.9, typescript@^5.5.2, typescript@^5.5.2, dependencies (+19 more)

### Community 4 - "generate_lab1.py"
Cohesion: 0.08
Nodes (4): generate_lab1_docx(), create_full_lab1_document(), insert_missing_section(), style_table()

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

### Community 12 - "main.py"
Cohesion: 0.25
Nodes (3): health_check(), SearchQuery, semantic_search()

### Community 13 - "ref_node_fs"
Cohesion: 0.29
Nodes (3): [tool, file, ...extra], [tool, file, ...extra], [tool, file, ...extra]

### Community 14 - "App.tsx"
Cohesion: 0.38
Nodes (3): App(), Card, Column

### Community 15 - "generate_enhanced_diagrams.py"
Cohesion: 0.35
Nodes (9): build_admin_diagram(), build_agent_diagram(), build_customer_diagram(), build_general_diagram(), draw_actor(), draw_arrow(), draw_dashed_line(), draw_ellipse_uc() (+1 more)

### Community 20 - "typescript"
Cohesion: 0.20
Nodes (10): devDependencies, @types/react@^18.3.3, typescript@^5.5.2, vite@^5.3.1, @vitejs/plugin-react@^4.3.1, @types/react, vite, @vitejs/plugin-react (+2 more)

### Community 21 - "devDependencies"
Cohesion: 0.17
Nodes (12): @types/react-dom@^18.3.0, @types/react-dom, autoprefixer, postcss, tailwindcss, devDependencies, autoprefixer@^10.4.19, postcss@^8.4.38 (+4 more)

### Community 22 - "scripts"
Cohesion: 0.50
Nodes (4): scripts, build, dev, preview

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `typescript` connect `Trello-Clone-MCP/package.json` to `Trello-Clone-Backend/package.json`, `Trello-Clone-Frontend/package.json`, `Chatbot-Frontend/package.json`, `typescript`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Should `Trello-Clone-Backend/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.07301587301587302 - nodes in this community are weakly interconnected._
- **Why does `create_lab1_document()` connect `create_lab1_document` to `generate_lab1.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Should `Trello-Clone-MCP/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.08045977011494253 - nodes in this community are weakly interconnected._
- **Should `generate_lab1.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08414634146341464 - nodes in this community are weakly interconnected._
- **Should `postgres` be split into smaller, more focused modules?**
  _Cohesion score 0.07142857142857142 - nodes in this community are weakly interconnected._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._