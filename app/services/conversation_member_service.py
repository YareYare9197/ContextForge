from sqlalchemy.orm import Session

from app.repositories.conversation_member_repository import (
    ConversationMemberRepository,
)
from app.schemas.conversation_member import AddConversationMemberRequest


class ConversationMemberService:
    def __init__(self):
        self.repository = ConversationMemberRepository()

    def add_member(
        self,
        db: Session,
        conversation_id: str,
        request: AddConversationMemberRequest,
    ) -> dict:
        row = self.repository.add_member(
            db,
            conversation_id,
            request.user_id,
            request.role,
        )

        return {
            "conversation_id": row.conversation_id,
            "user_id": row.user_id,
            "role": row.role,
            "joined_at": row.joined_at.isoformat(),
        }