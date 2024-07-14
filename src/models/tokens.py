from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.controllers.hasher import Hasher

from .base import Base

if TYPE_CHECKING:
    from .users import User


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="token")

    def __str__(self) -> str:
        return f"Token: {self.key}"

    @classmethod
    def is_valid(cls, token_key):
        return Hasher.verify_password(token_key, cls.key)
