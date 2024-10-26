from select import select

from fastapi import APIRouter
from sqlalchemy import Select
from starlette.websockets import WebSocket, WebSocketDisconnect

from apps.models import db
from apps.models.user import Message, User
from apps.utils.bot import bot_send_message_if_user_offline


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: dict, websocket: WebSocket):
        for connection in self.active_connections:
            user = connection.session.get('user')
            if user.get('id') == message.get('msg_recipient'):
                return await connection.send_json(message.pop('msg_recipient'))
        else:
            user = await User.get(message.get('msg_recipient'))
            tlg_id = user.tlg_id
            name = websocket.session.get('user').get('name')
            msg = message.get('message')
            text = msg.get('text')
            await bot_send_message_if_user_offline(name, text, tlg_id)
            await Message.create(user_id=message.get('msg_recipient'), owner_id=websocket.session.get('user').get('id'), text=text)

    # async def broadcast(self, message: str):
    #     for connection in self.active_connections:
    #         await connection.send_text(message)


manager = ConnectionManager()
websocket_router = APIRouter()


@websocket_router.websocket("/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.send_message({"message": data, "msg_recipient": user_id}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)



