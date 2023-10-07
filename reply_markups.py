from aiogram import types

import config


class BotReplyMarkups:
    select_title_type = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            types.KeyboardButton(text=i) for i in config.SEARCH_TYPES
        ]
    ])

    @staticmethod
    def main_menu():
        kb = [
            [types.KeyboardButton(text="/Тайтл"),
             types.KeyboardButton(text="Без пюрешки")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        return keyboard

    title_page_actions = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='назад'),
                types.KeyboardButton(text='отслеживать'),
            ]
        ], resize_keyboard=True)

    @staticmethod
    def select_title_actions(titles_count):
        kb = [
            [types.KeyboardButton(text=str(i + 1)) for i in range(titles_count)],
            [types.KeyboardButton(text='/Главная')]
        ]

        return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
