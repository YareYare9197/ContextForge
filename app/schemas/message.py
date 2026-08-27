from pydantic import BaseModel


class CreateMessageRequest(BaseModel):
    conversation_id: str
    role: str
    content: str
    sender_id: str | None = None
    model_name: str | None = None