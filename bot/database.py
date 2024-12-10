from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import postgres_settings
from models import Base, UnknownWords, Users


engine = create_async_engine(postgres_settings.url, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_table() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def add_word(user_id: str, word: str, translation: str) -> UnknownWords:
    async with async_session_maker() as session:
        new_unknown_word = UnknownWords(user_id=user_id, word=word, translation=translation)
        session.add(new_unknown_word)
        await session.commit()
        return new_unknown_word


async def add_user(user_id: int, name: str) -> Users:
    async with async_session_maker() as session:
        user = Users(id=user_id, name=name)
        session.add(user)
        await session.commit()
        return user


async def get_user_or_none(user_id: int) -> Users:
    async with async_session_maker() as session:
        query = select(Users).where(Users.id == user_id)
        response = await session.execute(query)
        user = response.scalar_one_or_none()
        return user


async def is_user_exist(user_id: int) -> bool:
    user = await get_user_or_none(user_id)
    return True if user else False


async def update_user_name(user_id: int, name: str) -> None:
    user = await get_user_or_none(user_id)
    user.name = name
    async with async_session_maker() as session:
        session.add(user)
        await session.commit()
