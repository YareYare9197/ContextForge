from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.services.embedding_service import EmbeddingService


class SearchService:
    def __init__(
        self,
        repository: DocumentRepository,
        embedding_service: EmbeddingService,
    ):
        self.repository = repository
        self.embedding_service = embedding_service

    def search(
        self,
        db: Session,
        query: str,
        limit: int = 5,
    ) -> list[dict]:
        query = query.strip()

        if not query:
            raise ValueError("Search query cannot be empty")

        query_embedding = self.embedding_service.embed(query)

        rows = self.repository.search_similar(
            db,
            query_embedding,
            limit,
        )

        return [
            {
                "chunk_id": row.id,
                "document_id": row.document_id,
                "chunk_index": row.chunk_index,
                "heading": row.heading,
                "content": row.content,
            }
            for row in rows
        ]