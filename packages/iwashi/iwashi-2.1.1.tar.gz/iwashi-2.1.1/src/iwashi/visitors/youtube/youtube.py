import json
import re
from typing import Tuple
from urllib import parse

import bs4

from iwashi.helper import HTTP_REGEX, session
from iwashi.visitor import Context, SiteVisitor

from .types import thumbnails, ytinitialdata
from .types.about import AboutRes


class Youtube(SiteVisitor):
    NAME = "Youtube"
    URL_REGEX: re.Pattern = re.compile(
        HTTP_REGEX + r"((m|gaming)\.)?(youtube\.com|youtu\.be)", re.IGNORECASE
    )

    async def normalize(self, url: str) -> str | None:
        uri = parse.urlparse(url)
        if uri.hostname == "youtu.be":
            return await self._channel_by_video(uri.path[1:])
        type = next(filter(None, uri.path.split("/")))
        if type.startswith("@"):
            return f"https://www.youtube.com/{type}"
        if type == "playlist":
            return None
        if type == "watch":
            return await self._channel_by_video(parse.parse_qs(uri.query)["v"][0])
        if type in ("channel", "user", "c"):
            return await self._channel_by_url(url)
        return url

    async def _channel_by_video(self, video_id: str) -> str | None:
        res = await session.get(
            f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        )
        if res.status == 404:
            return None
        data = await res.json()
        return data["author_url"]

    async def _channel_by_url(self, url: str) -> str | None:
        res = await session.get(url)
        if res.status == 404:
            return None
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        element = soup.select_one("#channel-handle")
        if element is None:
            return None
        return f"https://www.youtube.com/{element.text}"

    def parse_thumbnail(self, thumbnails: thumbnails) -> str:
        size = 0
        url: str | None = None
        for thumbnail in thumbnails["thumbnails"]:
            if thumbnail["width"] > size:
                size = thumbnail["width"]
                url = thumbnail["url"]
        if url is None:
            raise RuntimeError("Thumbnail not found")
        return url

    def parse_token(self, data: ytinitialdata) -> Tuple[str, str]:
        # TODO: 地獄
        runs = data["header"]["c4TabbedHeaderRenderer"]["headerLinks"][
            "channelHeaderLinksViewModel"
        ]["more"]["commandRuns"]
        command = runs[0]["onTap"]["innertubeCommand"]
        if "showEngagementPanelEndpoint" not in command:
            raise RuntimeError("token not found")
        contents1 = command["showEngagementPanelEndpoint"]["engagementPanel"][
            "engagementPanelSectionListRenderer"
        ]["content"]["sectionListRenderer"]["contents"]
        contents2 = contents1[0]["itemSectionRenderer"]["contents"]
        endpoint = contents2[0]["continuationItemRenderer"]["continuationEndpoint"]
        api_url = endpoint["commandMetadata"]["webCommandMetadata"]["apiUrl"]
        token = endpoint["continuationCommand"]["token"]
        return api_url, token

    async def visit(self, url: str, context: Context):
        res = await session.get(url)
        if res.status // 100 != 2:
            raise RuntimeError(f"HTTP Error: {res.status}")
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        for script in soup.select("script"):
            if script.string is None:
                continue
            match = re.search(r"ytInitialData\s*=\s*({.*?});", script.string)
            if match is not None:
                data: ytinitialdata = json.loads(match.group(1))
                break
        else:
            raise RuntimeError("ytInitialData not found")
        vanity_id = data["metadata"]["channelMetadataRenderer"]["vanityChannelUrl"]
        name = data["metadata"]["channelMetadataRenderer"]["title"]
        description = data["metadata"]["channelMetadataRenderer"]["description"]
        profile_picture = self.parse_thumbnail(
            data["metadata"]["channelMetadataRenderer"]["avatar"]
        )
        context.create_result(
            site_name="Youtube",
            url=f"https://www.youtube.com/{vanity_id}",
            name=name,
            description=description,
            profile_picture=profile_picture,
        )

        api_url, token = self.parse_token(data)
        about_res = await session.post(
            f"https://www.youtube.com{api_url}",
            data=json.dumps(
                {
                    "context": {
                        "client": {
                            "userAgent": session.headers["User-Agent"],
                            "clientName": "WEB",
                            "clientVersion": "2.20231219.04.00",
                        }
                    },
                    "continuation": token,
                }
            ),
        )
        about_data: AboutRes = await about_res.json()
        links = about_data["onResponseReceivedEndpoints"][0][
            "appendContinuationItemsAction"
        ]["continuationItems"][0]["aboutChannelRenderer"]["metadata"][
            "aboutChannelViewModel"
        ]["links"]
        for link in links:
            context.visit(link["channelExternalLinkViewModel"]["link"]["content"])
