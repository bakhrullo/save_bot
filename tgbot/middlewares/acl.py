from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.db.db_api import get_user

from typing import Union


class ACLMiddleware(BaseMiddleware):
    async def setup_chat(self, data: dict, obj: Union[types.Message, types.CallbackQuery]):
        user_loc = await get_user(obj.bot.get("db"), obj.from_user.id)
        if user_loc is None:
            data.update({'status': False, 'lang': obj.from_user.language_code})
        else:
            data.update({'status': True, 'lang': user_loc.lang})

    async def on_pre_process_message(self, m: types.Message, data: dict):
        await self.setup_chat(data, m)

    async def on_pre_process_callback_query(self, q: types.CallbackQuery, data: dict):
        await self.setup_chat(data, q)
