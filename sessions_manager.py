import asyncio
from abc import ABC

from aiogram import Bot, types

import config
import parser
import reply_markups
from reply_markups import BotReplyMarkups


class Session(ABC):
    def __init__(self, message: types.Message):
        self.channel_id = message.chat.id

    async def handle_message(self, message: types.Message):
        pass

    async def start(self, message: types.Message):
        pass


class SearchTitleSession(Session):
    def __init__(self, message: types.Message):
        super().__init__(message)
        self.search_type = 'all'
        self.wait_for = 'type'
        self.query = None

    async def start(self, message: types.Message):
        await message.answer(reply_markup=BotReplyMarkups.select_title(), text='Что ищем?')

    async def handle_message(self, message: types.Message):
        text = message.text.lower()

        if text in config.SEARCH_TYPES and self.wait_for == 'type':
            self.search_type = text
            self.wait_for = 'query'
            await message.answer('Введите название того что ищем')
        elif self.wait_for == 'type':
            await message.answer('Я не знаю что это такое, пожалуйста выберите из предложенных вариантов',
                                 reply_markup=BotReplyMarkups.select_title())
            return

        elif self.wait_for == 'query':
            self.query = message.text

            await message.answer('Секунду ищем')
            if self.search_type != 'all':
                item = parser.Parser.find(self.search_type, self.query)
                # await message.reply(f'{item.name} \n{item.url}')

                await message.answer_photo(photo=item.image_url, caption=f'{item.name} {item.url}')


class SessionsManager:
    def __init__(self):
        self.sessions: dict[int, Session] = {}

    def session(self, channel: int) -> Session | None:
        if channel in self.sessions:
            return self.sessions[channel]
        else:
            return None

    async def start_search_session(self, message: types.Message):
        self.sessions[message.chat.id] = SearchTitleSession(message)
        await self.sessions[message.chat.id].start(message)

    async def on_message(self, message: types.Message):
        if message.chat.id in self.sessions:
            await self.sessions[message.chat.id].handle_message(message)
