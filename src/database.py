from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import postgres_settings
from models import Base, UnknownWords


engine = create_async_engine(postgres_settings.url, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_table() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def add_word(user_id: str, word: str, translation: str) -> None:
    async with async_session_maker() as session:
        new_unknown_word = UnknownWords(user_id=user_id, word=word, translation=translation)
        session.add(new_unknown_word)
        await session.commit()
