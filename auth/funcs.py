from datetime import timedelta, datetime

import aiosqlite
from fastapi import Depends
from jose import jwt, JWTError
from passlib.context import CryptContext

from .constants import (
    ACCESS_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
    ALGORITHM,
    USER_DB,
    oauth2_scheme,
)
from .token import TokenData
from .exceptions import credentials_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(password, hash):
    return pwd_context.verify(password, hash)


async def replace(table, values: dict, db_path=USER_DB):
    values = values.items()
    stmt = f"""
    REPLACE INTO {table} ({', '.join((v[0] for v in values))})
    VALUES ({', '.join(("'" + v[1] + "'" for v in values))});
    """
    async with aiosqlite.connect(db_path) as db:
        await db.execute(stmt)
        await db.commit()


async def insert(table, values: dict, db_path=USER_DB):
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
        expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"require_sub": True}
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
