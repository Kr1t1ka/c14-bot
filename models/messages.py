from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    sender_id = Column(Integer, ForeignKey("users.vk_id"))
    sender = relationship("User", back_populates="messages")
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"{self.sender}: {self.text}"

    @classmethod
    async def create(cls, session: AsyncSession, text: str, sender_id: int):
        new_message = cls(text=text, sender_id=sender_id)
        session.add(new_message)
        await session.commit()
        return new_message
