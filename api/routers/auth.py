from fastapi import APIRouter, Body, Depends

from schemas import UserSchema, UserLoginSchema, UserDataSchema
from services import JWTService, get_jwt_service
from services import UserService, get_user_service
from exceptions.auth import UserAlreadyExistException, WrongLoginDetailsException
from helpers import get_current_user_data, has_role


router = APIRouter(tags=["auth"])


@router.post("/auth/signup", dependencies=[Depends(has_role("admin"))])
async def create_user(
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service),
        user_form: UserSchema = Body(...)
):
    user = await user_service.create(
        user_form.fullname,
        user_form.login,
        user_form.password
    )
    if user:
        return jwt_service.sign(user.id)
    raise UserAlreadyExistException


@router.post("/auth/login")
async def user_login(
        user_service: UserService = Depends(get_user_service),
        jwt_service: JWTService = Depends(get_jwt_service),
        user_form: UserLoginSchema = Body(...)
):
    user = await user_service.get_by(user_form.login)
    if user and user.password == user_form.password:
        return jwt_service.sign(user.id)
    raise WrongLoginDetailsException


@router.get("/auth/me")
def get_current_user_data(user_data: UserDataSchema = Depends(get_current_user_data)):
    return user_data
