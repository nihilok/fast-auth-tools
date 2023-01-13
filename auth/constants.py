import os

from fastapi.security import OAuth2PasswordBearer

from auth.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.login_url)
