from passlib.context import CryptContext
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import logging
import ssl

logger = logging.getLogger("uvicorn")
ssl._create_default_https_context = ssl._create_unverified_context


conf = ConnectionConfig(
    MAIL_USERNAME = "Tushar",
    MAIL_PASSWORD = "tushar123",
    MAIL_FROM = "tusharbadlani0@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    USE_CREDENTIALS = True,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    VALIDATE_CERTS = False
)

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def send_reset_password_email(email, token):

    try:
        message = MessageSchema(
            subject="Password reset",
            recipients=[email],
            body=f"Click this link to reset your password: http://localhost:3000/reset-password?token={token}",
            subtype="html"
        )
        fm = FastMail(conf)
        fm.send_message(message)
        print(message)
    except Exception as e:
        print(e)
        return {"message": "Error sending email"}
