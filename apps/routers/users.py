import bcrypt
from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from apps.models.user import User
from apps.utils.authentication import create_access_token
from config import templates

user_router = APIRouter()


@user_router.get('/register', name='user-create')
async def get_user_register(request: Request):
    return templates.TemplateResponse(request, 'auth/register.html', {})


@user_router.post('/register', name='user-create')
async def post_user_register(request: Request):
    form = await request.form()
    await User.create(name=form.get('name'), tlg_id=int(form.get('tlg_id')), username=form.get('username'),
                      password=str(
                          bcrypt.hashpw(password=form.get('password').encode('utf-8'), salt=bcrypt.gensalt()))[
                               2:-1])
    return RedirectResponse(request.url_for('user-login'))


@user_router.get('/logout', name='user-logout')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(request.url_for('user-login'))


@user_router.get('/login', name='user-login')
async def get_user_login(request: Request):
    return templates.TemplateResponse(request, 'auth/login.html', {})


@user_router.post('/login', name='user-login')
async def post_user_login(request: Request):
    form = await request.form()
    username = form.get('username')
    password = form.get('password')
    user = await User.get_user_by_username(username)

    if user is not None and (await user.check_password(password)):
        user_data = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
        }
        access_token = create_access_token(user_data)
        request.session.update({"token": access_token, "user": user_data})
        return RedirectResponse(request.url_for('messenger-home'))

    return RedirectResponse(request.url_for('user-login'), status_code=status.HTTP_303_SEE_OTHER)
