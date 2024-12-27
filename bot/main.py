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

from settings import bot_settings
from database import create_table, add_word, is_user_exist, add_user, update_user_name, get_task_or_none
from rabbit_queue import create_queue
from task import Task
from dialogs import Dialogs
from models import Tasks


dp = Dispatcher()
start_reply_keyboard = ReplyKeyboardBuilder()
start_reply_keyboard.button(text="Add new word")


class NewWordForm(StatesGroup):
    word = State()
    translation = State()


class NewUsernameForm(StatesGroup):
    name = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=f"Hello, {html.bold(message.from_user.full_name)}!",
        reply_markup=start_reply_keyboard.as_markup()
    )
    await asyncio.sleep(1)
    if not await is_user_exist(message.from_user.id):
        await add_user(message.from_user.id, message.from_user.full_name)
        await state.set_state(NewUsernameForm.name)
        await message.answer("What should I call you?")


@dp.message(NewUsernameForm.name)
async def process_new_username(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.clear()
    await update_user_name(message.from_user.id, message.text)
    await message.answer(f"Alright, I’ll call you {html.bold(message.text)}")


@dp.message(F.text == "Add new word")
async def command_add_new_word(message: Message, state: FSMContext) -> None:
    await state.set_state(NewWordForm.word)
    await message.answer("Which word are you want to add?")


@dp.message(NewWordForm.word)
async def process_word_name(message: Message, state: FSMContext) -> None:
    await state.update_data(word=message.text)
    await state.set_state(NewWordForm.translation)
    await message.answer("And what is translation of that word?")


async def process_state(state: FSMContext) -> list:
    data = await state.get_data()
    data = [str(element) for element in data.values()]
    await state.clear()
    return data


@dp.message(NewWordForm.translation)
async def process_word_translation(message: Message, state: FSMContext) -> None:
    await state.update_data(tranlation=message.text)
    word, translation = await process_state(state)
    word_in_db = await add_word(str(message.from_user.id), word, translation)
    question = Dialogs.task_question.format(html.bold(word))
    task = Task(message.from_user.id, word_in_db.id, message.chat.id, question)
    await task.create()
    await message.answer("New word successfully added")


def handle_answer(task: Tasks, message: str) -> str:
    translation = task.word.translation
    right_answer = "It's correct"
    wrong_answer = "You are down"
    return right_answer if translation == message else wrong_answer


@dp.message(F.reply_to_message)
async def handle_task(message: Message):
    task = await get_task_or_none(message.reply_to_message.text)
    await message.reply(handle_answer(task, message.text))


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token=bot_settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await create_table()
    await create_queue()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
