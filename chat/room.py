from .message import Message, MessageType
from .hub import ConnectionHub


class ChatRoom:
    def __init__(self, room_id: str, hub: ConnectionHub):
        self.room_id = room_id
        self._hub = hub
        self._members: set = set()
        self._history: list = []

    def join(self, user_id: str) -> None:
        self._members.add(user_id)

    def leave(self, user_id: str) -> None:
        self._members.discard(user_id)

    def send(self, message: Message) -> int:
        self._history.append(message)
        delivered = 0
        for uid in self._members:
            if uid != message.sender_id:
                if self._hub.deliver(uid, message):
                    delivered += 1
        return delivered

    @property
    def member_count(self) -> int:
        return len(self._members)

    @property
    def history(self) -> list:
        return list(self._history)
