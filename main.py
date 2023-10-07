import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import reply_markups
from sessions_manager import SessionsManager

bot = Bot(token="5315337669:AAG8SHRoX3jqT_RTmha1J8MTgHcqJA9fXVI")

dp = Dispatcher()
manager = SessionsManager()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    await message.answer("Hello!", reply_markup=reply_markups.BotReplyMarkups.main_menu())


@dp.message(Command("Главная"))
async def cmd_start(message: types.Message):

    await message.answer("Что теперь?", reply_markup=reply_markups.BotReplyMarkups.main_menu())


@dp.message(Command("Тайтл"))
async def start_title_mode(message: types.Message):
    await manager.start_search_session(message)


@dp.message()
async def on_message(message: types.Message):
    await manager.on_message(message)


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
