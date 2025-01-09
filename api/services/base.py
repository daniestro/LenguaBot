from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Base


class BaseService:

    def __init__(self, session: AsyncSession, model: Callable | Base) -> None:
        self.session = session
        self.model = model

    async def _add(self, **args):
        instance = self.model(**args)
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def _get(self, option=None, **kwargs):
        attr, value = next(iter(kwargs.items()))
        matching = getattr(self.model, attr) == value
        query = self._build_query(option, matching)
        response = await self.session.execute(query)
        instance = response.scalar_one_or_none()
        return instance

    def _build_query(self, option, matching):
        query = select(self.model).where(matching)
        return query.options(option) if option else query

    async def _all(self, page: int, page_size: int):
        offset = (page - 1) * page_size
        query = select(self.model).offset(offset).limit(page_size)
        result = await self.session.execute(query)
        instances = result.scalars().all()
        return instances


class GetIntf:
    async def get(self, option, **kwargs):
        return await self._get(option, **kwargs)


class AddIntf:
    async def add(self, **kwargs):
        return await self._add(**kwargs)


class AllIntf:
    async def all(self, *args):
        return await self._all(args)


class Interfaces:
    Get = GetIntf
    Add = AddIntf
    All = AllIntf

