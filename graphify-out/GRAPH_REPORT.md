# Graph Report - Net108Khai  (2026-11-05)

## Corpus Check
- 30 files · ~332,443 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 2, .mdc 1, .example 1)

## Summary
- 303 nodes · 369 edges · 20 communities (13 shown, 7 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b7b3c3a3`
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
- create_full_lab1_document
- main.py
- ref_node_fs
- App.tsx
- .agent/skills/idea-refine/scripts/idea-refine.sh
- .claude/skills/idea-refine/scripts/idea-refine.sh
- skills/idea-refine/scripts/idea-refine.sh

## God Nodes (most connected - your core abstractions)
1. `create_lab1_ainative_document()` - 12 edges
2. `generate_lab1_docx()` - 11 edges
3. `create_full_lab1_document()` - 10 edges
4. `compilerOptions` - 10 edges
5. `compilerOptions` - 9 edges
6. `typescript` - 8 edges
7. `scripts` - 8 edges
8. `postgres` - 7 edges
9. `redis` - 6 edges
10. `scripts` - 5 edges

## Surprising Connections (you probably didn't know these)
- `typescript@^5.5.2` --declares--> `typescript`  [EXTRACTED]
  Trello-Clone-Frontend/package.json → Chatbot-Frontend/package.json
- `typescript@^5.5.2` --declares--> `typescript`  [EXTRACTED]
  Trello-Clone-Backend/package.json → Chatbot-Frontend/package.json
- `typescript@^5.5.2` --declares--> `typescript`  [EXTRACTED]
  Trello-Clone-MCP/package.json → Chatbot-Frontend/package.json
- `dotenv@^16.4.5` --declares--> `dotenv`  [EXTRACTED]
  Trello-Clone-Backend/package.json → Trello-Clone-MCP/package.json
- `@types/react@^18.3.3` --declares--> `@types/react`  [EXTRACTED]
  Trello-Clone-Frontend/package.json → Chatbot-Frontend/package.json

## Import Cycles
- None detected.

## Communities (20 total, 7 thin omitted)

### Community 0 - "Trello-Clone-Backend/package.json"
Cohesion: 0.07
Nodes (32): cors, express, jsonwebtoken, socket.io, @types/cors, @types/express, @types/jsonwebtoken, zod (+24 more)

### Community 1 - "Trello-Clone-Frontend/package.json"
Cohesion: 0.08
Nodes (33): @types/react-dom@^18.3.0, @types/react-dom, autoprefixer, @dnd-kit/core, @dnd-kit/sortable, @dnd-kit/utilities, postcss, socket.io-client (+25 more)

### Community 2 - "Chatbot-Frontend/package.json"
Cohesion: 0.10
Nodes (25): dependencies, lucide-react@^0.395.0, react@^18.3.1, react-dom@^18.3.1, description, devDependencies, @types/react@^18.3.3, typescript@^5.5.2 (+17 more)

### Community 3 - "Trello-Clone-MCP/package.json"
Cohesion: 0.08
Nodes (26): typescript, axios, @modelcontextprotocol/sdk, dotenv@^16.4.5, @types/node@^20.14.9, typescript@^5.5.2, dependencies, axios@^1.7.2 (+18 more)

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

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `typescript` connect `Trello-Clone-MCP/package.json` to `Trello-Clone-Backend/package.json`, `Trello-Clone-Frontend/package.json`, `Chatbot-Frontend/package.json`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Should `Trello-Clone-Backend/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.07301587301587302 - nodes in this community are weakly interconnected._
- **Why does `devDependencies` connect `Trello-Clone-Frontend/package.json` to `Chatbot-Frontend/package.json`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Should `Trello-Clone-Frontend/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.0784313725490196 - nodes in this community are weakly interconnected._
- **Should `Chatbot-Frontend/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.09538461538461539 - nodes in this community are weakly interconnected._
- **Should `Trello-Clone-MCP/package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.08374384236453201 - nodes in this community are weakly interconnected._
- **Should `generate_lab1.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08097165991902834 - nodes in this community are weakly interconnected._