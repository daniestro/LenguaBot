from time import time
from typing import Optional, Any
from uuid import UUID

import jwt
from pydantic import BaseModel, Field
from jwt.exceptions import PyJWTError
from fastapi import FastAPI, Body, Request, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from settings import JWTSettings, jwt_settings
from database import create_table, get_session
from models import Users


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_table()


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


class UserService:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, fullname: str, login: str, password: str) -> Users:
        if await self.user_doesnt_exist(login):
            user = Users(
                fullname=fullname,
                login=login,
                password=password
            )
            self.session.add(user)
            await self.session.commit()
            return user

    async def user_doesnt_exist(self, login: str) -> bool:
        user = await self.get_by(login)
        return False if user else True

    async def get_by(self, login: str) -> Optional[Users]:
        query = select(Users).where(Users.login == login)
        return await self._execute(query)

    async def _execute(self, query):
        response = await self.session.execute(query)
        user = response.scalar_one_or_none()
        return user


async def get_user_service(
        session: AsyncSession = Depends(get_session)
) -> UserService:
    return UserService(session)


@app.post("/user/signup", tags=["user"])
async def create_user(
        user_service: UserService = Depends(get_user_service),
        user_form: UserSchema = Body(...)
):
    user = await user_service.create(user_form.fullname, user_form.login, user_form.password)
    return jwt_service.sign(str(user.id))


@app.post("/user/login", tags=["user"])
async def user_login(user_service: UserService = Depends(get_user_service), user_form: UserLoginSchema = Body(...)):
    user = await user_service.get_by(user_form.login)
    if user and user.password == user_form.password:
        return jwt_service.sign(str(user.id))
    return {"error": "Wrong login details!"}


def get_current_user(request: Request):
    authorization = request.headers.get("authorization")
    bearer, token = authorization.split()
    payload = jwt_service.get(token)
    return payload


@app.get("/", dependencies=[Depends(JWTBearer())])
def read_root(user_data: dict = Depends(get_current_user)):
    return user_data
