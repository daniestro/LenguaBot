from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UUID

from .base import Base


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(UUID, primary_key=True, default=uuid4)
    fullname: Mapped[str] = mapped_column(String(128))
    login: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(32))
