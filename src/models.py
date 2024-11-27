from uuid import uuid4

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class UnknownWords(Base):
    __tablename__ = "unknown_words"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid4] = mapped_column(String(36))
    word: Mapped[str] = mapped_column(String(128))
    translation: Mapped[str] = mapped_column(String(128))
