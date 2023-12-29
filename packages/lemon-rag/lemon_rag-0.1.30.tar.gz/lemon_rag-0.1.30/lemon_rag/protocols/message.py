from enum import Enum
from typing import Optional, List


class ChatRole(str, Enum):
    assistant = "assistant"
    notification_center = "notification_center"
    user = "user"


class Session:
    id: int
    topic: str
    title: str
    messages: Optional[List['Message']]
    latest_msg_ts: int
    create_at: int


class Message:
    msg_id: int
    session: str
