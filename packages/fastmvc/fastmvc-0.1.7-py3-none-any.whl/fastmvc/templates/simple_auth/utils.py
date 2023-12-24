from datetime import datetime, timedelta
from functools import wraps
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from hashlib import md5
from secrets import token_hex

import jwt

from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from starlette.config import Config


def current_user(request: Request):
    user = request.session.get('user')
    return user


def authenticated_path(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = current_user(kwargs['request'])
        if not user:
            return RedirectResponse('/user/not_authenticated', 303)
        return func(*args, **kwargs)
    return wrapper


class Auth():
    config = Config('.env')
    hasher= CryptContext(schemes=['bcrypt'])
    secret = config.get("APP_SECRET")

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(
        self,
        username,
        scope='access_token',
        exp=datetime.utcnow() + timedelta(days=14)):

        payload = {
            'exp' : exp,
            'iat' : datetime.utcnow(),
                'scope': scope,
            'sub' : username
        }

        encoded = jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )
        if isinstance(encoded, bytes):
            encoded = encoded.decode('utf-8')
        return encoded

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'access_token'):
                return payload['sub']
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def encode_refresh_token(self, username):
        return self.encode_token(
            username,
            scope='refresh_token',
            exp=datetime.utcnow() + timedelta(days=30))

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=['HS256'])
            if (payload['scope'] == 'refresh_token'):
                username = payload['sub']
                new_token = self.encode_token(username)
                return new_token
            raise HTTPException(status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')

    def construct_secret(self, add_to_secret: list):
        return md5(f"{''.join(add_to_secret + [self.secret])}".encode()).hexdigest()

    def send_validation_email(self, request: Request, user_email, user_id, validation_token: str):
        # 📦 all the variables we will need
        port = self.config.get("SMTP_PORT")
        smtp_server = self.config.get("SMTP_SERVER")
        login = self.config.get("SMTP_LOGIN")
        password =  self.config.get("SMTP_PASSWORD")

        sender_email = self.config.get("SMTP_SENDER_EMAIL")
        sender_name = self.config.get("SMTP_SENDER_NAME")
        receiver_email = user_email

        # write the text/plain part
        text = f"""\
        Hey there,
        Click the link below to complete logging in:

        {request.base_url}user/{user_id}/{validation_token}

        If you did not request this link, please take no action"""

        # write the HTML part
        html = f"""\
        <html>
        <body>
            <p>Hey there,<br>
            Click the link below to complete logging in:</p>
            <p><a href="{request.base_url}user/{user_id}/{validation_token}">Login Link</a></p>
            <br><br>
            <p>If you did not request this link, please take no action.</p>
        </body>
        </html>
        """

        # 📝 create the message object
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Continue Login"
        message["From"] = formataddr((sender_name, sender_email))
        message["To"] = receiver_email

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        # 👇 this helps emails to not be grouped together
        message.add_header('X-Entity-Ref-ID', token_hex(16))

        # 📨 send email
        with smtplib.SMTP(smtp_server, port) as server:
            server.login(login, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

