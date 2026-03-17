"""Task CRUD and Kanban operations."""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

router = APIRouter()


class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: str
    column_id: str
    priority: Priority = Priority.MEDIUM
    assignee_id: Optional[str] = None
    due_date: Optional[str] = None
    labels: list[str] = []


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    assignee_id: Optional[str] = None
    due_date: Optional[str] = None
    labels: Optional[list[str]] = None


class MoveTaskRequest(BaseModel):
    column_id: str
    position: int  # Position within the column (0-based)


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    project_id: str
    column_id: str
    column_name: str
    priority: str
    assignee: Optional[dict]
    due_date: Optional[str]
    labels: list[str]
    comment_count: int
    created_at: str
    updated_at: str


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    project_id: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[Priority] = None,
    assignee_id: Optional[str] = None,
):
    """List tasks with optional filters."""
    return [
        {
            "id": "task_1",
            "title": "Design homepage mockup",
            "description": "Create high-fidelity mockup for the new homepage",
            "project_id": "proj_1",
            "column_id": "col_1",
            "column_name": "To Do",
            "priority": "high",
            "assignee": {"id": "user_1", "name": "Vikas M."},
            "due_date": "2024-02-01",
            "labels": ["design", "frontend"],
            "comment_count": 3,
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-16T14:30:00Z",
        }
    ]


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(data: CreateTaskRequest):
    """Create a new task in a project column."""
    return {
        "id": "task_new",
        "title": data.title,
        "description": data.description,
        "project_id": data.project_id,
        "column_id": data.column_id,
        "column_name": "To Do",
        "priority": data.priority,
        "assignee": None,
        "due_date": data.due_date,
        "labels": data.labels,
        "comment_count": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, data: UpdateTaskRequest):
    """Update task fields."""
    return {
        "id": task_id,
        "title": data.title or "Updated Task",
        "description": data.description,
        "project_id": "proj_1",
        "column_id": "col_1",
        "column_name": "To Do",
        "priority": data.priority or "medium",
        "assignee": None,
        "due_date": data.due_date,
        "labels": data.labels or [],
        "comment_count": 0,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": datetime.utcnow().isoformat(),
    }


@router.patch("/{task_id}/move")
async def move_task(task_id: str, data: MoveTaskRequest):
    """Move task to a different column (drag-and-drop on Kanban)."""
    # In production: update column_id, reorder positions,
    # broadcast via WebSocket to other clients
    return {
        "id": task_id,
        "column_id": data.column_id,
        "position": data.position,
        "message": "Task moved successfully",
    }


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """Delete a task."""
    return None
