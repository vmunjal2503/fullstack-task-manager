"""Project management endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class CreateProjectRequest(BaseModel):
    name: str
    description: Optional[str] = None
    columns: list[str] = ["To Do", "In Progress", "Review", "Done"]


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    columns: list[dict]
    task_count: int
    member_count: int
    created_at: str


@router.get("/", response_model=list[ProjectResponse])
async def list_projects():
    """List all projects for the current user."""
    return [
        {
            "id": "proj_1",
            "name": "Website Redesign",
            "description": "Complete redesign of the company website",
            "columns": [
                {"id": "col_1", "name": "To Do", "order": 0},
                {"id": "col_2", "name": "In Progress", "order": 1},
                {"id": "col_3", "name": "Review", "order": 2},
                {"id": "col_4", "name": "Done", "order": 3},
            ],
            "task_count": 24,
            "member_count": 4,
            "created_at": "2024-01-15T00:00:00Z",
        }
    ]


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(data: CreateProjectRequest):
    """Create a new project with default columns."""
    columns = [
        {"id": f"col_{i}", "name": name, "order": i}
        for i, name in enumerate(data.columns)
    ]
    return {
        "id": "proj_new",
        "name": data.name,
        "description": data.description,
        "columns": columns,
        "task_count": 0,
        "member_count": 1,
        "created_at": datetime.utcnow().isoformat(),
    }


@router.get("/{project_id}/board")
async def get_board(project_id: str):
    """Get full Kanban board with all tasks grouped by column."""
    return {
        "project_id": project_id,
        "columns": [
            {
                "id": "col_1", "name": "To Do", "order": 0,
                "tasks": [
                    {"id": "task_1", "title": "Design homepage mockup", "priority": "high",
                     "assignee": {"name": "Vikas M.", "avatar": None}, "labels": ["design"],
                     "due_date": "2024-02-01", "comment_count": 3},
                    {"id": "task_2", "title": "Set up CI/CD pipeline", "priority": "medium",
                     "assignee": None, "labels": ["devops"], "due_date": None, "comment_count": 0},
                ]
            },
            {
                "id": "col_2", "name": "In Progress", "order": 1,
                "tasks": [
                    {"id": "task_3", "title": "Build REST API endpoints", "priority": "high",
                     "assignee": {"name": "Vikas M.", "avatar": None}, "labels": ["backend"],
                     "due_date": "2024-01-25", "comment_count": 5},
                ]
            },
            {"id": "col_3", "name": "Review", "order": 2, "tasks": []},
            {
                "id": "col_4", "name": "Done", "order": 3,
                "tasks": [
                    {"id": "task_4", "title": "Project setup & Docker config", "priority": "low",
                     "assignee": {"name": "Vikas M.", "avatar": None}, "labels": ["devops"],
                     "due_date": None, "comment_count": 1},
                ]
            },
        ]
    }
