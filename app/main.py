# app/main.py (обновленный)
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router
from app.database.db1 import engine_db1
from app.database.db2 import engine_db2, get_db2
from app.database.init_db import create_all_tables, seed_reference_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()

    async for db in get_db2():
        await seed_reference_data(db)
        break
    yield

    await engine_db1.dispose()
    await engine_db2.dispose()


app = FastAPI(
    title="User Activity API",
    description="Тестовое задание: API для анализа активности пользователей",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)
