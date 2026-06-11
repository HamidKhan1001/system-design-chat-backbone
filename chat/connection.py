import time
from dataclasses import dataclass, field
from enum import Enum


class ConnectionState(Enum):
    CONNECTED = "connected"
    IDLE = "idle"
    DEAD = "dead"


@dataclass
class WebSocketConnection:
    connection_id: str
    user_id: str
    connected_at: float = field(default_factory=time.monotonic)
    last_heartbeat: float = field(default_factory=time.monotonic)
    state: ConnectionState = ConnectionState.CONNECTED

    def beat(self) -> None:
        self.last_heartbeat = time.monotonic()
        self.state = ConnectionState.CONNECTED

    def is_stale(self, timeout_seconds: float = 30.0) -> bool:
        return (time.monotonic() - self.last_heartbeat) > timeout_seconds

    def mark_dead(self) -> None:
        self.state = ConnectionState.DEAD
