import time
import uuid
from dataclasses import dataclass, field
from enum import Enum


class MessageType(Enum):
    TEXT = "text"
    HEARTBEAT = "heartbeat"
    SYSTEM = "system"


@dataclass
class Message:
    room_id: str
    sender_id: str
    body: str
    msg_type: MessageType = MessageType.TEXT
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "message_id": self.message_id,
            "room_id": self.room_id,
            "sender_id": self.sender_id,
            "body": self.body,
            "msg_type": self.msg_type.value,
            "timestamp": self.timestamp,
        }
