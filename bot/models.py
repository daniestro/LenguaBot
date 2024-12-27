from uuid import uuid4

from sqlalchemy import String, BIGINT, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class UnknownWords(Base):
    __tablename__ = "unknown_words"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid4] = mapped_column(String(36))
    word: Mapped[str] = mapped_column(String(128))
    translation: Mapped[str] = mapped_column(String(128))
    tasks: Mapped[list["Tasks"]] = relationship("Tasks", back_populates="word", cascade="all, delete-orphan")


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BIGINT(), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    tasks: Mapped[list["Tasks"]] = relationship("Tasks", back_populates="user", cascade="all, delete-orphan")


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Users] = relationship("Users", back_populates="tasks")
    word_id: Mapped[int] = mapped_column(ForeignKey("unknown_words.id"))
    word: Mapped[UnknownWords] = relationship("UnknownWords", back_populates="tasks")
    message: Mapped[str] = mapped_column(String(256))
    status: Mapped[str] = mapped_column(String(36))
