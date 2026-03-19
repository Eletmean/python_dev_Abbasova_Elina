from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.db2.base import DB2Base


class EventType(DB2Base):
    __tablename__ = "event_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
