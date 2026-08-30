from sqlalchemy.orm import Session
from sqlalchemy import select

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
    
    def search_similar(
        self,
        db: Session,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[tuple[ChunkModel, float]]:
        distance = ChunkModel.embedding.cosine_distance(
            query_embedding
        ).label("distance")

        statement = (
            select(ChunkModel, distance)
            .where(ChunkModel.embedding.is_not(None))
            .order_by(distance)
            .limit(limit)
        )

        rows = db.execute(statement).all()

        return [
            (chunk, float(distance_value))
            for chunk, distance_value in rows
        ]


    def save_chunks(
        self,
        db: Session,
        document_id: str,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> list[ChunkModel]:
        if len(chunks) != len(embeddings):
            raise ValueError("Each chunk must have one embedding")

        rows = []

        for index, chunk_text in enumerate(chunks):
            rows.append(
                ChunkModel(
                    document_id=document_id,
                    chunk_index=index,
                    content=chunk_text,
                    embedding=embeddings[index],
                )
            )

        try:
            db.add_all(rows)
            db.commit()

            for row in rows:
                db.refresh(row)

            return rows

        except Exception:
            db.rollback()
            raise