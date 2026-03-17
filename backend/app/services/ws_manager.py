"""
WebSocket connection manager for real-time updates.
Manages connections per project board and broadcasts events.
"""

from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections grouped by project/board."""

    def __init__(self):
        # project_id → set of active WebSocket connections
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket, project_id: str):
        """Accept a new WebSocket connection for a project board."""
        await websocket.accept()
        self.connections[project_id].add(websocket)

    def disconnect(self, websocket: WebSocket, project_id: str):
        """Remove a disconnected client."""
        self.connections[project_id].discard(websocket)
        if not self.connections[project_id]:
            del self.connections[project_id]

    async def broadcast(self, project_id: str, message: dict, exclude: WebSocket = None):
        """Send a message to all connected clients on a board, except the sender."""
        dead_connections = set()

        for ws in self.connections.get(project_id, set()):
            if ws == exclude:
                continue
            try:
                await ws.send_json(message)
            except Exception:
                dead_connections.add(ws)

        # Clean up dead connections
        for ws in dead_connections:
            self.connections[project_id].discard(ws)
