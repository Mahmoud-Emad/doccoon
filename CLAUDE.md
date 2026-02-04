# Doccoon Project

Doccoon is a modern markdown book editor with a two-page spread interface. It supports Mermaid diagrams, LaTeX math, syntax highlighting, AI-powered writing assistance, and cloud sync.

## Project Structure

```
doccoon/
├── doccoon_backend/     # Django REST API
├── doccoon_frontend/    # Vue.js SPA
├── docker-compose.yml   # Full stack orchestration
└── .env.example         # Environment variables template
```

---

## Backend

- **Framework**: Django 6.0 + Django REST Framework
- **Language**: Python 3.14
- **Package Manager**: uv (not pip)
- **Working directory**: `doccoon_backend/`

### Common Commands

```bash
# Always run from doccoon_backend/ directory
cd doccoon_backend

# Run Django management commands
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py runserver

# Add a dependency
uv add <package>

# Update lock file
uv lock

# Run tests
uv run python manage.py test
```

### Project Structure

```
doccoon_backend/
├── config/              # Django project settings
│   ├── settings.py      # Main settings (reads from env vars)
│   ├── urls.py          # Root URL configuration
│   └── wsgi.py          # WSGI application
├── doccoon/             # Main Django app
│   ├── models/          # Database models
│   │   ├── user.py      # Custom User model
│   │   ├── book.py      # Book model
│   │   ├── page.py      # Page model
│   │   ├── settings.py  # UserSettings model
│   │   ├── sharing.py   # SharedPage, SharedBook models
│   │   └── notification.py
│   ├── views/           # API views (DRF APIView classes)
│   ├── serializers/     # DRF serializers
│   ├── services/        # Business logic / query helpers
│   ├── routes/          # URL patterns per feature
│   ├── api/             # Shared utilities
│   │   ├── permissions.py   # UserIsAuthenticated, IsBookOwner
│   │   └── response.py      # CustomResponse class
│   ├── middleware/      # Request logging middleware
│   ├── admin/           # Django admin configuration
│   └── migrations/      # Database migrations
├── components/          # Shared config (BASE_DIR, config loader)
├── Dockerfile           # Production Docker image
├── pyproject.toml       # Dependencies
└── .env.example         # Environment template
```

### Backend Conventions

1. **API Responses**: Always use `CustomResponse` class
   ```python
   from doccoon.api.response import CustomResponse
   
   return CustomResponse.success(data=serializer.data)
   return CustomResponse.bad_request(message="Invalid input")
   return CustomResponse.not_found(message="Book not found")
   return CustomResponse.unauthorized(message="Not authenticated")
   ```

2. **Permissions**: Use custom permission classes
   ```python
   from doccoon.api.permissions import UserIsAuthenticated, IsBookOwner
   
   class MyView(APIView):
       permission_classes = [UserIsAuthenticated]
   ```

3. **Service Layer**: Query logic goes in `services/`, not in views
   ```python
   # services/book_service.py
   def get_user_books(user):
       return Book.objects.filter(user=user, is_deleted=False)
   
   # views/book.py
   books = get_user_books(request.user)
   ```

4. **Soft Delete**: Never hard delete, use soft delete
   ```python
   book.is_deleted = True
   book.deleted_at = timezone.now()
   book.save()
   ```

5. **Swagger Documentation**: Add tags to all view classes
   ```python
   from drf_yasg.utils import swagger_auto_schema
   
   class BookView(APIView):
       @swagger_auto_schema(tags=["Books"])
       def get(self, request):
           ...
   ```

6. **Base Model**: All models inherit from `DoccoonBaseModel`
   - Provides: `created_at`, `modified_at`, `deleted_at`, `is_deleted`

### Environment Variables (Backend)

