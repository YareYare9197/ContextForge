from sqlalchemy.orm import Session

from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import CreateConversationRequest


class ConversationService:
    def __init__(self):
        self.repository = ConversationRepository()

    def create_conversation(
        self,
        db: Session,
        request: CreateConversationRequest,
    ) -> dict:
        row = self.repository.save(
            db,
            request.title,
        )

        return {
            "id": row.id,
            "title": row.title,
            "created_at": row.created_at.isoformat(),
        }