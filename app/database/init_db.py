from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db1 import engine_db1
from app.database.db2 import engine_db2
from app.models.db1.base import DB1Base
from app.models.db2.base import DB2Base
from app.models.db2.event_type import EventType
from app.models.db2.space_type import SpaceType


async def create_all_tables():
    """Создаёт все таблицы в обеих базах, если их ещё нет"""
    # db1
    async with engine_db1.begin() as conn:
        await conn.run_sync(DB1Base.metadata.create_all)

    # db2
    async with engine_db2.begin() as conn:
        await conn.run_sync(DB2Base.metadata.create_all)


async def seed_reference_data(session: AsyncSession):
    """
    Заполняет справочники space_type и event_type, если они пустые.
    """
    # space_types
    existing_spaces = await session.execute(select(SpaceType.name))
    existing_space_names = {row[0] for row in existing_spaces.all()}

    needed_spaces = {"global", "blog", "post"}
    to_add_spaces = needed_spaces - existing_space_names

    if to_add_spaces:
        session.add_all(SpaceType(name=name) for name in to_add_spaces)

    # event_types
    existing_events = await session.execute(select(EventType.name))
    existing_event_names = {row[0] for row in existing_events.all()}

    needed_events = {"login", "logout", "comment", "create_post", "delete_post"}
    to_add_events = needed_events - existing_event_names

    if to_add_events:
        session.add_all(EventType(name=name) for name in to_add_events)

    if to_add_spaces or to_add_events:
        await session.commit()
