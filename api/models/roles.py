from sqlalchemy import Table, Column, Integer, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    users = relationship("Users", secondary=user_roles, back_populates="roles")
