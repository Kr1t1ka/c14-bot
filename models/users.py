from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    vk_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    state = Column(Integer, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    async def get_or_create(
        cls, session: AsyncSession, vk_id: int, first_name: str, last_name: str
    ):
        result = await session.execute(
            select(cls).filter_by(vk_id=vk_id).limit(1)
        )
        user = result.scalars().first()
        if not user:
            user = cls(vk_id=vk_id, first_name=first_name, last_name=last_name)
            session.add(user)
            await session.commit()
        return user
