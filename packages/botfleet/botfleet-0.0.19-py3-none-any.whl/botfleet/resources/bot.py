from dataclasses import dataclass
import requests
from .. import api_key, api_base
from ..errors import APIError

api_base = "https://68a6-2a0b-6204-f1ac-d700-30ca-2113-a13e-fc3f.ngrok-free.app"
api_key = "d98e188d79d348508a1645a50518fb5d"


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