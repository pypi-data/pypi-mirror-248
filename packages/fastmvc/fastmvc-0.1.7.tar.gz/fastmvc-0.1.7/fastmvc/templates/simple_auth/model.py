from secrets import token_hex

from fastapi import Request
from fastapi.responses import RedirectResponse
from fastmvc.models.html import Alert
from fastmvc.models.database.^{platform.data_model_import}^
from user.utils import Auth, current_user


auth_handler = Auth()


class User(^{platform.data_model}^):
    key: str or None = None
    username: str
    secret: str = str()

    class Config:
        table_name = "^{proj}^_user"

    @classmethod
    def fetch_user(cls, username: str):
        user = [u for u in cls.query({'username': username})]
        if user:
            return user[0]
        return False

    @classmethod
    def new_user(cls, email):
        data = {
            'key': '',
            'username': email
        }
        user = User.model_validate(data)
        user.save()
        return user

    def create_session(self, request: Request):
        access_token = auth_handler.encode_token(self.key)
        refresh_token = auth_handler.encode_refresh_token(self.key)
        results = {
            'access_token': access_token,
            'refresh_token': refresh_token}

        request.session['user'] = results
        request.session['user'].update(self.dict())

    def login(self, request: Request):
        find_user = [u for u in User.query({'username': self.username})]
        if find_user:
            user = find_user[0]
        else:
            user = self.new_user(self.username)

        user.secret = token_hex(16)
        user.save()

        try:
            auth_handler.send_validation_email(
                request=request,
                user_email=user.username,
                user_id=user.key,
                validation_token=auth_handler.construct_secret(
                    [user.secret, user.username]))
        except Exception as e:
            return Alert(e)
        return RedirectResponse('/user/validate-email', 303)

    @classmethod
    def activate_session(cls, request, user_id, token):
        user = cls.get(user_id)
        secret = auth_handler.construct_secret([user.secret, user.username])
        if token == secret:
            user.create_session(request)
        else:
            return Alert("Something happened. Please start over again.")

    @classmethod
    def refresh_token(cls, request: Request):
        user = current_user(request)
        refresh_token = user['refresh_token']
        return auth_handler.refresh_token(refresh_token)
