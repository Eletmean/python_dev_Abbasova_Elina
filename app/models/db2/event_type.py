from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ...models.db1 import Base

class EventType(Base):
    __tablename__ = "event_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)