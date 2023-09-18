from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from settings import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

Base = declarative_base()

async def get_db() -> AsyncSession:
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        yield session

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)