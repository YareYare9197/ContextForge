from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ChunkModel, DocumentModel, UserModel


class DocumentRepository:
    def owner_exists(
        self,
        db: Session,
        owner_id: str,
    ) -> bool:
        return db.get(UserModel, owner_id) is not None

    def find_by_id(
        self,
        db: Session,
        document_id: str,
    ) -> DocumentModel | None:
        return db.get(DocumentModel, document_id)

    def update_status(
        self,
        db: Session,
        document_id: str,
        status: str,
    ) -> DocumentModel:
        row = db.get(DocumentModel, document_id)

        if row is None:
            raise LookupError("document not found")

        row.status = status
        db.commit()
        db.refresh(row)

        return row

    def save_chunks(
        self,
        db: Session,
        document_id: str,
        chunks: list[str],
    ) -> list[ChunkModel]:
        rows = [
            ChunkModel(
                id=str(uuid4()),
                document_id=document_id,
                chunk_index=index,
                content=content,
            )
            for index, content in enumerate(chunks)
        ]

        try:
            db.add_all(rows)
            db.commit()

            for row in rows:
                db.refresh(row)

            return rows

        except Exception:
            db.rollback()
            raise