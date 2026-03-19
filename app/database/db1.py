from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.database.config import DATABASE_URL_DB1

engine_db1 = create_async_engine(
    DATABASE_URL_DB1,
    connect_args={"check_same_thread": False},
    echo=False,   
)

async_session_db1 = sessionmaker(
    engine_db1,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db1():
    async with async_session_db1() as session:
        yield session