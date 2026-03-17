# Full-Stack Task Manager — React + FastAPI + PostgreSQL

A real-time project management app with Kanban boards, team collaboration, and activity tracking. Built as a production reference architecture.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Architecture                                │
│                                                                     │
│  ┌──────────────────────────┐       ┌────────────────────────────┐  │
│  │   Frontend (React + TS)  │       │   Backend (FastAPI)        │  │
│  │                          │ REST  │                            │  │
│  │  ┌─────────────────────┐ │──────▶│  • CRUD APIs              │  │
│  │  │   Kanban Board      │ │ API   │  • WebSocket (live sync)  │  │
│  │  │   ┌───┐ ┌───┐ ┌───┐│ │◀──────│  • File uploads (S3)     │  │
│  │  │   │To │ │In │ │Don││ │       │  • Activity logging       │  │
│  │  │   │Do │ │Pro││ │e  ││ │ WS    │  • Search (full-text)    │  │
│  │  │   │   │ │   ││ │   ││ │◀────▶│  • Export (CSV/PDF)      │  │
│  │  │   └───┘ └───┘ └───┘│ │       │                            │  │
│  │  └─────────────────────┘ │       └────────────┬───────────────┘  │
│  │                          │                    │                   │
│  │  • Drag & drop tasks     │       ┌────────────▼───────────────┐  │
│  │  • Real-time updates     │       │   PostgreSQL + Redis       │  │
│  │  • Filter & search       │       │                            │  │
│  │  • Dark/Light mode       │       │  • Full-text search index  │  │
│  │  • Responsive design     │       │  • WebSocket pub/sub      │  │
│  └──────────────────────────┘       └────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

## Features

### Task Management
- [x] Create, edit, delete tasks with rich text descriptions
- [x] Kanban board with drag-and-drop between columns
- [x] Custom columns (To Do, In Progress, Review, Done — or your own)
- [x] Priority levels (Critical, High, Medium, Low)
- [x] Due dates with overdue highlighting
- [x] Labels/tags for categorization
- [x] Assignee management

### Project Organization
- [x] Multiple projects with separate boards
- [x] Project-level settings and member access
- [x] Activity feed (who did what, when)
- [x] Dashboard with analytics (tasks completed, velocity, burndown)

### Collaboration
- [x] Real-time updates via WebSocket (instant sync across browsers)
- [x] Comments on tasks with @mentions
- [x] File attachments (images, docs)
- [x] Email notifications on assignment/mention

### Search & Export
- [x] Full-text search across tasks, comments, and descriptions
- [x] Advanced filters (status, priority, assignee, date range)
- [x] Export to CSV
- [x] Export to PDF report

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, Tailwind CSS, React DnD, React Query |
| Backend | FastAPI, Python 3.12, SQLAlchemy 2.0, WebSockets |
| Database | PostgreSQL 16 (full-text search), Redis (WebSocket pub/sub) |
| Storage | AWS S3 (file attachments) |
| Infra | Docker Compose, GitHub Actions |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/vmunjal2503/fullstack-task-manager.git
cd fullstack-task-manager

# 2. Set up environment
cp .env.example .env

# 3. Start
docker compose up -d

# 4. Run migrations
docker compose exec backend alembic upgrade head

# 5. Seed sample data
docker compose exec backend python -m app.seed

# Frontend: http://localhost:3000
# API docs: http://localhost:8000/docs
```

## Project Structure

```
fullstack-task-manager/
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/        # KanbanBoard, TaskCard, TaskModal, etc.
│   │   ├── pages/             # Dashboard, Projects, Board, Settings
│   │   ├── hooks/             # useTasks, useProjects, useWebSocket
│   │   └── lib/               # API client, types, utilities
│   └── public/
├── backend/                   # FastAPI application
│   ├── app/
│   │   ├── api/               # tasks, projects, comments, search
│   │   ├── models/            # SQLAlchemy models
│   │   └── services/          # Business logic, WebSocket manager
│   └── migrations/
├── docker-compose.yml
└── .github/workflows/
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/projects` | List all projects |
| POST | `/api/projects` | Create project |
| GET | `/api/projects/{id}/board` | Get Kanban board |
| GET | `/api/tasks` | List/filter tasks |
| POST | `/api/tasks` | Create task |
| PATCH | `/api/tasks/{id}` | Update task (status, assignee, etc.) |
| PATCH | `/api/tasks/{id}/move` | Move task between columns |
| POST | `/api/tasks/{id}/comments` | Add comment |
| GET | `/api/search?q=...` | Full-text search |
| GET | `/api/export/csv?project_id=...` | Export to CSV |
| WS | `/ws/{project_id}` | Real-time board updates |

---

Built by **Vikas Munjal** | Open source under MIT License
