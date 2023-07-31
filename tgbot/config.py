from dataclasses import dataclass
from pathlib import Path

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list
    channel_id: str
    channel_link: str
    use_redis: bool


@dataclass
class Miscellaneous:
    instagram_url: str = None
    instagram_host: str = None
    tiktok_url: str = None
    tiktok_host: str = None
    youtube_url: str = None
    youtube_host: str = None
    api_key: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            channel_id=env.str("CHANNEL_ID"),
            channel_link=env.str("CHANNEL_LINK"),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(
            instagram_url=env.str("INSTAGRAM_URL"),
            instagram_host=env.str("INSTAGRAM_HOST"),
            tiktok_url=env.str("TIKTOK_URL"),
            tiktok_host=env.str("TIKTOK_HOST"),
            youtube_url=env.str("YOUTUBE_URL"),
            youtube_host=env.str("YOUTUBE_HOST"),
            api_key=env.str("API_KEY"),
        )
    )


I18N_DOMAIN = 'testbot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
