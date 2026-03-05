from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.db1.author import Base

class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(String(500), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)
    blog_id: Mapped[int] = mapped_column(ForeignKey("blog.id"), nullable=False)

    author = relationship("Author", back_populates="posts")
    blog = relationship("Blog", back_populates="posts")