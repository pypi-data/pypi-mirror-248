from dataclasses import dataclass
import requests
from .. import api_key, api_base
from ..errors import APIError


@dataclass
class Bot:
    id: str
    name: str
    script: str
    requirements: str
    env_vars: str
    python_version: str
    store_id: str
    created: str

    @classmethod
    def class_url(cls):
        return "/v1/bots"

    @classmethod
    def retrieve(cls, id: str) -> "Bot":
        headers = {"Authorization": f"Bearer {api_key}"}
        r = requests.get(f"{api_base}{cls.class_url()}/{id}/", headers=headers)
        if r.status_code == 401:
            raise APIError(**r.json())
        if r.status_code == 404:
            raise APIError(**r.json())
        return cls(**r.json())