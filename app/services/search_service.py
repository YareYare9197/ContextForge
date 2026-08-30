from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.services.embedding_service import EmbeddingService


class SearchService:
    def __init__(
        self,
        repository: DocumentRepository,
        embedding_service: EmbeddingService,
        max_distance: float = 0.45,
    ):
        self.repository = repository
        self.embedding_service = embedding_service
        self.max_distance = max_distance

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

        matches = self.repository.search_similar(
            db,
            query_embedding,
            limit,
        )

        results = []

        for row, distance in matches:
            if distance > self.max_distance:
                continue

            results.append(
                {
                    "chunk_id": row.id,
                    "document_id": row.document_id,
                    "chunk_index": row.chunk_index,
                    "heading": row.heading,
                    "content": row.content,
                    "distance": distance,
                }
            )

        return results