from dataclasses import dataclass
from typing import Any, Optional, Self

from phare.auth import Auth
from phare.error import ServerError
from phare.serialize import Deserializable, deserialize, serialize

@dataclass
class ClientMessage:
    request_id: int
    verb: str
    path: list[str]
    meta: dict[str, str]
    auth: Auth
    payload: Any

    def serialize(self) -> dict[str, Any]:
        return {
            'REID': self.request_id,
            'VERB': self.verb,
            'PATH': self.path,
            'META': self.meta,
            'AUTH': serialize(self.auth),
            'PAYL': serialize(self.payload),
        }

@dataclass
class ServerMessage:
    code: int
    request_id: Optional[int]
    warnings: list[str]
    response: Optional[str]
    payload: Any

    @classmethod
    def deserialize(cls, raw: dict[str, Any]) -> Self:
        return ServerMessage(
            code=raw['RNUM'],
            request_id=raw.get('REID'),
            warnings=raw.get('WARNINGS', []),
            response=raw.get('RESPONSE'),
            payload=raw['PAYL'], # TODO: Deserialize
        )
    
    def check(self):
        if self.code != 200:
            raise ServerError(f'Request {self.request_id} errored with code {self.code} (warnings: {self.warnings}, response: {self.response})')

@dataclass
class InputEvent(Deserializable):
    source: int
    key: Optional[int]
    button: Optional[int]
    is_down: bool

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Self:
        return InputEvent(
            source=raw['src'],
            key=raw.get('key'),
            button=raw.get('btn'),
            is_down=raw['dwn'],
        )
