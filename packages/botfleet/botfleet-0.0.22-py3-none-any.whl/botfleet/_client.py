import requests
import websockets

import botfleet
from botfleet.errors import BadRequest, NotFound, Unauthenticated


class Client:
    @classmethod
    def request(
        cls, method: str, action_path: str, params: dict = None, data: dict = None
    ) -> requests.Response:
        headers = {"Authorization": f"Bearer {botfleet.api_key}"}
        url = f"https://{botfleet.api_base}/v1/{action_path}"
        r = requests.request(method, url, headers=headers, params=params, json=data)
        if r.status_code == 400:
            raise BadRequest(**r.json())
        if r.status_code == 401:
            raise Unauthenticated(**r.json())
        if r.status_code == 404:
            raise NotFound(**r.json())
        return r

    @classmethod
    async def listen_to_execution(cls, address: str) -> None:
        headers = [("Authorization", f"Bearer {botfleet.api_key}")]
        url = f"wss://{botfleet.api_base}/ws/v1/execution/{address}/"
        async with websockets.connect(url, extra_headers=headers) as ws:
            return await ws.recv()

    @classmethod
    async def listen_to_execution_stream(cls, address: str) -> None:
        headers = [("Authorization", f"Bearer {botfleet.api_key}")]
        url = f"wss://{botfleet.api_base}/ws/v1/execution-stream/{address}/"
        async with websockets.connect(url, extra_headers=headers) as ws:
            while True:
                message = await ws.recv()
                yield message
