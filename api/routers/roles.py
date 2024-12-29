from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from schemas import RoleCreateSchema
from services import RolesService, get_roles_service


router = APIRouter(tags=["roles"])


@router.post('/roles/')
async def create_role(
        role_schema: RoleCreateSchema,
        role_service: RolesService = Depends(get_roles_service)
):
    await role_service.create(role_schema.name)
    return JSONResponse(status_code=HTTPStatus.CREATED, content={"detail": "Successfully created"})


@router.get("/roles/")
async def get_roles(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        role_service: RolesService = Depends(get_roles_service)
):
    return await role_service.get_all(page, page_size)
