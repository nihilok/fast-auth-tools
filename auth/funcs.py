from datetime import timedelta, datetime

import aiosqlite
from fastapi import Depends
from jose import jwt, JWTError
from passlib.context import CryptContext

from .constants import (
    oauth2_scheme,
)
from .settings import settings
from .token import TokenData
from .exceptions import credentials_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(password, hash):
    return pwd_context.verify(password, hash)


async def replace(table, values: dict, db_path=settings.user_db_path):
    values = values.items()
    stmt = f"""
    REPLACE INTO {table} ({', '.join((v[0] for v in values))})
    VALUES ({', '.join(("'" + v[1] + "'" for v in values))});
    """
    async with aiosqlite.connect(db_path) as db:
        await db.execute(stmt)
        await db.commit()


async def insert(table, values: dict, db_path=settings.user_db_path):
    values = values.items()
    stmt = f"""
    INSERT INTO {table} ({', '.join((v[0] for v in values))})
    VALUES ({', '.join(("'" + v[1] + "'" for v in values))});
    """
    async with aiosqlite.connect(db_path) as db:
        await db.execute(stmt)
        await db.commit()


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(days=settings.access_token_expire_days)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
        options={"require_sub": True},
    )
    return decoded_token


async def get_data_from_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = decode_jwt(token)
        token_data = TokenData(username=payload["sub"])
        return token_data
    except JWTError:
        raise credentials_exception


def run(coroutine):
    import asyncio

    return asyncio.run(coroutine)
