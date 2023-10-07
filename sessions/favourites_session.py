from aiogram import types

import config
import parser
from database import Database
from reply_markups import BotReplyMarkups
from sessions.session_abc import Session


class FavouritesWaitFor:
    select_title = 'select'
    choice_action = 'action'


class FavouritesSession(Session):
    def __init__(self, message: types.Message, databases: Database):
        super().__init__(message)
        self.wait_for = FavouritesWaitFor.select_title
        self.founded_items: list[parser.FoundedObject] | None = None
        self.current_item: parser.FoundedObject | None = None
        self.databases = databases

    async def start(self, message: types.Message):
        self.founded_items = self.databases.get_user_favourites(message.from_user.id)
        items = self.founded_items
        await message.answer(reply_markup=BotReplyMarkups.favourites_menu(len(self.founded_items)),
                             text='Ваш список\n' + '\n\n'.join([f'{i + 1}. {items[i].preview()}' for i in range(len(items))]))

    async def handle_message(self, message: types.Message):
        if self.wait_for == FavouritesWaitFor.select_title:
            await self._handle_choice(message)
        if self.wait_for == FavouritesWaitFor.choice_action:
            await self._handle_actions(message)

    async def _handle_choice(self, message: types.Message):
        if message.text.isnumeric() and int(message.text) - 1 in range(len(self.founded_items)):
            self.current_item = self.founded_items[int(message.text) - 1]
            self.wait_for = FavouritesWaitFor.choice_action
            item = self.current_item
            await message.answer_photo(photo=item.image_url,
                                       caption=f'{item.name} | {"Аниме" if item.type == "anime" else "Манга"} {item.rating}⭐️️\n{item.original_name} \n{item.url}',
                                       reply_markup=BotReplyMarkups.title_page_actions(
                                           second_action='Прекратить отслеживать'))
        else:
            if message != '/Главная':
                await message.delete()

    async def _handle_actions(self, message: types.Message):
        if message.text == 'Прекратить отслеживать':
            self.databases.delete_favourite(user_id=message.from_user.id, title_url=self.current_item.url)
            self.founded_items = self.databases.get_user_favourites(message.from_user.id)
            self.current_item = None
            items = self.founded_items
            await message.answer(reply_markup=BotReplyMarkups.favourites_menu(len(self.founded_items)),
                                 text='Ваш список' + '\n\n'.join([f'{i + 1}. {items[i].preview()}' for i in range(len(items))]))

        elif message.text == 'назад':
            items = self.founded_items
            await message.answer(reply_markup=BotReplyMarkups.favourites_menu(len(self.founded_items)),
                                 text='Ваш список' + '\n\n'.join([f'{i + 1}. {items[i].preview()}' for i in range(len(items))]))
        else:
            await message.delete()
