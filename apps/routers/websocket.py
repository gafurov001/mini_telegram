from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from apps.models.user import Message, User
from celery_config import send_msg_if_offline


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
                text = message.get('message').get('text')
                await Message.create(user_id=user.get('id'),
                                     owner_id=websocket.session.get('user').get('id'),
                                     text=text)
                return await connection.send_json({'owner_id': websocket.session.get('user').get('name'), 'text': text})
        else:
            user = await User.get(message.get('msg_recipient'))
            tlg_id = user.tlg_id
            name = websocket.session.get('user').get('name')
            msg = message.get('message')
            text = msg.get('text')
            send_msg_if_offline(name, text, tlg_id)
            await Message.create(user_id=message.get('msg_recipient'), owner_id=websocket.session.get('user').get('id'),
                                 text=text)


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
