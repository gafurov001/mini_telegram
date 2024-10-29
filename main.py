import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from apps.models import db
from apps.routers import user_router, websocket_router, messenger_router
from config import secret_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists('static'):
        os.mkdir('static')
    app.mount("/static", StaticFiles(directory='static'), name='static')
    app.include_router(user_router, prefix='/user')
    app.include_router(messenger_router, prefix='/messenger')
    app.include_router(websocket_router, prefix='/ws')
    await db.create_all()

    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=secret_key)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
def auth_exception_handler(request: Request, exc):
    return RedirectResponse(request.url_for("user-login"))