| Variable | Required | Description |
|----------|----------|-------------|
| `DJANGO_DEBUG` | Yes | `True` or `False` |
| `ENV` | Yes | `development`, `staging`, `production` |
| `DJANGO_SECRET_KEY` | Yes | Django secret key |
| `SERVER_DOMAIN_NAME` | Yes | API domain (e.g., `api.doccoon.com`) |
| `CLIENT_DOMAIN_NAME` | Yes | Frontend domain (e.g., `doccoon.com`) |
| `DATABASE_*` | Prod | PostgreSQL credentials (NAME, USER, PASSWORD, HOST, PORT) |
| `GOOGLE_CLIENT_ID` | No | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | No | Google OAuth secret |
| `GITHUB_CLIENT_ID` | No | GitHub OAuth client ID |
| `GITHUB_CLIENT_SECRET` | No | GitHub OAuth secret |
| `EMAIL_HOST` | No | SMTP host |
| `EMAIL` | No | SMTP email |
| `EMAIL_PASSWORD` | No | SMTP password |

---

## Frontend

- **Framework**: Vue 3 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS 4 + CSS Variables
- **Working directory**: `doccoon_frontend/`

### Common Commands

```bash
# Always run from doccoon_frontend/ directory
cd doccoon_frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production (includes TypeScript check)
npm run build

# Type check only
npm run type-check
```

### Project Structure

```
doccoon_frontend/
├── src/
│   ├── api/             # API client modules
│   │   ├── client.ts    # Base API client with auth
│   │   ├── auth.ts      # Login, register, OAuth
│   │   ├── books.ts     # Book CRUD
│   │   ├── pages.ts     # Page CRUD
│   │   ├── settings.ts  # User settings
│   │   ├── sharing.ts   # Share pages/books
│   │   ├── ai.ts        # AI rewrite/refine
│   │   └── notifications.ts
│   ├── components/
│   │   ├── ui/          # Base UI components (BaseModal, BaseIcon, etc.)
│   │   ├── home/        # Home page sections
│   │   ├── settings/    # Settings modal tabs
│   │   ├── BookPage.vue # Single page in spread
│   │   ├── BookSpread.vue # Two-page spread
│   │   ├── EditorNavbar.vue
│   │   └── ...
│   ├── composables/     # Vue composables (hooks)
│   │   ├── useBook.ts       # Book state management
│   │   ├── useSettings.ts   # User settings (synced to backend)
│   │   ├── useTheme.ts      # Dark/light theme
│   │   ├── useViewMode.ts   # Edit/view mode
│   │   ├── useLayoutMode.ts # Book/page layout
│   │   ├── useMarkdown.ts   # Markdown rendering
│   │   ├── useKeyboardShortcuts.ts
│   │   ├── useToast.ts      # Toast notifications
│   │   └── ...
│   ├── views/           # Page components
│   │   ├── Home.vue     # Landing page
│   │   ├── Editor.vue   # Main editor
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── Profile.vue
│   │   ├── Docs.vue
│   │   ├── NotFound.vue # 404 page
│   │   └── ServerError.vue # 500 page
│   ├── types/           # TypeScript types
│   ├── utils/           # Utilities (storage, logger, html)
│   ├── router/          # Vue Router config
│   ├── config/          # App constants
│   └── assets/          # Images, styles
├── public/              # Static files (favicon)
├── index.html           # Entry HTML with meta tags
├── Dockerfile           # Production Docker image
├── nginx.conf           # Nginx config for SPA
└── .env.example         # Environment template
```

### Frontend Conventions

1. **Styling**: Use Tailwind utilities with CSS variables
   ```html
   <div class="bg-[var(--bg-color)] text-[var(--text-color)] border-[var(--border-color)]">
   ```

