from dataclasses import dataclass
from typing import Any

@dataclass
class Auth:
    user: str
    token: str

    def serialize(self) -> dict[str, Any]:
        return {
            'USER': self.user,
            'TOKEN': self.token,
        }
