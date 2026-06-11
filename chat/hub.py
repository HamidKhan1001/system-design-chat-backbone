from .connection import WebSocketConnection, ConnectionState
from .message import Message
from .offline_queue import OfflineMessageQueue


class ConnectionHub:
    """Manages all active WebSocket connections and prunes dead ones."""

    def __init__(self, heartbeat_timeout: float = 30.0):
        self._connections: dict = {}
        self._timeout = heartbeat_timeout
        self.offline_queue = OfflineMessageQueue()

    def connect(self, conn: WebSocketConnection) -> None:
        self._connections[conn.connection_id] = conn

    def disconnect(self, connection_id: str) -> None:
        self._connections.pop(connection_id, None)

    def heartbeat(self, connection_id: str) -> bool:
        conn = self._connections.get(connection_id)
        if conn:
            conn.beat()
            return True
        return False

    def prune_dead(self) -> list:
        """Remove stale connections; return list of pruned connection_ids."""
        dead = [
            cid for cid, conn in self._connections.items()
            if conn.is_stale(self._timeout)
        ]
        for cid in dead:
            self._connections[cid].mark_dead()
            del self._connections[cid]
        return dead

    def active_count(self) -> int:
        return len(self._connections)

    def deliver(self, user_id: str, message: Message) -> bool:
        for conn in self._connections.values():
            if conn.user_id == user_id and conn.state == ConnectionState.CONNECTED:
                return True
        self.offline_queue.enqueue(user_id, message)
        return False

    def get_connection(self, connection_id: str):
        return self._connections.get(connection_id)
