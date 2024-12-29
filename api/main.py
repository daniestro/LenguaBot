from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.base import HTTPException
from connectors.database import create_table
from routers import auth, roles, users


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_table()


@app.exception_handler(HTTPException)
async def unicorn_exception_handler(
        request: Request,
        exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(users.router)