2. **Theme Variables** (defined in `main.css`):
   - `--bg-color`, `--page-bg` - Backgrounds
   - `--text-color` - Text color
   - `--border-color` - Borders
   - `--section-alt-bg` - Alternate section background
   - `--code-bg` - Code block background
   - `bg-primary`, `text-primary` - Primary blue (#007acc)

3. **API Calls**: Use the API modules, not fetch directly
   ```typescript
   import { getBooks, createBook } from '@/api/books';
   
   const books = await getBooks();
   ```

4. **State Management**: Use composables for shared state
   ```typescript
   import { useTheme } from '@/composables/useTheme';
   
   const { isDarkTheme, toggleTheme } = useTheme();
   ```

5. **Toast Notifications**: Use useToast composable
   ```typescript
   import { useToast } from '@/composables/useToast';
   
   const toast = useToast();
   toast.success("Saved!");
   toast.error("Failed to save");
   ```

6. **Modals**: Use BaseModal component
   ```html
   <BaseModal :visible="showModal" title="My Modal" @close="showModal = false">
     <!-- content -->
   </BaseModal>
   ```

7. **Icons**: Use BaseIcon component
   ```html
   <BaseIcon name="save" :size="16" />
   ```

8. **Anonymous Users**: Check authentication state
   ```typescript
   import { isAuthenticated } from '@/api/auth';
   
   const isAnonymous = computed(() => !isAuthenticated());
   ```

### Environment Variables (Frontend)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_BASE_URL` | Yes | Backend API URL (e.g., `https://api.doccoon.com/api`) |
| `VITE_GOOGLE_CLIENT_ID` | No | Google OAuth client ID |
| `VITE_GITHUB_CLIENT_ID` | No | GitHub OAuth client ID |

---

## Docker Deployment

### Quick Start

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your values (see required variables)
nano .env

# 3. Build and start all services
docker-compose up --build -d

# 4. View logs
docker-compose logs -f
```

### Services

| Service | Port | Description |
|---------|------|-------------|
| `db` | 5432 (internal) | PostgreSQL 16 |
| `backend` | 8000 | Django API |
| `frontend` | 80 | Vue.js (nginx) |

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Rebuild specific service
docker-compose up --build backend

# View logs
docker-compose logs -f backend

# Run Django command in container
docker-compose exec backend python manage.py createsuperuser

# Access database
docker-compose exec db psql -U doccoon -d doccoon
```

---

## Development Setup

### Backend

```bash
cd doccoon_backend
cp .env.example .env
# Edit .env with development values

uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

### Frontend

```bash
cd doccoon_frontend
cp .env.example .env
# Set VITE_API_BASE_URL=http://127.0.0.1:8000/api

npm install
npm run dev
```

---

## Key Features

1. **Two-Page Book Spread**: Unique editor layout mimicking a physical book
2. **Markdown Support**: Full GFM with live preview
3. **Mermaid Diagrams**: Flowcharts, sequence diagrams, etc.
4. **LaTeX Math**: KaTeX rendering for equations
5. **Syntax Highlighting**: 100+ languages via highlight.js
6. **AI Writing Tools**: Rewrite/refine with OpenAI or Gemini
7. **Cloud Sync**: Auto-save with configurable intervals
8. **Sharing**: Share pages/books via secure links
9. **Dark/Light Theme**: System-aware with manual toggle
10. **Keyboard Shortcuts**: Comprehensive shortcut system

---

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login with email/password
- `POST /api/auth/register/` - Register new account
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/social/google/` - Google OAuth
- `POST /api/auth/social/github/` - GitHub OAuth

### Books
- `GET /api/books/` - List user's books
- `POST /api/books/` - Create book
- `GET /api/books/{id}/` - Get book details
- `PUT /api/books/{id}/` - Update book
- `DELETE /api/books/{id}/` - Delete book (soft delete)

### Pages
- `GET /api/books/{book_id}/pages/` - List pages
- `POST /api/books/{book_id}/pages/` - Create page
- `PUT /api/books/{book_id}/pages/{id}/` - Update page
- `DELETE /api/books/{book_id}/pages/{id}/` - Delete page

### Settings
- `GET /api/settings/` - Get user settings
- `PUT /api/settings/` - Update user settings

### Sharing
- `POST /api/shared/page/` - Share a page
- `POST /api/shared/book/` - Share a book
- `GET /api/shared/page/{token}/` - Get shared page (public)
- `GET /api/shared/book/{token}/` - Get shared book (public)

### AI
- `POST /api/ai/rewrite/` - Rewrite content
- `POST /api/ai/refine/` - Refine content
