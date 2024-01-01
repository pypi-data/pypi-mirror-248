from dataclasses import dataclass
from typing import Literal, Optional

from botfleet._client import Client
from botfleet.pagination import PagePaginatedResource


@dataclass
class BotTemplate:
    id: str
    name: str
    description: str
    script: str
    requirements: str
    env_vars: str
    python_version: Literal["3.9", "3.10", "3.11", "3.12"]
    public: bool
    created: str
    modified: str

    @classmethod
    def api_source(cls):
        return "bot-templates"

    @classmethod
    def list(
        cls, page: int = 1, page_size: int = 10
    ) -> PagePaginatedResource["BotTemplate"]:
        params = {"page": page, "page_size": page_size}
        r = Client.request("GET", f"{cls.api_source()}/", params=params)
        return PagePaginatedResource(
            count=r.json()["count"],
            next=r.json()["next"],
            previous=r.json()["previous"],
            results=[cls(**job) for job in r.json()["results"]],
        )

    @classmethod
    def retrieve(cls, id: str) -> "BotTemplate":
        r = Client.request("GET", f"{cls.api_source()}/{id}/")
        return cls(**r.json())

    @classmethod
    def create(
        cls,
        name: str,
        script: str,
        python_version: Literal["3.9", "3.10", "3.11", "3.12"],
        public: bool,
        description: str = "",
        requirements: str = "",
        env_vars: str = "",
    ) -> "BotTemplate":
        r = Client.request(
            "POST",
            f"{cls.api_source()}/create/",
            data={
                "name": name,
                "description": description,
                "script": script,
                "requirements": requirements,
                "env_vars": env_vars,
                "python_version": python_version,
                "public": public,
            },
        )
        return cls(**r.json())

    @classmethod
    def update(cls, id: str, **kwargs) -> "BotTemplate":
        """
        The following fields can be updated: `name`, `descriptiion`, `script`,
        `requirements`, `env_vars`, `python_version`, `public`.
        """

        r = Client.request("PATCH", f"{cls.api_source()}/{id}/update/", data=kwargs)
        return cls(**r.json())

    @classmethod
    def delete(cls, id: str) -> None:
        Client.request("DELETE", f"{cls.api_source()}/{id}/delete/")
