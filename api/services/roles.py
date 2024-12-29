from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from models import Roles
from connectors.database import get_session


class RolesService:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, name: str) -> Roles:
        role = Roles(name=name)
        self.session.add(role)
        await self.session.commit()
        return role

    async def get(self, _id: int) -> Roles:
        query = select(Roles).where(Roles.id == _id)
        response = await self.session.execute(query)
        role = response.scalar_one_or_none()
        return role


async def get_roles_service(
        session: AsyncSession = Depends(get_session)
) -> RolesService:
    return RolesService(session)
