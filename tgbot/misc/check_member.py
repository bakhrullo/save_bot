from aiogram.types import Message, ChatMember, CallbackQuery

from tgbot.config import Config

from typing import Union


async def check_member(obj: Union[Message, CallbackQuery], config: Config) -> ChatMember:
    return await obj.bot.get_chat_member(chat_id=config.tg_bot.channel_id, user_id=obj.from_user.id)
