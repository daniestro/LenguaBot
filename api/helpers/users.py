from fastapi import Request, Depends

from services import JWTService, get_jwt_service, JWTBearer
from services import UserService, get_user_service
from exceptions.role import RoleRequiredException
from schemas import UserDataSchema


def get_current_user_data(
        request: Request,
        bearer: JWTBearer = Depends(JWTBearer()),
        jwt_service: JWTService = Depends(get_jwt_service)
) -> UserDataSchema:
    authorization = request.headers.get("authorization")
    bearer, token = authorization.split()
    payload = jwt_service.get(token)
    return UserDataSchema(user_id=payload["user_id"], expires=payload["expires"])


def has_role(*requires_roles) -> callable:

    async def check(
            user_data: UserDataSchema = Depends(get_current_user_data),
            user_service: UserService = Depends(get_user_service)
    ):
        user = await user_service.get(id=user_data.user_id)
        user_roles_names = [role.name for role in user.roles]

        if not any(role in user_roles_names for role in requires_roles):
            raise RoleRequiredException

    return check
