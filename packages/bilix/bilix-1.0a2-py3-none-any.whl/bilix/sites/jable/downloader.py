import asyncio
import re
from pathlib import Path
from typing import Union, Tuple, Annotated
import httpx
from . import api
from bilix.download.base_downloader_m3u8 import BaseDownloaderM3u8
from bilix.download.utils import str2path, parse_speed_str


class DownloaderJable(BaseDownloaderM3u8):
    pattern = re.compile(r"^https?://([A-Za-z0-9-]+\.)*(jable\.tv)")

    def __init__(
            self,
            *,
            client: httpx.AsyncClient = None,
            browser: str = None,
            speed_limit: Annotated[float, parse_speed_str] = None,
            stream_retry: int = 5,
            progress=None,
            logger=None,
            part_concurrency: int = 10,
            video_concurrency: Union[int, asyncio.Semaphore] = 3,
            # unique params
            hierarchy: bool = True,

    ):
        client = client or httpx.AsyncClient(**api.dft_client_settings)
        super(DownloaderJable, self).__init__(
            client=client,
            browser=browser,
            speed_limit=speed_limit,
            stream_retry=stream_retry,
            progress=progress,
            logger=logger,
            part_concurrency=part_concurrency,
            video_concurrency=video_concurrency,
        )
        self.hierarchy = hierarchy

    async def get_model(self, url: str, path: Annotated[Path, str2path] = Path("."), image=True):
        """
        download videos of a model
        :cli short: m
        :param url: model page url
        :param path: save path
        :param image: download cover
        :return:
        """
        data = await api.get_model_info(self.client, url)
        if self.hierarchy:
            path /= data['model_name']
            path.mkdir(parents=True, exist_ok=True)
        await asyncio.gather(*[self.get_video(url, path, image) for url in data['urls']])

    async def get_video(self, url: str, path: Annotated[Path, str2path] = Path("."),
                        image=True, time_range: Tuple[int, int] = None):
        """
        :cli short: v
        :param url:
        :param path:
        :param image:
        :param time_range:
        :return:
        """
        video_info = await api.get_video_info(self.client, url)
        if self.hierarchy:
            path /= f"{video_info.avid} {video_info.model_name}"
            path.mkdir(parents=True, exist_ok=True)
        cors = [self.get_m3u8_video(m3u8_url=video_info.m3u8_url, path=path / f"{video_info.title}.mp4",
                                    time_range=time_range)]
        if image:
            cors.append(self.get_static(video_info.img_url, path=path / video_info.title, ))
        await asyncio.gather(*cors)
