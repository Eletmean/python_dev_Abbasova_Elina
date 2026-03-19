from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database.config import DATABASE_URL_DB2

engine_db2 = create_async_engine(
    DATABASE_URL_DB2,
    connect_args={"check_same_thread": False},
    echo=False,
)

async_session_db2 = sessionmaker(
    engine_db2,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db2():
    async with async_session_db2() as session:
        yield session