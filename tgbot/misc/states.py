from aiogram.dispatcher.filters.state import State, StatesGroup


class Start(StatesGroup):
    get_lang = State()


class Download(StatesGroup):
    get_link = State()

class Admin(StatesGroup):
    get_msg = State()