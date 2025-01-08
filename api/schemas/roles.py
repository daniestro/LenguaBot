from pydantic import BaseModel


class RoleCreateSchema(BaseModel):
    name: str
