from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db1.base import DB1Base


class Users(DB1Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    posts = relationship("Post", back_populates="author")
    owned_blogs = relationship("Blog", back_populates="owner")
