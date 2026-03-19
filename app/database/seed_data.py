import asyncio
import random
from datetime import datetime, timedelta

from sqlalchemy import select

from app.database.db1 import async_session_db1
from app.database.db2 import async_session_db2
from app.models.db1.blog import Blog
from app.models.db1.post import Post
from app.models.db1.users import Users
from app.models.db2.event_type import EventType
from app.models.db2.logs import Log
from app.models.db2.space_type import SpaceType


async def seed_test_data():
    # DB1: пользователи
    async with async_session_db1() as db1:
        result = await db1.execute(select(Users))
        if not result.scalars().first():
            users = [
                Users(login="Masha", email="Masha@example.com"),
                Users(login="Kate", email="Kate@example.com"),
                Users(login="Fedya", email="Fedya@example.com"),
            ]
            db1.add_all(users)
            await db1.commit()

            blogs = [
                Blog(owner_id=1, name="Блог Маши", description="Личный блог Маши"),
                Blog(owner_id=2, name="Блог Кати", description="Личный блог Кати"),
                Blog(owner_id=3, name="Блог Феди", description="Личный блог Феди"),
            ]
            db1.add_all(blogs)
            await db1.commit()

            posts = [
                Post(
                    header="Первый пост",
                    text="Привет, это мой первый пост!",
                    author_id=1,
                    blog_id=1,
                ),
                Post(
                    header="Второй пост",
                    text="Сегодня отличная погода!",
                    author_id=2,
                    blog_id=2,
                ),
                Post(
                    header="Третий пост",
                    text="Всем привет!",
                    author_id=1,
                    blog_id=3,
                ),
                Post(
                    header="Четвертый пост",
                    text="Новый пост в блоге",
                    author_id=3,
                    blog_id=3,
                ),
            ]
            db1.add_all(posts)
            await db1.commit()

    # DB2: логи
    async with async_session_db2() as db2:
        result = await db2.execute(select(Log))
        if not result.scalars().first():
            space_result = await db2.execute(select(SpaceType))
            space_types = space_result.scalars().all()
            space_map = {st.name: st.id for st in space_types}

            event_result = await db2.execute(select(EventType))
            event_types = event_result.scalars().all()
            event_map = {et.name: et.id for et in event_types}

            logs = []
            now = datetime.now()

            for day in range(30):
                date = now - timedelta(days=day)

                for user_id in [1, 2, 3]:
                    for _ in range(random.randint(1, 5)):
                        event = random.choice(
                            ["login", "logout", "comment", "create_post", "delete_post"]
                        )

                        if event in ["login", "logout"]:
                            space = "global"
                            post_id = None
                        elif event in ["create_post", "delete_post"]:
                            space = "blog"
                            post_id = None
                        else:
                            space = "post"
                            post_id = random.choice([1, 2, 3, 4])

                        log = Log(
                            datetime=date
                            + timedelta(
                                hours=random.randint(0, 23),
                                minutes=random.randint(0, 59),
                            ),
                            user_id=user_id,
                            space_type_id=space_map[space],
                            event_type_id=event_map[event],
                            post_id=post_id,
                        )
                        logs.append(log)

            db2.add_all(logs)
            await db2.commit()


async def main():
    await seed_test_data()


if __name__ == "__main__":
    asyncio.run(main())
