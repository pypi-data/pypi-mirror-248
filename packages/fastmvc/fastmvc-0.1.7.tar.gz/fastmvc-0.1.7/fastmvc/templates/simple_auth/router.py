from fastmvc.models.html import Alert
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from user.model import User
from user.utils import current_user, authenticated_path


user_router = APIRouter()
templates = Jinja2Templates(directory="")


#LOGIN
@user_router.get('/login')
def login_form(request: Request):
    return templates.TemplateResponse(
        'user/templates/login.html',
        context={'request': request})


@user_router.post('/login')
async def login(request: Request):
    form_data = await request.form()
    potential_user = User.model_validate(form_data)
    result = potential_user.login(request)
    if isinstance(result, Alert):
        return templates.TemplateResponse(
        'user/templates/login.html',
        context={'request': request, 'alert': result})
    else:
        return result


@user_router.get('/validate-email')
def validate_email(request: Request):
    return templates.TemplateResponse(
        'user/templates/validate_email.html',
        context={'request': request})


@user_router.get('/{user_id}/{token}')
def activate_session(request: Request, user_id: str, token: str):
    issue = User.activate_session(request, user_id, token)
    if issue:
        return templates.TemplateResponse(
            'user/templates/login.html',
            context={'request': request, 'alert': issue}
        )
    return RedirectResponse('/user/dashboard', 303)


@user_router.get('/dashboard')
@authenticated_path
def dashboard(request: Request):
    return templates.TemplateResponse(
        'user/templates/dashboard.html',
        context={'request': request, 'user': current_user(request) })


@user_router.get('/not_authenticated')
def not_authenticated(request: Request):
    return templates.TemplateResponse(
        'user/templates/not_authenticated.html',
        context={'request': request})


@user_router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


