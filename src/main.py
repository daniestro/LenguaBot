import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from settings import bot_settings


dp = Dispatcher()


class DialogForm(StatesGroup):
    ready = State()
    answer = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message(Command("dialog"))
async def command_dialog_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(DialogForm.ready)
    await message.answer("Do you want start a conversation?")


@dp.message(DialogForm.ready, F.text.casefold() == "yes")
async def process_positive_readiness(message: Message, state: FSMContext) -> None:
    await state.update_data(ready=message.text)
    await state.set_state(DialogForm.answer)
    await message.answer("Okey, lets start!")


@dp.message(DialogForm.ready, F.text.casefold() == "no")
async def process_positive_readiness(message: Message, state: FSMContext) -> None:
    await state.update_data(ready=message.text)
    await message.answer("Okey, see you next time!")


@dp.message(DialogForm.answer)
async def process_answer(message: Message, state: FSMContext) -> None:
    await state.update_data(answer=message.text)
    data = await state.get_data()
    data_string = [str(element) for element in data.values()]
    print(data_string)
    await state.clear()
    await message.answer("Hey, I am just kidding. I dont wanna talk with you xDD")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token=bot_settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
