from time import time
from typing import Optional
from uuid import UUID

import jwt
from jwt.exceptions import PyJWTError
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from exceptions.jwt import InvalidAuthenticationSchemeException
from exceptions.jwt import InvalidAuthorizationCodeException
from exceptions.jwt import InvalidTokenException
from settings import JWTSettings, jwt_settings


class JWTService:

    EXPIRE_TIME = 600
    EXPIRES = "expires"
    ACCESS_TOKEN = "access_token"

    def __init__(self, jwt_stg: JWTSettings) -> None:
        self.secret = jwt_stg.SECRET
        self.algorithm = jwt_stg.ALGORITHM

    def sign(self, user_id: str | UUID) -> str:
        user_id = str(user_id)
        payload = self._create_payload(user_id)
        token = self._encode(payload)
        return self._response(token) # noqa: stupid linter

    def get(self, token: str) -> Optional[dict]:
        token = self._decode(token)
        if token and self._is_not_expired(token):
            return token

    def _decode(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except PyJWTError:
            return None

    def _is_not_expired(self, token: dict) -> bool:
        current_time = time()
        expire_time = token[self.EXPIRES]
        return True if current_time <= expire_time else False

    def _encode(self, payload: dict) -> str:
        return jwt.encode(payload, self.secret, self.algorithm)

    def _create_payload(self, user_id: str) -> dict:
        return {
            "user_id": user_id,
            "expires": self._get_expire_time()
        }

    def _get_expire_time(self) -> time:
        return time() + self.EXPIRE_TIME

    def _response(self, token: str):
        return {
            self.ACCESS_TOKEN: token
        }


async def get_jwt_service() -> JWTService:
    return JWTService(jwt_settings)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        self.jwt_service = JWTService(jwt_settings)
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise InvalidAuthenticationSchemeException
            if not self.verify(credentials.credentials):
                raise InvalidTokenException
            return credentials.credentials
        else:
            raise InvalidAuthorizationCodeException

    def verify(self, token: str) -> bool:
        payload = self.jwt_service.get(token)
        if payload:
            return True
        return False
