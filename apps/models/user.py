import datetime

import bcrypt
from sqlalchemy import String, BigInteger, select, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.models.database import BaseModel, db


class User(BaseModel):
    name: Mapped[str] = mapped_column(String(255))
    tlg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    messages: Mapped[list['User']] = relationship('Message', back_populates='owner', foreign_keys='Message.owner_id')

    @classmethod
    async def get_user_by_username(cls, username):
        query = select(cls).where(cls.username == username)
        return (await db.execute(query)).scalar()

    async def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password.encode())


class Message(BaseModel):
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(User.id, ondelete='CASCADE'))
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(User.id, ondelete='CASCADE'))
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.datetime.now())
    owner: Mapped['User'] = relationship('User', back_populates='messages', foreign_keys=[owner_id])
