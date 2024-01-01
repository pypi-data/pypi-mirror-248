from dataclasses import dataclass
from typing import Optional

from botfleet._client import Client
from botfleet.pagination import PagePaginatedResource


@dataclass
class BotBuilderJob:
    id: str
    bot_id: str
    created: str

    @classmethod
    def api_source(cls):
        return "bot-builder-jobs"

    @classmethod
    def list(
        cls, bot_id: Optional[str] = None, page: int = 1, page_size: int = 10
    ) -> PagePaginatedResource["BotBuilderJob"]:
        params = {"page": page, "page_size": page_size}
        if bot_id is not None:
            params["bot_id"] = bot_id
        r = Client.request("GET", f"{cls.api_source()}/", params=params)
        return PagePaginatedResource(
            count=r.json()["count"],
            next=r.json()["next"],
            previous=r.json()["previous"],
            results=[cls(**job) for job in r.json()["results"]],
        )

    @classmethod
    def retrieve(cls, id: str) -> "BotBuilderJob":
        r = Client.request("GET", f"{cls.api_source()}/{id}/")
        return cls(**r.json())
