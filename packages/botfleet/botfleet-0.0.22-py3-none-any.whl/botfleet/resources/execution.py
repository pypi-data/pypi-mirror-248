from dataclasses import dataclass
from typing import Literal, Optional

from botfleet._client import Client
from botfleet.pagination import CursorPaginatedResource
from botfleet.types import JSON


@dataclass
class Execution:
    id: str
    bot_id: str
    bot_executor_job_id: Optional[str]
    bot_executor_cron_job_id: Optional[str]
    status: Literal["success", "in_progress", "failure", "termination"]
    start: str
    finish: Optional[str]
    logs: list[dict[str, str]]
    return_value: JSON

    @classmethod
    def api_source(cls):
        return "executions"

    @classmethod
    def list(
        cls,
        bot_id: Optional[str] = None,
        bot_executor_job_id: Optional[str] = None,
        bot_executor_cron_job_id: Optional[str] = None,
    ) -> CursorPaginatedResource["Execution"]:
        params = {}
        if bot_id is not None:
            params["bot_id"] = bot_id
        if bot_executor_job_id is not None:
            params["bot_executor_job_id"] = bot_executor_job_id
        if bot_executor_cron_job_id is not None:
            params["bot_executor_cron_job_id"] = bot_executor_cron_job_id
        r = Client.request("GET", f"{cls.api_source()}/", params=params)
        return CursorPaginatedResource(
            next=r.json()["next"],
            previous=r.json()["previous"],
            results=[cls(**execution) for execution in r.json()["results"]],
        )

    @classmethod
    def retrieve(cls, id: str) -> "Execution":
        r = Client.request("GET", f"{cls.api_source()}/{id}/")
        return cls(**r.json())
