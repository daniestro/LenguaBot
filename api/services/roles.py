from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from models import Roles
from connectors.database import get_session
from .base import OpenBaseService


class RolesService(OpenBaseService):
    pass


async def get_roles_service(
        session: AsyncSession = Depends(get_session)
) -> RolesService:
    return RolesService(session, Roles)
