# Doccoon Frontend

Vue.js SPA for the Doccoon markdown book editor.

## Requirements

- Node.js 18+
- npm

## Setup

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Edit .env
# VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## Development

```bash
npm run dev
```

Runs at http://localhost:5173

## Build

```bash
npm run build
```

Output goes to `dist/` directory.

## Type Check

```bash
npm run type-check
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_BASE_URL` | Yes | Backend API URL |
| `VITE_GOOGLE_CLIENT_ID` | No | Google OAuth client ID |
| `VITE_GITHUB_CLIENT_ID` | No | GitHub OAuth client ID |

## Docker

```bash
docker build -t doccoon-frontend .
docker run -d -p 80:80 doccoon-frontend
```

## Tech Stack

- Vue 3
- TypeScript
- Vite
- Tailwind CSS 4
- Marked.js (Markdown)
- KaTeX (Math)
- Mermaid (Diagrams)
- highlight.js (Code)
