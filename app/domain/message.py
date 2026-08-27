from datetime import datetime, timezone
from uuid import uuid4


class Message:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

    def __init__(
        self,
        conversation_id,
        role,
        content,
        sender_id=None,
        model_name=None
    ):
        if role not in {
            Message.USER,
            Message.ASSISTANT,
            Message.SYSTEM
        }:
            raise ValueError("invalid message role")

        if not content.strip():
            raise ValueError("message content cannot be empty")

        if role == Message.USER and sender_id is None:
            raise ValueError("user message needs a sender")

        self.id = str(uuid4())
        self.conversation_id = conversation_id
        self.role = role
        self.content = content
        self.sender_id = sender_id
        self.model_name = model_name
        self.created_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "sender_id": self.sender_id,
            "model_name": self.model_name,
            "created_at": self.created_at.isoformat()
        }