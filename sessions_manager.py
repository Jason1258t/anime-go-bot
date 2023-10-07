from aiogram import types

import database
from sessions.favourites_session import FavouritesSession
from sessions.search_session import SearchTitleSession
from sessions.session_abc import Session


class SessionsManager:
    def __init__(self):
        self.sessions: dict[int, Session] = {}

    def session(self, channel: int) -> Session | None:
        if channel in self.sessions:
            return self.sessions[channel]
        else:
            return None

    async def start_search_session(self, message: types.Message, db: database.Database):
        self.sessions[message.chat.id] = SearchTitleSession(message, databases=db)
        await self.sessions[message.chat.id].start(message)

    async def start_favourites_session(self, message: types.Message, db: database.Database):
        self.sessions[message.chat.id] = FavouritesSession(message, databases=db)
        await self.sessions[message.chat.id].start(message)

    async def on_message(self, message: types.Message):
        if message.chat.id in self.sessions:
            await self.sessions[message.chat.id].handle_message(message)
