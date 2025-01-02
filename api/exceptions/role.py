from http import HTTPStatus

from .base import HTTPException


RoleRequiredException = HTTPException(HTTPStatus.FORBIDDEN, "Access denied. User doesn't have role.")