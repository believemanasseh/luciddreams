import secrets
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .posts import Post


def generate_auth_token():
    return secrets.token_hex(20)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    modified: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
    auth_token: Mapped[str] = mapped_column(
        unique=True, nullable=False, default=generate_auth_token
    )
    posts: Mapped[list["Post"]] = relationship()

    def __str__(self) -> str:
        return f"User: {self.email}"
