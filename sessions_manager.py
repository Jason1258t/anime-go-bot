from aiogram import types
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

    async def start_search_session(self, message: types.Message):
        self.sessions[message.chat.id] = SearchTitleSession(message)
        await self.sessions[message.chat.id].start(message)

    async def on_message(self, message: types.Message):
        if message.chat.id in self.sessions:
            await self.sessions[message.chat.id].handle_message(message)
