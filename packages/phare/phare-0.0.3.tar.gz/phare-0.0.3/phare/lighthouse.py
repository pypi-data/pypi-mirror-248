from numpy.typing import ArrayLike
from typing import Any, Self, TypeVar, cast

from phare.auth import Auth
from phare.constants import LIGHTHOUSE_FRAME_SHAPE, LIGHTHOUSE_URL
from phare.serialize import deserialize, serialize
from phare.protocol import ClientMessage, ServerMessage

import asyncio
import msgpack
import numpy as np
import websockets

T = TypeVar("T")

class Lighthouse:
    def __init__(self, auth: Auth, websocket: websockets.WebSocketClientProtocol):
        self.auth = auth
        self._websocket = websocket
        self._request_id = 0
        self._receive_loop_task = asyncio.create_task(self._run_receive_loop())
        self._received_messages = cast(dict[str, ServerMessage], {})
        self._receive_events = asyncio.Queue()
    
    async def _run_receive_loop(self):
        try:
            while True:
                binary = await self._websocket.recv()
                message = deserialize(ServerMessage, msgpack.unpackb(binary))
                self._received_messages[message.request_id] = message
                while not self._receive_events.empty():
                    event = cast(asyncio.Event, await self._receive_events.get())
                    event.set()
        except websockets.ConnectionClosed:
            pass

    @classmethod
    async def connect(cls, auth: Auth, url: str = LIGHTHOUSE_URL) -> Self:
        websocket = await websockets.connect(url)
        return Lighthouse(
            auth=auth,
            websocket=websocket,
        )

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, _exc_type: Any, _exc_value: Any, _exc_traceback: Any):
        await self._websocket.close()

    async def put_model(self, frame: ArrayLike):
        frame = np.asarray(frame)
        assert frame.shape == LIGHTHOUSE_FRAME_SHAPE
        assert frame.dtype == np.uint8
        await self.put(['user', self.auth.user, 'model'], frame)

    async def put(self, path: list[str], payload: Any):
        await self.perform('PUT', path, payload)

    async def perform(self, verb: str, path: list[str], payload: Any):
        assert verb != 'STREAM'
        request_id = await self.send_request(verb, path, payload)
        response = await self.receive_message(request_id)
        response.check()

    async def send_request(self, verb: str, path: list[str], payload: Any) -> int:
        request_id = self._request_id
        self._request_id += 1
        await self.send_message(ClientMessage(
            request_id=request_id,
            verb=verb,
            path=path,
            meta={},
            auth=self.auth,
            payload=payload,
        ))
        return request_id

    async def send_message(self, message: ClientMessage):
        binary: bytes = msgpack.packb(serialize(message))
        await self._websocket.send(binary)

    async def next_message_event(self) -> asyncio.Event:
        event = asyncio.Event()
        await self._receive_events.put(event)
        return event

    async def receive_message(self, request_id: int) -> ServerMessage:
        while request_id not in self._received_messages:
            event = await self.next_message_event()
            await event.wait()
        # TODO: This only handles the one most recent message for every request_id
        return self._received_messages.pop(request_id)
