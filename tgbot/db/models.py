from sqlalchemy import Column, VARCHAR, BigInteger

from tgbot.db.base import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    lang = Column(VARCHAR(length=2))

