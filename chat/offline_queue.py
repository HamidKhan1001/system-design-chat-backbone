from collections import deque
from .message import Message


class OfflineMessageQueue:
    """Per-user offline message queue; drains when user reconnects."""

    def __init__(self, max_per_user: int = 500):
        self._max = max_per_user
        self._queues: dict = {}

    def enqueue(self, user_id: str, message: Message) -> None:
        q = self._queues.setdefault(user_id, deque(maxlen=self._max))
        q.append(message)

    def drain(self, user_id: str) -> list:
        q = self._queues.pop(user_id, deque())
        return list(q)

    def pending_count(self, user_id: str) -> int:
        return len(self._queues.get(user_id, []))

    def has_pending(self, user_id: str) -> bool:
        return bool(self._queues.get(user_id))
