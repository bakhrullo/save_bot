import os

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, MediaGroup
from aiogram.types.input_file import InputFile

from tgbot.config import Config
from tgbot.db.db_api import create_user
from tgbot.keyboards.inline import channels_kb, lang_kb
from tgbot.misc.check_member import check_member
from tgbot.misc.i18n import i18ns
from tgbot.misc.states import Start, Download
from tgbot.services.mp4_to_mp3 import convert
from tgbot.services.request import Request

_ = i18ns.gettext
__ = i18ns.lazy_gettext


async def user_start(m: Message, status: bool):
    if status:
        await m.answer(_("Linkni tashlang"))
        return await Download.get_link.set()
    await m.answer(_("Tilni tanlang 👇"), reply_markup=lang_kb)
    await Start.get_lang.set()


async def get_lang(c: CallbackQuery):
    session = c.bot.get("db")
    await create_user(session, c.from_user.id, c.data)
    await c.message.edit_text(_("Linkni tashlang", locale=c.data))
    await Download.get_link.set()


async def get_link(m: Message, config: Config):
    res = await check_member(m, config)
    if res["status"] == "left":
        return await m.answer(_("Botdan foydlanish uchun kanalga a'zo bo'ling 👇"), reply_markup=channels_kb(config))
    link = m.text
    mes = await m.answer("⏳")
    if link.startswith("https://youtu"):
        if link.startswith("https://youtube.com/shorts/"):
            link = link.replace("https://youtube.com/shorts/", "")
            link = link.replace("?feature=share", "")
        else:
            link = link.replace("https://youtu.be/", "")
        content = await Request(config, link).you_tube()
        await mes.delete()
        await m.answer_video(video=content["formats"][-1]["url"], caption=content["title"])
        await convert(video_url=content["formats"][-1]["url"], file_name=m.from_user.id)
        await m.answer_audio(audio=InputFile(f"{m.from_user.id}.mp3"), caption=content["title"])
        os.remove(f"{m.from_user.id}.mp4")
        return os.remove(f"{m.from_user.id}.mp3")
    elif link.startswith("https://www.instagram.com"):
        content = await Request(config, link).instagram()
        await mes.delete()
        print(content)
        if len(content["posts"]) == 1:
            if content["posts"][0]["is_video"]:
                await m.answer_video(video=content["posts"][0]["contentUrl"], caption=content["articleBody"])
                await convert(video_url=content["posts"][0]["contentUrl"], file_name=m.from_user.id)
                await m.answer_audio(audio=InputFile(f"{m.from_user.id}.mp3"))
                os.remove(f"{m.from_user.id}.mp4")
                return os.remove(f"{m.from_user.id}.mp3")
            return await m.answer_photo(photo=content["posts"][0]["contentUrl"], caption=content["articleBody"])
        media, count = MediaGroup(), 0
        for i in content["posts"]:
            if i["is_video"]:
                media.attach_video(i["contentUrl"], caption=content["articleBody"] if count == 0 else None)
            else:
                media.attach_photo(i["display_url"], caption=content["articleBody"] if count == 0 else None)
            count += 1
        await m.answer_media_group(media=media)

    elif link.startswith("https://www.tiktok.com") or link.startswith("https://vm.tiktok.com") or link.startswith(
            "https://vt.tiktok.com"):
        content = await Request(config, link).tik_tok()
        await mes.delete()
        await m.answer_video(video=content["video"][0], caption=content["description"][0])
        await m.answer_audio(audio=content["music"][0])
    else:
        return await mes.edit_text(_("Notog'ri link yuborlidi ❌"))


async def done(c: CallbackQuery, config: Config):
    res = await check_member(c, config)
    if res["status"] == "left":
        return await c.answer(_("Siz hali a'zo bo'lmadingiz"))
    await c.message.edit_text(_("Linkni tashlang"))
    await Download.get_link.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(get_lang, state=Start.get_lang)
    dp.register_callback_query_handler(done, state="*")
    dp.register_message_handler(get_link, state=Download.get_link)
