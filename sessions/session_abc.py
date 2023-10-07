from abc import ABC

from aiogram import types


class Session(ABC):
    def __init__(self, message: types.Message):
        self.channel_id = message.chat.id

    async def handle_message(self, message: types.Message):
        pass

    async def start(self, message: types.Message):
        pass