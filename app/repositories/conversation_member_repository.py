from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ConversationUserModel


class ConversationMemberRepository:
    def add_member(
        self,
        db: Session,
        conversation_id: str,
        user_id: str,
        role: str,
    ) -> ConversationUserModel:
        row = ConversationUserModel(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
        )

        db.add(row)
        db.commit()
        db.refresh(row)

        return row

    def is_member(
        self,
        db: Session,
        conversation_id: str,
        user_id: str,
    ) -> bool:
        statement = (
            select(ConversationUserModel.user_id)
            .where(
                ConversationUserModel.conversation_id == conversation_id,
                ConversationUserModel.user_id == user_id,
            )
        )

        return db.scalar(statement) is not None