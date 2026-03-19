from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db1 import get_db1
from app.database.db2 import get_db2
from app.schemas.responses import CommentResponse
from app.services.analytics import AnalyticsService

router = APIRouter()


@router.get("/comments", response_model=List[CommentResponse])
async def get_comments(
    login: str = Query(..., description="Логин пользователя"),
    db1: AsyncSession = Depends(get_db1),
    db2: AsyncSession = Depends(get_db2),
):
    """
    Возвращает датасет комментариев пользователя:
    - логин пользователя
    - заголовок поста
    - логин автора поста
    - количество комментариев
    """
    service = AnalyticsService(db1, db2)
    result = await service.get_comments_dataset(login)
    return result
