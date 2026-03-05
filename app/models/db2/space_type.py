from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.db1.author import Base

class SpaceType(Base):
    __tablename__ = "space_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)