from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import Users


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
