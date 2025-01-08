from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from connectors.database import get_session
from .base import BaseService
from models import Users


class UserService(BaseService):

    async def create(self, **kwargs) -> Users:
        login = kwargs['login']
        if await self._user_doesnt_exist(login):
            return await self._add(**kwargs)

    async def _user_doesnt_exist(self, login: str) -> bool:
        user = await self.get(login=login)
        return False if user else True

    async def get(self, **kwargs):
        option = None
        if 'id' in kwargs.keys():
            option = selectinload(self.model.roles)
        return await self._get(option, **kwargs)

    async def all(self, *args):
        return await self._all(args)


async def get_user_service(
        session: AsyncSession = Depends(get_session)
) -> UserService:
    return UserService(session, Users)
