from http import HTTPStatus

from .base import HTTPException


UserAlreadyExistException = HTTPException(HTTPStatus.CONFLICT, "User already exist")
WrongLoginDetailsException = HTTPException(HTTPStatus.UNAUTHORIZED, "Wrong login details!")

