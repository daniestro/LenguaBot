from uuid import UUID
from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from connectors.database import get_session
from services import UserService, get_user_service
from services import RolesService, get_roles_service
from services import JWTBearer
from helpers import has_role


router = APIRouter(tags=["users"])


@router.post("/users/{user_id}/roles/{role_id}", dependencies=[Depends(has_role("admin"))])
async def add_role_to_user(
        user_id: UUID, role_id: int,
        session: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(get_user_service),
        roles_service: RolesService = Depends(get_roles_service)
):
    user = await user_service.get(user_id)
    role = await roles_service.get(role_id)
    user.roles.append(role)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"detail": "Role to user added successfully."})


@router.get("/users/", dependencies=[Depends(JWTBearer())])
async def get_users(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_all(page, page_size)
