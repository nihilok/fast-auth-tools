import time
from datetime import timedelta

import pytest
from jose import ExpiredSignatureError

from ..funcs import create_access_token, decode_jwt


def test_encoded_token_is_decoded():
    data = {"sub": "test_name"}
    token = create_access_token(data)
    decoded = decode_jwt(token)
    assert data["sub"] == decoded["sub"]
    assert decoded["exp"] > time.time()


def test_token_expires():
    data = {"sub": "test_name"}
    token = create_access_token(data, expires_delta=timedelta(milliseconds=1))
    time.sleep(1)
    with pytest.raises(ExpiredSignatureError):
        decode_jwt(token)
