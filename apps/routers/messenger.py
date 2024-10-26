from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.sql.selectable import and_
from starlette.requests import Request

from apps.models import db
from apps.models.user import User, Message
from apps.utils.authentication import get_current_user
from config import templates

messenger_router = APIRouter()


@messenger_router.get('/home', name='messenger-home')
async def get_messenger(request: Request, user=Depends(get_current_user)):
    users = await User.get_all()
    for i in users:
        print(i)
    context = {
        'user': user,
        'users': users,
    }
    return templates.TemplateResponse(request, 'home.html', context)


@messenger_router.get('/room/{id}', name='room-page')
async def get_messenger(request: Request, id: int):
    context = {
        'owner': request.session.get('user'),
        'user': await User.get(id),
    }
    return templates.TemplateResponse(request, 'room.html', context)


@messenger_router.get("/chat_history/{user_id}")
async def chat_history(request: Request, user_id: int, ):
    owner_id = request.session.get('user').get('id')
    query = select(Message).where(Message.user_id.in_([user_id, owner_id]), Message.owner_id.in_([user_id, owner_id]))
    return (await db.execute(query)).scalars().all()
