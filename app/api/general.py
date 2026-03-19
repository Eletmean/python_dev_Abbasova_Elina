from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db1 import get_db1
from app.database.db2 import get_db2
from app.schemas.responses import GeneralResponse
from app.services.analytics import AnalyticsService

router = APIRouter()


@router.get("/general", response_model=List[GeneralResponse])
async def get_general(
    login: str = Query(..., description="Логин пользователя"),
    db1: AsyncSession = Depends(get_db1),
    db2: AsyncSession = Depends(get_db2),
):
    """
    Возвращает общую статистику действий пользователя по дням:
    - дата
    - количество входов
    - количество выходов
    - количество действий в блогах
    """
    service = AnalyticsService(db1, db2)
    result = await service.get_general_dataset(login)
    return result
