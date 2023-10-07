from aiogram import types

import config
import parser
from reply_markups import BotReplyMarkups
from sessions.session_abc import Session


class SearchWaitFor:
    type = 'type'
    query = 'query'
    select_title = 'select_title'
    page_actions = 'page_actions'


class SearchTitleSession(Session):
    def __init__(self, message: types.Message):
        super().__init__(message)
        self.search_type = 'all'
        self.wait_for = SearchWaitFor.type
        self.query = None
        self.founded_items: list[parser.FoundedObject] | None = None

    async def start(self, message: types.Message):
        await message.answer(reply_markup=BotReplyMarkups.select_title_type, text='Что ищем?')

    async def handle_message(self, message: types.Message):
        if self.wait_for == SearchWaitFor.type:
            await self._handle_type(message)

        elif self.wait_for == SearchWaitFor.query:
            await self._handle_query(message)

        elif self.wait_for == SearchWaitFor.select_title:
            await self._handle_select_title_actions(message)

        elif self.wait_for == SearchWaitFor.page_actions:
            await self._handle_title_page_actions(message)

    async def _handle_type(self, message: types.Message):
        text = message.text.lower()
        if text in config.SEARCH_TYPES:
            self.search_type = text
            self.wait_for = SearchWaitFor.query
            await message.answer('Введите название того что ищем', reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer('Я не знаю что это такое, пожалуйста выберите из предложенных вариантов',
                                 reply_markup=BotReplyMarkups.select_title_type())
            return

    async def _handle_query(self, message: types.Message):
        self.query = message.text

        await message.answer('Секунду ищем')
        if self.search_type != 'all':
            items = parser.Parser.find(self.search_type, self.query)
            self.founded_items = items
            await message.answer('\n\n'.join([f'{i + 1}. {items[i].preview()}' for i in range(len(items))]),
                                 reply_markup=BotReplyMarkups.select_title_actions(len(items)))

            self.wait_for = SearchWaitFor.select_title

    async def _handle_select_title_actions(self, message: types.Message):
        if message.text in [str(i + 1) for i in range(len(self.founded_items))]:
            item = self.founded_items[int(message.text) - 1]
            await message.answer_photo(photo=item.image_url,
                                       caption=f'{item.name}  {item.rating}\n{item.original_name} \n{item.url}',
                                       reply_markup=BotReplyMarkups.title_page_actions)

            self.wait_for = SearchWaitFor.page_actions
        else:
            if message.text != '/Главная':
                await message.delete()

    async def _handle_title_page_actions(self, message: types.Message):
        if message.text == 'назад':
            await message.answer(
                '\n\n'.join([f'{i + 1}. {self.founded_items[i].preview()}' for i in range(len(self.founded_items))]),
                reply_markup=BotReplyMarkups.select_title_actions(len(self.founded_items)))

            self.wait_for = SearchWaitFor.select_title
