from fastapi import Depends, FastAPI, HTTPException, status, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.db.database import check_database_connection, get_db
from app.schemas.conversation import CreateConversationRequest
from app.schemas.message import CreateMessageRequest
from app.schemas.user import CreateUserRequest
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from app.services.user_service import UserService
from app.schemas.conversation_member import AddConversationMemberRequest
from app.services.conversation_member_service import ConversationMemberService
from app.services.document_service import DocumentService
from app.repositories.document_repository import DocumentRepository
from app.schemas.search import SearchRequest
from app.services.embedding_service import EmbeddingService
from app.services.search_service import SearchService
from app.services.answer_service import AnswerService
from app.services.gemini_client import GeminiClient
from app.services.prompt_builder import PromptBuilder
from app.schemas.answer import AnswerRequest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ContextForge"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://context-forge-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

message_service = MessageService()
conversation_service = ConversationService()
user_service = UserService()
conversation_member_service = ConversationMemberService()
embedding_service = EmbeddingService()
document_repository = DocumentRepository()

document_service = DocumentService(
    repository=document_repository,
    embedding_service=embedding_service,
)

search_service = SearchService(
    repository=document_repository,
    embedding_service=embedding_service,
)
answer_service = AnswerService(
    search_service=search_service,
    prompt_builder=PromptBuilder(),
    llm_client=GeminiClient(),
)

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/db-health")
def database_health_check():
    check_database_connection()
    return {
        "database": "connected"
    }

@app.post("/answers")
def answer_question(
    request: SearchRequest,
    db: Session = Depends(get_db),
):
    return answer_service.answer(
        db,
        request.query,
        request.limit,
    )
@app.post(
    "/messages",
    status_code=status.HTTP_201_CREATED
)
def create_message(
    request: CreateMessageRequest,
    db: Session = Depends(get_db),
):
    return message_service.create_message(db, request)


@app.get("/conversations/{conversation_id}/messages")
def list_messages(
    conversation_id: str,
    user_id: str,
    db: Session = Depends(get_db),
):
    try:
        return message_service.list_messages(
            db,
            conversation_id,
            user_id,
        )

    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error),
        )

@app.post("/conversations", status_code=201)
def create_conversation(
    request: CreateConversationRequest,
    db: Session = Depends(get_db),
):
    return conversation_service.create_conversation(
        db,
        request,
    )
    
@app.post("/users", status_code=201)
def create_user(
    request: CreateUserRequest,
    db: Session = Depends(get_db),
):
    return user_service.create_user(
        db,
        request,
    )
    
@app.post(
    "/conversations/{conversation_id}/members",
    status_code=201,
)
def add_conversation_member(
    conversation_id: str,
    request: AddConversationMemberRequest,
    db: Session = Depends(get_db),
):
    return conversation_member_service.add_member(
        db,
        conversation_id,
        request,
    )
    
    
@app.post(
    "/messages",
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    request: CreateMessageRequest,
    db: Session = Depends(get_db),
):
    try:
        return message_service.create_message(db, request)

    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
        
@app.get("/users/{user_id}")
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    try:
        return user_service.get_user(db, user_id)

    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

@app.post("/search")
def search_documents(
    request: SearchRequest,
    db: Session = Depends(get_db),
):
    try:
        return search_service.search(
            db,
            request.query,
            request.limit,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
        
@app.post("/documents", status_code=201)
def upload_document(
    owner_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        return document_service.upload_document(
            db,
            owner_id,
            file,
        )

    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
@app.post("/documents/{document_id}/process")
def process_document(
    document_id: str,
    db: Session = Depends(get_db),
):
    try:
        return document_service.process_document(
            db,
            document_id,
        )

    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
        
        
@app.post("/answers")
def answer_question(
    request: AnswerRequest,
    db: Session = Depends(get_db),
):
    return answer_service.answer(
        db=db,
        question=request.query,
        limit=request.limit,
    )