# Full-Stack Task Manager

**A Kanban board (like Trello) where drag-and-drop updates appear instantly on everyone's screen — built with React, FastAPI, and WebSockets.**

---

## What is this?

A project management app with a drag-and-drop board:

```
┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│   To Do    │  │ In Progress│  │   Review   │  │    Done    │
│            │  │            │  │            │  │            │
│ ┌────────┐ │  │ ┌────────┐ │  │            │  │ ┌────────┐ │
│ │Design  │ │  │ │Build   │ │  │            │  │ │Setup   │ │
│ │homepage│ │  │ │REST API│ │  │            │  │ │Docker  │ │
│ │ high   │ │  │ │ high   │ │  │            │  │ │ low    │ │
│ └────────┘ │  │ └────────┘ │  │            │  │ └────────┘ │
│ ┌────────┐ │  │            │  │            │  │            │
│ │Setup   │ │  │            │  │            │  │            │
│ │CI/CD   │ │  │            │  │            │  │            │
│ │ med    │ │  │            │  │            │  │            │
│ └────────┘ │  │            │  │            │  │            │
└────────────┘  └────────────┘  └────────────┘  └────────────┘
```

When you drag a task from "To Do" to "In Progress", everyone else looking at the same board sees it move **instantly** — no page refresh needed. That's the WebSocket real-time sync.

---

## What problem does this solve?

**Without this:** Your team uses Jira ($10/user/month) or a whiteboard. With most self-hosted alternatives, if Alice drags a task on her screen, Bob doesn't see it until he refreshes. People work on the same task without knowing. Tasks get lost.

**With this:** Changes sync in real-time across all browsers. You can search across all tasks and comments instantly. It's self-hosted (your data stays on your server) and free. One `docker compose up` and it's running.

---

## What can you do with it?

| Feature | How it works | Technical Details |
|---------|-------------|-------------------|
| **Kanban board** | Drag tasks between columns | `react-beautiful-dnd` library. Drop triggers optimistic UI update + API call + WebSocket broadcast. |
| **Real-time sync** | Changes appear instantly on all browsers | WebSocket per project room. Server broadcasts via `ConnectionManager`. No polling. |
| **Multiple projects** | Each project has its own board with custom columns | Project → Columns → Tasks hierarchy. Board state fetched in one query with eager loading. |
| **Task details** | Title, description, priority, due date, labels | Priority stored as enum (critical/high/medium/low). Labels stored as JSONB array for flexible filtering. |
| **Comments** | Comment on tasks, @mention teammates | `@username` parsed and stored as mention. Could trigger notifications (webhook-ready). |
| **Full-text search** | Type a keyword → finds matching tasks and comments | PostgreSQL `tsvector` + `ts_query`. GIN index for sub-10ms search across 100K+ records. |
| **Assign people** | Assign tasks, filter board by assignee | Many-to-many relationship. Filter applied at query level, not client-side. |

---

## How the real-time sync works

```
Alice's browser ◀──── WebSocket ────▶ Server ◀──── WebSocket ────▶ Bob's browser
      │                                 │                                │
      │  1. Alice drags "Build API"     │                                │
      │     from "To Do" → "In Progress"│                                │
      │                                 │                                │
      │  2. Optimistic update:          │                                │
      │     UI moves card immediately   │                                │
      │     (no waiting for server)     │                                │
      │                                 │                                │
      │  3. REST API call:              │                                │
      │     PATCH /api/tasks/42         │                                │
      │     {column_id: 2, position: 0} │                                │
      │     ──────────────────────────▶ │                                │
      │                                 │  4. Server saves to DB          │
      │                                 │                                │
      │                                 │  5. Broadcasts to all           │
      │                                 │     connected clients           │
      │                                 │     in project room:            │
      │                                 │     {type: "task_moved",        │
      │                                 │      task_id: 42,               │
      │                                 │      column_id: 2,              │
      │                                 │      position: 0}               │
      │                                 │     ──────────────────────────▶ │
      │                                 │                                │
      │                                 │                   6. Bob's UI   │
      │                                 │                   moves the card│
      │                                 │                   automatically │
```

