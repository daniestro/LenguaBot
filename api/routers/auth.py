from fastapi import APIRouter, Body, Request, Depends

from schemas import UserSchema, UserLoginSchema
from services import JWTService, get_jwt_service, JWTBearer
from services import UserService, get_user_service
from exceptions.auth import UserAlreadyExistException, WrongLoginDetailsException


router = APIRouter(tags=["auth"])


@router.post("/auth/signup")
async def create_user(
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service),
        user_form: UserSchema = Body(...)
):
    user = await user_service.create(user_form.fullname, user_form.login, user_form.password)
    if user:
        return jwt_service.sign(str(user.id))
    raise UserAlreadyExistException


@router.post("/auth/login")
async def user_login(
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service),
        user_form: UserLoginSchema = Body(...)
):
    user = await user_service.get_by(user_form.login)
    if user and user.password == user_form.password:
        return jwt_service.sign(str(user.id))
    raise WrongLoginDetailsException


def get_current_user(
        request: Request,
        jwt_service: JWTService = Depends(get_jwt_service)
):
    authorization = request.headers.get("authorization")
    bearer, token = authorization.split()
    payload = jwt_service.get(token)
    return payload


@router.get("/auth/me", dependencies=[Depends(JWTBearer())])
def get_current_user_data(user_data: dict = Depends(get_current_user)):
    return user_data
