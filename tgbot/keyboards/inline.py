from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.config import Config
from tgbot.misc.i18n import i18ns

_ = i18ns.gettext

lang_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="🇺🇿 uz", callback_data="uz"),
                                                InlineKeyboardButton(text="🇷🇺 ru", callback_data="ru"))


def channels_kb(config: Config) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=_("A'zo bo'lmoq"),
                                                                      url=config.tg_bot.channel_link),
                                                 InlineKeyboardButton(text=_("A'zo bo'ldim"),
                                                                      callback_data="done"))

