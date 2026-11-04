# Code Style & Quality Rules

## 1. Frontend Standards
- Use TypeScript for all components and utility functions.
- Prefer functional components with React Hooks (`useState`, `useEffect`, `useCallback`, `useMemo`).
- Keep components small and focused: split large board views into `BoardHeader`, `ListContainer`, `CardItem`, `CardDetailModal`.
- Manage state with Zustand stores; avoid prop drilling deeper than 2 levels.
- Style with TailwindCSS classes; extract repeated styles to custom components or `@apply` utility rules.

## 2. Error Handling & Accessibility
- Always wrap asynchronous fetch calls in `try/catch` and provide user feedback via toast notifications.
- Ensure all interactive elements have accessible `aria-label` tags for screen readers.
- Support keyboard shortcuts for quick card navigation (e.g. `n` for new card, `esc` to close modal).
