"""Full-text search endpoint."""

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/")
async def search_tasks(
    q: str = Query(..., min_length=2, description="Search query"),
    project_id: str = Query(None, description="Filter by project"),
):
    """
    Full-text search across tasks, comments, and descriptions.
    Uses PostgreSQL tsvector for efficient text search.
    """
    # In production: use PostgreSQL full-text search
    # SELECT * FROM tasks
    # WHERE search_vector @@ plainto_tsquery('english', :query)
    # ORDER BY ts_rank(search_vector, plainto_tsquery('english', :query)) DESC

    return {
        "query": q,
        "total": 2,
        "results": [
            {
                "type": "task",
                "id": "task_1",
                "title": "Design homepage mockup",
                "project": "Website Redesign",
                "highlight": f"...{q}... found in task title",
                "score": 0.95,
            },
            {
                "type": "comment",
                "id": "comment_1",
                "task_id": "task_1",
                "content_preview": f"...{q}... found in comment",
                "score": 0.72,
            },
        ],
    }
