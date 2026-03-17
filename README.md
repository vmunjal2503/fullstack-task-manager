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
│ │ 🔴 high│ │  │ │ 🔴 high│ │  │            │  │ │ 🟢 low │ │
│ └────────┘ │  │ └────────┘ │  │            │  │ └────────┘ │
│ ┌────────┐ │  │            │  │            │  │            │
│ │Setup   │ │  │            │  │            │  │            │
│ │CI/CD   │ │  │            │  │            │  │            │
│ │ 🟡 med │ │  │            │  │            │  │            │
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

| Feature | How it works |
|---------|-------------|
| **Kanban board** | Drag tasks between columns (To Do → In Progress → Done) |
| **Real-time sync** | Uses WebSocket — changes appear instantly on all connected browsers |
| **Multiple projects** | Each project has its own board with custom columns |
| **Task details** | Title, description, priority (critical/high/medium/low), due date, labels |
| **Comments** | Comment on tasks, @mention teammates to notify them |
| **Search** | Type a keyword → finds matching tasks and comments instantly (PostgreSQL full-text search) |
| **Assign people** | Assign tasks to team members, filter board by assignee |

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

## How does the real-time sync work?

```
Alice's browser ◀──── WebSocket ────▶ Server ◀──── WebSocket ────▶ Bob's browser
      │                                 │                                │
      │  Alice drags "Build API"        │                                │
      │  from "To Do" to "In Progress"  │                                │
      │                                 │                                │
      │  ──── sends event ────────────▶ │                                │
      │                                 │  ──── broadcasts to Bob ─────▶ │
      │                                 │                                │
      │                                 │                   Bob sees the │
      │                                 │                   task move    │
      │                                 │                   instantly    │
```

No polling. No refreshing. Instant.

---

## How is the code organized?

```
fullstack-task-manager/
├── frontend/                          # What the user sees
│   ├── src/components/KanbanBoard.tsx # The drag-and-drop board
│   ├── src/hooks/useWebSocket.ts      # Connects to server for real-time updates
│   ├── src/pages/index.tsx            # Dashboard with project overview
│   └── src/lib/api.ts                 # Talks to the backend
│
├── backend/                           # The brain
│   ├── app/api/projects.py            # Create projects, get board data
│   ├── app/api/tasks.py               # Create/edit/move/delete tasks
│   ├── app/api/comments.py            # Add comments with @mentions
│   ├── app/api/search.py              # Full-text search across everything
│   ├── app/api/websocket.py           # Real-time connection handler
│   ├── app/services/ws_manager.py     # Tracks who's connected, broadcasts changes
│   └── app/models/task.py             # Database tables (Project, Column, Task, Comment)
│
├── docker-compose.yml                 # Starts everything: frontend + backend + PostgreSQL + Redis
└── .env.example
```

---

## Who is this for?

- Small teams that want a free, self-hosted alternative to Trello/Jira
- Developers learning how to build real-time apps with WebSockets
- Anyone who wants to see how a modern full-stack app is structured (React + FastAPI + PostgreSQL)

---

Built by **Vikas Munjal** | Open source under MIT License
