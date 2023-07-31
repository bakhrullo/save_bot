from typing import List

from sqlalchemy.orm import sessionmaker

from tgbot.db.models import User
from sqlalchemy import select


async def create_user(db_session: sessionmaker, user_id: int, lang: str) -> None:
    async with db_session() as session:
        await session.merge(User(user_id=user_id, lang=lang))
        await session.commit()


async def get_user(db_session: sessionmaker, user_id: int) -> User:
    async with db_session() as session:
        user: User = await session.get(User, user_id)
        return user


async def get_users(db_session: sessionmaker) -> List[User]:
    async with db_session() as session:
        res = await session.execute(select(User))
        return res.scalars()
