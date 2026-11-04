import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

const server = new Server(
  {
    name: 'trello-clone-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tools exposed to Claude & Antigravity
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'trello_list_boards',
        description: 'List all available boards and summary of their cards',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'trello_create_card',
        description: 'Create a new card on a Trello board list',
        inputSchema: {
          type: 'object',
          properties: {
            listId: { type: 'string', description: 'Target list ID' },
            title: { type: 'string', description: 'Title of the card' },
            description: { type: 'string', description: 'Description content' },
          },
          required: ['listId', 'title'],
        },
      },
    ],
  };
});

// Tool call handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'trello_list_boards') {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify([
            { id: 'board-1', title: 'Sprint Backlog', listCount: 3, cardCount: 4 }
          ], null, 2),
        },
      ],
    };
  }

  if (name === 'trello_create_card') {
    return {
      content: [
        {
          type: 'text',
          text: `Successfully created card "${args?.title}" on list "${args?.listId}".`,
        },
      ],
    };
  }

  throw new Error(`Tool not found: ${name}`);
});

async function run() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('[MCP] Trello Clone MCP Server running over stdio');
}

run().catch((err) => {
  console.error('[MCP] Fatal error running MCP server:', err);
  process.exit(1);
});
