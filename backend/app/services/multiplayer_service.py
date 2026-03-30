from collections import defaultdict
from fastapi import WebSocket
import json


class PresenceHub:
    def __init__(self) -> None:
        self.connections: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, world_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[world_id].add(websocket)

    def disconnect(self, world_id: str, websocket: WebSocket):
        self.connections[world_id].discard(websocket)

    async def broadcast(self, world_id: str, payload: dict, sender: WebSocket):
        dead = []
        for conn in self.connections[world_id]:
            if conn is sender:
                continue
            try:
                await conn.send_text(json.dumps(payload))
            except Exception:
                dead.append(conn)
        for conn in dead:
            self.disconnect(world_id, conn)


hub = PresenceHub()
