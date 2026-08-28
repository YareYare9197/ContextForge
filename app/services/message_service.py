from sqlalchemy.orm import Session

from app.domain.message import Message
from app.repositories.conversation_member_repository import (
    ConversationMemberRepository,
)
from app.repositories.message_repository import MessageRepository
from app.schemas.message import CreateMessageRequest


class MessageService:
    def __init__(self):
        self.repository = MessageRepository()
        self.member_repository = ConversationMemberRepository()

    def list_messages(
        self,
        db: Session,
        conversation_id: str,
        user_id: str,
    ) -> list[dict]:
        allowed = self.member_repository.is_member(
            db,
            conversation_id,
            user_id,
        )

        if not allowed:
            raise PermissionError(
                "user is not a member of this conversation"
            )

        rows = self.repository.find_by_conversation_id(
            db,
            conversation_id,
        )

        return [
            {
                "id": row.id,
                "conversation_id": row.conversation_id,
                "role": row.role,
                "content": row.content,
                "sender_id": row.sender_id,
                "model_name": row.model_name,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]

    def create_message(
        self,
        db: Session,
        request: CreateMessageRequest,
    ) -> dict:
        if request.sender_id is not None:
            allowed = self.member_repository.is_member(
                db,
                request.conversation_id,
                request.sender_id,
            )

            if not allowed:
                raise PermissionError(
                    "user is not a member of this conversation"
                )

        message = Message(
            conversation_id=request.conversation_id,
            role=request.role,
            content=request.content,
            sender_id=request.sender_id,
            model_name=request.model_name,
        )

        saved_row = self.repository.save(db, message)

        return {
            "id": saved_row.id,
            "conversation_id": saved_row.conversation_id,
            "role": saved_row.role,
            "content": saved_row.content,
            "sender_id": saved_row.sender_id,
            "model_name": saved_row.model_name,
            "created_at": saved_row.created_at.isoformat(),
        }
    
