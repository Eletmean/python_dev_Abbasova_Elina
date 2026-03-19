from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db2.base import DB2Base


class Log(DB2Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[DateTime] = mapped_column(DateTime, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    space_type_id: Mapped[int] = mapped_column(
        ForeignKey("space_type.id"), nullable=False, index=True
    )
    event_type_id: Mapped[int] = mapped_column(
        ForeignKey("event_types.id"), nullable=False, index=True
    )

    post_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)

    space_type = relationship("SpaceType", foreign_keys=[space_type_id])
    event_type = relationship("EventType", foreign_keys=[event_type_id])
