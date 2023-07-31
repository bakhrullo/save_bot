import asyncio

import aiofiles
import aiohttp
import yarl
from moviepy.editor import *


async def convert(video_url: str, file_name: str) -> None:
    url = yarl.URL(video_url, encoded=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:

            if resp.status == 200:
                f = await aiofiles.open(f'{file_name}.mp4', mode='wb')
                await f.write(await resp.read())
                await f.close()

    video = VideoFileClip(f"{file_name}.mp4")
    video.audio.write_audiofile(f"{file_name}.mp3")
    video.close()

