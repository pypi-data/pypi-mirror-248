from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ^{obj}^.model import ^{Obj}^
^% if options.requires_login %^from user.utils import authenticated_path, current_user ^% endif %^


^{obj}^_router = APIRouter()
templates = Jinja2Templates(directory="")


# INDEX
@^{obj}^_router.get('/')
^% if options.requires_login %^@authenticated_path
^% endif %^
def index(request: Request):
    ^{obj}^_list = ^{Obj}^.get_all()
    return templates.TemplateResponse(
        '^{obj}^/templates/index.html',
        context={'request': request, '^{obj}^_list': ^{obj}^_list })


# CREATE
@^{obj}^_router.get('/new')
^% if options.requires_login %^@authenticated_path
^% endif %^
def new(request: Request):
    return templates.TemplateResponse(
        '^{obj}^/templates/form.html',
        context={'request': request, 'vals': dict() })


@^{obj}^_router.post('/new', response_model=^{Obj}^)
async def create(request: Request):
    ^% if options.requires_login %^
    user = current_user(request)
    if not user:
        return RedirectResponse('/user/not_authenticated', 303)
    form_data = await request.form()
    ^{obj}^ = ^{Obj}^.model_validate(form_data)
    # ^{obj}^.user_id = user['key']
    ^{obj}^.save()
    ^% else %^
    form_data = await request.form()
    ^{obj}^ = ^{Obj}^.model_validate(form_data)
    ^{obj}^.save()
    ^% endif %^
    return RedirectResponse(f'/^{obj}^/{^{obj}^.key}', status_code=303)


# UPDATE
@^{obj}^_router.get('/edit/{key}')
^% if options.requires_login %^@authenticated_path
^% endif %^
def edit(request: Request, key: str):
    vals = ^{Obj}^.get(key)
    return templates.TemplateResponse(
        '^{obj}^/templates/form.html',
        context={'request': request, 'vals': vals.model_dump() })


@^{obj}^_router.post("/edit/{key}")
async def update(request: Request, key: str):
    ^% if options.requires_login %^
    user = current_user(request)
    in_db =  ^{Obj}^.get(key)
    if user['key'] == in_db.user_id:
        update_data = await request.form()
        in_db.update(update_data)
    ^% else %^
    in_db = ^{Obj}^.get(key)
    update_data = await request.form()
    in_db.update(update_data)
    ^% endif %^
    return RedirectResponse(f'/^{obj}^/{key}', status_code=303)


# DELETE
@^{obj}^_router.get('/delete/{key}')
^% if options.requires_login %^@authenticated_path
^% endif %^
def delete(request: Request, key: str):
    ^% if options.requires_login %^
    user = current_user(request)
    ^{obj}^ = ^{Obj}^.get(key)
    if user and user['key'] == ^{obj}^.user_id:
        ^{Obj}^.delete_key(key)
    ^% else %^
    ^{Obj}^.delete_key(key)
    ^% endif %^
    return RedirectResponse(f'/^{obj}^', status_code=303)


# VIEW
@^{obj}^_router.get('/{key}')
def view(request: Request, key: str):
    ^{obj}^ = ^{Obj}^.get(key)
    return templates.TemplateResponse(
        '^{obj}^/templates/view.html',
        context={'request': request, '^{obj}^': ^{obj}^ })
