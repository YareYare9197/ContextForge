from sqlalchemy.orm import Session

from app.schemas.message import CreateMessageRequest
from app.services.llm_client import LLMClient
from app.services.message_service import MessageService
from app.services.prompt_builder import PromptBuilder
from app.services.search_service import SearchService


class AskService:
    def __init__(
        self,
        message_service: MessageService,
        search_service: SearchService,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
    ):
        self.message_service = message_service
        self.search_service = search_service
        self.prompt_builder = prompt_builder
        self.llm_client = llm_client

    def ask(
        self,
        db: Session,
        conversation_id: str,
        user_id: str,
        question: str,
        limit: int = 5,
    ) -> dict:
        user_message = self.message_service.create_message(
            db,
            CreateMessageRequest(
                conversation_id=conversation_id,
                role="user",
                content=question,
                sender_id=user_id,
            ),
        )

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

        assistant_message = self.message_service.create_message(
            db,
            CreateMessageRequest(
                conversation_id=conversation_id,
                role="assistant",
                content=answer,
                model_name=self.llm_client.model_name,
            ),
        )

        return {
            "message_id": assistant_message["id"],
            "answer": answer,
            "sources": [
                {
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "chunk_index": chunk["chunk_index"],
                    "heading": chunk["heading"],
                }
                for chunk in chunks
            ],
        }