import asyncio
import logging

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.types import ContentType

from tgbot.db.db_api import get_users
from tgbot.misc.states import Admin

log = logging.getLogger('broadcast')


async def admin_start(message: Message):
    await message.reply("Salom!, Foydalanuvchilarga yuborish kerak bo'lgan xabarni tashlang")
    await Admin.get_msg.set()


async def get_msg(m: Message):
    count, session = 0, m.bot.get("db")
    users = await get_users(session)
    mes = await m.answer("⏳")
    for user_id in users:
        if user_id.user_id == m.from_user.id:
            continue
        try:
            if await m.bot.copy_message(from_chat_id=m.chat.id, message_id=m.message_id, chat_id=user_id.user_id):
                count += 1
            await asyncio.sleep(.05)
        except:
            pass
    log.info(f"{count} messages successful sent.")
    await mes.edit_text(f"{count}ta odamga yetkazildi!✅")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(get_msg, content_types=ContentType.ANY, state=Admin.get_msg, is_admin=True)
