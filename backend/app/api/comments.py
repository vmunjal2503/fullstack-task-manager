"""Task comment endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class CreateCommentRequest(BaseModel):
    content: str
    mentions: list[str] = []  # User IDs mentioned with @


class CommentResponse(BaseModel):
    id: str
    task_id: str
    content: str
    author: dict
    mentions: list[str]
    created_at: str


@router.get("/{task_id}/comments", response_model=list[CommentResponse])
async def list_comments(task_id: str):
    """Get all comments on a task."""
    return [
        {
            "id": "comment_1",
            "task_id": task_id,
            "content": "I've started working on the initial wireframes. Should be ready by EOD.",
            "author": {"id": "user_1", "name": "Vikas M.", "avatar": None},
            "mentions": [],
            "created_at": "2024-01-16T09:30:00Z",
        },
        {
            "id": "comment_2",
            "task_id": task_id,
            "content": "@user_1 Looks great! Can you also include a mobile view?",
            "author": {"id": "user_2", "name": "Client", "avatar": None},
            "mentions": ["user_1"],
            "created_at": "2024-01-16T14:15:00Z",
        },
    ]


@router.post("/{task_id}/comments", response_model=CommentResponse, status_code=201)
async def add_comment(task_id: str, data: CreateCommentRequest):
    """Add a comment to a task. Sends notifications for @mentions."""
    # In production: save to DB, notify mentioned users, broadcast via WebSocket
    return {
        "id": "comment_new",
        "task_id": task_id,
        "content": data.content,
        "author": {"id": "user_1", "name": "Vikas M.", "avatar": None},
        "mentions": data.mentions,
        "created_at": datetime.utcnow().isoformat(),
    }
