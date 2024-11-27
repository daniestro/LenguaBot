import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import create_async_engine

from settings import bot_settings, postgres_settings
from models import Base


dp = Dispatcher()
start_reply_keyboard = ReplyKeyboardBuilder()
start_reply_keyboard.button(text="Add new word")


class NewWordForm(StatesGroup):
    word = State()
    translation = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=start_reply_keyboard.as_markup()
    )


@dp.message(F.text == "Add new word")
async def command_add_new_word(message: Message, state: FSMContext) -> None:
    await state.set_state(NewWordForm.word)
    await message.answer("Which word are you want to add?")


@dp.message(NewWordForm.word)
async def process_word_name(message: Message, state: FSMContext) -> None:
    await state.update_data(word=message.text)
    await state.set_state(NewWordForm.translation)
    await message.answer("And what is translation of that word?")


async def process_state(state: FSMContext) -> None:
    data = await state.get_data()
    data_string = [str(element) for element in data.values()]
    print(data_string)
    await state.clear()


@dp.message(NewWordForm.translation)
async def process_word_translation(message: Message, state: FSMContext) -> None:
    await state.update_data(tranlation=message.text)
    await process_state(state)
    await message.answer("New word successfully added")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def create_table() -> None:
    engine = create_async_engine(postgres_settings.url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main() -> None:
    bot = Bot(token=bot_settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
