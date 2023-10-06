from aiogram import types

import config


class BotReplyMarkups:
    @staticmethod
    def select_title():
        return types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [
                types.KeyboardButton(text=i) for i in config.SEARCH_TYPES
            ]
        ])

    @staticmethod
    def main_menu():
        kb = [
            [types.KeyboardButton(text="/Тайтл")],
            [types.KeyboardButton(text="Без пюрешки")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        return keyboard
