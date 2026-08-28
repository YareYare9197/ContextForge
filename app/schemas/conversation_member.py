from pydantic import BaseModel


class AddConversationMemberRequest(BaseModel):
    user_id: str
    role: str = "MEMBER"