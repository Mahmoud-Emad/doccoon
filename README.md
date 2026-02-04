# Doccoon

A modern markdown book editor with a two-page spread interface. Supports Mermaid diagrams, LaTeX math, syntax highlighting, AI-powered writing assistance, and cloud sync.

**Live Demo:** [https://doccoon.com](https://doccoon.com)

## Features

- Two-page book spread editor
- Full Markdown support (GFM)
- Mermaid diagrams (flowcharts, sequence diagrams, etc.)
- LaTeX math rendering (KaTeX)
- Syntax highlighting (100+ languages)
- AI writing tools (OpenAI/Gemini integration)
- Cloud sync with auto-save
- Share pages/books via secure links
- Dark/Light theme
- Keyboard shortcuts

## Project Structure

```
doccoon/
├── doccoon_backend/     # Django REST API
├── doccoon_frontend/    # Vue.js SPA
├── docker-compose.yml   # Full stack orchestration
└── .env.example         # Environment variables template
```

## Quick Start with Docker

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your values
nano .env

# 3. Build and start all services
docker-compose up --build -d
```

Services will be available at:
- Frontend: http://localhost (port 80)
- Backend API: http://localhost:8000
- Database: PostgreSQL on port 5432 (internal)

## Development Setup

### Backend (Django)

```bash
cd doccoon_backend
cp .env.example .env
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

### Frontend (Vue.js)

```bash
cd doccoon_frontend
cp .env.example .env
npm install
npm run dev
```

See individual README files in each directory for more details.

## Tech Stack

**Backend:**
- Python 3.14
- Django 6.0 + Django REST Framework
- PostgreSQL
- uv (package manager)

**Frontend:**
- Vue 3 + TypeScript
- Vite
- Tailwind CSS 4

## License

MIT

## Author

2025 Doccoon
