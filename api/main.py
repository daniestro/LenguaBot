from time import time
from typing import Optional

import jwt
from pydantic import BaseModel, Field
from jwt.exceptions import PyJWTError
from fastapi import FastAPI, Body, Request, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from settings import JWTSettings, jwt_settings


app = FastAPI()


class UserSchema(BaseModel):
    fullname: str = Field(...)
    login: str = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "login": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }


class UserLoginSchema(BaseModel):
    login: str = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "login": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }


class JWTService:

    EXPIRE_TIME = 600
    EXPIRES = "expires"
    ACCESS_TOKEN = "access_token"

    def __init__(self, jwt_stg: JWTSettings) -> None:
        self.secret = jwt_stg.SECRET
        self.algorithm = jwt_stg.ALGORITHM

    def sign(self, user_id: str) -> str:
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


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify(token: str) -> bool:
        payload = jwt_service.get(token)
        if payload:
            return True
        return False


users = []
jwt_service = JWTService(jwt_settings)


def check_user(data: UserLoginSchema) -> bool:
    for user in users:
        if user.login == data.login and user.password == data.password:
            return True
    return False


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)) -> str:
    users.append(user)
    return jwt_service.sign(user.login)


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)) -> [str, dict]:
    if check_user(user):
        return jwt_service.sign(user.login)
    return {"error": "Wrong login details!"}


def get_current_user(authorization: str = Header(...)) -> dict:
    bearer, token = authorization.split()
    payload = jwt_service.get(token)
    return payload


@app.get("/", dependencies=[Depends(JWTBearer())])
def read_root(user_data: dict = Depends(get_current_user)) -> dict:
    return user_data
