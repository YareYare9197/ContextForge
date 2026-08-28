from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import MessageModel
from app.domain.message import Message


class MessageRepository:
    def save(self, db: Session, message: Message) -> MessageModel:
        row = MessageModel(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            sender_id=message.sender_id,
            model_name=message.model_name,
            created_at=message.created_at,
        )

        db.add(row)
        db.commit()
        db.refresh(row)

        return row

    def find_by_conversation_id(
        self,
        db: Session,
        conversation_id: str,
    ) -> list[MessageModel]:
        statement = (
            select(MessageModel)
            .where(MessageModel.conversation_id == conversation_id)
            .order_by(MessageModel.created_at)
        )

        return list(db.scalars(statement).all())