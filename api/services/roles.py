from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from models import Roles
from connectors.database import get_session
from .base import Interfaces, BaseService


class RolesService(
    BaseService,
    Interfaces.Add,
    Interfaces.Get,
    Interfaces.All
):
    def __str__(self):
        return "Service for managing roles"


async def get_roles_service(
        session: AsyncSession = Depends(get_session)
) -> RolesService:
    return RolesService(session, Roles)
