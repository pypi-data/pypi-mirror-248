from dataclasses import dataclass
from typing import Literal, Optional

from botfleet._client import Client
from botfleet.pagination import PagePaginatedResource


@dataclass
class Build:
    id: str
    bot_builder_job_id: str
    status: Literal["success", "in_progress", "failure"]
    logs: list[dict[str, str]]
    created: str

    @classmethod
    def api_source(cls):
        return "builds"

    @classmethod
    def list(
        cls,
        bot_builder_job_id: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> PagePaginatedResource["Build"]:
        params = {"page": page, "page_size": page_size}
        if bot_builder_job_id is not None:
            params["bot_builder_job_id"] = bot_builder_job_id
        r = Client.request("GET", f"{cls.api_source()}/", params=params)
        return PagePaginatedResource(
            count=r.json()["count"],
            next=r.json()["next"],
            previous=r.json()["previous"],
            results=[cls(**job) for job in r.json()["results"]],
        )

    @classmethod
    def retrieve(cls, id: str) -> "Build":
        r = Client.request("GET", f"{cls.api_source()}/{id}/")
        return cls(**r.json())
