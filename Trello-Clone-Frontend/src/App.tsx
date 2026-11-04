import React, { useState } from 'react';

interface Card {
  id: string;
  title: string;
}

interface Column {
  id: string;
  title: string;
  cards: Card[];
}

export default function App() {
  const [columns] = useState<Column[]>([
    {
      id: 'col-1',
      title: '📋 To Do',
      cards: [
        { id: 'c-1', title: 'Initialize Multi-Agent Monorepo' },
        { id: 'c-2', title: 'Connect Claude Code & Antigravity' }
      ]
    },
    {
      id: 'col-2',
      title: '⚡ In Progress',
      cards: [
        { id: 'c-3', title: 'Setup MCP Reference Architecture' }
      ]
    },
    {
      id: 'col-3',
      title: '✅ Done',
      cards: [
        { id: 'c-4', title: 'Scaffold Workspace Directories' }
      ]
    }
  ]);

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: '24px', backgroundColor: '#0f172a', minHeight: '100vh', color: '#f8fafc' }}>
      <header style={{ marginBottom: '24px', borderBottom: '1px solid #334155', paddingBottom: '16px' }}>
        <h1 style={{ fontSize: '24px', fontWeight: 'bold' }}>Trello Clone — AI-Powered Kanban</h1>
        <p style={{ color: '#94a3b8', fontSize: '14px', marginTop: '4px' }}>
          Collaborative board managed by Claude Code CLI & Antigravity
        </p>
      </header>

      <div style={{ display: 'flex', gap: '20px', alignItems: 'flex-start', overflowX: 'auto' }}>
        {columns.map((col) => (
          <div
            key={col.id}
            style={{
              backgroundColor: '#1e293b',
              borderRadius: '8px',
              width: '280px',
              padding: '16px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
            }}
          >
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '12px' }}>{col.title}</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {col.cards.map((card) => (
                <div
                  key={card.id}
                  style={{
                    backgroundColor: '#334155',
                    borderRadius: '6px',
                    padding: '10px 12px',
                    fontSize: '14px',
                    cursor: 'grab'
                  }}
                >
                  {card.title}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
