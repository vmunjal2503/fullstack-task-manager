"""
Task Manager — FastAPI Backend
Full-stack project management with Kanban boards and real-time sync.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import tasks, projects, comments, search, websocket

app = FastAPI(
    title="Task Manager API",
    description="Project management API with Kanban boards, real-time sync, and search",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(comments.router, prefix="/api/tasks", tags=["Comments"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(websocket.router, tags=["WebSocket"])


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "task-manager"}
