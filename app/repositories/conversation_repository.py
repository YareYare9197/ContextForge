from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.models import ConversationModel


class ConversationRepository:
    def save(
        self,
        db: Session,
        title: str | None,
    ) -> ConversationModel:
        row = ConversationModel(
            id=str(uuid4()),
            title=title,
        )

        db.add(row)
        db.commit()
        db.refresh(row)

        return row