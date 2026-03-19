import os
import sys
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.models.db1.users import Users
from app.services.analytics import AnalyticsService


@pytest.mark.asyncio
async def test_get_comments_dataset_user_not_found():
    """пользователь не найден - должен вернуть пустой список"""
    mock_db1 = AsyncMock()
    mock_db2 = AsyncMock()

    mock_result = Mock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db1.execute.return_value = mock_result

    service = AnalyticsService(mock_db1, mock_db2)
    result = await service.get_comments_dataset("unknown_user")

    assert result == []
    mock_db1.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_comments_dataset_no_comments():
    """пользователь есть, но нет комментариев"""
    mock_db1 = AsyncMock()
    mock_db2 = AsyncMock()

    mock_user = Users(id=1, login="Masha", email="masha@test.com")
    mock_user_result = MagicMock()
    mock_user_result.scalar_one_or_none.return_value = mock_user
    mock_db1.execute.return_value = mock_user_result

    mock_comments_result = MagicMock()
    mock_comments_result.__aiter__.return_value = iter([])
    mock_db2.execute.return_value = mock_comments_result

    service = AnalyticsService(mock_db1, mock_db2)
    result = await service.get_comments_dataset("Masha")

    assert result == []


@pytest.mark.asyncio
async def test_get_general_dataset_user_not_found():
    """пользователь не найден в general"""
    mock_db1 = AsyncMock()
    mock_db2 = AsyncMock()

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db1.execute.return_value = mock_result

    service = AnalyticsService(mock_db1, mock_db2)
    result = await service.get_general_dataset("unknown_user")

    assert result == []


@pytest.mark.asyncio
async def test_get_general_dataset_empty():
    """общая статистика пустая"""
    mock_db1 = AsyncMock()
    mock_db2 = AsyncMock()

    mock_user = Users(id=1, login="Masha", email="masha@test.com")
    mock_user_result = MagicMock()
    mock_user_result.scalar_one_or_none.return_value = mock_user
    mock_db1.execute.return_value = mock_user_result

    mock_stats_result = MagicMock()
    mock_stats_result.__aiter__.return_value = iter([])
    mock_db2.execute.return_value = mock_stats_result

    service = AnalyticsService(mock_db1, mock_db2)
    result = await service.get_general_dataset("Masha")

    assert result == []
