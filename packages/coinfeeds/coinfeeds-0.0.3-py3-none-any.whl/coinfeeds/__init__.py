import os
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel


class Coin(BaseModel):
    id: str  # noqa: A003
    name: str
    symbol: str


class News(BaseModel):
    url: str
    title: str
    image: str
    summary: str
    newsSiteName: str  # noqa: N815
    newsSiteLogo: str  # noqa: N815
    publishDate: float  # noqa: N815
    language: str


class Coinfeeds:
    def __init__(
        self,
        api_key: str | None = None,
        api_url: str = "https://api.coinfeeds.io/",
    ) -> None:
        api_key = api_key or os.getenv("COINFEEDS_API_KEY")
        if not api_key:
            msg = "`COINFEEDS_API_KEY` is not provided"
            raise RuntimeError(msg)
        self.api_key = api_key
        self.api_url = api_url

    def headers(self) -> dict:
        return {
            "x-api-key": self.api_key,
        }

    def coins(self, **kwargs) -> list[Coin]:
        url = urljoin(self.api_url, "/coins/list")
        response = httpx.get(url, headers=self.headers(), **kwargs)

        return [Coin(**x) for x in response.json()]

    def news(self, coin_name: str, *, symbol: bool = False, **kwargs) -> list[News]:
        url = urljoin(
            self.api_url,
            f"/coins/{coin_name.lower()}/news?symbol={str(symbol).lower()}",
        )
        response = httpx.get(url, headers=self.headers(), **kwargs)

        return [News(**x) for x in response.json()["newsFeed"]]

    def tweets(self, coin_name: str, *, symbol: bool = False, **kwargs) -> list[str]:
        url = urljoin(
            self.api_url,
            f"/coins/{coin_name.lower()}/tweets?symbol={str(symbol).lower()}",
        )
        response = httpx.get(url, headers=self.headers(), **kwargs).json()

        return response["tweet_ids"]

    def podcasts(self, coin_name: str, *, symbol: bool = False, **kwargs) -> list[str]:
        url = urljoin(
            self.api_url,
            f"/coins/{coin_name.lower()}/podcasts?symbol={str(symbol).lower()}",
        )
        response = httpx.get(url, headers=self.headers(), **kwargs).json()

        return response["podcast_ids"]

    def videos(self, coin_name: str, *, symbol: bool = False, **kwargs) -> list[str]:
        url = urljoin(
            self.api_url,
            f"/coins/{coin_name.lower()}/videos?symbol={str(symbol).lower()}",
        )
        response = httpx.get(url, headers=self.headers(), **kwargs).json()

        return response["video_ids"]