### Why this architecture?

- **Optimistic updates** — Alice sees the card move immediately. If the API fails, the UI reverts. This makes drag-and-drop feel instant even on slow connections.
- **REST for mutations, WebSocket for broadcasts** — Mutations go through REST (easier to validate, retry, rate limit). WebSocket is only used for pushing updates to other clients.
- **Room-based connections** — Each project is a "room." When you open a board, your WebSocket joins that room. You only receive events for the board you're looking at. Reduces noise and bandwidth.
- **ConnectionManager pattern** — Server tracks `{project_id: [websocket1, websocket2, ...]}`. On any change, it iterates and sends to all connections in that room except the sender.

---

## Full-text search implementation

```python
# PostgreSQL tsvector column — auto-updated on INSERT/UPDATE
class Task(Base):
    title = Column(String)
    description = Column(Text)
    search_vector = Column(TSVector)  # GIN-indexed for fast lookup

    __table_args__ = (
        Index('ix_task_search', 'search_vector', postgresql_using='gin'),
    )

# Search query — uses ts_query for ranked results
# "build api" → finds tasks with "build" AND "api" anywhere in title/description
# Returns results ranked by relevance (ts_rank), sub-10ms on 100K rows
```

---

## Database schema

```
┌──────────┐       ┌──────────┐       ┌──────────┐       ┌──────────┐
│ projects │       │ columns  │       │  tasks   │       │ comments │
├──────────┤       ├──────────┤       ├──────────┤       ├──────────┤
│ id (PK)  │──┐    │ id (PK)  │──┐    │ id (PK)  │──┐    │ id (PK)  │
│ name     │  └───▶│ project_id│  └───▶│ column_id│  └───▶│ task_id  │
│ created  │       │ title    │       │ title    │       │ author_id│
└──────────┘       │ position │       │ position │       │ body     │
                   └──────────┘       │ priority │       │ mentions │
                                      │ due_date │       └──────────┘
                                      │ labels   │ (JSONB)
                                      │ search_vector │ (tsvector, GIN index)
                                      └──────────┘
```

---

## How to use it

```bash
# 1. Clone
git clone https://github.com/vmunjal2503/fullstack-task-manager.git
cd fullstack-task-manager

# 2. Configure
cp .env.example .env

# 3. Start
docker compose up -d

# 4. Open
# App:       http://localhost:3000
# API docs:  http://localhost:8000/docs
```

---

## How is the code organized?

```
fullstack-task-manager/
├── frontend/                          # What the user sees (React + TypeScript)
│   ├── src/components/KanbanBoard.tsx # Drag-and-drop board (react-beautiful-dnd)
│   ├── src/hooks/useWebSocket.ts      # WebSocket hook: connect, reconnect, message handler
│   ├── src/pages/index.tsx            # Dashboard with project list
│   └── src/lib/api.ts                 # Axios client for REST endpoints
│
├── backend/                           # The brain (FastAPI + Python)
│   ├── app/api/tasks.py               # CRUD + move task (PATCH with column_id + position)
│   ├── app/api/projects.py            # Project CRUD + full board endpoint (eager-loaded)
│   ├── app/api/comments.py            # Comments with @mention parsing
│   ├── app/api/search.py              # Full-text search via PostgreSQL ts_query
│   ├── app/api/websocket.py           # WebSocket endpoint: join room, receive/broadcast events
│   ├── app/services/ws_manager.py     # ConnectionManager: tracks connections per project room
│   └── app/models/task.py             # SQLAlchemy models with tsvector + GIN index
│
├── docker-compose.yml                 # Frontend + Backend + PostgreSQL + Redis
└── .env.example
```

---

## Who is this for?

- Small teams that want a free, self-hosted alternative to Trello/Jira
- Developers learning how to build real-time apps with WebSockets
- Anyone who wants to see how a modern full-stack app is structured (React + FastAPI + PostgreSQL + WebSocket)

---

Built by **Vikas Munjal** | Open source under MIT License
