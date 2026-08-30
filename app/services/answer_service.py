from sqlalchemy.orm import Session

from app.services.llm_client import LLMClient
from app.services.prompt_builder import PromptBuilder
from app.services.search_service import SearchService


class AnswerService:
    def __init__(
        self,
        search_service: SearchService,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
    ):
        self.search_service = search_service
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def answer(
        self,
        db: Session,
        question: str,
        limit: int = 5,
    ) -> dict:
        chunks = self.search_service.search(
            db,
            question,
            limit,
        )

        prompts = self.prompt_builder.build(
            question,
            chunks,
        )

        answer = self.llm_client.generate(
            prompts["system"],
            prompts["user"],
        )

        sources = [
            {
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "chunk_index": chunk["chunk_index"],
                "heading": chunk["heading"],
            }
            for chunk in chunks
        ]

        return {
            "answer": answer,
            "sources": sources,
        }