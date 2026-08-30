import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.services.document_reader import DocumentReader
from app.services.text_chunker import TextChunker
from app.services.embedding_service import EmbeddingService


UPLOAD_DIRECTORY = Path("storage/uploads")


class DocumentService:
    def __init__(self,
        repository: DocumentRepository | None = None,
        embedding_service: EmbeddingService | None = None):
        self.repository = (
            repository
            if repository is not None
            else DocumentRepository()
        )
        self.reader = DocumentReader()
        self.chunker = TextChunker()
        self.embedding_service = (
            embedding_service
            if embedding_service is not None
            else EmbeddingService()
        )

    def upload_document(
        self,
        db: Session,
        owner_id: str,
        upload: UploadFile,
    ) -> dict:
        if not self.repository.owner_exists(db, owner_id):
            raise LookupError("owner not found")

        if not upload.filename:
            raise ValueError("file name is missing")

        document_id = str(uuid4())
        safe_filename = Path(upload.filename).name
        content_type = upload.content_type or "application/octet-stream"

        UPLOAD_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        stored_filename = f"{document_id}-{safe_filename}"
        stored_path = UPLOAD_DIRECTORY / stored_filename

        try:
            # Copy the uploaded file into local storage.
            with stored_path.open("wb") as destination:
                shutil.copyfileobj(upload.file, destination)

            row = self.repository.save(
                db,
                document_id,
                owner_id,
                safe_filename,
                content_type,
            )

            return {
                "id": row.id,
                "owner_id": row.owner_id,
                "filename": row.filename,
                "content_type": row.content_type,
                "status": row.status,
                "stored_filename": stored_filename,
                "created_at": row.created_at.isoformat(),
            }

        except Exception:
            # Remove the file if database saving fails.
            stored_path.unlink(missing_ok=True)
            raise

    def process_document(
        self,
        db: Session,
        document_id: str,
    ) -> dict:
        row = self.repository.find_by_id(db, document_id)

        if row is None:
            raise LookupError("document not found")

        self.repository.update_status(
            db,
            document_id,
            "PROCESSING",
        )

        stored_path = (
            UPLOAD_DIRECTORY
            / f"{row.id}-{row.filename}"
        )

        try:
            text = self.reader.read(
                stored_path,
                row.content_type,
            )

            chunks = self.chunker.split(text)
            embeddings = self.embedding_service.embed_many(chunks)

            saved_chunks = self.repository.save_chunks(
                db,
                document_id,
                chunks,
            )

            updated_row = self.repository.update_status(
                db,
                document_id,
                "PROCESSED",
            )

            return {
                "id": updated_row.id,
                "filename": updated_row.filename,
                "status": updated_row.status,
                "chunks_created": len(saved_chunks),
            }

        except Exception:
            self.repository.update_status(
                db,
                document_id,
                "FAILED",
            )
            raise
        
