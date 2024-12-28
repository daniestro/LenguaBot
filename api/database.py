from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from settings import postgres_settings
from models import Base


engine = create_async_engine(postgres_settings.url, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_table() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
