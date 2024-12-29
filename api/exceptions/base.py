from http import HTTPStatus


class HTTPException(Exception):

    def __init__(self, status_code: HTTPStatus, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail

