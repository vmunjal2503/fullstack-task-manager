"""
WebSocket endpoint for real-time Kanban board updates.
When one user moves a task, all other users on the same board see it instantly.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.ws_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/{project_id}")
async def board_websocket(websocket: WebSocket, project_id: str):
    """
    WebSocket connection for real-time board updates.

    Events sent to clients:
    - task.moved: { task_id, from_column, to_column, position }
    - task.created: { task }
    - task.updated: { task_id, changes }
    - task.deleted: { task_id }
    - comment.added: { task_id, comment }
    """
    await manager.connect(websocket, project_id)
    try:
        while True:
            # Receive events from client (e.g., drag-and-drop)
            data = await websocket.receive_json()

            # Broadcast to all other clients on the same project board
            await manager.broadcast(
                project_id,
                {
                    "event": data.get("event", "unknown"),
                    "payload": data.get("payload", {}),
                    "sender": data.get("user_id", "anonymous"),
                },
                exclude=websocket,
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, project_id)
