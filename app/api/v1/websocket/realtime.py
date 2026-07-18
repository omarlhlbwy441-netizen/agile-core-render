from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                disconnected.append(connection)
        for conn in disconnected:
            self.disconnect(conn)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "task_update":
                await manager.broadcast({
                    "type": "task_update",
                    "task_id": message.get("task_id"),
                    "status": message.get("status"),
                    "timestamp": message.get("timestamp")
                })
            elif message.get("type") == "sprint_update":
                await manager.broadcast({
                    "type": "sprint_update",
                    "sprint_id": message.get("sprint_id"),
                    "velocity": message.get("velocity")
                })
            else:
                await manager.send_personal_message({
                    "type": "echo",
                    "message": message
                }, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
