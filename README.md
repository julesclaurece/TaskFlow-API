# TaskFlow API

> Freelancers and teams waste time juggling tasks across sticky notes, spreadsheets, and emails — things fall through the cracks and deadlines are missed. TaskFlow centralizes everything in one place with a clean REST API and a visual Kanban frontend.

A task management REST API built with **Django REST Framework**. Supports JWT authentication, project organization, task CRUD with filtering, pagination, and full Swagger documentation.

**Live API:** `https://taskflow-api-production-0a90.up.railway.app`  
**Swagger Docs:** `https://taskflow-api-production-0a90.up.railway.app/api/docs/`  
**Frontend:** `https://taskflow-client-cyan.vercel.app`

---

## Features

- JWT Authentication (register, login, refresh token)
- Projects — create and organize tasks by project
- Tasks — full CRUD with status, priority, due date, assignee
- Filtering — by status, priority, project, due date range, title search
- Pagination — 10 results per page, configurable
- Ordering — sort by created date, due date, priority
- Swagger UI — interactive API documentation at `/api/docs/`
- ReDoc — alternative docs at `/api/redoc/`

## Tech Stack

| Layer | Tech |
|---|---|
| Framework | Django 6 + Django REST Framework |
| Auth | JWT via `djangorestframework-simplejwt` |
| Database | PostgreSQL (Neon) / SQLite (local) |
| Filters | `django-filter` |
| Docs | `drf-spectacular` (OpenAPI 3) |
| Deployment | Railway |

---

## API Endpoints

### Authentication
```
POST /api/auth/register/     — Create account, returns JWT tokens
POST /api/auth/login/        — Login, returns JWT tokens
POST /api/auth/token/refresh/ — Refresh access token
GET  /api/auth/me/           — Current user profile
```

### Projects
```
GET    /api/projects/         — List your projects
POST   /api/projects/         — Create a project
GET    /api/projects/{id}/    — Get project detail
PUT    /api/projects/{id}/    — Update project
DELETE /api/projects/{id}/    — Delete project
GET    /api/projects/{id}/tasks/ — List tasks for a project
```

### Tasks
```
GET    /api/tasks/            — List tasks (with filters)
POST   /api/tasks/            — Create a task
GET    /api/tasks/{id}/       — Get task detail
PUT    /api/tasks/{id}/       — Update task
PATCH  /api/tasks/{id}/       — Partial update
DELETE /api/tasks/{id}/       — Delete task
```

### Filters (GET /api/tasks/)
```
?status=todo|in_progress|done
?priority=low|medium|high
?project=<id>
?search=<title keyword>
?due_date_before=YYYY-MM-DD
?due_date_after=YYYY-MM-DD
?ordering=due_date|-created_at|priority
```

---

## Quick Start

```bash
git clone https://github.com/julesclaurece/TaskFlow-API
cd taskflow-api

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

cp .env.example .env         # fill in your values

python manage.py migrate
python manage.py runserver
```

Open `http://localhost:8000/api/docs/` to explore the API interactively.

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | insecure dev key |
| `DEBUG` | Debug mode | `True` |
| `DATABASE_URL` | PostgreSQL URL | SQLite (local) |
| `ALLOWED_HOSTS` | Comma-separated hosts | `*` |
| `CORS_ALLOW_ALL_ORIGINS` | Allow all CORS origins | `True` |

---

## Example Usage

**Register and get tokens:**
```bash
curl -X POST https://taskflow-api-production-0a90.up.railway.app/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"Secure123!"}'
```

**Create a task:**
```bash
curl -X POST https://taskflow-api-production-0a90.up.railway.app/api/tasks/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Build landing page","priority":"high","status":"todo","due_date":"2024-02-01"}'
```

**Filter tasks:**
```bash
curl "https://taskflow-api-production-0a90.up.railway.app/api/tasks/?status=in_progress&priority=high&ordering=-due_date" \
  -H "Authorization: Bearer <your_access_token>"
```
