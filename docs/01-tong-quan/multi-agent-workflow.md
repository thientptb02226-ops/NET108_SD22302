# Multi-Agent Workflow Guide

## How to Run Multiple AI CLI Agents Simultaneously

### Step 1: Open Terminal 1 for Claude Code CLI
```bash
# In project root
claude
# Claude will automatically read CLAUDE.md, AGENTS.md, and .claude/
```

### Step 2: Open Terminal 2 for Antigravity / Gemini CLI or Codex
```bash
# In project root
agy
# Or run with Antigravity IDE / Codex CLI
```

### Step 3: Assign Tasks Without Conflict
- Give Claude tasks focused on UI/UX:
  > *"Claude, implement the draggable card component in Trello-Clone-Frontend with smooth animations."*
- Give Antigravity/Codex tasks focused on Backend/API/MCP:
  > *"Antigravity, implement the card reordering endpoint in Trello-Clone-Backend and expose it via Trello-Clone-MCP."*

### Step 4: Automatic Synchronization
Both agents commit to the shared git repo with tagged commits (`[agent:claude]` and `[agent:anti]`), ensuring smooth collaboration without merge conflicts.

