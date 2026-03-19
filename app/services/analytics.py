from typing import Dict, List

from sqlalchemy import Integer, and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db1.post import Post
from app.models.db1.users import Users
from app.models.db2.event_type import EventType
from app.models.db2.logs import Log
from app.models.db2.space_type import SpaceType


class AnalyticsService:
    def __init__(self, db1: AsyncSession, db2: AsyncSession):
        self.db1 = db1
        self.db2 = db2

    async def get_comments_dataset(self, login: str) -> List[Dict]:
        """
        Датасет comments:
        - логин пользователя
        - заголовок поста (header) к которому он оставлял комментарии
        - логин автора поста
        - кол-во комментариев
        """
        # Найти пользователя по логину
        user_result = await self.db1.execute(select(Users).where(Users.login == login))
        user = user_result.scalar_one_or_none()
        if not user:
            return []

        # Найти все комментарии пользователя
        comments_query = (
            select(Log.post_id, func.count(Log.id).label("comment_count"))
            .join(EventType, Log.event_type_id == EventType.id)
            .join(SpaceType, Log.space_type_id == SpaceType.id)
            .where(
                and_(
                    Log.user_id == user.id,
                    EventType.name == "comment",
                    SpaceType.name == "post",
                    Log.post_id.isnot(None),
                )
            )
            .group_by(Log.post_id)
        )

        comments_result = await self.db2.execute(comments_query)
        comments_data = {}
        for row in comments_result:
            comments_data[row.post_id] = row.comment_count

        if not comments_data:
            return []

        # Получить информацию о постах из БД1
        posts_query = (
            select(Post.id, Post.header, Users.login.label("author_login"))
            .join(Users, Post.author_id == Users.id)
            .where(Post.id.in_(list(comments_data.keys())))
        )

        posts_result = await self.db1.execute(posts_query)

        result = []
        for post in posts_result:
            result.append(
                {
                    "user_login": login,
                    "post_header": post.header,
                    "author_login": post.author_login,
                    "comments_count": comments_data[post.id],
                }
            )

        return result

    async def get_general_dataset(self, login: str) -> List[Dict]:
        """
        Датасет general:
        - дата
        - кол-во входов на сайт
        - кол-во выходов с сайта
        - кол-во действий внутри блога
        """
        # Найти пользователя
        user_result = await self.db1.execute(select(Users).where(Users.login == login))
        user = user_result.scalar_one_or_none()
        if not user:
            return []

        # Агрегация по дням для SQLite
        stats_query = (
            select(
                func.date(Log.datetime).label("date"),
                func.sum(func.cast(EventType.name == "login", Integer)).label("logins"),
                func.sum(func.cast(EventType.name == "logout", Integer)).label(
                    "logouts"
                ),
                func.sum(func.cast(SpaceType.name == "blog", Integer)).label(
                    "blog_actions"
                ),
            )
            .join(EventType, Log.event_type_id == EventType.id)
            .join(SpaceType, Log.space_type_id == SpaceType.id)
            .where(Log.user_id == user.id)
            .group_by(func.date(Log.datetime))
            .order_by(func.date(Log.datetime))
        )

        result = await self.db2.execute(stats_query)

        response = []
        for row in result:
            response.append(
                {
                    "date": row.date,
                    "logins": row.logins or 0,
                    "logouts": row.logouts or 0,
                    "blog_actions": row.blog_actions or 0,
                }
            )

        return response
