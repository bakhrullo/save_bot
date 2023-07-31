import json

import aiohttp


from dataclasses import dataclass

from tgbot.config import Config


@dataclass
class Request:
    config: Config
    video_url: str

    async def create_session(self, **kwargs) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(headers={"X-RapidAPI-Key": kwargs["config"].misc.api_key,
                                              "X-RapidAPI-Host": kwargs["host"]})

    async def get(self, **kwargs) -> json:
        session = await self.create_session(**kwargs)
        async with session.get(url=kwargs["url"], params=kwargs["params"]) as response:
            await session.close()
            return await response.json()

    async def post(self, **kwargs) -> json:
        session = await self.create_session(**kwargs)
        async with session.post(url=kwargs["url"], json=kwargs["data"]) as response:
            await session.close()
            return await response.json()

    async def instagram(self) -> dict:
        return await self.post(config=self.config, host=self.config.misc.instagram_host,
                               url=self.config.misc.instagram_url, data={"mediaUrl": self.video_url})

    async def tik_tok(self) -> dict:
        return await self.get(config=self.config, host=self.config.misc.tiktok_host,
                              url=self.config.misc.tiktok_url, params={"url": self.video_url})

    async def you_tube(self) -> dict:
        return await self.get(config=self.config, host=self.config.misc.youtube_host,
                              url=self.config.misc.youtube_url, params={"id": self.video_url})
