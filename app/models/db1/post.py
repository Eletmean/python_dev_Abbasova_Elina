from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db1.base import DB1Base


class Post(DB1Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(String(500), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    blog_id: Mapped[int] = mapped_column(
        ForeignKey("blogs.id"), nullable=False, index=True
    )

    author = relationship("Users", back_populates="posts")
    blog = relationship("Blog", back_populates="posts")
