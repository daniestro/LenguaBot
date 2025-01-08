from http import HTTPStatus

from .base import HTTPException


InvalidAuthenticationSchemeException = HTTPException(HTTPStatus.FORBIDDEN, "Invalid authentication scheme.")
InvalidTokenException = HTTPException(HTTPStatus.FORBIDDEN, "Invalid token or expired token.")
InvalidAuthorizationCodeException = HTTPException(HTTPStatus.FORBIDDEN, "Invalid authorization code.")
