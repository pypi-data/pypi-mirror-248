from dataclasses import dataclass
from typing import Optional

from botfleet._client import Client
from botfleet.pagination import CursorPaginatedResource
from botfleet.types import JSON


@dataclass
class BotExecutorJob:
    id: str
    bot_id: str
    execution_address: str
    created: str

    @classmethod
    def api_source(cls):
        return "bot-executor-jobs"

    @classmethod
    def list(
        cls,
        bot_id: Optional[str] = None,
    ) -> CursorPaginatedResource["BotExecutorJob"]:
        params = {}
        if bot_id is not None:
            params["bot_id"] = bot_id
        r = Client.request("GET", f"{cls.api_source()}/", params=params)
        return CursorPaginatedResource(
            next=r.json()["next"],
            previous=r.json()["previous"],
            results=[cls(**job) for job in r.json()["results"]],
        )

    @classmethod
    def retrieve(cls, id: str) -> "BotExecutorJob":
        r = Client.request("GET", f"{cls.api_source()}/{id}/")
        return cls(**r.json())

    @classmethod
    def create(cls, bot_id: str, payload: JSON = None) -> "BotExecutorJob":
        r = Client.request(
            "POST",
            f"{cls.api_source()}/create/",
            data={
                "bot_id": bot_id,
                "payload": payload,
            },
        )
        return cls(**r.json())
